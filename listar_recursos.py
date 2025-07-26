import boto3
import json
import csv

session = boto3.session.Session()

# Serviços globais (não precisam de região)
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

# ---------------- FUNÇÕES DE LISTAGEM ----------------

def list_ec2():
    for reg in get_regions_for_service("ec2"):
        ec2 = create_client("ec2", reg)
        try:
            paginator = ec2.get_paginator("describe_instances")
            for page in paginator.paginate():
                for res in page["Reservations"]:
                    for inst in res["Instances"]:
                        state = inst["State"]["Name"]
                        add_resource("ec2", f"{inst['InstanceId']} ({reg})", state)
        except Exception as e:
            print(f"[ERRO] EC2 {reg}: {e}")

def list_s3():
    s3 = create_client("s3")
    try:
        buckets = s3.list_buckets()
        for b in buckets.get("Buckets", []):
            add_resource("s3", b["Name"])
    except Exception as e:
        print(f"[ERRO] S3: {e}")

def list_lambda():
    for reg in get_regions_for_service("lambda"):
        lam = create_client("lambda", reg)
        try:
            paginator = lam.get_paginator("list_functions")
            for page in paginator.paginate():
                for f in page["Functions"]:
                    add_resource("lambda", f"{f['FunctionName']} ({reg})")
        except Exception as e:
            print(f"[ERRO] Lambda {reg}: {e}")

def list_rds():
    for reg in get_regions_for_service("rds"):
        rds = create_client("rds", reg)
        try:
            paginator = rds.get_paginator("describe_db_instances")
            for page in paginator.paginate():
                for db in page["DBInstances"]:
                    add_resource("rds", f"{db['DBInstanceIdentifier']} ({reg})")
        except Exception as e:
            print(f"[ERRO] RDS {reg}: {e}")

def list_vpcs():
    for reg in get_regions_for_service("ec2"):
        ec2 = create_client("ec2", reg)
        try:
            vpcs = ec2.describe_vpcs()
            for vpc in vpcs["Vpcs"]:
                add_resource("vpc", f"{vpc['VpcId']} ({reg})", vpc.get("CidrBlock", ""))
        except Exception as e:
            print(f"[ERRO] VPC {reg}: {e}")

def list_subnets():
    for reg in get_regions_for_service("ec2"):
        ec2 = create_client("ec2", reg)
        try:
            subnets = ec2.describe_subnets()
            for s in subnets["Subnets"]:
                add_resource("subnet", f"{s['SubnetId']} ({reg})", s.get("CidrBlock", ""))
        except Exception as e:
            print(f"[ERRO] Subnet {reg}: {e}")

def list_security_groups():
    for reg in get_regions_for_service("ec2"):
        ec2 = create_client("ec2", reg)
        try:
            sgs = ec2.describe_security_groups()
            for sg in sgs["SecurityGroups"]:
                add_resource("security_group", f"{sg['GroupId']} ({reg})", sg.get("GroupName", ""))
        except Exception as e:
            print(f"[ERRO] SG {reg}: {e}")

def list_iam_users():
    iam = create_client("iam")
    paginator = iam.get_paginator("list_users")
    for page in paginator.paginate():
        for u in page["Users"]:
            add_resource("iam_user", u["UserName"])

def list_iam_roles():
    iam = create_client("iam")
    paginator = iam.get_paginator("list_roles")
    for page in paginator.paginate():
        for r in page["Roles"]:
            add_resource("iam_role", r["RoleName"])

def list_iam_policies():
    iam = create_client("iam")
    paginator = iam.get_paginator("list_policies")
    for page in paginator.paginate(Scope="Local"):
        for p in page["Policies"]:
            add_resource("iam_policy", p["PolicyName"])

def list_elbs():
    for reg in get_regions_for_service("elb"):
        elb = create_client("elb", reg)
        try:
            lbs = elb.describe_load_balancers()
            for lb in lbs["LoadBalancerDescriptions"]:
                add_resource("elb", f"{lb['LoadBalancerName']} ({reg})", lb.get("DNSName", ""))
        except Exception as e:
            print(f"[ERRO] ELB {reg}: {e}")

def list_elbv2():
    for reg in get_regions_for_service("elbv2"):
        elbv2 = create_client("elbv2", reg)
        try:
            lbs = elbv2.describe_load_balancers()
            for lb in lbs["LoadBalancers"]:
                add_resource("elbv2", f"{lb['LoadBalancerName']} ({reg})", lb.get("DNSName", ""))
        except Exception as e:
            print(f"[ERRO] ELBv2 {reg}: {e}")

def list_cloudfront():
    cf = create_client("cloudfront")
    paginator = cf.get_paginator("list_distributions")
    for page in paginator.paginate():
        for d in page.get("DistributionList", {}).get("Items", []):
            add_resource("cloudfront", d["Id"], d.get("DomainName", ""))

def list_route53_zones():
    r53 = create_client("route53")
    paginator = r53.get_paginator("list_hosted_zones")
    for page in paginator.paginate():
        for z in page["HostedZones"]:
            add_resource("route53_zone", z["Id"], z["Name"])

def list_eips():
    for reg in get_regions_for_service("ec2"):
        ec2 = create_client("ec2", reg)
        try:
            eips = ec2.describe_addresses()
            for e in eips["Addresses"]:
                add_resource("eip", f"{e.get('PublicIp','')} ({reg})", e.get("InstanceId", ""))
        except Exception as e:
            print(f"[ERRO] EIP {reg}: {e}")

def list_enis():
    for reg in get_regions_for_service("ec2"):
        ec2 = create_client("ec2", reg)
        try:
            enis = ec2.describe_network_interfaces()
            for eni in enis["NetworkInterfaces"]:
                add_resource("eni", f"{eni['NetworkInterfaceId']} ({reg})", eni.get("Description", ""))
        except Exception as e:
            print(f"[ERRO] ENI {reg}: {e}")

def list_api_gateways():
    for reg in get_regions_for_service("apigateway"):
        apigw = create_client("apigateway", reg)
        try:
            paginator = apigw.get_paginator("get_rest_apis")
            for page in paginator.paginate():
                for api in page.get("items", []):
                    add_resource("apigateway", f"{api['id']} ({reg})", api.get("name", ""))
        except Exception as e:
            print(f"[ERRO] API GW {reg}: {e}")

def list_waf_webacls():
    waf = create_client("waf")
    try:
        webacls = waf.list_web_acls()
        for acl in webacls.get("WebACLs", []):
            add_resource("waf_webacl", acl["WebACLId"], acl.get("Name", ""))
    except Exception as e:
        print(f"[ERRO] WAF: {e}")

def list_global_accelerators():
    ga = create_client("globalaccelerator")
    try:
        accs = ga.list_accelerators()
        for acc in accs.get("Accelerators", []):
            add_resource("global_accelerator", acc["AcceleratorArn"], acc.get("Name", ""))
    except Exception as e:
        print(f"[ERRO] GA: {e}")

def list_direct_connect():
    dc = create_client("directconnect")
    try:
        conns = dc.describe_connections()
        for conn in conns.get("connections", []):
            add_resource("direct_connect", conn["connectionId"], conn.get("connectionName", ""))
    except Exception as e:
        print(f"[ERRO] DC: {e}")

def list_transit_gateways():
    for reg in get_regions_for_service("ec2"):
        ec2 = create_client("ec2", reg)
        try:
            tgs = ec2.describe_transit_gateways()
            for tg in tgs.get("TransitGateways", []):
                add_resource("transit_gateway", f"{tg['TransitGatewayId']} ({reg})", tg.get("Description", ""))
        except Exception as e:
            print(f"[ERRO] TGW {reg}: {e}")

def list_nat_gateways():
    for reg in get_regions_for_service("ec2"):
        ec2 = create_client("ec2", reg)
        try:
            ngws = ec2.describe_nat_gateways()
            for ngw in ngws.get("NatGateways", []):
                add_resource("nat_gateway", f"{ngw['NatGatewayId']} ({reg})", ngw.get("State", ""))
        except Exception as e:
            print(f"[ERRO] NAT GW {reg}: {e}")

def list_vpn_connections():
    for reg in get_regions_for_service("ec2"):
        ec2 = create_client("ec2", reg)
        try:
            vpns = ec2.describe_vpn_connections()
            for vpn in vpns.get("VpnConnections", []):
                add_resource("vpn_connection", f"{vpn['VpnConnectionId']} ({reg})", vpn.get("State", ""))
        except Exception as e:
            print(f"[ERRO] VPN {reg}: {e}")

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
