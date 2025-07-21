import boto3

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
            tags = inst.get('Tags', [])
            tag_str = ", ".join(f"{t['Key']}={t['Value']}" for t in tags)
            add_resource('ec2', instance_id, tag_str)

def list_s3():
    s3 = boto3.client('s3')
    buckets = s3.list_buckets()
    for bucket in buckets['Buckets']:
        bucket_name = bucket['Name']
        add_resource('s3', bucket_name)

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

print("\nRecursos encontrados na conta:")
for service, resources in all_resources.items():
    print(f"\n{service.upper()} ({len(resources)}):")
    for res in resources:
        print(f"  - {res}")
