"""
report.py

Generates the final Markdown PCI DSS evidence report.
"""

import os
from collections import defaultdict

from models import PCIReport


OUTPUT_DIRECTORY = "outputs"
REPORT_FILE = "report.md"


REPORT_CATEGORIES = [
    "Identification",
    "Containers",
    "Security Context",
    "Resources",
    "Secrets",
    "Volumes",
    "Service Account",
    "Network",
    "Image Security",
    "Probes",
]


def create_output_directory():
    """
    Creates the output directory if it does not exist.
    """

    os.makedirs(
        OUTPUT_DIRECTORY,
        exist_ok=True
    )


def group_findings_by_category(findings):
    """
    Groups findings by category.
    """

    grouped = defaultdict(list)

    for finding in findings:
        grouped[finding.category].append(
            finding
        )

    return grouped


def generate_header(report):
    """
    Generates report header.
    """

    workload = report.workload.identification

    return (
        "# PCI DSS Workload Security Evidence Report\n\n"
        "## Workload Identification\n\n"
        f"- Kind: `{workload.kind}`\n"
        f"- Name: `{workload.name}`\n"
        f"- Namespace: `{workload.namespace}`\n"
        f"- Replicas: `{workload.replicas}`\n\n"
    )


def generate_category_section(category, findings):
    """
    Generates a Markdown section for a category.
    """

    content = []

    content.append(
        f"## {category}\n\n"
    )

    if not findings:

        content.append(
            "No findings detected.\n\n"
        )

        return "".join(content)

    content.append(
        "| Severity | Rule | Evidence | PCI DSS Reference |\n"
    )

    content.append(
        "| --- | --- | --- | --- |\n"
    )

    for finding in findings:

        content.append(
            f"| {finding.severity} "
            f"| {finding.rule} "
            f"| {finding.evidence} "
            f"| {finding.pci_reference} |\n"
        )

    content.append("\n")

    return "".join(content)


def generate_report_content(report):
    """
    Generates complete Markdown content.
    """

    content = []

    content.append(
        generate_header(report)
    )

    grouped_findings = group_findings_by_category(
        report.findings
    )

    for category in REPORT_CATEGORIES:

        content.append(
            generate_category_section(
                category,
                grouped_findings.get(
                    category,
                    []
                ),
            )
        )

    return "".join(content)


def save_report(content):
    """
    Saves Markdown report.
    """

    create_output_directory()

    report_path = os.path.join(
        OUTPUT_DIRECTORY,
        REPORT_FILE
    )

    with open(
        report_path,
        "w",
        encoding="utf-8"
    ) as report_file:

        report_file.write(
            content
        )

    return report_path


def generate_markdown_report(report: PCIReport):
    """
    Main report generation function.
    """

    content = generate_report_content(
        report
    )

    return save_report(
        content
    )