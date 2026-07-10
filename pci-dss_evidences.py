import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import subprocess
from datetime import datetime
import json
import sys

from typing import Any


def get_timestamp() -> str:

    return datetime.now().strftime("%Y%m%d%H%M%S")

def dict_to_json(data: dict) -> str:
    return json.dumps(data, indent=4)

def get_dict_keys(data: Any, parent: str = "") -> list[str]:
    keys = []

    if isinstance(data, dict):
        for key, value in data.items():
            path = f"{parent}.{key}" if parent else key
            keys.append(path)
            keys.extend(get_dict_keys(value, path))

    elif isinstance(data, list):
        for item in data:
            keys.extend(get_dict_keys(item, parent))

    return keys

timenow = get_timestamp()
def create_logger(
    name: str = "app",
    log_dir: str = "logs",
    log_file: str = f"pci-dss_2.2.3evidences{timenow}.log",
    level: int = logging.INFO,
) -> logging.Logger:

    Path(log_dir).mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)

    if logger.hasHandlers():
        return logger

    logger.setLevel(level)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(filename)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = RotatingFileHandler(
        filename=f"{log_dir}/{log_file}",
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

logger = create_logger()

def run_command(cmd, json_afirmative):
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=True
    )
    if json_afirmative is True:
        return json.loads(result.stdout)
    else:
        return result.stdout
    

def run_main_py(deployment_yaml):
    result = subprocess.run(
        [
            sys.executable,
            "main.py",
            deployment_yaml
        ],
        capture_output=True,
        text=True
    )

    print("RETURN CODE:", result.returncode)
    print("STDOUT:")
    print(result.stdout)

    print("STDERR:")
    print(result.stderr)

def getting_deploy_list():
    cmd = [
        "kubectl",
        "get",
        "deploy",
        "-A",
        "-o",
        "json"
    ]

    return run_command(cmd, json_afirmative=True)

def getting_deployment(deployment, namespace):
    cmd = [
        "kubectl",
        "get",
        "deploy",
        deployment,
        "-n",
        namespace,
        "-o",
        "yaml",
    ]

    return run_command(cmd, json_afirmative=False)

def getting_pods(described_deployment: dict[str, Any]) -> list[dict[str, Any]]:
    spec = described_deployment.get("spec", {})

    # CronJob
    if "jobTemplate" in spec:
        spec = (
            spec["jobTemplate"]
            .get("spec", {})
            .get("template", {})
            .get("spec", {})
        )

    # Deployment, StatefulSet, DaemonSet, Job...
    elif "template" in spec:
        spec = spec["template"].get("spec", {})

    return spec.get("containers", [])

from pathlib import Path

def rename_file(old_name, new_name):
    old_path = Path(old_name)
    new_path = old_path.parent / new_name

    if not old_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {old_path}")

    old_path.rename(new_path)

    return new_path

logger.info("Starting script - Getting Deploy list")
getting_deploy_list_result = getting_deploy_list().get("items")
getting_deploy_list_results = dict_to_json(getting_deploy_list_result)

# getting_deploy_list_result = get_dict_keys(getting_deploy_list_result)
logger.info("Starting script - Getting deployments")
logger.info(getting_deploy_list_results)



for deploy in getting_deploy_list_result:
    # deploy = dict_to_json(deploy)
# try:
    deployment = deploy.get("metadata").get("name")
    namespace = deploy.get("metadata").get("namespace")
    deployment_yaml = getting_deployment(deployment, namespace)
    yaml_file = f"deployments/{deployment}_{namespace}.yaml"
    logger.info(f"Saving {yaml_file}")
    with open(yaml_file, "w", encoding="utf-8") as file:
        file.write(deployment_yaml)

    run_main_py(yaml_file)
    old_name = "outputs/report.md"
    new_name = f"report_{deployment}_{namespace}_{timenow}.md"
    rename_file(old_name, new_name)
    
    # pods = getting_pods(described_deployment)
    # logger.info(pods)
    # pods = dict_to_json(pods)
    # # for pod in pods:
    # #     print("*" * 100)
    # #     pod = dict_to_json(pod)
    # #     print(pod)

# except Exception as erro:
#     print(erro)
#     exit()

