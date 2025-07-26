import boto3
import json
import csv

session = boto3.session.Session()

GLOBAL_SERVICES = ["iam", "cloudfront", "route53", "waf", "globalaccelerator"]

def get_regions_for_service(service_name):
    try:
        return session.get_available_regions(service_name)
    except Exception:
        return []

def create_client(service_name, region=None):
    if service_name in GLOBAL_SERVICES:
        return boto3.client(service_name)
    return boto3.client(service_name, region_name=region)

all_resources = {}

def add_resource(service, resource_id, extra=""):
    if service not in all_resources:
        all_resources[service] = []
    all_resources[service].append(f"{resource_id} {extra}".strip())

# ---------------- FUNÇÕES EXISTENTES ----------------
# (mantém as funções list_ec2, list_s3, list_lambda, etc. iguais às que você já tem)

# ---------------- NOVAS FUNÇÕES ----------------

def list_sns_topics():
    for reg in get_regions_for_service("sns"):
        sns = create_client("sns", reg)
        try:
            paginator = sns.get_paginator("list_topics")
            for page in paginator.paginate():
                for topic in page.get("Topics", []):
                    add_resource("sns_topic", f"{topic['TopicArn']} ({reg})")
        except Exception as e:
            print(f"[ERRO] SNS Topics {reg}: {e}")

def list_sns_subscriptions():
    for reg in get_regions_for_service("sns"):
        sns = create_client("sns", reg)
        try:
            paginator = sns.get_paginator("list_subscriptions")
            for page in paginator.paginate():
                for sub in page.get("Subscriptions", []):
                    add_resource(
                        "sns_subscription",
                        f"{sub['SubscriptionArn']} ({reg})",
                        sub.get("Protocol", "")
                    )
        except Exception as e:
            print(f"[ERRO] SNS Subscriptions {reg}: {e}")

def list_sqs_queues():
    for reg in get_regions_for_service("sqs"):
        sqs = create_client("sqs", reg)
        try:
            paginator = sqs.get_paginator("list_queues")
            for page in paginator.paginate():
                for queue_url in page.get("QueueUrls", []):
                    add_resource("sqs_queue", f"{queue_url} ({reg})")
        except Exception as e:
            print(f"[ERRO] SQS Queues {reg}: {e}")

# ---------------- EXECUTAR TUDO ----------------

def run_all():
    list_ec2()
    list_s3()
    list_lambda()
    list_rds()
    list_vpcs()
    list_subnets()
    list_security_groups()
    list_iam_users()
    list_iam_roles()
    list_iam_policies()
    list_elbs()
    list_elbv2()
    list_cloudfront()
    list_route53_zones()
    list_eips()
    list_enis()
    list_api_gateways()
    list_waf_webacls()
    list_global_accelerators()
    list_direct_connect()
    list_transit_gateways()
    list_nat_gateways()
    list_vpn_connections()
    # 🔹 Novos serviços
    list_sns_topics()
    list_sns_subscriptions()
    list_sqs_queues()

run_all()

# ---------------- EXPORTAR ----------------

print("\nRecursos encontrados na conta:")
for service, resources in all_resources.items():
    print(f"\n{service.upper()} ({len(resources)}):")
    for res in resources:
        print(f"  - {res}")

with open("recursos_aws.json", "w", encoding="utf-8") as f_json:
    json.dump(all_resources, f_json, ensure_ascii=False, indent=2)

with open("recursos_aws.csv", "w", newline="", encoding="utf-8") as f_csv:
    writer = csv.writer(f_csv)
    writer.writerow(["servico", "id", "extra"])
    for service, resources in all_resources.items():
        for res in resources:
            parts = res.split(" ", 1)
            resource_id = parts[0]
            extra = parts[1] if len(parts) > 1 else ""
            writer.writerow([service, resource_id, extra])
