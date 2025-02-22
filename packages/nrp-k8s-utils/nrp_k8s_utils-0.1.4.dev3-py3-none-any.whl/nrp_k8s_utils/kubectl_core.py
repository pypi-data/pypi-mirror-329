import shutil
import yaml
import logging
import subprocess
import tempfile
import os

from typing import Dict, List, Any, Union, Optional


class KubectlCore():

    def __init__(
            self, 
            logger: logging.Logger = None,
            context:Optional[str] = None, 
            kubectl_path:Optional[str] = None, 
            debug_mode: Optional[bool] = False
        ): 
        """
        Initialize the Kubectl core with the path to the Kubernetes manifest file and optional kubeconfig file.

        :param manifest_path: Path to the Kubernetes manifest YAML file.
        :param self.logger_level: self.logger level for the PodManager instance. Default is INFO.
        """    

        self.debug_mode = debug_mode
        self.logger = logger
        self.logger.setLevel(logging.DEBUG if debug_mode else logging.INFO)

        if kubectl_path:
            self.kubectl_path = kubectl_path
        else:
            self._get_kubectl_path()

        if context and not isinstance(context, str):
            raise ValueError("Context must be a string")
        
        if context and isinstance(context, str):
            self.context = context
            self.logger.debug(f"Using provided context: {context}")
        else:
            self.context = self._get_current_context(verbose=False)
            self.logger.debug(f"Using current context: {self.context}")

        self.namespace = self._get_current_namespace(verbose=False)


    def _parse_manifest(self, manifest: Union[str, Dict]):
        if isinstance(manifest, str):
            self._manifest_path = manifest
            try:
                with open(self._manifest_path, 'r') as file:
                    self._manifest: Dict[str, Any] = yaml.safe_load(file)
            except FileNotFoundError:
                raise ValueError(f"Manifest file not found: {manifest}")
            except yaml.YAMLError as e:
                raise ValueError(f"Error parsing manifest file: {e}")
            try:
                with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".yml") as temp_file:
                    yaml.dump(self._manifest, temp_file)
                    self._manifest_path = temp_file.name
            except yaml.YAMLError as e:
                raise ValueError(f"Error serializing the manifest to YAML: {e}")
        elif isinstance(manifest, Dict):
            self._manifest = manifest
            try:
                with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".yml") as temp_file:
                    yaml.dump(self._manifest, temp_file)
                    self._manifest_path = temp_file.name
            except yaml.YAMLError as e:
                raise ValueError(f"Error serializing the manifest to YAML: {e}")
        else:
            raise ValueError("Manifest must be a file path or a dictionary")
        
    def _get_kubectl_path(self):
        """Get the path to the kubectl binary."""
        kubectl_path = os.getenv("KUBECTL_PATH", shutil.which("kubectl"))
        if not kubectl_path:
            raise FileNotFoundError(
                "The `kubectl` command is not found. Install it or set the KUBECTL_PATH environment variable."
            )
        self.kubectl_path = kubectl_path

# --------------------------------------------------------------------------------
# Core Methods
# --------------------------------------------------------------------------------

    def get_current_namespace(self, verbose:bool=True) -> str:
        """
        Retrieve the namespace defined in the current kubectl context.
        If no namespace is defined, return 'default'.

        :return: The namespace defined in the current context or 'default'.
        """
        try:
            cmd = ["config", "view", "--minify", "--output", "jsonpath={..namespace}"]
            result = self.run_kubectl_cmd(cmd, check=True, verbose=verbose)
            namespace = result.stdout.strip()
            if namespace:
                self.logger.debug(f"Current namespace: {namespace}")
                return namespace
            else:
                self.logger.debug("No namespace defined in the current context. Using 'default'.")
                self.logger.info(f"Current namespace: default")
                return "default"
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error retrieving current namespace: {e.stderr.strip()}")
            raise RuntimeError(f"Failed to retrieve current namespace: {e.stderr.strip()}")

    def get_current_context(self, verbose:bool=True) -> str:
        """
        Retrieve the current kubectl context as selected in the terminal.

        :return: The name of the currently active kubectl context.
        """
        try:
            cmd = ["kubectl", "config", "current-context"]
            result = self.run_subprocess_cmd(cmd, check=True, verbose=verbose)
            context = result.stdout.strip()
            self.logger.debug(f"Current context: {context}")
            return context
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error retrieving current kubectl context: {e.stderr.strip()}")
            raise RuntimeError(f"Failed to retrieve current kubectl context: {e.stderr.strip()}")
    
    def run_kubectl_cmd(self, command: Union[str, List], check: bool = True, verbose: bool = True) -> subprocess.CompletedProcess:
        """
        Run a kubectl command using subprocess.run.

        :param command: Command to run as a list of arguments.
        :param check: If True, raise an exception if the command fails.
        :param verbose: If True, print the output of the command.
        :return: CompletedProcess object containing the result of the command.
        """
        if isinstance(command, str):
            command = command.split()
        cmd = [self.kubectl_path, "--context", self.context]
        cmd.extend(command)

        result = self.run_subprocess_cmd(cmd, check=check, verbose=verbose)
        return result
    
    def run_subprocess_cmd(self, cmd: Union[str, List], check: bool = True, verbose: bool = True) -> subprocess.CompletedProcess:
        """
        Run a subprocess command using subprocess.run.
        :param cmd: Command to run as a list of arguments.
        :param check: If True, raise an exception if the command fails.
        :param verbose: If True, print the output of the command.
        """
        if not isinstance(cmd, list) or not all(isinstance(arg, str) for arg in cmd):
            raise ValueError(f"Invalid command: {cmd}. It must be a list of strings.")

        self.logger.debug(f"Running command: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        if check and result.returncode != 0:
            self.logger.error(f"Command failed: {result.stderr}")
            raise RuntimeError(f"Command failed: {result.stderr}")
        if verbose:
            self.logger.info(result.stdout)
        return result