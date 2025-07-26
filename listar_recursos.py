

import boto3
import json
import csv


# Detectar região padrão
session = boto3.Session()
region = session.region_name or 'us-east-1'

# Função utilitária para obter todas as regiões disponíveis para um serviço
def get_all_regions(service_name):
    ec2 = boto3.client('ec2', region_name=region)
    regions = ec2.describe_regions(AllRegions=True)
    return [r['RegionName'] for r in regions['Regions'] if r.get('OptInStatus', 'opt-in-not-required') in ['opt-in-not-required', 'opted-in']]

all_resources = {}

def add_resource(service, resource_id, extra=""):
    if service not in all_resources:
        all_resources[service] = []
    all_resources[service].append(f"{resource_id} {extra}".strip())

def list_ec2():
    regions = get_all_regions('ec2')
    for reg in regions:
        print(f"[DEBUG] Buscando EC2 em {reg}")
        ec2 = boto3.client('ec2', region_name=reg)
        try:
            instances = ec2.describe_instances()
            for res in instances['Reservations']:
                for inst in res['Instances']:
                    instance_id = inst['InstanceId']
                    state = inst.get('State', {}).get('Name', '')
                    add_resource('ec2', f"{instance_id} ({reg})", state)
        except Exception as e:
            print(f"[ERRO] EC2 {reg}: {e}")
def list_s3():
    s3 = boto3.client('s3')
    buckets = s3.list_buckets()
    for bucket in buckets.get('Buckets', []):
        add_resource('s3', bucket['Name'])

def list_lambda():
    lam = boto3.client('lambda')
    funcs = lam.list_functions()
    for f in funcs['Functions']:
        add_resource('lambda', f['FunctionName'])

def list_rds():
    regions = get_all_regions('rds')
    for reg in regions:
        print(f"[DEBUG] Buscando RDS em {reg}")
        rds = boto3.client('rds', region_name=reg)
        try:
            instances = rds.describe_db_instances()
            for db in instances['DBInstances']:
                add_resource('rds', f"{db['DBInstanceIdentifier']} ({reg})")
        except Exception as e:
            print(f"[ERRO] RDS {reg}: {e}")

def list_vpcs():
    regions = get_all_regions('ec2')
    for reg in regions:
        print(f"[DEBUG] Buscando VPC em {reg}")
        ec2 = boto3.client('ec2', region_name=reg)
        try:
            vpcs = ec2.describe_vpcs()
            for vpc in vpcs['Vpcs']:
                vpc_id = vpc['VpcId']
                cidr = vpc.get('CidrBlock', '')
                add_resource('vpc', f"{vpc_id} ({reg})", cidr)
        except Exception as e:
            print(f"[ERRO] VPC {reg}: {e}")

def list_subnets():
    regions = get_all_regions('ec2')
    for reg in regions:
        print(f"[DEBUG] Buscando Subnets em {reg}")
        ec2 = boto3.client('ec2', region_name=reg)
        try:
            subnets = ec2.describe_subnets()
            for subnet in subnets['Subnets']:
                subnet_id = subnet['SubnetId']
                cidr = subnet.get('CidrBlock', '')
                add_resource('subnet', f"{subnet_id} ({reg})", cidr)
        except Exception as e:
            print(f"[ERRO] Subnet {reg}: {e}")

def list_security_groups():
    regions = get_all_regions('ec2')
    for reg in regions:
        print(f"[DEBUG] Buscando Security Groups em {reg}")
        ec2 = boto3.client('ec2', region_name=reg)
        try:
            sgs = ec2.describe_security_groups()
            for sg in sgs['SecurityGroups']:
                sg_id = sg['GroupId']
                name = sg.get('GroupName', '')
                add_resource('security_group', f"{sg_id} ({reg})", name)
        except Exception as e:
            print(f"[ERRO] Security Group {reg}: {e}")

def list_iam_users():
    iam = boto3.client('iam')
    users = iam.list_users()
    for u in users['Users']:
        add_resource('iam_user', u['UserName'])

def list_iam_roles():
    iam = boto3.client('iam')
    paginator = iam.get_paginator('list_roles')
    for page in paginator.paginate():
        for role in page['Roles']:
            add_resource('iam_role', role['RoleName'])

def list_iam_policies():
    iam = boto3.client('iam')
    paginator = iam.get_paginator('list_policies')
    for page in paginator.paginate(Scope='Local'):
        for policy in page['Policies']:
            add_resource('iam_policy', policy['PolicyName'])

def list_elbs():
    regions = get_all_regions('elb')
    for reg in regions:
        elb = boto3.client('elb', region_name=reg)
        try:
            lbs = elb.describe_load_balancers()
            for lb in lbs['LoadBalancerDescriptions']:
                add_resource('elb', f"{lb['LoadBalancerName']} ({reg})", lb.get('DNSName', ''))
        except Exception:
            pass

def list_elbv2():
    regions = get_all_regions('elbv2')
    for reg in regions:
        elbv2 = boto3.client('elbv2', region_name=reg)
        try:
            lbs = elbv2.describe_load_balancers()
            for lb in lbs['LoadBalancers']:
                add_resource('elbv2', f"{lb['LoadBalancerName']} ({reg})", lb.get('DNSName', ''))
        except Exception:
            pass

def list_cloudfront():
    cf = boto3.client('cloudfront')
    dists = cf.list_distributions()
    for dist in dists.get('DistributionList', {}).get('Items', []):
        add_resource('cloudfront', dist['Id'], dist.get('DomainName', ''))

def list_route53_zones():
    r53 = boto3.client('route53')
    zones = r53.list_hosted_zones()
    for zone in zones['HostedZones']:
        add_resource('route53_zone', zone['Id'], zone['Name'])

def list_eips():
    regions = get_all_regions('ec2')
    for reg in regions:
        ec2 = boto3.client('ec2', region_name=reg)
        try:
            eips = ec2.describe_addresses()
            for eip in eips['Addresses']:
                add_resource('eip', f"{eip.get('PublicIp', '')} ({reg})", eip.get('InstanceId', ''))
        except Exception:
            pass

def list_enis():
    regions = get_all_regions('ec2')
    for reg in regions:
        ec2 = boto3.client('ec2', region_name=reg)
        try:
            enis = ec2.describe_network_interfaces()
            for eni in enis['NetworkInterfaces']:
                add_resource('eni', f"{eni['NetworkInterfaceId']} ({reg})", eni.get('Description', ''))
        except Exception:
            pass

def list_api_gateways():
    regions = get_all_regions('apigateway')
    for reg in regions:
        apigw = boto3.client('apigateway', region_name=reg)
        position = None
        while True:
            if position:
                apis = apigw.get_rest_apis(position=position)
            else:
                apis = apigw.get_rest_apis()
            for api in apis.get('items', []):
                add_resource('apigateway', f"{api['id']} ({reg})", api.get('name', ''))
            position = apis.get('position')
            if not position:
                break

def list_waf_webacls():
    waf = boto3.client('waf')
    try:
        webacls = waf.list_web_acls()
        for acl in webacls.get('WebACLs', []):
            add_resource('waf_webacl', acl['WebACLId'], acl.get('Name', ''))
    except Exception:
        pass

def list_global_accelerators():
    ga = boto3.client('globalaccelerator')
    try:
        accs = ga.list_accelerators()
        for acc in accs.get('Accelerators', []):
            add_resource('global_accelerator', acc['AcceleratorArn'], acc.get('Name', ''))
    except Exception:
        pass

def list_direct_connect():
    dc = boto3.client('directconnect')
    try:
        conns = dc.describe_connections()
        for conn in conns.get('connections', []):
            add_resource('direct_connect', conn['connectionId'], conn.get('connectionName', ''))
    except Exception:
        pass

def list_transit_gateways():
    regions = get_all_regions('ec2')
    for reg in regions:
        ec2 = boto3.client('ec2', region_name=reg)
        try:
            tgs = ec2.describe_transit_gateways()
            for tg in tgs.get('TransitGateways', []):
                add_resource('transit_gateway', f"{tg['TransitGatewayId']} ({reg})", tg.get('Description', ''))
        except Exception:
            pass

def list_nat_gateways():
    regions = get_all_regions('ec2')
    for reg in regions:
        ec2 = boto3.client('ec2', region_name=reg)
        try:
            ngws = ec2.describe_nat_gateways()
            for ngw in ngws.get('NatGateways', []):
                add_resource('nat_gateway', f"{ngw['NatGatewayId']} ({reg})", ngw.get('State', ''))
        except Exception:
            pass

def list_vpn_connections():
    regions = get_all_regions('ec2')
    for reg in regions:
        ec2 = boto3.client('ec2', region_name=reg)
        try:
            vpns = ec2.describe_vpn_connections()
            for vpn in vpns.get('VpnConnections', []):
                add_resource('vpn_connection', f"{vpn['VpnConnectionId']} ({reg})", vpn.get('State', ''))
        except Exception:
            pass

# Não inclua chaves ou segredos no código! Use aws configure para definir suas credenciais.




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


print("\nRecursos encontrados na conta:")
for service, resources in all_resources.items():
    print(f"\n{service.upper()} ({len(resources)}):")
    for res in resources:
        print(f"  - {res}")

# Exportar para JSON
with open("recursos_aws.json", "w", encoding="utf-8") as f_json:
    json.dump(all_resources, f_json, ensure_ascii=False, indent=2)

# Exportar para CSV
with open("recursos_aws.csv", "w", newline='', encoding="utf-8") as f_csv:
    writer = csv.writer(f_csv)
    writer.writerow(["servico", "id", "extra"])
    for service, resources in all_resources.items():
        for res in resources:
            parts = res.split(' ', 1)
            resource_id = parts[0]
            extra = parts[1] if len(parts) > 1 else ""
            writer.writerow([service, resource_id, extra])
