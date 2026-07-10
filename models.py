"""
models.py

Data models used by the PCI DSS Evidence Scanner.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# ============================================================================
# Identification
# ============================================================================

@dataclass
class Identification:
    kind: Optional[str] = None
    name: Optional[str] = None
    namespace: Optional[str] = None
    replicas: Optional[int] = None
    labels: Dict[str, str] = field(default_factory=dict)
    helm_annotations: Dict[str, str] = field(default_factory=dict)


# ============================================================================
# Container
# ============================================================================

@dataclass
class ContainerSecurityContext:
    run_as_non_root: Optional[bool] = None
    run_as_user: Optional[int] = None
    run_as_group: Optional[int] = None
    allow_privilege_escalation: Optional[bool] = None
    privileged: Optional[bool] = None
    read_only_root_filesystem: Optional[bool] = None
    capabilities_add: List[str] = field(default_factory=list)
    capabilities_drop: List[str] = field(default_factory=list)
    seccomp_profile: Optional[str] = None


@dataclass
class ContainerResources:
    requests: Dict[str, str] = field(default_factory=dict)
    limits: Dict[str, str] = field(default_factory=dict)


@dataclass
class EnvironmentVariable:
    name: str
    value: Optional[str] = None
    secret_ref: Optional[str] = None
    secret_key: Optional[str] = None
    configmap_ref: Optional[str] = None
    configmap_key: Optional[str] = None


@dataclass
class EnvFromSource:
    secret_ref: Optional[str] = None
    configmap_ref: Optional[str] = None


@dataclass
class VolumeMount:
    name: str
    mount_path: Optional[str] = None
    read_only: Optional[bool] = None


@dataclass
class Probe:
    enabled: bool = False


@dataclass
class Container:
    name: str
    image: str
    image_pull_policy: Optional[str] = None

    ports: List[Any] = field(default_factory=list)
    command: List[str] = field(default_factory=list)
    args: List[str] = field(default_factory=list)

    security_context: ContainerSecurityContext = field(
        default_factory=ContainerSecurityContext
    )

    resources: ContainerResources = field(
        default_factory=ContainerResources
    )

    env: List[EnvironmentVariable] = field(default_factory=list)
    env_from: List[EnvFromSource] = field(default_factory=list)

    volume_mounts: List[VolumeMount] = field(default_factory=list)

    liveness_probe: Probe = field(default_factory=Probe)
    readiness_probe: Probe = field(default_factory=Probe)
    startup_probe: Probe = field(default_factory=Probe)


# ============================================================================
# Volumes
# ============================================================================

@dataclass
class Volume:
    name: str

    volume_type: str

    secret_name: Optional[str] = None
    pvc_name: Optional[str] = None
    host_path: Optional[str] = None


# ============================================================================
# Service Account
# ============================================================================

@dataclass
class ServiceAccount:
    service_account: Optional[str] = None
    service_account_name: Optional[str] = None
    automount_service_account_token: Optional[bool] = None


# ============================================================================
# Networking
# ============================================================================

@dataclass
class Networking:
    host_network: Optional[bool] = None
    host_pid: Optional[bool] = None
    host_ipc: Optional[bool] = None
    dns_policy: Optional[str] = None


# ============================================================================
# Scheduling
# ============================================================================

@dataclass
class Scheduling:
    node_selector: Dict[str, str] = field(default_factory=dict)
    tolerations: List[Dict[str, Any]] = field(default_factory=list)
    affinity: Dict[str, Any] = field(default_factory=dict)


# ============================================================================
# Metadata
# ============================================================================

@dataclass
class RelevantAnnotations:
    values: Dict[str, str] = field(default_factory=dict)


# ============================================================================
# PCI Findings
# ============================================================================

@dataclass
class PCIFinding:
    category: str
    severity: str
    rule: str
    evidence: str
    pci_reference: str


# ============================================================================
# Parsed Workload
# ============================================================================

@dataclass
class ParsedWorkload:
    identification: Identification = field(default_factory=Identification)

    containers: List[Container] = field(default_factory=list)

    volumes: List[Volume] = field(default_factory=list)

    service_account: ServiceAccount = field(default_factory=ServiceAccount)

    networking: Networking = field(default_factory=Networking)

    scheduling: Scheduling = field(default_factory=Scheduling)

    annotations: RelevantAnnotations = field(
        default_factory=RelevantAnnotations
    )


# ============================================================================
# PCI Report
# ============================================================================

@dataclass
class PCIReport:
    workload: ParsedWorkload
    findings: List[PCIFinding] = field(default_factory=list)