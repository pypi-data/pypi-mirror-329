from .kubectl_core import KubectlCore

import yaml
import logging
import time
import json
import tempfile
import os

from typing import Dict, List, Any, Union, Optional

class PodManager(KubectlCore):

    def __init__(
            self, 
            manifest: Union[str, Dict], 
            context:Optional[str] = None, 
            kubectl_path:Optional[str] = None, 
            debug_mode: Optional[bool] = False
        ): 
        """
        Initialize the PodManager with the path to the Kubernetes manifest file and optional kubeconfig file.

        :param manifest_path: Path to the Kubernetes manifest YAML file.
        :param self.logger_level: self.logger level for the PodManager instance. Default is INFO.
        """    

        self.debug_mode = debug_mode
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG if debug_mode else logging.INFO)

        super().__init__(
            context=context, 
            logger=self.logger,
            kubectl_path=kubectl_path, 
            debug_mode=debug_mode
        )

        super()._parse_manifest(manifest)

        self.name = self._manifest.get("metadata", {}).get("name", "Unknown")
        self.containers = self._manifest.get("spec", {}).get("containers", [])
        self.volumes = self._manifest.get("spec", {}).get("volumes", [])


# --------------------------------------------------------------------------------
# Pod Lifecycle Methods
# --------------------------------------------------------------------------------

    def _start_pod(self):
        """
        Start a pod using the provided Kubernetes manifest.
        """
        self.logger.info("Starting pod")
        cmd = ["apply", "-f", self._manifest_path]
        super().run_kubectl_cmd(cmd, check=True, verbose=False)

    def start_pod(self) -> bool:
        """
        Start a pod using the provided Kubernetes manifest and wait until it is running.
        """
        self.logger.info("Starting pod")
        cmd = ["apply", "-f", self._manifest_path]
        super().run_kubectl_cmd(cmd, check=True, verbose=True)

        start_time = time.time()
        timeout = 300
        while time.time() - start_time < timeout:
            status = self.get_pod_status(verbose=False)
            if status == "Running":
                self.logger.info(f"Pod {self.name} is running")
                return True
            self.logger.debug(f"Waiting for pod {self.name}, current status: {status}")
            time.sleep(1)
        raise TimeoutError(f"Timed out waiting for pod {self.name} to be running.")

    def stop_pod(self):
        """
        Stop a pod defined in the Kubernetes manifest.
        """
        self.logger.info("Stopping pod")
        cmd = ["delete", "pod", self.name, "-n", self.namespace]
        self.run_kubectl_cmd(cmd, check=False) 

# --------------------------------------------------------------------------------
# Public Methods
# --------------------------------------------------------------------------------
    
    def print_logs(self, container_name: str = None):
        """
        Print logs from a specified pod (and optionally container).
        """
        cmd = ["logs", self.name, "-n", self.namespace]
        if container_name:
            cmd.extend(["-c", container_name])

        result = self.run_kubectl_cmd(cmd, check=False)
        if result.returncode != 0:
            self.logger.error(f"Failed to get logs: {result.stderr}")
            raise RuntimeError(result.stderr)

        self.logger.info(result.stdout)
        return result.stdout

    def describe_pod(self):
        """
        Describe the pod defined in the Kubernetes manifest.
        """
        cmd = ["describe", "pod", self.name, "-n", self.namespace]
        result = self.run_kubectl_cmd(cmd, check=False)

        self.logger.info(result.stdout)
        return result.stdout

    def get_pod_status(self, verbose:bool = True) -> str:
        """
        Get the status of the pod defined in the Kubernetes manifest.
        """
        cmd = [
            "get", "pod", self.name, "-n", self.namespace, "-o", "json"
        ]
        result = self.run_kubectl_cmd(cmd, check=False, verbose=verbose)
        if result.returncode != 0:
            self.logger.error(f"Failed to get pod status: {result.stderr}")
            raise RuntimeError(result.stderr)
        try:
            pod_info = json.loads(result.stdout)
            status = pod_info.get("status", {}).get("phase", "Unknown")
            self.logger.debug(f"Pod status: {status}")
            return status
        except json.JSONDecodeError as e:
            self.logger.error(f"Error parsing JSON output: {e}")
            raise RuntimeError("Failed to parse pod status JSON")
    
    def run_container_cmd(self, command: Union[str, List], container_name: str = None, verbose: bool = True) -> str:
        """
        Run a command inside a pod using kubectl exec.
        :param command: Command to run as a list of arguments.
        :param container_name: (Optional) Name of the container in which to run the command.
        :return: Output of the command.
        """

        if isinstance(command, str):
            command = command.split

        cmd = ["exec", self.name, "--"]

        if container_name:
            cmd.insert(cmd.index("exec") + 1, f"-c={container_name}")
        cmd.extend(command)

        if verbose:
            self.logger.info(f"Running command: {' '.join(cmd)}")

        result = super().run_kubectl_cmd(cmd, check=True, verbose=verbose)

        return result.stdout
        
    def kubectl_copy(self, container_name: str, src_path: str, dest_path: str, verbose:bool = True) -> bool:
        """
        Kubectl CP a file from the local filesystem to a directory in a container.

        :param container_name: Name of the container.
        :param src_path: Path to the source file on the local filesystem.
        :param dest_path: Path to the destination directory in the container.
        :return: True if the file was copied successfully, False otherwise.
        """
        cmd = [
            "cp", src_path, f"{self.namespace}/{self.name}:{dest_path}", "-c", container_name
        ]

        if verbose:
            self.logger.info(f"Copying file {src_path} to {self.name}:{dest_path} in {container_name}")

        result = super().run_kubectl_cmd(cmd, check=True, verbose=verbose)
        if result.returncode == 0:
            self.logger.debug(f"File {src_path} copied to {self.name}:{dest_path} in container {container_name}")
            return True
        else:
            self.logger.error(f"Error copying file to container: {result.stderr}")
            return False


    def delete_files(self, container_name: str, file_path: str, verbose:bool = True) -> bool:
        """
        Delete a file from a container.

        :param container_name: Name of the container.
        :param file_path: Path to the file in the container.
        :return: True if the file was deleted successfully, False otherwise.
        """
        cmd = [
            "exec", self.name, "-n", self.namespace, "-c", container_name, "--", "rm", "-rf", file_path
        ]

        if verbose:
            self.logger.info(f"Deleting file {file_path} in {container_name}")

        result = super().run_kubectl_cmd(cmd, check=False, verbose=verbose)
        if result.returncode == 0:
            self.logger.debug(f"File {file_path} deleted from container {container_name}")
            return True
        else:
            self.logger.error(f"Error deleting file from container: {result.stderr}")
            return False


# --------------------------------------------------------------------------------
# Manifest Methods
# --------------------------------------------------------------------------------

    def add_container(self, container: Dict):
        """
        Add a container to the pod manifest.

        :param container: Dictionary containing the container definition.
        """
        # Check if container is valid
        if not container.get("name"):
            raise ValueError("Container must have a name")
        if not container.get("image"):
            raise ValueError("Container must have an image")
        
        for c in self.containers:
            if c["name"] == container["name"]:
                raise ValueError(f"Container with name {container['name']} already exists")

        self.containers.append(container)
        self._manifest["spec"]["containers"] = self.containers
        try:
            with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".yml") as temp_file:
                yaml.dump(self._manifest, temp_file)
        except yaml.YAMLError as e:
            raise ValueError(f"Error serializing the manifest to YAML: {e}")
        os.remove(self._manifest_path)
        self._manifest_path = temp_file.name

    def add_volume(self, volume: Dict):
        """
        Add a volume to the pod manifest.

        :param volume: Dictionary containing the volume definition.
        """

        # Check if volume is valid
        if not volume.get("name"):
            raise ValueError("Volume must have a name")

        for v in self.volumes:
            if v["name"] == volume["name"]:
                raise ValueError(f"Volume with name {volume['name']} already exists")

        self.volumes.append(volume)
        self._manifest["spec"]["volumes"] = self.volumes
        try:
            with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".yml") as temp_file:
                yaml.dump(self._manifest, temp_file)
        except yaml.YAMLError as e:
            raise ValueError(f"Error serializing the manifest to YAML: {e}")
        os.remove(self._manifest_path)
        self._manifest_path = temp_file.name

    def remove_container(self, container_name: str):
        """
        Remove a container from the pod manifest.

        :param container_name: Name of the container to remove.
        """
        for c in self.containers:
            if c["name"] == container_name:
                self.containers.remove(c)
                break
        else:
            raise ValueError(f"Container with name {container_name} not found")
        
        self._manifest["spec"]["containers"] = self.containers
        try:
            with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".yml") as temp_file:
                yaml.dump(self._manifest, temp_file)
        except yaml.YAMLError as e:
            raise ValueError(f"Error serializing the manifest to YAML: {e}")
        os.remove(self._manifest_path)
        self._manifest_path = temp_file.name
    
    def remove_volume(self, volume_name: str):
        """
        Remove a volume from the pod manifest.

        :param volume_name: Name of the volume to remove.
        """
        for v in self.volumes:
            if v["name"] == volume_name:
                self.volumes.remove(v)
                break
        else:
            raise ValueError(f"Volume with name {volume_name} not found")
        
        self._manifest["spec"]["volumes"] = self.volumes
        try:
            with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".yml") as temp_file:
                yaml.dump(self._manifest, temp_file)
        except yaml.YAMLError as e:
            raise ValueError(f"Error serializing the manifest to YAML: {e}")
        os.remove(self._manifest_path)
        self._manifest_path = temp_file.name

    def overwrite_manifest (self, manifest: Dict):
        """
        Replace the current manifest with a new one.

        :param manifest: Dictionary containing the new manifest.
        """
        self._manifest = manifest
        try:
            with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".yml") as temp_file:
                yaml.dump(self._manifest, temp_file)
        except yaml.YAMLError as e:
            raise ValueError(f"Error serializing the manifest to YAML: {e}")
        os.remove(self._manifest_path)
        self._manifest_path = temp_file.name
