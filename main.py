"""
main.py

Main execution flow for PCI DSS Evidence Scanner.
"""

import argparse

from logger import (
    setup_logger,
    log_operation,
    log_error,
)

from collector import collect_manifest

from parser import parse_workload

from rules import execute_rules

from report import generate_markdown_report


def parse_arguments():
    """
    Parse application arguments.
    """

    parser = argparse.ArgumentParser(
        description=(
            "PCI DSS Evidence Scanner for Kubernetes workloads"
        )
    )

    parser.add_argument(
        "manifest",
        help=(
            "Path to Kubernetes YAML manifest"
        ),
    )

    return parser.parse_args()


def main():
    """
    Main application execution flow.
    """

    logger = setup_logger()

    try:

        log_operation(
            logger,
            "PCI DSS Evidence Scanner started"
        )

        args = parse_arguments()

        log_operation(
            logger,
            f"Loading YAML manifest: {args.manifest}"
        )

        manifest = collect_manifest(
            args.manifest
        )
        

        log_operation(
            logger,
            "YAML manifest loaded successfully"
        )

        log_operation(
            logger,
            "Parsing workload information"
        )

        workload = parse_workload(
            manifest
        )

        log_operation(
            logger,
            "Workload parsing completed"
        )

        log_operation(
            logger,
            "Executing PCI DSS rules"
        )

        report = execute_rules(
            workload
        )

        log_operation(
            logger,
            (
                f"PCI DSS rules completed. "
                f"Findings generated: {len(report.findings)}"
            ),
        )

        log_operation(
            logger,
            "Generating Markdown report"
        )

        report_path = generate_markdown_report(
            report
        )

        log_operation(
            logger,
            f"Markdown report generated: {report_path}"
        )

        log_operation(
            logger,
            "PCI DSS Evidence Scanner finished successfully"
        )

    except Exception as error:

        log_error(
            logger,
            f"Execution failed: {str(error)}"
        )

        raise


if __name__ == "__main__":
    main()