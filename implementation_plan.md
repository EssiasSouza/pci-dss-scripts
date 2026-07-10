# PCI DSS Evidence Scanner for GKE

## Implementation Plan

### Version

1.0

---

# 1. Objective

Develop a Python application capable of collecting Kubernetes Deployment manifests and extracting only the information that provides security evidence for PCI DSS audits.

The application is intended to support auditors by producing a concise and objective report focused on the workload security posture.

The application shall not collect operational or informational data that do not contribute to the audit.

---

# 2. Project Structure

```
project/
│
├── main.py
├── collector.py
├── parser.py
├── rules.py
├── report.py
├── logger.py
├── models.py
│
├── outputs/
│     └── relatório.md
│
└── logs/
      └── PCI-DSS_evidences_YYYYMMDD_HHMMSS.log
```

---

# 3. Development Order

The project shall be developed in the following order.

## Step 1

Create the implementation plan.

Status

```
Completed
```

---

## Step 2

Create `models.py`

Responsibilities

* Define the data structures used across the application.
* Represent the workload information.
* Represent PCI findings.
* Represent the final parsed object.

Status

```
Completed
```

---

## Step 3

Create `logger.py`

Responsibilities

* Configure application logging.
* Create the log directory if necessary.
* Generate log file.

Log format

```
PCI-DSS_evidences_YYYYMMDD_HHMMSS.log
```

Every important operation performed by the application shall be logged.

Status

```
Completed
```

---

## Step 4

Create `collector.py`

Responsibilities

* Receive the YAML manifest.
* Load the YAML file.
* Validate basic syntax.
* Return the parsed YAML object.

No PCI rules shall be executed here.

Status

```
Completed
```

---

## Step 5

Create `parser.py`

Responsibilities

Extract only the approved fields.

### Identification

* kind
* metadata.name
* metadata.namespace
* metadata.labels
* metadata.annotations.meta.helm.sh/*
* spec.replicas

### Containers

For each container

* name
* image
* imagePullPolicy
* ports
* command
* args

### Security Context

* runAsNonRoot
* runAsUser
* runAsGroup
* allowPrivilegeEscalation
* privileged
* readOnlyRootFilesystem
* capabilities.add
* capabilities.drop
* seccompProfile.type

### Resources

* requests
* limits

### Image

* image
* imagePullPolicy

### Secrets

* envFrom.secretRef
* env.valueFrom.secretKeyRef
* env.value
* volumes.secret

### ConfigMaps

* envFrom.configMapRef
* env.valueFrom.configMapKeyRef

### Volumes

* volumes
* volumeMounts

### Service Account

* serviceAccount
* serviceAccountName
* automountServiceAccountToken

### Probes

* livenessProbe
* readinessProbe
* startupProbe

### Networking

* hostNetwork
* hostPID
* hostIPC
* dnsPolicy

### Scheduling

* nodeSelector
* tolerations
* affinity

### Relevant Annotations

Only

* iam.gke.io/*
* vault.hashicorp.com/*
* sidecar.istio.io/*
* linkerd.io/*
* container.apparmor.*
* seccomp.*

Status

```
Completed
```

---

## Step 6

Create `rules.py`

Responsibilities

Execute all PCI DSS validation rules.

Severity levels

### Critical

* privileged=true
* allowPrivilegeEscalation=true
* hostPath volume
* Hardcoded credentials
* Database and application in the same Pod

### Warning

* runAsNonRoot=false
* readOnlyRootFilesystem=false
* Image without digest
* Image using latest

### Info

* Requests/Limits
* Helm deployment
* Workload Identity
* Probes
* Labels
* Relevant annotations

Each finding shall contain

* Category
* Severity
* Rule
* Evidence
* PCI DSS reference

Status

```
Completed
```

---

## Step 7

Create `report.py`

Responsibilities

Generate the final Markdown report.

The report shall be organized by categories.

Categories

* Identification
* Containers
* Security Context
* Resources
* Secrets
* Volumes
* Service Account
* Network
* Image Security
* Probes

The report shall be saved as

```
outputs/relatório.md
```

Status

```
Completed
```

---

## Step 8

Create `main.py`

Responsibilities

Coordinate the complete execution flow.

Execution sequence

1. Initialize logger.
2. Load YAML.
3. Parse workload.
4. Execute PCI rules.
5. Generate Markdown report.
6. Finish execution.

Status

```
Completed
```

---

# 4. Excluded Fields

The following fields shall never be collected.

```
status
managedFields
creationTimestamp
resourceVersion
uid
generation
selfLink
terminationMessagePath
terminationMessagePolicy
dnsConfig
restartPolicy
schedulerName
```

---

# 5. Logging

Every module shall register its major operations.

Examples

* Application started.
* YAML loaded.
* Parsing started.
* Parsing completed.
* Rules executed.
* Report generated.
* Execution completed.
* Errors.

---

# 6. Output Files

## Logs

```
logs/PCI-DSS_evidences_YYYYMMDD_HHMMSS.log
```

## Report

```
outputs/relatório.md
```

---

# 7. Development Rule

Every new source file shall be developed only after the previous planned step has been completed and reviewed.

The implementation shall strictly follow the sequence defined in this document.
