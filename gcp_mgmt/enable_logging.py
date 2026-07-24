#!/usr/bin/env python3

import subprocess

GCLOUD = r"C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd"


def run(cmd):
    command = [GCLOUD] + cmd
    return subprocess.run(
        command,
        capture_output=True,
        text=True
    )


GLOBAL_BACKENDS = [
    "service-api-fetch-limit-user-permission-refresher",
    "service-api-fetch-limit-user-permission-refresher2",
    "service-base-nacional-http-api",
    "service-braze-campaign-trigger-api",
    "service-cloud-storage-fipe-trigger",
    "service-convert-html-to-base64-image-function",
    "service-database-access-mgmt",
    "service-database-access-mgmt-gen2",
    "service-distrito-federal",
    "service-fipe",
    "service-gringo-gcb-bot",
    "service-hasura-order-steps-transformation",
    "service-ipva-notification-slack",
    "service-memory-store-proxy",
    "service-minas-gerais",
    "service-national",
    "service-order-executed-id-echo",
    "service-order-monitor-amplitude",
    "service-order-status-braze",
    "service-order-status-event-function",
    "service-order-status-review-in-app",
    "service-parana",
    "service-parana-modulo-veiculo",
    "service-pr-modulo-veiculo",
    "service-rendimento-http-proxy",
    "service-rio-de-janeiro",
    "service-rio-de-janeiro-gen2",
    "service-rio-grande-sul",
    "service-santa-catarina",
    "service-sao-paulo",
    "service-sao-paulo-restrictions",
    "service-send-message-function",
    "service-send-whatsapp-message-blip-api",
    "service-sergipe",
    "sparkpost-engagement-tracking",
]

REGIONAL_BACKENDS = [
    "a8ee924d9be1a4964927575a5fc4ec73",
    "http-event-publisher-private",
    "kong-int-backend-service",
    "renainf-billet-function-private",
]

REGION = "southamerica-east1"

success = 0
failed = 0

print("=" * 100)
print("Enabling logging for GLOBAL backend services")
print("=" * 100)

for backend in GLOBAL_BACKENDS:

    print(f"Updating {backend}... ", end="", flush=True)

    result = run([
        "compute",
        "backend-services",
        "update",
        backend,
        "--global",
        "--enable-logging",
        "--logging-sample-rate=1.0",
    ])

    if result.returncode == 0:
        print("OK")
        success += 1
    else:
        print("FAILED")
        print(result.stderr.strip())
        failed += 1


print("\n" + "=" * 100)
print(f"Enabling logging for REGIONAL backend services ({REGION})")
print("=" * 100)

for backend in REGIONAL_BACKENDS:

    print(f"Updating {backend}... ", end="", flush=True)

    result = run([
        "compute",
        "backend-services",
        "update",
        backend,
        "--region",
        REGION,
        "--enable-logging",
        "--logging-sample-rate=1.0",
    ])

    if result.returncode == 0:
        print("OK")
        success += 1
    else:
        print("FAILED")
        print(result.stderr.strip())
        failed += 1

print("\n" + "=" * 100)
print("Summary")
print("=" * 100)
print(f"Successful updates : {success}")
print(f"Failed updates     : {failed}")
print("=" * 100)