
import boto3
import json
import csv

all_resources = {}

def add_resource(service, resource_id, extra=""):
    if service not in all_resources:
        all_resources[service] = []
    all_resources[service].append(f"{resource_id} {extra}".strip())

def list_ec2():
    ec2 = boto3.client('ec2')
    instances = ec2.describe_instances()
    for res in instances['Reservations']:
        for inst in res['Instances']:
            instance_id = inst['InstanceId']
            state = inst.get('State', {}).get('Name', '')
            add_resource('ec2', instance_id, state)
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
    rds = boto3.client('rds')
    instances = rds.describe_db_instances()
    for db in instances['DBInstances']:
        add_resource('rds', db['DBInstanceIdentifier'])

def list_vpcs():
    ec2 = boto3.client('ec2')
    vpcs = ec2.describe_vpcs()
    for vpc in vpcs['Vpcs']:
        vpc_id = vpc['VpcId']
        cidr = vpc.get('CidrBlock', '')
        add_resource('vpc', vpc_id, cidr)

def list_subnets():
    ec2 = boto3.client('ec2')
    subnets = ec2.describe_subnets()
    for subnet in subnets['Subnets']:
        subnet_id = subnet['SubnetId']
        cidr = subnet.get('CidrBlock', '')
        add_resource('subnet', subnet_id, cidr)

def list_security_groups():
    ec2 = boto3.client('ec2')
    sgs = ec2.describe_security_groups()
    for sg in sgs['SecurityGroups']:
        sg_id = sg['GroupId']
        name = sg.get('GroupName', '')
        add_resource('security_group', sg_id, name)

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
    elb = boto3.client('elb')
    lbs = elb.describe_load_balancers()
    for lb in lbs['LoadBalancerDescriptions']:
        add_resource('elb', lb['LoadBalancerName'], lb.get('DNSName', ''))

def list_elbv2():
    elbv2 = boto3.client('elbv2')
    lbs = elbv2.describe_load_balancers()
    for lb in lbs['LoadBalancers']:
        add_resource('elbv2', lb['LoadBalancerName'], lb.get('DNSName', ''))

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
    ec2 = boto3.client('ec2')
    eips = ec2.describe_addresses()
    for eip in eips['Addresses']:
        add_resource('eip', eip.get('PublicIp', ''), eip.get('InstanceId', ''))

def list_enis():
    ec2 = boto3.client('ec2')
    enis = ec2.describe_network_interfaces()
    for eni in enis['NetworkInterfaces']:
        add_resource('eni', eni['NetworkInterfaceId'], eni.get('Description', ''))

def list_api_gateways():
    apigw = boto3.client('apigateway')
    apis = apigw.get_rest_apis()
    for api in apis.get('items', []):
        add_resource('apigateway', api['id'], api.get('name', ''))

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
    ec2 = boto3.client('ec2')
    try:
        tgs = ec2.describe_transit_gateways()
        for tg in tgs.get('TransitGateways', []):
            add_resource('transit_gateway', tg['TransitGatewayId'], tg.get('Description', ''))
    except Exception:
        pass

def list_nat_gateways():
    ec2 = boto3.client('ec2')
    try:
        ngws = ec2.describe_nat_gateways()
        for ngw in ngws.get('NatGateways', []):
            add_resource('nat_gateway', ngw['NatGatewayId'], ngw.get('State', ''))
    except Exception:
        pass

def list_vpn_connections():
    ec2 = boto3.client('ec2')
    try:
        vpns = ec2.describe_vpn_connections()
        for vpn in vpns.get('VpnConnections', []):
            add_resource('vpn_connection', vpn['VpnConnectionId'], vpn.get('State', ''))
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
