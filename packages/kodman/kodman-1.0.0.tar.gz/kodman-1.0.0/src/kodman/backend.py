import io
import logging
import sys
import tarfile
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from kubernetes import client, config, watch
from kubernetes.client.models.v1_pod import V1Pod
from kubernetes.client.rest import ApiException
from kubernetes.stream import stream

log = logging.getLogger("kodman")


@dataclass(frozen=True)
class RunOptions:
    image: str
    command: list[str] = field(default_factory=lambda: [])
    args: list[str] = field(default_factory=lambda: [])
    volumes: list[str] = field(default_factory=lambda: [])

    def __hash__(self):
        hash_candidates = (
            self.image,
            self.command,
            self.args,
            self.volumes,
            time.time(),  # Add timestamp
        )

        to_hash = []
        for item in hash_candidates:
            if not item:  # Skip unhashable falsy items
                pass
            elif type(item) is list:  # Make hashable
                to_hash.append(tuple(item))
            else:
                to_hash.append(item)

        _hash = hash(tuple(to_hash))
        _hash += sys.maxsize + 1  # Ensure always positive
        return _hash


@dataclass(frozen=True)
class DeleteOptions:
    name: str


def cp_k8s(
    kube_conn: client.CoreV1Api,
    namespace: str,
    pod_name: str,
    container: str,
    source_path: Path,
    dest_path: Path,
):
    buf = io.BytesIO()
    if not source_path.is_dir() and dest_path.is_dir():
        arcname = dest_path.joinpath(source_path.name)
    else:
        arcname = dest_path

    with tarfile.open(fileobj=buf, mode="w:tar") as tar:
        tar.add(source_path, arcname=arcname)
    commands = [buf.getvalue()]

    # Copying file
    exec_command = ["tar", "xvf", "-", "-C", "/"]
    resp = stream(
        kube_conn.connect_get_namespaced_pod_exec,
        pod_name,
        namespace,
        container=container,
        command=exec_command,
        stderr=True,
        stdin=True,
        stdout=True,
        tty=False,
        _preload_content=False,
    )

    while resp.is_open():
        resp.update(timeout=1)
        if resp.peek_stdout():
            log.debug(f"STDOUT: {resp.read_stdout()}")
        if resp.peek_stderr():
            log.debug(f"STDERR: {resp.read_stderr()}")
        if commands:
            c = commands.pop(0)
            resp.write_stdin(c)
        else:
            break
    resp.close()


def get_incluster_context():
    ns_path = "/var/run/secrets/kubernetes.io/serviceaccount/namespace"
    context = {}
    with open(ns_path) as f:
        context["namespace"] = f.read().strip()
    context["cluster"] = "default"
    context["user"] = "default"
    return context


class Backend:
    def __init__(self):
        self.return_code = 0
        self._polling_freq = 1
        self._grace_period = 2  # Is this too aggressive?

    def connect(self):
        # Load config for user/serviceaccount
        # https://github.com/kubernetes-client/python/issues/1005
        try:
            log.debug(
                "Loading kube config for user interaction from outside of cluster"
            )
            config.load_kube_config()
            log.debug("Loaded kube config successfully")
            self._context = config.list_kube_config_contexts()[1]["context"]
        except config.config_exception.ConfigException:
            log.debug("Failed to load kube config, trying in-cluster config")
            config.load_incluster_config()
            log.debug("Loaded in-cluster config successfully")
            self._context = get_incluster_context()

        self._client = client.CoreV1Api()
        log.debug("The current context is:")
        log.debug(f"  Cluster: {self._context['cluster']}")
        log.debug(f"  Namespace: {self._context['namespace']}")
        log.debug(f"  User: {self._context['user']}")

    def run(self, options: RunOptions) -> str:
        unique_pod_name = f"kodman-run-{hash(options)}"
        init_container_name = "wait-for-signal"
        namespace = self._context["namespace"]
        pod_manifest: dict[str, Any] = {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {
                "name": unique_pod_name,
            },
            "spec": {
                "initContainers": [
                    {
                        "name": init_container_name,
                        "image": "busybox",
                        "command": [
                            "sh",
                            "-c",
                            "until [ -f /tmp/trigger ];"
                            'do echo "Waiting for trigger...";'
                            "sleep 1;"
                            "done;"
                            'echo "Trigger file found!"',
                        ],
                        "volumeMounts": [],
                    },
                ],
                "containers": [
                    {
                        "image": options.image,
                        "name": "kodman-exec",
                        "volumeMounts": [],
                    }
                ],
                "volumes": [],
            },
        }

        if options.command:
            container = pod_manifest["spec"]["containers"][0]
            container["command"] = options.command

        if options.args:
            pod_manifest["spec"]["containers"][0]["args"] = options.args

        volumes: list[dict[str, Path]] = []
        if options.volumes:
            for i, options_volume in enumerate(options.volumes):
                process = options_volume.split(":")
                src = Path(process[0]).resolve()
                dst = src  # If no dst, set same as src
                try:
                    dst = Path(process[1])
                except IndexError:
                    pass
                if not dst.is_absolute():
                    raise ValueError("Destination path must be absolute")
                volumes.append({"src": src, "dst": dst})  # cache for later
                log.debug(f"Mount: {src} to {dst}")

                pod_manifest["spec"]["initContainers"][0]["volumeMounts"].append(
                    {"name": f"shared-data-{i}", "mountPath": str(dst)}
                )
                pod_manifest["spec"]["containers"][0]["volumeMounts"].append(
                    {"name": f"shared-data-{i}", "mountPath": str(dst)}
                )
                pod_manifest["spec"]["volumes"].append(
                    {
                        "name": f"shared-data-{i}",
                        "emptyDir": {},
                    }
                )

        # Schedule pod and block until read
        log.debug(f"Creating pod: {unique_pod_name}")
        self._client.create_namespaced_pod(body=pod_manifest, namespace=namespace)
        while True:
            read_resp = self._client.read_namespaced_pod(
                name=unique_pod_name, namespace=namespace
            )
            # Runtime type checking
            if isinstance(read_resp, V1Pod):
                if not read_resp.status:
                    raise ValueError("Empty pod status")
                if read_resp.status.init_container_statuses:
                    init_status = read_resp.status.init_container_statuses[0]
                    if init_status.state.running:
                        log.debug("Init container is running, pod is ready")
                        break
            else:
                raise TypeError("Unexpected response type")

        # Fill volumes
        for volume in volumes:
            log.debug(f"Transferring {volume['src']} to {volume['dst']}")
            cp_k8s(
                self._client,
                namespace,
                unique_pod_name,
                init_container_name,
                volume["src"],
                volume["dst"],
            )
            log.debug("Transfer completed")

        # Start execution
        log.debug("Execution start")
        exec_command = [
            "/bin/sh",
            "-c",
            "touch /tmp/trigger",
        ]
        _ = stream(
            self._client.connect_get_namespaced_pod_exec,
            unique_pod_name,
            namespace,
            container=init_container_name,
            command=exec_command,
            stderr=True,
            stdin=False,
            stdout=True,
            tty=False,
        )

        while True:
            read_resp = self._client.read_namespaced_pod(
                name=unique_pod_name, namespace=namespace
            )
            if isinstance(read_resp, V1Pod):  # Runtime type checking
                if not read_resp.status:
                    raise ValueError("Empty pod status")
                elif read_resp.status.phase != "Pending":
                    log.debug(f"Pod status: {read_resp.status.phase}")
                    break
                time.sleep(1 / self._polling_freq)
                log.debug(f"Pod status: {read_resp.status.phase}")
            else:
                raise TypeError("Unexpected response type")

        # Attach to pod logging
        log.debug("Try attach to pod logs")
        w = watch.Watch()
        for e in w.stream(
            self._client.read_namespaced_pod_log,
            name=unique_pod_name,
            namespace=namespace,
            follow=True,
        ):
            print(e)
        log.debug("Execution complete")
        w.stop()

        # Check exit codes
        final_pod = self._client.read_namespaced_pod(
            name=unique_pod_name,
            namespace=namespace,
        )
        if isinstance(final_pod, V1Pod):  # Runtime type checking
            if not final_pod.status:
                raise ValueError("Empty pod status")
            container_status = final_pod.status.container_statuses[0]
            while not container_status.state.terminated:
                # Exit early if container didnt even start
                if not container_status.started:
                    log.debug("Container failed to start")
                    self.return_code = 1
                    reason = container_status.state.waiting.reason
                    message = container_status.state.waiting.message
                    log.debug(f"{reason}: {message}")
                    print(message)
                    return unique_pod_name

                log.debug("Awaiting pod termination...")
                time.sleep(1 / self._polling_freq)
                final_pod = self._client.read_namespaced_pod(
                    name=unique_pod_name,
                    namespace=namespace,
                )
                container_status = final_pod.status.container_statuses[0]  # type: ignore
            self.return_code = container_status.state.terminated.exit_code

        return unique_pod_name

    def delete(self, options: DeleteOptions):
        namespace = self._context["namespace"]
        try:
            exists_resp = self._client.read_namespaced_pod(
                name=options.name,
                namespace=namespace,
            )
            self._client.delete_namespaced_pod(
                name=options.name,
                namespace=namespace,
                grace_period_seconds=self._grace_period,
            )
            log.debug("Awaiting pod cleanup...")
            while exists_resp:
                try:
                    exists_resp = self._client.read_namespaced_pod(
                        name=options.name,
                        namespace=namespace,
                    )
                    time.sleep(1 / self._polling_freq)
                except ApiException as e:
                    if e.status == 404:
                        log.debug(f"Pod {options.name} deleted successfully")
                        break
                    else:
                        raise e

        except ApiException as e:
            log.debug(f"Error deleting pod: {e}")
