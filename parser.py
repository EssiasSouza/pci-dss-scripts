"""
parser.py

Extracts only security-relevant fields from Kubernetes manifests.
"""

from models import (
    ParsedWorkload,
    Identification,
    Container,
    ContainerSecurityContext,
    ContainerResources,
    EnvironmentVariable,
    EnvFromSource,
    Volume,
    VolumeMount,
    ServiceAccount,
    Networking,
    Scheduling,
    RelevantAnnotations,
    Probe,
)


def parse_identification(manifest):
    """
    Extract workload identification information.
    """

    metadata = manifest.get("metadata", {})

    annotations = metadata.get("annotations", {})

    helm_annotations = {
        key: value
        for key, value in annotations.items()
        if key.startswith("meta.helm.sh/")
    }

    return Identification(
        kind=manifest.get("kind"),
        name=metadata.get("name"),
        namespace=metadata.get("namespace"),
        labels=metadata.get("labels", {}),
        helm_annotations=helm_annotations,
        replicas=(
            manifest.get("spec", {})
            .get("replicas")
        ),
    )


def parse_security_context(container):
    """
    Extract container security context.
    """

    context = container.get("securityContext", {})

    capabilities = context.get("capabilities", {})

    seccomp_profile = context.get(
        "seccompProfile",
        {}
    )

    return ContainerSecurityContext(
        run_as_non_root=context.get("runAsNonRoot"),
        run_as_user=context.get("runAsUser"),
        run_as_group=context.get("runAsGroup"),
        allow_privilege_escalation=context.get(
            "allowPrivilegeEscalation"
        ),
        privileged=context.get("privileged"),
        read_only_root_filesystem=context.get(
            "readOnlyRootFilesystem"
        ),
        capabilities_add=capabilities.get(
            "add",
            []
        ),
        capabilities_drop=capabilities.get(
            "drop",
            []
        ),
        seccomp_profile=seccomp_profile.get(
            "type"
        ),
    )


def parse_resources(container):
    """
    Extract resource requests and limits.
    """

    resources = container.get(
        "resources",
        {}
    )

    return ContainerResources(
        requests=resources.get(
            "requests",
            {}
        ),
        limits=resources.get(
            "limits",
            {}
        ),
    )


def parse_environment(container):
    """
    Extract environment variables and references.
    """

    variables = []

    for env in container.get("env", []):

        value_from = env.get(
            "valueFrom",
            {}
        )

        secret_ref = value_from.get(
            "secretKeyRef",
            {}
        )

        configmap_ref = value_from.get(
            "configMapKeyRef",
            {}
        )

        variables.append(
            EnvironmentVariable(
                name=env.get("name"),
                value=env.get("value"),
                secret_ref=secret_ref.get("name"),
                secret_key=secret_ref.get("key"),
                configmap_ref=configmap_ref.get("name"),
                configmap_key=configmap_ref.get("key"),
            )
        )

    return variables


def parse_env_from(container):
    """
    Extract envFrom references.
    """

    sources = []

    for item in container.get("envFrom", []):

        secret_ref = item.get(
            "secretRef",
            {}
        )

        configmap_ref = item.get(
            "configMapRef",
            {}
        )

        sources.append(
            EnvFromSource(
                secret_ref=secret_ref.get("name"),
                configmap_ref=configmap_ref.get("name"),
            )
        )

    return sources


def parse_volume_mounts(container):
    """
    Extract volume mounts.
    """

    mounts = []

    for mount in container.get(
        "volumeMounts",
        []
    ):
        mounts.append(
            VolumeMount(
                name=mount.get("name"),
                mount_path=mount.get("mountPath"),
                read_only=mount.get("readOnly"),
            )
        )

    return mounts


def parse_probe(container, probe_name):
    """
    Extract probe existence.
    """

    return Probe(
        enabled=probe_name in container
    )


def parse_containers(manifest):
    """
    Extract containers information.
    """

    containers = []

    pod_spec = (
        manifest.get("spec", {})
        .get("template", {})
        .get("spec", {})
    )

    for item in pod_spec.get(
        "containers",
        []
    ):

        containers.append(
            Container(
                name=item.get("name"),
                image=item.get("image"),
                image_pull_policy=item.get(
                    "imagePullPolicy"
                ),
                ports=item.get(
                    "ports",
                    []
                ),
                command=item.get(
                    "command",
                    []
                ),
                args=item.get(
                    "args",
                    []
                ),
                security_context=parse_security_context(
                    item
                ),
                resources=parse_resources(
                    item
                ),
                env=parse_environment(
                    item
                ),
                env_from=parse_env_from(
                    item
                ),
                volume_mounts=parse_volume_mounts(
                    item
                ),
                liveness_probe=parse_probe(
                    item,
                    "livenessProbe"
                ),
                readiness_probe=parse_probe(
                    item,
                    "readinessProbe"
                ),
                startup_probe=parse_probe(
                    item,
                    "startupProbe"
                ),
            )
        )

    return containers


def parse_volumes(manifest):
    """
    Extract volumes information.
    """

    volumes = []

    pod_spec = (
        manifest.get("spec", {})
        .get("template", {})
        .get("spec", {})
    )

    for item in pod_spec.get(
        "volumes",
        []
    ):

        volume_type = "unknown"

        if "secret" in item:
            volume_type = "secret"

        elif "hostPath" in item:
            volume_type = "hostPath"

        elif "persistentVolumeClaim" in item:
            volume_type = "persistentVolumeClaim"

        elif "projected" in item:
            volume_type = "projected"

        elif "emptyDir" in item:
            volume_type = "emptyDir"

        volumes.append(
            Volume(
                name=item.get("name"),
                volume_type=volume_type,
                secret_name=(
                    item.get("secret", {})
                    .get("secretName")
                ),
                pvc_name=(
                    item.get(
                        "persistentVolumeClaim",
                        {}
                    )
                    .get("claimName")
                ),
                host_path=(
                    item.get("hostPath", {})
                    .get("path")
                ),
            )
        )

    return volumes


def parse_service_account(manifest):
    """
    Extract service account configuration.
    """

    pod_spec = (
        manifest.get("spec", {})
        .get("template", {})
        .get("spec", {})
    )

    return ServiceAccount(
        service_account=pod_spec.get(
            "serviceAccount"
        ),
        service_account_name=pod_spec.get(
            "serviceAccountName"
        ),
        automount_service_account_token=pod_spec.get(
            "automountServiceAccountToken"
        ),
    )


def parse_networking(manifest):
    """
    Extract networking security settings.
    """

    pod_spec = (
        manifest.get("spec", {})
        .get("template", {})
        .get("spec", {})
    )

    return Networking(
        host_network=pod_spec.get(
            "hostNetwork"
        ),
        host_pid=pod_spec.get(
            "hostPID"
        ),
        host_ipc=pod_spec.get(
            "hostIPC"
        ),
        dns_policy=pod_spec.get(
            "dnsPolicy"
        ),
    )


def parse_scheduling(manifest):
    """
    Extract scheduling information.
    """

    pod_spec = (
        manifest.get("spec", {})
        .get("template", {})
        .get("spec", {})
    )

    return Scheduling(
        node_selector=pod_spec.get(
            "nodeSelector",
            {}
        ),
        tolerations=pod_spec.get(
            "tolerations",
            []
        ),
        affinity=pod_spec.get(
            "affinity",
            {}
        ),
    )


def parse_annotations(manifest):
    """
    Extract relevant annotations only.
    """

    annotations = (
        manifest.get("metadata", {})
        .get("annotations", {})
    )

    prefixes = (
        "iam.gke.io/",
        "vault.hashicorp.com/",
        "sidecar.istio.io/",
        "linkerd.io/",
        "container.apparmor.",
        "seccomp.",
    )

    filtered = {
        key: value
        for key, value in annotations.items()
        if key.startswith(prefixes)
    }

    return RelevantAnnotations(
        values=filtered
    )


def parse_workload(manifest):
    """
    Main parser function.
    """

    return ParsedWorkload(
        identification=parse_identification(
            manifest
        ),
        containers=parse_containers(
            manifest
        ),
        volumes=parse_volumes(
            manifest
        ),
        service_account=parse_service_account(
            manifest
        ),
        networking=parse_networking(
            manifest
        ),
        scheduling=parse_scheduling(
            manifest
        ),
        annotations=parse_annotations(
            manifest
        ),
    )