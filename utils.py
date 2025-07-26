#!/usr/bin/env python3
import json
import csv
from datetime import datetime
import os

class AWSResourceExporter:
    def __init__(self, resources_data):
        self.resources_data = resources_data
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    def export_to_json(self, filename=None):
        """Export resources to JSON format"""
        if not filename:
            filename = f"aws_resources_{self.timestamp}.json"
        
        # Convert to JSON-serializable format
        export_data = {
            'timestamp': datetime.now().isoformat(),
            'total_resources': sum(len(resources) for resources in self.resources_data.values()),
            'resources': self.resources_data
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"✅ Dados exportados para: {filename}")
        return filename
    
    def export_to_csv(self, filename=None):
        """Export resources to CSV format"""
        if not filename:
            filename = f"aws_resources_{self.timestamp}.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow(['Service', 'Resource_ID', 'Details', 'Status'])
            
            # Data
            for service, resources in self.resources_data.items():
                for resource in resources:
                    writer.writerow([
                        service,
                        resource['id'],
                        resource['extra'],
                        resource['status']
                    ])
        
        print(f"✅ Dados exportados para: {filename}")
        return filename
    
    def export_to_html(self, filename=None):
        """Export resources to HTML format"""
        if not filename:
            filename = f"aws_resources_{self.timestamp}.html"
        
        html_content = self._generate_html_report()
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Relatório HTML gerado: {filename}")
        return filename
    
    def _generate_html_report(self):
        """Generate HTML report content"""
        total_resources = sum(len(resources) for resources in self.resources_data.values())
        
        html = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AWS Resources Report - {datetime.now().strftime('%Y-%m-%d %H:%M')}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        h1 {{ color: #232f3e; text-align: center; }}
        h2 {{ color: #ff9900; border-bottom: 2px solid #ff9900; padding-bottom: 5px; }}
        .summary {{ background: #e8f4fd; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
        .resource-group {{ margin-bottom: 30px; }}
        .resource-item {{ background: #f9f9f9; margin: 5px 0; padding: 10px; border-left: 4px solid #ff9900; }}
        .status-active {{ border-left-color: #28a745; }}
        .status-terminated {{ border-left-color: #dc3545; }}
        .status-stopped {{ border-left-color: #ffc107; }}
        .resource-id {{ font-weight: bold; color: #232f3e; }}
        .resource-details {{ color: #666; font-size: 0.9em; margin-top: 5px; }}
        .timestamp {{ text-align: center; color: #666; margin-top: 20px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
        th, td {{ padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 AWS Resources Report</h1>
        
        <div class="summary">
            <h2>📊 Resumo Executivo</h2>
            <p><strong>Total de recursos encontrados:</strong> {total_resources}</p>
            <ul>
"""
        
        # Add summary items
        for service, resources in self.resources_data.items():
            if resources:
                html += f"                <li><strong>{service}:</strong> {len(resources)} recursos</li>\n"
        
        html += """
            </ul>
        </div>
        
        <h2>📋 Detalhamento por Serviço</h2>
"""
        
        # Add detailed resources
        for service, resources in self.resources_data.items():
            if resources:
                html += f"""
        <div class="resource-group">
            <h3>🔹 {service} ({len(resources)} recursos)</h3>
"""
                
                for resource in resources:
                    status_class = f"status-{resource['status'].lower()}" if resource['status'] else ""
                    html += f"""
            <div class="resource-item {status_class}">
                <div class="resource-id">{resource['id']}</div>
                <div class="resource-details">{resource['extra']}</div>
                {f'<div class="resource-details"><strong>Status:</strong> {resource["status"]}</div>' if resource['status'] and resource['status'] != 'active' else ''}
            </div>
"""
                
                html += "        </div>\n"
        
        html += f"""
        <div class="timestamp">
            <p>Relatório gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </div>
</body>
</html>
"""
        
        return html

class AWSResourceAnalyzer:
    def __init__(self, resources_data):
        self.resources_data = resources_data
    
    def analyze_costs_potential(self):
        """Analyze potential cost-generating resources"""
        cost_resources = {
            'EC2 Instances': [],
            'RDS Instances': [],
            'EBS Volumes': [],
            'NAT Gateways': [],
            'Elastic IPs': [],
            'Load Balancers': []
        }
        
        for service, resources in self.resources_data.items():
            if service in cost_resources:
                cost_resources[service] = resources
        
        return cost_resources
    
    def find_unused_resources(self):
        """Identify potentially unused resources"""
        unused = {
            'unattached_volumes': [],
            'unassociated_eips': [],
            'empty_security_groups': [],
            'unused_key_pairs': []
        }
        
        # Find unattached EBS volumes
        if 'EBS Volumes' in self.resources_data:
            for volume in self.resources_data['EBS Volumes']:
                if 'Não anexado' in volume['extra']:
                    unused['unattached_volumes'].append(volume)
        
        # Find unassociated Elastic IPs
        if 'Elastic IPs' in self.resources_data:
            for eip in self.resources_data['Elastic IPs']:
                if eip['status'] == 'available':
                    unused['unassociated_eips'].append(eip)
        
        return unused
    
    def generate_security_report(self):
        """Generate basic security analysis"""
        security_issues = {
            'public_security_groups': [],
            'unused_key_pairs': [],
            'old_access_keys': []
        }
        
        # This would need more detailed analysis
        # For now, just return the structure
        return security_issues
    
    def print_analysis(self):
        """Print analysis results"""
        print("\n" + "="*60)
        print("📈 ANÁLISE DE RECURSOS AWS")
        print("="*60)
        
        # Cost analysis
        cost_resources = self.analyze_costs_potential()
        total_cost_resources = sum(len(resources) for resources in cost_resources.values())
        
        print(f"\n💰 Recursos que geram custos: {total_cost_resources}")
        for service, resources in cost_resources.items():
            if resources:
                print(f"  • {service}: {len(resources)} recursos")
        
        # Unused resources
        unused = self.find_unused_resources()
        total_unused = sum(len(resources) for resources in unused.values())
        
        print(f"\n🗑️  Recursos potencialmente não utilizados: {total_unused}")
        for category, resources in unused.items():
            if resources:
                print(f"  • {category.replace('_', ' ').title()}: {len(resources)} recursos")
        
        print(f"\n🕒 Análise realizada em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def create_directory_structure():
    """Create directory structure for exports"""
    directories = ['exports', 'reports', 'configs']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 Diretório criado: {directory}")

def load_previous_scan(filename):
    """Load previous scan results for comparison"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('resources', {})
    except FileNotFoundError:
        print(f"⚠️  Arquivo não encontrado: {filename}")
        return {}
    except json.JSONDecodeError:
        print(f"❌ Erro ao ler arquivo JSON: {filename}")
        return {}

def compare_scans(current_resources, previous_resources):
    """Compare current scan with previous scan"""
    changes = {
        'added': {},
        'removed': {},
        'modified': {}
    }
    
    # Find added and modified resources
    for service, current_items in current_resources.items():
        if service not in previous_resources:
            changes['added'][service] = current_items
        else:
            previous_items = previous_resources[service]
            current_ids = {item['id'] for item in current_items}
            previous_ids = {item['id'] for item in previous_items}
            
            # Added resources in this service
            added_ids = current_ids - previous_ids
            if added_ids:
                changes['added'][service] = [item for item in current_items if item['id'] in added_ids]
    
    # Find removed resources
    for service, previous_items in previous_resources.items():
        if service in current_resources:
            current_items = current_resources[service]
            current_ids = {item['id'] for item in current_items}
            previous_ids = {item['id'] for item in previous_items}
            
            # Removed resources in this service
            removed_ids = previous_ids - current_ids
            if removed_ids:
                changes['removed'][service] = [item for item in previous_items if item['id'] in removed_ids]
        else:
            changes['removed'][service] = previous_items
    
    return changes

def print_changes_report(changes):
    """Print changes between scans"""
    print("\n" + "="*60)
    print("🔄 RELATÓRIO DE MUDANÇAS")
    print("="*60)
    
    total_added = sum(len(items) for items in changes['added'].values())
    total_removed = sum(len(items) for items in changes['removed'].values())
    
    print(f"\n✅ Recursos adicionados: {total_added}")
    for service, items in changes['added'].items():
        if items:
            print(f"  • {service}: {len(items)} recursos")
            for item in items[:3]:  # Show first 3
                print(f"    - {item['id']}")
            if len(items) > 3:
                print(f"    ... e mais {len(items) - 3} recursos")
    
    print(f"\n❌ Recursos removidos: {total_removed}")
    for service, items in changes['removed'].items():
        if items:
            print(f"  • {service}: {len(items)} recursos")
            for item in items[:3]:  # Show first 3
                print(f"    - {item['id']}")
            if len(items) > 3:
                print(f"    ... e mais {len(items) - 3} recursos")
    
    if total_added == 0 and total_removed == 0:
        print("\n🔄 Nenhuma mudança detectada desde o último scan.")
