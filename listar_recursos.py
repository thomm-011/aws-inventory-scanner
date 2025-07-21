import boto3

services = ['ec2', 's3', 'lambda', 'rds']
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

def list_iam_users():
    iam = boto3.client('iam')
    users = iam.list_users()
    for u in users['Users']:
        add_resource('iam', u['UserName'])

# Não inclua chaves ou segredos no código! Use aws configure para definir suas credenciais.

list_ec2()
list_s3()
list_lambda()
list_rds()
list_iam_users()

print("\nRecursos encontrados na conta:")
for service, resources in all_resources.items():
    print(f"\n{service.upper()} ({len(resources)}):")
    for res in resources:
        print(f"  - {res}")
