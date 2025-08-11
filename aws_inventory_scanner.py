#!/usr/bin/env python3
"""
AWS Inventory Scanner - Comprehensive AWS Resource Discovery Tool
Author: Thomas
Version: 2.0.0
"""

import argparse
import sys
from listar_recursos import AWSResourceLister
from utils import AWSResourceExporter, AWSResourceAnalyzer, create_directory_structure, load_previous_scan, compare_scans, print_changes_report
from config import DEFAULT_REGION, SERVICES_CONFIG, OUTPUT_CONFIG

def main():
    parser = argparse.ArgumentParser(
        description='AWS Inventory Scanner - Comprehensive AWS Resource Discovery Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                          # Scan with default settings
  %(prog)s --region us-west-2       # Scan specific region
  %(prog)s --export-json            # Export results to JSON
  %(prog)s --export-all             # Export to all formats
  %(prog)s --analyze                # Include resource analysis
  %(prog)s --compare previous.json  # Compare with previous scan
  %(prog)s --summary-only           # Show only executive summary
        """
    )
    
    # Basic options
    parser.add_argument('--region', '-r', 
                       default=DEFAULT_REGION,
                       help=f'AWS region to scan (default: {DEFAULT_REGION})')
    
    parser.add_argument('--profile', '-p',
                       help='AWS profile to use')
    
    # Output options
    parser.add_argument('--summary-only', '-s',
                       action='store_true',
                       help='Show only executive summary')
    
    parser.add_argument('--no-emojis',
                       action='store_true',
                       help='Disable emoji output')
    
    # Export options
    parser.add_argument('--export-json',
                       action='store_true',
                       help='Export results to JSON file')
    
    parser.add_argument('--export-csv',
                       action='store_true',
                       help='Export results to CSV file')
    
    parser.add_argument('--export-html',
                       action='store_true',
                       help='Export results to HTML report')
    
    parser.add_argument('--export-all',
                       action='store_true',
                       help='Export to all formats (JSON, CSV, HTML)')
    
    parser.add_argument('--output-dir', '-o',
                       default='exports',
                       help='Output directory for exports (default: exports)')
    
    # Analysis options
    parser.add_argument('--analyze', '-a',
                       action='store_true',
                       help='Include resource analysis (costs, unused resources)')
    
    parser.add_argument('--compare',
                       help='Compare with previous scan results (JSON file)')
    
    # Service filtering
    parser.add_argument('--services',
                       nargs='+',
                       help='Specific services to scan (e.g., ec2 s3 lambda)')
    
    parser.add_argument('--exclude-services',
                       nargs='+',
                       help='Services to exclude from scan')
    
    # Utility options
    parser.add_argument('--list-services',
                       action='store_true',
                       help='List all available services and exit')
    
    parser.add_argument('--version', '-v',
                       action='version',
                       version='AWS Inventory Scanner 2.0.0')
    
    args = parser.parse_args()
    
    # Handle list services
    if args.list_services:
        print("Available services:")
        for service in sorted(SERVICES_CONFIG.keys()):
            status = "✅" if SERVICES_CONFIG[service] else "❌"
            print(f"  {status} {service}")
        return
    
    # Create directory structure
    create_directory_structure()
    
    try:
        # Initialize scanner
        print("🚀 AWS Inventory Scanner v2.0.0")
        print("=" * 50)
        
        lister = AWSResourceLister(region=args.region)
        
        # Apply service filtering if specified
        if args.services:
            # Enable only specified services
            for service in SERVICES_CONFIG:
                SERVICES_CONFIG[service] = service in args.services
        
        if args.exclude_services:
            # Disable specified services
            for service in args.exclude_services:
                if service in SERVICES_CONFIG:
                    SERVICES_CONFIG[service] = False
        
        # Run the scan
        lister.run_all_checks()
        
        # Display results
        if args.summary_only:
            lister.print_executive_summary()
        else:
            lister.print_results()
        
        # Analysis
        if args.analyze:
            analyzer = AWSResourceAnalyzer(lister.all_resources)
            analyzer.print_analysis()
        
        # Comparison with previous scan
        if args.compare:
            previous_resources = load_previous_scan(args.compare)
            if previous_resources:
                changes = compare_scans(lister.all_resources, previous_resources)
                print_changes_report(changes)
        
        # Export results
        exporter = AWSResourceExporter(lister.all_resources)
        
        if args.export_all:
            args.export_json = True
            args.export_csv = True
            args.export_html = True
        
        if args.export_json:
            json_file = exporter.export_to_json(f"{args.output_dir}/aws_resources_{exporter.timestamp}.json")
        
        if args.export_csv:
            csv_file = exporter.export_to_csv(f"{args.output_dir}/aws_resources_{exporter.timestamp}.csv")
        
        if args.export_html:
            html_file = exporter.export_to_html(f"{args.output_dir}/aws_resources_{exporter.timestamp}.html")
        
        # Summary
        total_resources = sum(len(resources) for resources in lister.all_resources.values())
        print(f"\n🎯 Scan concluído! {total_resources} recursos encontrados na região {args.region}")
        
    except KeyboardInterrupt:
        print("\n⚠️  Scan interrompido pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro durante o scan: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
