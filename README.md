# PCI DSS Evidence Scanner for GKE

## Overview

The PCI DSS Evidence Scanner is a Python application designed to collect and analyze Kubernetes workload manifests to support PCI DSS security audits.

The main objective is to extract only security-relevant evidence from Kubernetes workloads, evaluate the security posture based on predefined PCI DSS rules, and generate an objective Markdown report that can be reviewed during audit activities.

The scanner focuses on identifying security risks and configuration weaknesses without collecting unnecessary operational information.

---

# Purpose

This project helps security teams and auditors evaluate Kubernetes workloads by analyzing:

* Workload identification
* Container security configuration
* Image security posture
* Secret usage
* Volume exposure
* Service account configuration
* Network security settings
* Runtime hardening controls
* Operational maturity indicators

---

# Architecture

The application is organized into independent modules, each with a specific responsibility.

```text
.
├── main.py
│
├── collector.py
│      Loads Kubernetes YAML manifests
│
├── parser.py
│      Extracts security-relevant fields
│
├── rules.py
│      Executes PCI DSS validation rules
│
├── report.py
│      Generates Markdown audit report
│
├── logger.py
│      Handles application logging
│
├── models.py
│      Defines application data structures
│
├── logs/
│      PCI-DSS_evidences_YYYYMMDD_HHMMSS.log
│
└── outputs/
       relatório.md
```

---

# Execution Flow

The application execution follows this sequence:

1. Initialize logging.
2. Load Kubernetes YAML manifest.
3. Parse relevant workload information.
4. Execute PCI DSS security rules.
5. Generate Markdown evidence report.
6. Finish execution.

---

# Security Analysis Scope

The scanner analyzes the following security areas:

## Identification

Collects workload identity information:

* Kubernetes resource kind
* Name
* Namespace
* Labels
* Helm metadata
* Replica configuration

---

## Containers

Analyzes container execution details:

* Container names
* Images
* Image pull policies
* Ports
* Commands
* Arguments

---

## Security Context

Evaluates workload hardening settings:

* Running as non-root
* User and group configuration
* Privilege escalation
* Privileged containers
* Read-only filesystem
* Linux capabilities
* Seccomp profile

---

## Resources

Checks resource configuration:

* CPU requests
* Memory requests
* CPU limits
* Memory limits

---

## Secrets

Identifies sensitive configuration usage:

* Secret references
* Secret environment variables
* Hardcoded sensitive values

Sensitive variables analyzed include:

* PASSWORD
* SECRET
* TOKEN
* KEY
* ACCESS_KEY
* PRIVATE
* CERT
* CLIENT_SECRET
* API_KEY

---

## Volumes

Analyzes workload storage exposure:

* Secret volumes
* Projected volumes
* Persistent volume claims
* EmptyDir volumes
* HostPath usage

---

## Service Account

Evaluates identity configuration:

* Service account usage
* Token mounting configuration
* Workload Identity integration

---

## Network Security

Checks Kubernetes networking isolation:

* Host network
* Host PID
* Host IPC
* DNS policy

---

## Image Security

Validates container image security posture:

* Usage of latest tag
* Image digest presence

---

## Probes

Checks workload health validation:

* Liveness probes
* Readiness probes
* Startup probes

---

# PCI DSS Severity Model

Findings are categorized into three severity levels.

## Critical

Security issues requiring immediate attention.

Examples:

* Privileged containers
* Privilege escalation enabled
* HostPath volumes
* Hardcoded credentials
* Database and application running in the same Pod

---

## Warning

Configuration weaknesses that increase security risk.

Examples:

* Missing runAsNonRoot
* Writable root filesystem
* Images without digest
* Usage of latest image tag

---

## Info

Security maturity indicators.

Examples:

* Resource limits configured
* Helm deployment metadata
* Workload Identity
* Kubernetes probes
* Security annotations
* Labels

---

# Report Output

After execution, the scanner generates:

```text
outputs/relatório.md
```

The report contains findings grouped by category with:

* Severity
* Rule
* Evidence
* PCI DSS reference

---

# Logging

All application activities are recorded in:

```text
logs/PCI-DSS_evidences_YYYYMMDD_HHMMSS.log
```

The log contains:

* Application startup
* Manifest loading
* Parsing operations
* Rule execution
* Report generation
* Errors

---

# Requirements

Python:

```text
Python 3.10+
```

Required package:

```bash
pip install pyyaml
```

---

# Usage

Execute the scanner providing a Kubernetes YAML manifest:

```bash
python main.py deployment.yaml
```

Example execution:

```text
PCI DSS Evidence Scanner started

Loading YAML manifest: deployment.yaml

YAML manifest loaded successfully

Workload parsing completed

PCI DSS rules completed

Markdown report generated:
outputs/relatório.md

PCI DSS Evidence Scanner finished successfully
```

---

# Security Philosophy

The scanner follows a security-focused approach:

* Collect only audit-relevant evidence.
* Prioritize security posture over operational information.
* Highlight risks according to severity.
* Produce objective evidence for PCI DSS assessment.
* Avoid unnecessary workload data collection.

---

# Project Status

Initial version completed.

Implemented components:

* Data models
* Logging framework
* YAML collector
* Kubernetes workload parser
* PCI DSS rule engine
* Markdown report generator
* Application execution workflow
