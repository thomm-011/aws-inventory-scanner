#!/bin/bash

# AWS Inventory Scanner - Installation Script
# Author: Thomas
# Version: 2.0.0

echo "🚀 AWS Inventory Scanner v2.0.0 - Installation"
echo "================================================"

# Check Python version
echo "🔍 Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Por favor, instale Python 3.6+"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Python $PYTHON_VERSION encontrado"

# Check pip
echo "🔍 Verificando pip..."
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 não encontrado. Por favor, instale pip3"
    exit 1
fi
echo "✅ pip3 encontrado"

# Install dependencies
echo "📦 Instalando dependências..."
pip3 install boto3

# Check AWS CLI
echo "🔍 Verificando AWS CLI..."
if ! command -v aws &> /dev/null; then
    echo "⚠️  AWS CLI não encontrado. Recomendamos instalar:"
    echo "   curl 'https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip' -o 'awscliv2.zip'"
    echo "   unzip awscliv2.zip"
    echo "   sudo ./aws/install"
else
    echo "✅ AWS CLI encontrado"
fi

# Make scripts executable
echo "🔧 Configurando permissões..."
chmod +x aws_inventory_scanner.py
chmod +x listar_recursos_expandido.py

# Create directories
echo "📁 Criando estrutura de diretórios..."
mkdir -p exports reports configs

echo ""
echo "✅ Instalação concluída!"
echo ""
echo "📋 Próximos passos:"
echo "1. Configure suas credenciais AWS:"
echo "   aws configure"
echo ""
echo "2. Execute o scanner:"
echo "   ./aws_inventory_scanner.py"
echo ""
echo "3. Para ver todas as opções:"
echo "   ./aws_inventory_scanner.py --help"
echo ""
echo "🎯 Exemplos de uso:"
echo "   ./aws_inventory_scanner.py --summary-only"
echo "   ./aws_inventory_scanner.py --analyze --export-all"
echo "   ./aws_inventory_scanner.py --region us-west-2"
echo ""
echo "📖 Para mais informações, consulte o README.md"
