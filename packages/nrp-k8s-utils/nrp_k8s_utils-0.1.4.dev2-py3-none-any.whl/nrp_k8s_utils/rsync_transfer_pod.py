from .pod_manager import PodManager
from .utils.ssh_key_generator import generate_ssh_key_pair

import subprocess
import os
import socket
import tempfile
import time
import yaml
import re

from typing import Dict, List, Optional, Union


class RsyncTransferPod(PodManager):

    def __init__(
        self, 
        manifest:Union[str, Dict], 
        volume:Optional[str]=None, 
        context: Optional[str] = None, 
        kubectl_path:Optional[str] = None, 
        debug_mode:Optional[str]=False
    ):
        """
        Initialize the RSyncPodManager with the path to the Kubernetes manifest.
        """
        super().__init__(manifest, context, kubectl_path, debug_mode)
    
        if volume is None and len(self.volumes) == 1:
            volume = self.volumes[0].get("name")
            self.logger.debug(f"Using the only volume in the manifest by default: {volume}")
        elif volume is None and len(self.volumes) > 1:
            raise ValueError("Multiple volumes found in the manifest. Please specify a volume to use with the sidecar.")

        if not any(volume in v.get("name") for v in self.volumes):
            raise ValueError(f"Volume {volume} not found in the manifest.")

        for container in self.containers:
            if container.get("name") == "rsync-sidecar":
                self.logger.warning("container with name rsync-sidecar already exists.")
                return

        self.sidecar_volume = volume
        self.ssh_port_forward_process = None
        self.private_key = None
        self.public_key = None
        self.private_key_path = None
        self.ssh_port = None


#--------------------------------------------------------------------------------
# Pod Lifecycle Methods
#--------------------------------------------------------------------------------


    def start_pod(
        self, 
        ports: Union[List[int], int] = [2222, 2223, 2224, 2225],
    ):
        """
        Start a pod using the provided Kubernetes manifest.
        :param sidecar_volume: Name of the volume to mount in the rsync sidecar container.
        :param ports: List of local ports or port to attempt for port forwarding.
        """
        self._inject_sidecar()
        super().start_pod()
        self._transfer_ssh_key()
        if isinstance(ports, int):
            ports = [ports]
        self._attempt_port_forwarding(ports)  # Try multiple ports for redundancy


    def stop_pod(self):
        """
        Stop the pod and terminate any active port-forwarding processes.
        """
        super().stop_pod()
        self._stop_port_forward()
        self._cleanup_private_key()

# --------------------------------------------------------------------------------
# RSync Sidecar Helper Methods
# --------------------------------------------------------------------------------


    def _inject_sidecar(self):
        """
        Inject the rsync sidecar container into the Kubernetes manifest.
        The updated manifest is written to a temporary file, and self._manifest_path is updated to point to it.
        """

        # Define the sidecar container spec
        sidecar = {
            "name": "rsync-sidecar",
            "image": "gitlab-registry.nrp-nautilus.io/trevin/nrp_k8s_utils:latest",
            "imagePullPolicy": "IfNotPresent",
            "ports": [{"containerPort": 22}],
            "resources": {
                "requests": {"cpu": "400m", "memory": "1Gi"},
                "limits": {"cpu": "500m", "memory": "2Gi"}
            },
            "volumeMounts": [
                {"name": self.sidecar_volume, "mountPath": "/data"}
            ]
        }

        self._manifest["spec"]["containers"].append(sidecar)

        try:
            with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".yaml") as temp_file:
                yaml.dump(self._manifest, temp_file)
                updated_manifest_path = temp_file.name
                self.logger.debug(f"Updated manifest written to temporary file: {updated_manifest_path}")

            self._manifest_path = updated_manifest_path
        except Exception as e:
            self.logger.error(f"Failed to write updated manifest to temporary file: {e}")
            raise


    def _attempt_port_forwarding(self, candidate_ports: list) -> bool:
            """
            Attempt to set up port forwarding using a list of candidate ports.

            :param candidate_ports: List of local ports to attempt for port forwarding.
            :return: True if port forwarding starts successfully, False otherwise.
            """
            self.logger.debug(f"Attempting to set up port forwarding for pod {self.name} using ports: {candidate_ports}")
            for port in candidate_ports:
                if self._port_forward(local_port=port, pod_port=22):
                    self.ssh_port = port  # Save the successfully forwarded port
                    self.logger.debug(f"Port forwarding established on local port {port}")
                    return True
            self.logger.error("Failed to establish port forwarding on any of the candidate ports.")
            return False


    def _port_forward(self, local_port: int, pod_port: int) -> bool:
        """
        Set up port forwarding from a pod's container to the local machine.
        :param local_port: Local machine port to forward traffic to.
        :param pod_port: Port in the pod to forward traffic from.
        :return: True if port forwarding starts successfully, False otherwise.
        """
        self.logger.debug(
            f"Setting up port forwarding from local port {local_port} to pod {self.name} on port {pod_port}"
        )
        try:
            # Start the port-forwarding process
            self.ssh_port_forward_process = subprocess.Popen(
                [
                    "kubectl",
                    "--context", self.context,
                    "--namespace", self.namespace,
                    "port-forward", self.name,
                    f"{local_port}:{pod_port}"
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            # Wait for the local port to become active (retry up to 10 times)
            for _ in range(10):
                if self._is_port_active(local_port):
                    self.logger.debug(f"Port forwarding is active and ready on port {local_port}.")
                    return True
                time.sleep(1)  # Wait 1 second before retrying

            # If the loop completes, the port is still not active
            self.logger.error(f"Port forwarding process started, but port {local_port} is not active.")
            self.ssh_port_forward_process.terminate()
            self.ssh_port_forward_process = None
            return False

        except Exception as e:
            self.logger.error(f"Failed to set up port forwarding: {e}")
            self.ssh_port_forward_process = None
            return False


    def _is_port_active(self, port: int) -> bool:
        """
        Check if a local port is active and listening.

        :param port: Port number to check.
        :return: True if the port is active, False otherwise.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)  # Set a timeout for the connection attempt
            result = sock.connect_ex(('localhost', port))
            return result == 0


    def _transfer_ssh_key(self):
        """
        Generate and transfer an SSH key to the rsync sidecar for secure communication.
        The private key is written to a temporary file for SSH login, and the public key is
        temporarily saved for transfer to the pod.
        """
        # Generate SSH keys
        self.private_key, self.public_key = generate_ssh_key_pair()

        # Create a temporary file for the private key
        public_key_temp_file = None

        try:
            # Save private key to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, mode="w") as private_key_file:
                self.private_key_path = private_key_file.name
                self.logger.debug(f"Saving private key to temporary file: {self.private_key_path}")
                private_key_file.write(self.private_key)
            os.chmod(self.private_key_path, 0o600)  # Set proper permissions for the private key

            # Write public key to a temporary file for transfer
            with tempfile.NamedTemporaryFile(delete=False, mode="w") as public_key_file:
                public_key_temp_file = public_key_file.name
                self.logger.debug(f"Saving public key to temporary file: {public_key_temp_file}")
                public_key_file.write(self.public_key)

            # Transfer the public key to the pod
            self.logger.debug("Transferring SSH public key to rsync sidecar")
            if not super().kubectl_copy(
                container_name="rsync-sidecar",
                src_path=public_key_temp_file,
                dest_path="/root/.ssh/authorized_keys",
                verbose=False
            ):
                raise RuntimeError("Failed to copy public key to container")

            # Set proper permissions for the SSH key inside the container
            super().run_container_cmd(
                command=["chmod", "600", "/root/.ssh/authorized_keys"],
                container_name="rsync-sidecar"
            )
            super().run_container_cmd(
                command=["chown", "root:root", "/root/.ssh/authorized_keys"],
                container_name="rsync-sidecar"
            )
            self.logger.debug("SSH key transferred and permissions set successfully")
        except Exception as e:
            self.logger.error(f"Error transferring SSH key: {e}")
            raise
        finally:
            # Cleanup the temporary public key file
            if public_key_temp_file and os.path.exists(public_key_temp_file):
                self.logger.debug(f"Cleaning up temporary public key file: {public_key_temp_file}")
                os.remove(public_key_temp_file)


    def _cleanup_private_key(self):
        """
        Clean up the temporary private key file.
        """
        if self.private_key_path and os.path.exists(self.private_key_path):
            self.logger.debug(f"Cleaning up private key file: {self.private_key_path}")
            os.remove(self.private_key_path)
            self.private_key_path = None


    def _stop_port_forward(self):
        """
        Terminate the port-forwarding process.
        """
        if self.ssh_port_forward_process:
            self.logger.debug("Terminating port forwarding process.")
            self.ssh_port_forward_process.terminate()
            self.ssh_port_forward_process = None
        else:
            self.logger.warning("No active port-forwarding process to terminate.")


# --------------------------------------------------------------------------------
# Public Methods
# --------------------------------------------------------------------------------


    def transfer_files(self, src_path: str, dest_path: str, flags: str = "-avz"):
        """
        Transfer files to the rsync sidecar using rsync over SSH with clean progress display.
        :param source: Path to the source file or directory on the local machine.
        :param destination: Path inside the rsync sidecar where the file(s) should be transferred.
        :param flags: Additional flags to pass to the rsync command.
        """
        if not self.private_key_path:
            raise ValueError("A private key must be generated or provided to use rsync.")

        if os.path.isdir(src_path) and not src_path.endswith('/'):
            self.logger.warning("Source path does not end with '/'. Adjusting to avoid nesting issues.")
            src_path += '/'

        ssh_target = f"root@localhost:{dest_path}"

        rsync_command = [
            "rsync",
            flags,
            "--progress",  # Show progress
            "-e", f"ssh -i {self.private_key_path} -o StrictHostKeyChecking=no -p {self.ssh_port}",
            src_path,
            ssh_target,
        ]

        try:
            self.logger.info(f"Transferring files with rsync: {rsync_command}")
            process = subprocess.Popen(
                rsync_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,  # Enable line-by-line text output
                bufsize=1,  # Line buffering
            )

            current_file = None

            for line in process.stdout:
                line = line.strip()

                # Skip lines with undesired content
                if any(skip in line for skip in ["building file list", "files to consider", "files...", "./"]):
                    continue

                # Detect a new file being transferred
                if line and '%' not in line and "xfer#" not in line and "to-check=" not in line:
                    # Print the new file name on a new line
                    current_file = line
                    print(f"\nTransferring: {current_file}")
                    continue

                # Match progress information for the current file
                # Regex example: "247693312   35%    5.32MB/s    0:01:20"
                progress_match = re.match(r"^(\d+)\s+(\d+)%\s+([\d.]+\S+)\s+(\S+)", line)
                if progress_match:
                    transferred, percent, speed, eta = progress_match.groups()

                    # Clear any leftover text from previous updates
                    print("\r" + " " * 80 + "\r", end="")

                    # Update progress line for the current file
                    print(f"Progress: {transferred} bytes, {percent}% complete, {speed}, ETA {eta}", end="", flush=True)

            # Ensure the final progress line completes
            print("\n")

            process.wait()

            if process.returncode != 0:
                stderr = process.stderr.read()
                self.logger.error(f"Rsync failed: {stderr}")
                raise RuntimeError(f"Rsync command failed with error: {stderr}")

            self.logger.info("Rsync transfer completed successfully.")
            print("Rsync transfer completed successfully.")

        except Exception as e:
            self.logger.error(f"Error during rsync file transfer: {e}")
            raise

    def print_ssh_command(self):
        """
        Print the SSH command to connect to the rsync sidecar container.
        """
        if not self.ssh_port:
            raise ValueError("Port forwarding must be established to connect to the rsync sidecar.")

        ssh_command = f"ssh -i {self.private_key_path} -p {self.ssh_port} root@localhost"
        print(f"Use the following command to connect to the rsync sidecar container:\n{ssh_command}")
        return ssh_command
