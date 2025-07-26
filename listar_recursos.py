#!/usr/bin/env python3
import boto3
import json
from datetime import datetime
from botocore.exceptions import ClientError, NoCredentialsError

class AWSResourceLister:
    def __init__(self, region='us-east-1'):
        self.region = region
        self.all_resources = {}
        
    def add_resource(self, service, resource_id, extra="", status=""):
        if service not in self.all_resources:
            self.all_resources[service] = []
        
        resource_info = {
            'id': resource_id,
            'extra': extra,
            'status': status
        }
        self.all_resources[service].append(resource_info)

    def safe_call(self, func, service_name):
        """Safely call AWS API with error handling"""
        try:
            func()
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code in ['AccessDenied', 'UnauthorizedOperation']:
                print(f"⚠️  Sem permissão para acessar {service_name}")
            else:
                print(f"❌ Erro ao acessar {service_name}: {error_code}")
        except Exception as e:
            print(f"❌ Erro inesperado em {service_name}: {str(e)}")

    def list_ec2_instances(self):
        def _list():
            ec2 = boto3.client('ec2', region_name=self.region)
            instances = ec2.describe_instances()
            
            for res in instances['Reservations']:
                for inst in res['Instances']:
                    instance_id = inst['InstanceId']
                    instance_type = inst['InstanceType']
                    state = inst['State']['Name']
                    
                    # Get tags
                    tags = inst.get('Tags', [])
                    name_tag = next((t['Value'] for t in tags if t['Key'] == 'Name'), 'Sem nome')
                    
                    # Launch time
                    launch_time = inst.get('LaunchTime', '').strftime('%Y-%m-%d %H:%M') if inst.get('LaunchTime') else ''
                    
                    extra = f"{instance_type} | {name_tag} | {launch_time}"
                    self.add_resource('EC2 Instances', instance_id, extra, state)
        
        self.safe_call(_list, 'EC2 Instances')

    def list_s3_buckets(self):
        def _list():
            s3 = boto3.client('s3')
            buckets = s3.list_buckets()
            
            for bucket in buckets['Buckets']:
                bucket_name = bucket['Name']
                creation_date = bucket['CreationDate'].strftime('%Y-%m-%d %H:%M')
                
                # Try to get bucket region
                try:
                    location = s3.get_bucket_location(Bucket=bucket_name)
                    region = location['LocationConstraint'] or 'us-east-1'
                except:
                    region = 'unknown'
                
                extra = f"Criado: {creation_date} | Região: {region}"
                self.add_resource('S3 Buckets', bucket_name, extra, 'active')
        
        self.safe_call(_list, 'S3 Buckets')

    def list_lambda_functions(self):
        def _list():
            lam = boto3.client('lambda', region_name=self.region)
            funcs = lam.list_functions()
            
            for f in funcs['Functions']:
                func_name = f['FunctionName']
                runtime = f['Runtime']
                memory = f['MemorySize']
                last_modified = f['LastModified']
                
                extra = f"{runtime} | {memory}MB | Modificado: {last_modified}"
                self.add_resource('Lambda Functions', func_name, extra, 'active')
        
        self.safe_call(_list, 'Lambda Functions')

    def list_rds_instances(self):
        def _list():
            rds = boto3.client('rds', region_name=self.region)
            instances = rds.describe_db_instances()
            
            for db in instances['DBInstances']:
                db_id = db['DBInstanceIdentifier']
                engine = db['Engine']
                instance_class = db['DBInstanceClass']
                status = db['DBInstanceStatus']
                
                extra = f"{engine} | {instance_class}"
                self.add_resource('RDS Instances', db_id, extra, status)
        
        self.safe_call(_list, 'RDS Instances')

    def list_dynamodb_tables(self):
        def _list():
            dynamodb = boto3.client('dynamodb', region_name=self.region)
            tables = dynamodb.list_tables()
            
            for table_name in tables['TableNames']:
                # Get table details
                try:
                    table_info = dynamodb.describe_table(TableName=table_name)
                    status = table_info['Table']['TableStatus']
                    item_count = table_info['Table'].get('ItemCount', 0)
                    
                    extra = f"Items: {item_count}"
                    self.add_resource('DynamoDB Tables', table_name, extra, status)
                except:
                    self.add_resource('DynamoDB Tables', table_name, '', 'unknown')
        
        self.safe_call(_list, 'DynamoDB Tables')

    def list_api_gateway(self):
        def _list():
            # REST APIs (v1)
            apigw = boto3.client('apigateway', region_name=self.region)
            rest_apis = apigw.get_rest_apis()
            
            for api in rest_apis['items']:
                api_id = api['id']
                api_name = api['name']
                created_date = api['createdDate'].strftime('%Y-%m-%d %H:%M')
                
                extra = f"REST API | Criado: {created_date}"
                self.add_resource('API Gateway', f"{api_name} ({api_id})", extra, 'active')
            
            # HTTP APIs (v2)
            try:
                apigwv2 = boto3.client('apigatewayv2', region_name=self.region)
                http_apis = apigwv2.get_apis()
                
                for api in http_apis['Items']:
                    api_id = api['ApiId']
                    api_name = api['Name']
                    protocol = api['ProtocolType']
                    created_date = api['CreatedDate'].strftime('%Y-%m-%d %H:%M')
                    
                    extra = f"{protocol} API | Criado: {created_date}"
                    self.add_resource('API Gateway', f"{api_name} ({api_id})", extra, 'active')
            except:
                pass  # HTTP APIs might not be available in all regions
        
        self.safe_call(_list, 'API Gateway')

    def list_vpc_resources(self):
        def _list():
            ec2 = boto3.client('ec2', region_name=self.region)
            
            # VPCs
            vpcs = ec2.describe_vpcs()
            for vpc in vpcs['Vpcs']:
                vpc_id = vpc['VpcId']
                cidr = vpc['CidrBlock']
                is_default = vpc['IsDefault']
                
                extra = f"CIDR: {cidr} | {'Padrão' if is_default else 'Customizada'}"
                self.add_resource('VPCs', vpc_id, extra, vpc['State'])
            
            # Security Groups
            sgs = ec2.describe_security_groups()
            for sg in sgs['SecurityGroups']:
                sg_id = sg['GroupId']
                sg_name = sg['GroupName']
                vpc_id = sg['VpcId']
                
                extra = f"{sg_name} | VPC: {vpc_id}"
                self.add_resource('Security Groups', sg_id, extra, 'active')
        
        self.safe_call(_list, 'VPC Resources')

    def list_key_pairs(self):
        def _list():
            ec2 = boto3.client('ec2', region_name=self.region)
            key_pairs = ec2.describe_key_pairs()
            
            for kp in key_pairs['KeyPairs']:
                key_name = kp['KeyName']
                key_id = kp['KeyPairId']
                key_type = kp['KeyType']
                created = kp.get('CreateTime', '').strftime('%Y-%m-%d %H:%M') if kp.get('CreateTime') else ''
                
                extra = f"Tipo: {key_type} | Criado: {created}"
                self.add_resource('Key Pairs', f"{key_name} ({key_id})", extra, 'active')
        
        self.safe_call(_list, 'Key Pairs')

    def list_ebs_volumes(self):
        def _list():
            ec2 = boto3.client('ec2', region_name=self.region)
            volumes = ec2.describe_volumes()
            
            for vol in volumes['Volumes']:
                vol_id = vol['VolumeId']
                size = vol['Size']
                vol_type = vol['VolumeType']
                state = vol['State']
                
                # Check if attached to instance
                attachments = vol.get('Attachments', [])
                attached_to = attachments[0]['InstanceId'] if attachments else 'Não anexado'
                
                extra = f"{size}GB | {vol_type} | Anexado a: {attached_to}"
                self.add_resource('EBS Volumes', vol_id, extra, state)
        
        self.safe_call(_list, 'EBS Volumes')

    def list_iam_resources(self):
        def _list():
            iam = boto3.client('iam')
            
            # Users
            users = iam.list_users()
            for user in users['Users']:
                user_name = user['UserName']
                created = user['CreateDate'].strftime('%Y-%m-%d %H:%M')
                
                extra = f"Criado: {created}"
                self.add_resource('IAM Users', user_name, extra, 'active')
            
            # Roles
            roles = iam.list_roles()
            for role in roles['Roles']:
                role_name = role['RoleName']
                created = role['CreateDate'].strftime('%Y-%m-%d %H:%M')
                
                extra = f"Criado: {created}"
                self.add_resource('IAM Roles', role_name, extra, 'active')
        
        self.safe_call(_list, 'IAM Resources')

    def run_all_checks(self):
        """Execute all resource listing functions"""
        print("🔍 Listando recursos AWS...")
        print(f"📍 Região: {self.region}")
        print("-" * 50)
        
        self.list_ec2_instances()
        self.list_s3_buckets()
        self.list_lambda_functions()
        self.list_rds_instances()
        self.list_dynamodb_tables()
        self.list_api_gateway()
        self.list_vpc_resources()
        self.list_key_pairs()
        self.list_ebs_volumes()
        self.list_iam_resources()

    def print_results(self):
        """Print formatted results"""
        print("\n" + "="*60)
        print("📊 RECURSOS AWS ENCONTRADOS")
        print("="*60)
        
        total_resources = sum(len(resources) for resources in self.all_resources.values())
        
        if total_resources == 0:
            print("❌ Nenhum recurso encontrado ou sem permissões adequadas.")
            return
        
        for service, resources in self.all_resources.items():
            if resources:  # Only show services with resources
                print(f"\n🔹 {service} ({len(resources)} recursos):")
                print("-" * 40)
                
                for resource in resources:
                    status_emoji = {
                        'running': '🟢',
                        'active': '🟢', 
                        'stopped': '🔴',
                        'terminated': '⚫',
                        'available': '🟢',
                        'pending': '🟡'
                    }.get(resource['status'].lower(), '🔵')
                    
                    print(f"  {status_emoji} {resource['id']}")
                    if resource['extra']:
                        print(f"     └─ {resource['extra']}")
                    if resource['status'] and resource['status'] != 'active':
                        print(f"     └─ Status: {resource['status']}")
        
        print(f"\n📈 Total de recursos: {total_resources}")
        print(f"🕒 Verificação realizada em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def main():
    try:
        # You can change the region here
        lister = AWSResourceLister(region='us-east-1')
        lister.run_all_checks()
        lister.print_results()
        
    except NoCredentialsError:
        print("❌ Credenciais AWS não encontradas!")
        print("Configure suas credenciais com: aws configure")
    except Exception as e:
        print(f"❌ Erro inesperado: {str(e)}")

if __name__ == "__main__":
    main()
