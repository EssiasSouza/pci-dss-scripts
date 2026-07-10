"""
collector.py

Responsible for collecting and loading Kubernetes YAML manifests.
"""

import yaml


def load_yaml_manifest(file_path):
    """
    Loads a Kubernetes YAML manifest file.

    Args:
        file_path (str): Path to the YAML manifest.

    Returns:
        dict: Parsed YAML content.

    Raises:
        FileNotFoundError: When the YAML file does not exist.
        yaml.YAMLError: When the YAML syntax is invalid.
    """

    with open(file_path, "r", encoding="utf-8") as yaml_file:
        manifest = yaml.safe_load(yaml_file)

    return manifest


def validate_manifest(manifest):
    """
    Performs basic validation of the loaded Kubernetes manifest.

    Args:
        manifest (dict): Loaded YAML content.

    Returns:
        bool: True when the manifest structure is valid.

    Raises:
        ValueError: When required Kubernetes structure is missing.
    """

    if not isinstance(manifest, dict):
        raise ValueError(
            "Invalid manifest format. Expected YAML object."
        )

    if "kind" not in manifest:
        raise ValueError(
            "Invalid Kubernetes manifest. Missing kind."
        )

    if "metadata" not in manifest:
        raise ValueError(
            "Invalid Kubernetes manifest. Missing metadata."
        )

    return True


def collect_manifest(file_path):
    """
    Main collector function.

    Loads and validates the Kubernetes manifest.

    Args:
        file_path (str): Path to YAML manifest.

    Returns:
        dict: Validated Kubernetes manifest.
    """

    manifest = load_yaml_manifest(file_path)

    validate_manifest(manifest)

    return manifest