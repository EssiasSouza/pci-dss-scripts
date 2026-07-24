#!/usr/bin/env python3

import json
import subprocess
from pathlib import Path
from datetime import datetime

GCLOUD = r"C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd"

OUTPUT_DIR = Path("./outputs/files/10.2.1-pci/")
OUTPUT_DIR.mkdir(exist_ok=True)

LOG_FILE = OUTPUT_DIR / f"cloudsql_logging_remediation_{datetime.now():%Y%m%d_%H%M%S}.log"

DESIRED = {
    "log_connections": "on",
    "log_disconnections": "on",
    "log_statement": "ddl"
}


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


def get_database_flags(instance):

    result = run([
        "sql",
        "instances",
        "describe",
        instance,
        "--format=json"
    ])

    if result.returncode != 0:
        write_log(result.stderr)
        return None

    instance_data = json.loads(result.stdout)

    flags = instance_data.get("settings", {}).get("databaseFlags", [])

    return {
        flag["name"]: flag["value"]
        for flag in flags
    }


def show_flags(flags):

    write_log("")
    write_log("Database Flags encontradas")
    write_log("=" * 80)

    if not flags:
        write_log("Nenhuma databaseFlag encontrada.")
        return

    size = max(len(name) for name in flags)

    for name in sorted(flags):
        write_log(f"{name.ljust(size)} : {flags[name]}")

    write_log("")

def analyze_flags(flags):

    changes = []

    write_log("Análise das configurações")
    write_log("=" * 80)

    for flag, desired in DESIRED.items():

        if flag not in flags:

            write_log(f"{flag}")
            write_log("    Status : NÃO EXISTE")
            write_log(f"    Ação   : Criar com valor '{desired}'")
            write_log("")

            changes.append((flag, desired))

            continue

        current = flags[flag]

        if current == desired:

            write_log(f"{flag}")
            write_log(f"    Status : OK ({current})")
            write_log("")

        else:

            write_log(f"{flag}")
            write_log(f"    Atual  : {current}")
            write_log(f"    Novo   : {desired}")
            write_log("")

            changes.append((flag, desired))

    return changes


def confirm():

    while True:

        option = input("Aplicar alterações? [Y/N/Q]: ").strip().upper()

        if option in ("Y", "N", "Q"):
            return option


def build_flags(current_flags, changes):

    new_flags = current_flags.copy()

    for flag, value in changes:
        new_flags[flag] = value

    return ",".join(
        f"{name}={value}"
        for name, value in sorted(new_flags.items())
    )

def remediate(instance, database_flags):

    result = run([
        "sql",
        "instances",
        "patch",
        instance,
        f"--database-flags={database_flags}",
        "--quiet"
    ])

    if result.returncode != 0:
        write_log(result.stderr)
        return False

    write_log("Remediação executada com sucesso.")
    return True


def main():

    write_log("=" * 80)
    write_log("Cloud SQL Logging Remediation")
    write_log("=" * 80)

    while True:

        instance = input("\nNome da instância (ENTER para sair): ").strip()

        if not instance:
            break

        flags = get_database_flags(instance)

        if flags is None:
            continue

        show_flags(flags)

        changes = analyze_flags(flags)

        if not changes:
            write_log("Instância já está em conformidade.")
            continue

        option = confirm()

        if option == "Q":
            break

        if option == "N":
            write_log("Remediação cancelada pelo operador.")
            continue

        database_flags = build_flags(flags, changes)

        write_log("")
        write_log("Aplicando alterações...")

        if not remediate(instance, database_flags):
            continue

        write_log("")
        write_log("Validando configuração...")

        flags = get_database_flags(instance)

        if flags is None:
            continue

        show_flags(flags)

        remaining = analyze_flags(flags)

        if not remaining:
            write_log("STATUS FINAL: COMPLIANT")
        else:
            write_log("STATUS FINAL: NÃO COMPLIANT")

        input("\nPressione ENTER para continuar...")

    write_log("")
    write_log("Fim da execução.")


if __name__ == "__main__":
    main()