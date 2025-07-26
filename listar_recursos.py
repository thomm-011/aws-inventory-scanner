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

    # ========== NOVOS RECURSOS ADICIONADOS ==========

    def list_cloudformation_stacks(self):
        def _list():
            cf = boto3.client('cloudformation', region_name=self.region)
            stacks = cf.describe_stacks()
            
            for stack in stacks['Stacks']:
                stack_name = stack['StackName']
                status = stack['StackStatus']
                created = stack['CreationTime'].strftime('%Y-%m-%d %H:%M')
                
                # Get template description if available
                description = stack.get('Description', 'Sem descrição')
                
                extra = f"Status: {status} | Criado: {created} | {description}"
                self.add_resource('CloudFormation Stacks', stack_name, extra, status)
        
        self.safe_call(_list, 'CloudFormation Stacks')

    def list_sns_topics(self):
        def _list():
            sns = boto3.client('sns', region_name=self.region)
            topics = sns.list_topics()
            
            for topic in topics['Topics']:
                topic_arn = topic['TopicArn']
                topic_name = topic_arn.split(':')[-1]
                
                # Get topic attributes
                try:
                    attrs = sns.get_topic_attributes(TopicArn=topic_arn)
                    subscriptions_confirmed = attrs['Attributes'].get('SubscriptionsConfirmed', '0')
                    subscriptions_pending = attrs['Attributes'].get('SubscriptionsPending', '0')
                    
                    extra = f"Confirmadas: {subscriptions_confirmed} | Pendentes: {subscriptions_pending}"
                    self.add_resource('SNS Topics', topic_name, extra, 'active')
                except:
                    self.add_resource('SNS Topics', topic_name, '', 'active')
        
        self.safe_call(_list, 'SNS Topics')

    def list_sqs_queues(self):
        def _list():
            sqs = boto3.client('sqs', region_name=self.region)
            queues = sqs.list_queues()
            
            if 'QueueUrls' in queues:
                for queue_url in queues['QueueUrls']:
                    queue_name = queue_url.split('/')[-1]
                    
                    # Get queue attributes
                    try:
                        attrs = sqs.get_queue_attributes(
                            QueueUrl=queue_url,
                            AttributeNames=['ApproximateNumberOfMessages', 'CreatedTimestamp']
                        )
                        
                        msg_count = attrs['Attributes'].get('ApproximateNumberOfMessages', '0')
                        created_timestamp = attrs['Attributes'].get('CreatedTimestamp', '')
                        
                        if created_timestamp:
                            created = datetime.fromtimestamp(int(created_timestamp)).strftime('%Y-%m-%d %H:%M')
                            extra = f"Mensagens: {msg_count} | Criado: {created}"
                        else:
                            extra = f"Mensagens: {msg_count}"
                        
                        self.add_resource('SQS Queues', queue_name, extra, 'active')
                    except:
                        self.add_resource('SQS Queues', queue_name, '', 'active')
        
        self.safe_call(_list, 'SQS Queues')

    def list_cloudwatch_alarms(self):
        def _list():
            cw = boto3.client('cloudwatch', region_name=self.region)
            alarms = cw.describe_alarms()
            
            for alarm in alarms['MetricAlarms']:
                alarm_name = alarm['AlarmName']
                state = alarm['StateValue']
                metric_name = alarm['MetricName']
                namespace = alarm['Namespace']
                
                extra = f"Estado: {state} | Métrica: {metric_name} | Namespace: {namespace}"
                self.add_resource('CloudWatch Alarms', alarm_name, extra, state)
        
        self.safe_call(_list, 'CloudWatch Alarms')

    def list_route53_zones(self):
        def _list():
            route53 = boto3.client('route53')
            zones = route53.list_hosted_zones()
            
            for zone in zones['HostedZones']:
                zone_name = zone['Name'].rstrip('.')
                zone_id = zone['Id'].split('/')[-1]
                is_private = zone.get('Config', {}).get('PrivateZone', False)
                record_count = zone['ResourceRecordSetCount']
                
                zone_type = 'Privada' if is_private else 'Pública'
                extra = f"Tipo: {zone_type} | Records: {record_count} | ID: {zone_id}"
                self.add_resource('Route53 Hosted Zones', zone_name, extra, 'active')
        
        self.safe_call(_list, 'Route53 Hosted Zones')

    def list_elastic_load_balancers(self):
        def _list():
            # Classic Load Balancers
            elb = boto3.client('elb', region_name=self.region)
            classic_lbs = elb.describe_load_balancers()
            
            for lb in classic_lbs['LoadBalancerDescriptions']:
                lb_name = lb['LoadBalancerName']
                scheme = lb['Scheme']
                created = lb['CreatedTime'].strftime('%Y-%m-%d %H:%M')
                instances = len(lb['Instances'])
                
                extra = f"Tipo: Classic | Esquema: {scheme} | Instâncias: {instances} | Criado: {created}"
                self.add_resource('Load Balancers', lb_name, extra, 'active')
            
            # Application/Network Load Balancers (ELBv2)
            elbv2 = boto3.client('elbv2', region_name=self.region)
            modern_lbs = elbv2.describe_load_balancers()
            
            for lb in modern_lbs['LoadBalancers']:
                lb_name = lb['LoadBalancerName']
                lb_type = lb['Type']
                scheme = lb['Scheme']
                state = lb['State']['Code']
                created = lb['CreatedTime'].strftime('%Y-%m-%d %H:%M')
                
                extra = f"Tipo: {lb_type.upper()} | Esquema: {scheme} | Criado: {created}"
                self.add_resource('Load Balancers', lb_name, extra, state)
        
        self.safe_call(_list, 'Load Balancers')

    def list_auto_scaling_groups(self):
        def _list():
            asg = boto3.client('autoscaling', region_name=self.region)
            groups = asg.describe_auto_scaling_groups()
            
            for group in groups['AutoScalingGroups']:
                group_name = group['AutoScalingGroupName']
                min_size = group['MinSize']
                max_size = group['MaxSize']
                desired = group['DesiredCapacity']
                current_instances = len(group['Instances'])
                created = group['CreatedTime'].strftime('%Y-%m-%d %H:%M')
                
                extra = f"Min: {min_size} | Max: {max_size} | Desejado: {desired} | Atual: {current_instances} | Criado: {created}"
                self.add_resource('Auto Scaling Groups', group_name, extra, 'active')
        
        self.safe_call(_list, 'Auto Scaling Groups')

    def list_elastic_ips(self):
        def _list():
            ec2 = boto3.client('ec2', region_name=self.region)
            eips = ec2.describe_addresses()
            
            for eip in eips['Addresses']:
                public_ip = eip['PublicIp']
                allocation_id = eip.get('AllocationId', 'N/A')
                instance_id = eip.get('InstanceId', 'Não associado')
                domain = eip.get('Domain', 'classic')
                
                extra = f"Domínio: {domain} | Instância: {instance_id} | Allocation ID: {allocation_id}"
                status = 'associated' if instance_id != 'Não associado' else 'available'
                self.add_resource('Elastic IPs', public_ip, extra, status)
        
        self.safe_call(_list, 'Elastic IPs')

    def list_nat_gateways(self):
        def _list():
            ec2 = boto3.client('ec2', region_name=self.region)
            nat_gws = ec2.describe_nat_gateways()
            
            for nat in nat_gws['NatGateways']:
                nat_id = nat['NatGatewayId']
                state = nat['State']
                subnet_id = nat['SubnetId']
                vpc_id = nat['VpcId']
                created = nat['CreateTime'].strftime('%Y-%m-%d %H:%M')
                
                # Get public IP if available
                public_ip = 'N/A'
                if 'NatGatewayAddresses' in nat and nat['NatGatewayAddresses']:
                    public_ip = nat['NatGatewayAddresses'][0].get('PublicIp', 'N/A')
                
                extra = f"VPC: {vpc_id} | Subnet: {subnet_id} | IP Público: {public_ip} | Criado: {created}"
                self.add_resource('NAT Gateways', nat_id, extra, state)
        
        self.safe_call(_list, 'NAT Gateways')

    def list_internet_gateways(self):
        def _list():
            ec2 = boto3.client('ec2', region_name=self.region)
            igws = ec2.describe_internet_gateways()
            
            for igw in igws['InternetGateways']:
                igw_id = igw['InternetGatewayId']
                
                # Check VPC attachments
                attachments = igw.get('Attachments', [])
                if attachments:
                    vpc_id = attachments[0]['VpcId']
                    state = attachments[0]['State']
                    extra = f"Anexado à VPC: {vpc_id}"
                else:
                    state = 'detached'
                    extra = "Não anexado"
                
                self.add_resource('Internet Gateways', igw_id, extra, state)
        
        self.safe_call(_list, 'Internet Gateways')

    def list_ecr_repositories(self):
        def _list():
            ecr = boto3.client('ecr', region_name=self.region)
            repos = ecr.describe_repositories()
            
            for repo in repos['repositories']:
                repo_name = repo['repositoryName']
                repo_uri = repo['repositoryUri']
                created = repo['createdAt'].strftime('%Y-%m-%d %H:%M')
                
                # Get image count
                try:
                    images = ecr.describe_images(repositoryName=repo_name)
                    image_count = len(images['imageDetails'])
                except:
                    image_count = 0
                
                extra = f"URI: {repo_uri} | Imagens: {image_count} | Criado: {created}"
                self.add_resource('ECR Repositories', repo_name, extra, 'active')
        
        self.safe_call(_list, 'ECR Repositories')

    def list_ecs_clusters(self):
        def _list():
            ecs = boto3.client('ecs', region_name=self.region)
            clusters = ecs.list_clusters()
            
            if clusters['clusterArns']:
                cluster_details = ecs.describe_clusters(clusters=clusters['clusterArns'])
                
                for cluster in cluster_details['clusters']:
                    cluster_name = cluster['clusterName']
                    status = cluster['status']
                    active_services = cluster['activeServicesCount']
                    running_tasks = cluster['runningTasksCount']
                    pending_tasks = cluster['pendingTasksCount']
                    
                    extra = f"Serviços: {active_services} | Tasks rodando: {running_tasks} | Tasks pendentes: {pending_tasks}"
                    self.add_resource('ECS Clusters', cluster_name, extra, status)
        
        self.safe_call(_list, 'ECS Clusters')

    def list_secrets_manager(self):
        def _list():
            sm = boto3.client('secretsmanager', region_name=self.region)
            secrets = sm.list_secrets()
            
            for secret in secrets['SecretList']:
                secret_name = secret['Name']
                created = secret['CreatedDate'].strftime('%Y-%m-%d %H:%M')
                last_accessed = secret.get('LastAccessedDate', '')
                
                if last_accessed:
                    last_accessed = last_accessed.strftime('%Y-%m-%d %H:%M')
                    extra = f"Criado: {created} | Último acesso: {last_accessed}"
                else:
                    extra = f"Criado: {created} | Nunca acessado"
                
                self.add_resource('Secrets Manager', secret_name, extra, 'active')
        
        self.safe_call(_list, 'Secrets Manager')

    def run_all_checks(self):
        """Execute all resource listing functions"""
        print("🔍 Listando recursos AWS...")
        print(f"📍 Região: {self.region}")
        print("-" * 50)
        
        # Recursos originais
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
        
        # Novos recursos adicionados
        self.list_cloudformation_stacks()
        self.list_sns_topics()
        self.list_sqs_queues()
        self.list_cloudwatch_alarms()
        self.list_route53_zones()
        self.list_elastic_load_balancers()
        self.list_auto_scaling_groups()
        self.list_elastic_ips()
        self.list_nat_gateways()
        self.list_internet_gateways()
        self.list_ecr_repositories()
        self.list_ecs_clusters()
        self.list_secrets_manager()

    def print_executive_summary(self):
        """Print executive summary of resources"""
        print("\n" + "="*60)
        print("📊 RESUMO EXECUTIVO DOS RECURSOS AWS")
        print("="*60)
        
        total_resources = sum(len(resources) for resources in self.all_resources.values())
        
        if total_resources == 0:
            print("❌ Nenhum recurso encontrado ou sem permissões adequadas.")
            return
        
        print(f"A ferramenta encontrou {total_resources} recursos na sua conta:")
        print()
        
        # Count active vs inactive resources for key services
        summary_items = []
        
        for service, resources in self.all_resources.items():
            if resources:
                count = len(resources)
                
                # Special handling for EC2 to show active vs terminated
                if service == 'EC2 Instances':
                    active_count = sum(1 for r in resources if r['status'] not in ['terminated', 'stopped'])
                    terminated_count = sum(1 for r in resources if r['status'] == 'terminated')
                    if terminated_count > 0:
                        summary_items.append(f"• {terminated_count} EC2 instances (terminadas)")
                    if active_count > 0:
                        summary_items.append(f"• {active_count} EC2 instances (ativas)")
                else:
                    # For other services, assume active
                    status_suffix = ""
                    if service in ['S3 Buckets', 'Lambda Functions']:
                        status_suffix = " ativos" if count > 1 else " ativo"
                    elif service == 'API Gateway':
                        status_suffix = " ativos" if count > 1 else " ativo"
                    
                    summary_items.append(f"• {count} {service.lower()}{status_suffix}")
        
        # Print summary items
        for item in summary_items:
            print(item)
        
        print(f"\n🕒 Verificação realizada em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    def print_detailed_results(self):
        """Print detailed formatted results"""
        print("\n" + "="*60)
        print("📋 DETALHAMENTO COMPLETO DOS RECURSOS")
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
                        'pending': '🟡',
                        'associated': '🟢',
                        'attached': '🟢',
                        'detached': '🔴'
                    }.get(resource['status'].lower(), '🔵')
                    
                    print(f"  {status_emoji} {resource['id']}")
                    if resource['extra']:
                        print(f"     └─ {resource['extra']}")
                    if resource['status'] and resource['status'] != 'active':
                        print(f"     └─ Status: {resource['status']}")
        
        print(f"\n📈 Total de recursos: {total_resources}")

    def print_results(self):
        """Print both summary and detailed results"""
        self.print_executive_summary()
        self.print_detailed_results()

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
