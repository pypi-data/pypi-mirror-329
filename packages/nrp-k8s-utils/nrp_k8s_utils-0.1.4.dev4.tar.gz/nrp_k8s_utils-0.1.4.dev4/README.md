# NRP_K8S_UTILS

`nrp_k8s_utils` is a utility package for researchers using the National Research Platform kubernetes cluster. Currently the package is general purpose and can be used for other kubernetes clusters but may be specialized in the future and may not be compatible with non NRP clusters in the future. 


## Installation

To install the package, clone the repository into your project directory. The package will eventually be available to install through anaconda:

```sh
pip install nrp_k8s_utils
```

# Dependencies
NRP_K8S_Utils is built off of kubectl and runs kubectl commands using the subprocess module. Kubectl is required for the package to run. additionally, rsync and ssh is required to use the RSyncTransferPod class.

- `kubectl` 
- `rsync`
- `ssh`

Python dependencies include cryptography and pyyaml, ensure both packages are installed in your conda environment

- `cryptography`
- `pyyaml`


## Overview

```python
from nrp_k8s_utils import RSyncTransferPod, PodManager, ControllerManager, KubectlCore
```
The package currently offers the RSyncTransferPod, PodManager, and ControllerManager Classes

KubectlCore is the base class for all other classes in the package. It abstracts running subprocess commands with Kubectl and include methods for running kubectl commands using the subprocess package in the python standard library. 

PodManager inherits from KubectlCore and contains all of the same methods to run Kubectl commands. PodManager adds on additional functionality to manage the state of a Pod. PodManager include methods for monitoring, running commands within a specified container, copying files with Kubectl,  and starting and stopping pods automatically. 

RSyncTransferPod is a superset of PodManager and contains all of the functionality of the PodManager class. RSyncTransferPod adds the Rsync sidecar to any manifest and automatically sets up ssh, portforwarding, and abstracts file transfer to a specified persistent volume. 

Controller Manager also inherits from KubectlCore and is the analog to PodManager for running Kubernetes controllers (Jobs, Stateful Sets, Replica Sets, etc)


## Instantiating a class

### Context and Path
The package runs kubectl commands using the subprocess module and uses the current context set in  kubectl by default. Users can optionally specify a specific context when instantiating any class in the package and it will append the desired context automatically to all future commands.

The classes within the package also accept an optional path argument for Kubectl if Kubectl is not recognized as an environment variable.

### Manifests
```python
manifest: str = "/path/to/manifest.yaml"
manifest: dict = {
    "apiVersion": "v1",
    "kind": "Pod",
    "metadata": {
        "name": "example-pod"
    },
    "spec": {
        "containers": [],
        "volumes": [
            {
                "name": "main",
                "persistentVolumeClaim": {
                    "claimName": "mdsmlvol"
                }
            }
        ],
        "restartPolicy": "Always"
    },
}
```

All classes, except KubectlCore, take a python dict or path to a valid yaml file specifying the manifest for the Kubernetes object. Once the class is instantiated, the manifest is managed internally. If a yaml file was used, editing the yaml file after the class is instantiated will not change the manifest used by the class, unless the object is stopped and restarted. 

KubectlCore contains the _parse_manifest() method which is intended to be used in child classes. Users can extend the KubectlCore class for their applications or just use KubectlCore as a stand-alone and lightweight class to run Kubectl Commands


```python
rsync_pod = RSyncTransferPod(
    manifest=manifest, 
    path="path"
    context="context"
    volume="main_volume", 
)
rsync_pod.start_pod()

pod = PodManager(manifest=manifest, )
pod.start_pod()
pod.stop_pod()
```
 RSyncTransferPod must have a persistent volume specified as an argument to which the rsync-sidecar container will mount to. If volume is not specified and there is one persistent volume in the manifest, the rsync-sidebar will automatically mount to that one. 


### Transfering Files

```python
src_path = "/path/to/source/dir"
dest_path = "/data" 

rsync_pod.transfer_files(src_path=src_path, dest_path=dest_path)
pod.kubectl_copy(container_name="my_container_name", src_path=src_path, dest_path=dest_path)
```

RSyncTransferPod and PodManager can both transfer files using kubectl cp. However, `kubectl_copy()` should only be used for small files as running large transfers can overload the kubernetes api node. `transfer_files()` can be used with the RSyncTransferPod for long-running or large file transfers. A container is not specified because the class can only RSync files to the RSyncSidecar container which is added automatically. `dest_path` in the `transfer_files()` method refers to the destination path within the persistent volume that was specified, whereas in `kubectl_copy` dest_path is any path within any container in the pod. 


### Monitoring and Logging

```python
pod.describe_pod()
pod.get_pod_status()
pod.print_logs(container="my_container_name")

namespace: str = pod.get_current_namespace()
context: str = pod.get_current_context()
```
All methods are accessible in both versions of PodManager. The above methods run kubectl commands `describe pod`, `get pod`, and `logs`. `get_current_context()` and `get_current_namespace()` returns strings containing currently selected kubectl context and namespace. 


### Running Commands

```python
command = 'ls -l /data'
rsync_pod.run_container_cmd(command=command, container="my_container_name")

command = ['rm', '-rf', file_name]
pod.run_container_cmd(command=command, container="my_container_name")
```
commands can be run by specifying a container name and command. A command can either be a list or a string. A list is useful if a parameter is a variable.

```python
command = ["get", "pods"]
pod.run_kubectl_cmd(command)
```
the run_kubectl_cmd method includes all context information to run a kubectl command so only the arguments after kubectl can be included


### Modifying the Manifest

```python
pod.add_volume(volume_dict)
pod.add_container(container_dict)

pod.delete_volume("Volume Name")
pod.delete_container("Container Name")

pod.overwrite_manifest(new_manifest)
```

The manifest is managed internally after the class is instantiated. To modify the manifest, the above methods can be used. 



