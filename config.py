# AWS Resource Scanner Configuration

# Default AWS region
DEFAULT_REGION = 'us-east-1'

# Services to scan (set to False to disable)
SERVICES_CONFIG = {
    # Core Compute & Storage
    'ec2_instances': True,
    's3_buckets': True,
    'ebs_volumes': True,
    'elastic_ips': True,
    
    # Serverless & Functions
    'lambda_functions': True,
    
    # Databases
    'rds_instances': True,
    'dynamodb_tables': True,
    
    # Networking
    'vpc_resources': True,
    'nat_gateways': True,
    'internet_gateways': True,
    'elastic_load_balancers': True,
    
    # Security & Identity
    'iam_resources': True,
    'key_pairs': True,
    'secrets_manager': True,
    
    # Application Services
    'api_gateway': True,
    'sns_topics': True,
    'sqs_queues': True,
    
    # DevOps & Deployment
    'cloudformation_stacks': True,
    'ecr_repositories': True,
    'ecs_clusters': True,
    'auto_scaling_groups': True,
    
    # Monitoring & DNS
    'cloudwatch_alarms': True,
    'route53_zones': True,
}

# Output configuration
OUTPUT_CONFIG = {
    'show_executive_summary': True,
    'show_detailed_results': True,
    'use_emojis': True,
    'show_timestamps': True,
}

# Regions to scan (for multi-region scanning)
REGIONS_TO_SCAN = [
    'us-east-1',      # N. Virginia
    'us-west-2',      # Oregon
    'eu-west-1',      # Ireland
    'ap-southeast-1', # Singapore
]

# Services that are global (not region-specific)
GLOBAL_SERVICES = [
    'route53_zones',
    'iam_resources',
]
