from .kubectl_core import KubectlCore
import yaml
import logging
import time
import json
import tempfile
import os

from typing import Dict, Union, Optional

class ControllerManager(KubectlCore):
    def __init__(
            self, 
            manifest: Union[str, Dict], 
            context: Optional[str] = None, 
            kubectl_path: Optional[str] = None, 
            debug_mode: Optional[bool] = False
        ):
        """
        Initialize the ControllerManager with a Kubernetes manifest defining a controller
        (e.g. Deployment, StatefulSet, DaemonSet, or Job).

        :param manifest: Path to the manifest file or a dictionary containing the manifest.
        :param context: (Optional) Kubernetes context to use.
        :param kubectl_path: (Optional) Path to the kubectl binary.
        :param debug_mode: (Optional) Enable debug logging.
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
        self.kind = self._manifest.get("kind", "Unknown")
        self.replicas = self._manifest.get("spec", {}).get("replicas", 1)

    # --------------------------------------------------------------------------------
    # Controller Lifecycle Methods
    # --------------------------------------------------------------------------------
    
    def start_controller(self) -> bool:
        """
        Create or update the controller using the manifest and wait until it is ready.
        """
        self.logger.info(f"Starting {self.kind} '{self.name}'")
        cmd = ["apply", "-f", self._manifest_path]
        self.run_kubectl_cmd(cmd, check=True, verbose=True)

        # For controllers that support rollouts, wait for readiness
        self.wait_for_readiness()
        return True

    def stop_controller(self):
        """
        Delete the controller defined in the manifest.
        """
        self.logger.info(f"Stopping {self.kind} '{self.name}'")
        cmd = ["delete", self.kind.lower(), self.name, "-n", self.namespace]
        self.run_kubectl_cmd(cmd, check=False, verbose=True)

    def scale_controller(self, replicas: int, verbose: bool = True) -> bool:
        """
        Scale the controller to the desired number of replicas.

        :param replicas: The number of replicas to scale to.
        :param verbose: If True, print command output.
        :return: True if scaling succeeds.
        """
        self.logger.info(f"Scaling {self.kind} '{self.name}' to {replicas} replicas")
        cmd = [
            "scale", self.kind.lower(), self.name,
            "-n", self.namespace, f"--replicas={replicas}"
        ]
        result = self.run_kubectl_cmd(cmd, check=True, verbose=verbose)
        if result.returncode == 0:
            self.logger.info(f"Scaled {self.kind} '{self.name}' successfully")
            return True
        else:
            self.logger.error(f"Error scaling {self.kind} '{self.name}': {result.stderr}")
            return False

    def describe_controller(self, verbose: bool = True) -> str:
        """
        Retrieve a detailed description of the controller.

        :param verbose: If True, print command output.
        :return: The description output as a string.
        """
        self.logger.info(f"Describing {self.kind} '{self.name}'")
        cmd = ["describe", self.kind.lower(), self.name, "-n", self.namespace]
        result = self.run_kubectl_cmd(cmd, check=True, verbose=verbose)
        return result.stdout

    def get_controller_status(self, verbose: bool = True) -> Dict:
        """
        Retrieve the status of the controller as a JSON dictionary.

        :param verbose: If True, print command output.
        :return: The status section of the controller's JSON representation.
        """
        self.logger.info(f"Getting status for {self.kind} '{self.name}'")
        cmd = ["get", self.kind.lower(), self.name, "-n", self.namespace, "-o", "json"]
        result = self.run_kubectl_cmd(cmd, check=True, verbose=verbose)
        try:
            controller_info = json.loads(result.stdout)
            status = controller_info.get("status", {})
            self.logger.debug(f"{self.kind} status: {status}")
            return status
        except json.JSONDecodeError as e:
            self.logger.error(f"Error parsing JSON output: {e}")
            raise RuntimeError("Failed to parse controller status JSON")

    def wait_for_readiness(self, timeout: int = 300, interval: int = 5) -> bool:
        """
        Wait until the controller is ready. For Deployments, StatefulSets, and DaemonSets,
        readiness is determined by the number of available replicas. For Jobs, the job is
        considered ready if it has succeeded.

        :param timeout: Maximum time in seconds to wait.
        :param interval: Time in seconds between status checks.
        :return: True if the controller becomes ready before timeout.
        """
        self.logger.info(f"Waiting for {self.kind} '{self.name}' to become ready")
        start_time = time.time()
        lower_kind = self.kind.lower()

        while time.time() - start_time < timeout:
            status = self.get_controller_status(verbose=False)
            if lower_kind in ["deployment", "statefulset", "daemonset"]:
                desired = self._manifest.get("spec", {}).get("replicas", 1)
                available = status.get("availableReplicas", 0)
                if available >= desired:
                    self.logger.info(f"{self.kind} '{self.name}' is ready (available replicas: {available})")
                    return True
            elif lower_kind == "job":
                succeeded = status.get("succeeded", 0)
                if succeeded >= 1:
                    self.logger.info(f"Job '{self.name}' has completed successfully")
                    return True
            else:
                if status:
                    self.logger.info(f"{self.kind} '{self.name}' status retrieved")
                    return True

            self.logger.debug(f"Current {self.kind} status: {status}. Waiting...")
            time.sleep(interval)

        raise TimeoutError(f"Timed out waiting for {self.kind} '{self.name}' to become ready")

    # --------------------------------------------------------------------------------
    # Manifest Modification Methods
    # --------------------------------------------------------------------------------

    def overwrite_manifest(self, manifest: Dict):
        """
        Replace the current manifest with a new one and update the stored attributes.

        :param manifest: Dictionary containing the new manifest.
        """
        self.logger.info(f"Overwriting manifest for {self.kind} '{self.name}'")
        self._manifest = manifest
        try:
            with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".yml") as temp_file:
                yaml.dump(self._manifest, temp_file)
                new_manifest_path = temp_file.name
        except yaml.YAMLError as e:
            raise ValueError(f"Error serializing the manifest to YAML: {e}")
        os.remove(self._manifest_path)
        self._manifest_path = new_manifest_path

        # Update controller properties based on the new manifest
        self.name = self._manifest.get("metadata", {}).get("name", self.name)
        self.kind = self._manifest.get("kind", self.kind)
        self.replicas = self._manifest.get("spec", {}).get("replicas", self.replicas)
