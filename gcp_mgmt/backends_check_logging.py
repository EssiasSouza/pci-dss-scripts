#!/usr/bin/env python3

import json
import subprocess

BACKEND_SERVICES = """
gringo-desk-prod-backend-service
gringo-web-prod-backend-service
k8s-be-32613--b4f8cb8e00b9ce37
k8s1-b4f8cb8e-default-zitadel-external-8080-9064385e
kong-ext-backend-service
service-api-fetch-limit-user-permission-refresher
service-api-fetch-limit-user-permission-refresher2
service-base-nacional-http-api
service-braze-campaign-trigger-api
service-cloud-storage-fipe-trigger
service-convert-html-to-base64-image-function
service-database-access-mgmt
service-database-access-mgmt-gen2
service-distrito-federal
service-event-publisher
service-fipe
service-gringo-gcb-bot
service-hasura-order-steps-transformation
service-ipva-notification-slack
service-memory-store-proxy
service-minas-gerais
service-national
service-order-executed-id-echo
service-order-monitor-amplitude
service-order-status-braze
service-order-status-event-function
service-order-status-review-in-app
service-parana
service-parana-modulo-veiculo
service-partner-webhook-mtls
service-partner-webhook-v2
service-pr-modulo-veiculo
service-rendimento-http-proxy
service-rio-de-janeiro
service-rio-de-janeiro-gen2
service-rio-grande-sul
service-santa-catarina
service-sao-paulo
service-sao-paulo-restrictions
service-send-message-function
service-send-whatsapp-message-blip-api
service-sergipe
sparkpost-engagement-tracking
a8ee924d9be1a4964927575a5fc4ec73
gkegw1-u91f-defa-gringo-plus-subscription-serv-443-zq68ps208lno
gkegw1-u91f-defa-vehicle-assistance-service-jo-443-f0ph1klacpz9
gkegw1-u91f-defau-axle-control-panel-internal--443-5vg63ljr9ent
gkegw1-u91f-defau-buy-and-sell-service-interna-443-5qvw1ypftbsy
gkegw1-u91f-defau-conciliation-service-interna-443-sw34my5vs098
gkegw1-u91f-defau-consortium-service-internal--443-irhkwq93dstb
gkegw1-u91f-defau-consortium-service-subs-inte-443-3fdrwhwalm89
gkegw1-u91f-defau-email-braze-webhook-internal-443-wavues4983py
gkegw1-u91f-defau-email-metrics-api-internal-w-443-roicarpb68no
gkegw1-u91f-defau-email-template-api-internal--443-2h2laeopfl4e
gkegw1-u91f-defau-free-flow-service-internal-w-443-1qc43etr88vy
gkegw1-u91f-defau-gringo-plus-subscription-ser-443-2pfi4jqm4djm
gkegw1-u91f-defau-owner-review-service-interna-443-fvoowgusrhoh
gkegw1-u91f-defau-receivable-register-service--443-6xcl4o921dyu
gkegw1-u91f-defau-scrapers-free-flow-internal--443-10wqapzrg2nz
gkegw1-u91f-defau-temporal-codec-server-intern-443-6pqcca5l1hbr
gkegw1-u91f-defau-vehicle-assistance-service-i-443-w9jruhpfz1ju
gkegw1-u91f-defau-vehicle-assistance-service-j-443-p4mwv7goap2z
gkegw1-u91f-defaul-alerts-service-internal-wei-443-4rddhrtoj6i9
gkegw1-u91f-defaul-api-integration-service-int-443-a7t20ca4ygyg
gkegw1-u91f-defaul-consortium-service-subs-int-443-wgyzpryep1as
gkegw1-u91f-defaul-debits-service-internal-wei-443-lt7dxagtmjen
gkegw1-u91f-defaul-drivers-license-service-int-443-9sb2cry5q4be
gkegw1-u91f-defaul-ggo-bff-chatbot-internal-we-443-ydydks93miu1
gkegw1-u91f-defaul-gringo-notification-service-443-pg54owgw6ir3
gkegw1-u91f-defaul-mock-data-forge-internal-we-443-w4377nfdtd07
gkegw1-u91f-defaul-nba-service-internal-weight-443-14dubnm07cyd
gkegw1-u91f-defaul-pages-service-internal-weig-443-dvw8hcuewzfv
gkegw1-u91f-defaul-permissions-manager-service-443-l061s1zvv7xc
gkegw1-u91f-defaul-receivable-register-service-443-44wrieced9n0
gkegw1-u91f-defaul-report-service-internal-wei-443-q61gas45oanm
gkegw1-u91f-defaul-scraper-distrito-federal-in-443-0n0n8ipukk9i
gkegw1-u91f-defaul-scrapers-distrito-federal-i-443-t9g94bvrk5wx
gkegw1-u91f-defaul-scrapers-rio-de-janeiro-int-443-2fafi9h2obk5
gkegw1-u91f-defaul-survey-service-internal-wei-443-u5b71qzxynvt
gkegw1-u91f-defaul-vehicle-assistance-service--443-zooslzpy50rm
gkegw1-u91f-defaul-vehicle-insurance-service-a-443-f7la0884vp3x
gkegw1-u91f-default-alerts-service-internal-443-c9pczbqpv9uy
http-event-publisher-private
k8s1-b4f8cb8e-default-prometheus-grafana-80-e9a06d61
k8s1-b4f8cb8e-default-zitadel-8080-7b07f3ee
k8s1-b4f8cb8e-kube-system-default-http-backend-80-72168804
kong-int-backend-service
renainf-billet-function-private
""".strip().splitlines()

GCLOUD = "C:\\Program Files (x86)\\Google\\Cloud SDK\\google-cloud-sdk\\bin\\gcloud.cmd"
def run(cmd):
    command = [GCLOUD] + cmd
    return subprocess.run(
        command,
        capture_output=True,
        text=True
    )


def describe_global(name):
    return run([

        "compute",
        "backend-services",
        "describe",
        name,
        "--global",
        "--format=json"
    ])


def get_region(name):
    result = run([

        "compute",
        "backend-services",
        "list",
        "--format=json"
    ])

    if result.returncode != 0:
        return None

    services = json.loads(result.stdout)

    for svc in services:
        if svc["name"] == name:
            region = svc.get("region")
            if region:
                return region.split("/")[-1]

    return None


def describe_region(name, region):
    return run([

        "compute",
        "backend-services",
        "describe",
        name,
        "--region",
        region,
        "--format=json"
    ])


enabled = 0
disabled = 0
not_found = 0

print("=" * 120)
print(f'{"Backend":70} {"Scope":10} {"Logging":10} {"Sample"}')
print("=" * 120)

for backend in BACKEND_SERVICES:

    result = describe_global(backend)

    scope = "GLOBAL"

    if result.returncode != 0:

        region = get_region(backend)

        if region:
            result = describe_region(backend, region)
            scope = region.upper()

    if result.returncode != 0:
        print(f"{backend:70} {'-':10} NOT FOUND")
        not_found += 1
        continue

    data = json.loads(result.stdout)

    log = data.get("logConfig", {})

    enable = log.get("enable", False)
    sample = log.get("sampleRate", 0)

    if enable:
        status = "YES"
        enabled += 1
    else:
        status = "NO"
        disabled += 1

    print(f"{backend:70} {scope:10} {status:10} {sample}")

print("\nSummary")
print("=" * 30)
print(f"Logging Enabled : {enabled}")
print(f"Logging Disabled: {disabled}")
print(f"Not Found       : {not_found}")