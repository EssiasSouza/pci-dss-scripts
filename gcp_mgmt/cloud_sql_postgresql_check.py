#!/usr/bin/env python3

import json
import subprocess
from pathlib import Path
from datetime import datetime

GCLOUD = r"C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd"

OUTPUT_DIR = Path("./outputs/files/10.2.1-pci/")
OUTPUT_DIR.mkdir(exist_ok=True)

LOG_FILE = OUTPUT_DIR / f"cloudsql_logging_{datetime.now():%Y%m%d_%H%M%S}.log"


def run(cmd):
    command = [GCLOUD] + cmd

    return subprocess.run(
        command,
        capture_output=True,
        text=True
    )


def write_log(message):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    line = f"[{timestamp}] {message}"

    print(line)

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def list_instances():

    write_log("Obtendo lista de instâncias Cloud SQL PostgreSQL...")

    result = run([
        "sql",
        "instances",
        "list",
        "--filter=DATABASE_VERSION~POSTGRES",
        "--format=json"
    ])

    if result.returncode != 0:
        write_log(result.stderr)
        raise Exception(result.stderr)

    return json.loads(result.stdout)

def check_logging(instance_name):

    flags = get_database_flags(instance_name)

    log_connections = flags.get("log_connections", "off")
    log_disconnections = flags.get("log_disconnections", "off")
    log_statement = flags.get("log_statement", "none")

    write_log("Configuração de Logging:")

    write_log(
        f"  SQL_LOG_CONNECTIONS_DISABLED     : "
        f"{'PASS' if log_connections == 'on' else 'FAIL'} "
        f"(valor={log_connections})"
    )

    write_log(
        f"  SQL_LOG_DISCONNECTIONS_DISABLED  : "
        f"{'PASS' if log_disconnections == 'on' else 'FAIL'} "
        f"(valor={log_disconnections})"
    )

    write_log(
        f"  SQL_LOG_STATEMENT                : "
        f"{'PASS' if log_statement != 'none' else 'FAIL'} "
        f"(valor={log_statement})"
    )

def get_database_flags(instance_name):

    result = run([
        "sql",
        "instances",
        "describe",
        instance_name,
        "--format=json"
    ])

    if result.returncode != 0:
        write_log(f"Erro ao obter configurações da instância {instance_name}")
        write_log(result.stderr)
        return {}

    instance = json.loads(result.stdout)

    flags = instance.get("settings", {}).get("databaseFlags", [])

    return {
        flag["name"]: flag["value"]
        for flag in flags
    }



def main():

    instances = list_instances()

    write_log(f"Foram encontradas {len(instances)} instâncias.\n")

    for instance in instances:

        write_log("=" * 80)
        write_log(f"Nome      : {instance['name']}")
        write_log(f"Versão    : {instance['databaseVersion']}")
        write_log(f"Região    : {instance['region']}")
        write_log(f"Estado    : {instance['state']}")

        check_logging(instance["name"])

    write_log("=" * 80)
    write_log("Fim da execução.")


if __name__ == "__main__":
    main()