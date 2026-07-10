"""
rules.py

Executes PCI DSS security validation rules against parsed workloads.
"""

from models import PCIReport, PCIFinding, ParsedWorkload


# ============================================================================
# Critical Rules
# ============================================================================

def check_privileged_containers(workload):
    """
    Check containers running in privileged mode.
    """

    findings = []

    for container in workload.containers:
        if container.security_context.privileged is True:
            findings.append(
                PCIFinding(
                    category="Security Context",
                    severity="Critical",
                    rule="Privileged container execution",
                    evidence=(
                        f"Container '{container.name}' "
                        "has privileged=true"
                    ),
                    pci_reference="PCI DSS 2.2.5",
                )
            )

    return findings


def check_privilege_escalation(workload):
    """
    Check privilege escalation configuration.
    """

    findings = []

    for container in workload.containers:
        if (
            container.security_context
            .allow_privilege_escalation
            is True
        ):
            findings.append(
                PCIFinding(
                    category="Security Context",
                    severity="Critical",
                    rule="Privilege escalation enabled",
                    evidence=(
                        f"Container '{container.name}' "
                        "has allowPrivilegeEscalation=true"
                    ),
                    pci_reference="PCI DSS 2.2.5",
                )
            )

    return findings


def check_host_path(workload):
    """
    Check hostPath volumes.
    """

    findings = []

    for volume in workload.volumes:
        if volume.volume_type == "hostPath":
            findings.append(
                PCIFinding(
                    category="Volumes",
                    severity="Critical",
                    rule="HostPath volume usage",
                    evidence=(
                        f"Volume '{volume.name}' "
                        f"uses hostPath: {volume.host_path}"
                    ),
                    pci_reference="PCI DSS 2.2.5",
                )
            )

    return findings


def check_hardcoded_credentials(workload):
    """
    Detect sensitive environment variables using plain values.
    """

    findings = []

    sensitive_keywords = (
        "PASSWORD",
        "SECRET",
        "TOKEN",
        "KEY",
        "ACCESS_KEY",
        "PRIVATE",
        "CERT",
        "CLIENT_SECRET",
        "API_KEY",
    )

    for container in workload.containers:

        for env in container.env:

            if env.value and env.name:

                variable_name = env.name.upper()

                if any(
                    keyword in variable_name
                    for keyword in sensitive_keywords
                ):
                    findings.append(
                        PCIFinding(
                            category="Secrets",
                            severity="Critical",
                            rule="Hardcoded credential detected",
                            evidence=(
                                f"Container '{container.name}' "
                                f"contains sensitive variable "
                                f"'{env.name}' with direct value"
                            ),
                            pci_reference="PCI DSS 3.3.2",
                        )
                    )

    return findings


def check_database_and_application(workload):
    """
    Detect possible database and application containers
    running in the same pod.
    """

    findings = []

    database_keywords = (
        "mysql",
        "postgres",
        "postgresql",
        "oracle",
        "mongo",
        "mssql",
        "database",
        "db",
    )

    application_keywords = (
        "api",
        "app",
        "application",
        "frontend",
        "backend",
        "service",
    )

    has_database = False
    has_application = False

    for container in workload.containers:

        image = container.image.lower()

        if any(
            item in image
            for item in database_keywords
        ):
            has_database = True

        if any(
            item in image
            for item in application_keywords
        ):
            has_application = True

    if has_database and has_application:

        findings.append(
            PCIFinding(
                category="Containers",
                severity="Critical",
                rule="Database and application in same pod",
                evidence=(
                    "Workload contains both database "
                    "and application containers"
                ),
                pci_reference="PCI DSS 2.2.5",
            )
        )

    return findings


# ============================================================================
# Warning Rules
# ============================================================================

def check_run_as_non_root(workload):
    """
    Check containers running without non-root enforcement.
    """

    findings = []

    for container in workload.containers:

        if (
            container.security_context.run_as_non_root
            is not True
        ):
            findings.append(
                PCIFinding(
                    category="Security Context",
                    severity="Warning",
                    rule="Container does not enforce runAsNonRoot",
                    evidence=(
                        f"Container '{container.name}' "
                        "does not define runAsNonRoot=true"
                    ),
                    pci_reference="PCI DSS 2.2.5",
                )
            )

    return findings


def check_read_only_filesystem(workload):
    """
    Check root filesystem protection.
    """

    findings = []

    for container in workload.containers:

        if (
            container.security_context
            .read_only_root_filesystem
            is not True
        ):
            findings.append(
                PCIFinding(
                    category="Security Context",
                    severity="Warning",
                    rule="Writable root filesystem",
                    evidence=(
                        f"Container '{container.name}' "
                        "does not define readOnlyRootFilesystem=true"
                    ),
                    pci_reference="PCI DSS 2.2.5",
                )
            )

    return findings


def check_image_security(workload):
    """
    Check image tag and digest usage.
    """

    findings = []

    for container in workload.containers:

        image = container.image

        if not image:
            continue

        if ":latest" in image or image.endswith(":latest"):

            findings.append(
                PCIFinding(
                    category="Image Security",
                    severity="Warning",
                    rule="Image using latest tag",
                    evidence=(
                        f"Container '{container.name}' "
                        f"uses image '{image}'"
                    ),
                    pci_reference="PCI DSS 6.3.2",
                )
            )

        if "@sha256:" not in image:

            findings.append(
                PCIFinding(
                    category="Image Security",
                    severity="Warning",
                    rule="Image without digest",
                    evidence=(
                        f"Container '{container.name}' "
                        f"image '{image}' has no digest"
                    ),
                    pci_reference="PCI DSS 6.3.2",
                )
            )

    return findings


# ============================================================================
# Info Rules
# ============================================================================

def check_resources(workload):
    """
    Record resources configuration.
    """

    findings = []

    for container in workload.containers:

        resources = container.resources

        if resources.requests or resources.limits:

            findings.append(
                PCIFinding(
                    category="Resources",
                    severity="Info",
                    rule="Resources configured",
                    evidence=(
                        f"Container '{container.name}' "
                        "contains requests or limits"
                    ),
                    pci_reference="Best Practice",
                )
            )

    return findings


def check_helm(workload):
    """
    Check Helm deployment metadata.
    """

    if workload.identification.helm_annotations:

        return [
            PCIFinding(
                category="Identification",
                severity="Info",
                rule="Helm deployment detected",
                evidence="Workload contains Helm annotations",
                pci_reference="Best Practice",
            )
        ]

    return []


def check_workload_identity(workload):
    """
    Check GKE Workload Identity annotation.
    """

    if "iam.gke.io/gcp-service-account" in workload.annotations.values:

        return [
            PCIFinding(
                category="Service Account",
                severity="Info",
                rule="Workload Identity configured",
                evidence=(
                    "GKE Workload Identity annotation detected"
                ),
                pci_reference="PCI DSS 8.x",
            )
        ]

    return []


def check_probes(workload):
    """
    Check health probes.
    """

    findings = []

    for container in workload.containers:

        if (
            container.liveness_probe.enabled
            or container.readiness_probe.enabled
            or container.startup_probe.enabled
        ):

            findings.append(
                PCIFinding(
                    category="Probes",
                    severity="Info",
                    rule="Health probes configured",
                    evidence=(
                        f"Container '{container.name}' "
                        "has Kubernetes probes"
                    ),
                    pci_reference="Best Practice",
                )
            )

    return findings


def check_labels(workload):
    """
    Check workload labels.
    """

    if workload.identification.labels:

        return [
            PCIFinding(
                category="Identification",
                severity="Info",
                rule="Labels detected",
                evidence=(
                    "Workload contains metadata labels"
                ),
                pci_reference="Best Practice",
            )
        ]

    return []


def check_annotations(workload):
    """
    Check relevant security annotations.
    """

    if workload.annotations.values:

        return [
            PCIFinding(
                category="Annotations",
                severity="Info",
                rule="Security annotations detected",
                evidence=(
                    "Relevant security annotations found"
                ),
                pci_reference="Best Practice",
            )
        ]

    return []


# ============================================================================
# Rule Engine
# ============================================================================

def execute_rules(workload: ParsedWorkload):
    """
    Executes all PCI DSS rules.
    """

    findings = []

    rules = [
        check_privileged_containers,
        check_privilege_escalation,
        check_host_path,
        check_hardcoded_credentials,
        check_database_and_application,

        check_run_as_non_root,
        check_read_only_filesystem,
        check_image_security,

        check_resources,
        check_helm,
        check_workload_identity,
        check_probes,
        check_labels,
        check_annotations,
    ]

    for rule in rules:
        findings.extend(
            rule(workload)
        )

    return PCIReport(
        workload=workload,
        findings=findings,
    )