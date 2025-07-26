# 🔍 AWS Inventory Scanner v2.0

Uma ferramenta Python completa e profissional para descobrir, auditar e analisar todos os recursos AWS da sua conta de forma organizada e visual.

## 📋 Índice

- [Características](#-características)
- [Novidades v2.0](#-novidades-v20)
- [Recursos Suportados](#-recursos-suportados)
- [Instalação](#-instalação)
- [Uso](#-uso)
- [Exemplos de Uso](#-exemplos-de-uso)
- [Exportação de Dados](#-exportação-de-dados)
- [Análise de Recursos](#-análise-de-recursos)
- [Configuração](#-configuração)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Contribuição](#-contribuição)

## ✨ Características

### 🎯 **Descoberta Completa**
- **25+ serviços AWS** suportados
- **Resumo executivo** com overview rápido
- **Detalhamento completo** com informações técnicas
- **Status em tempo real** de cada recurso

### 🎨 **Interface Rica**
- **Emojis e formatação colorida** para fácil leitura
- **Indicadores visuais de status** (🟢 ativo, 🔴 parado, ⚫ terminado)
- **Contadores e estatísticas** detalhadas
- **Timestamps** de verificação

### 📊 **Exportação Múltipla**
- **JSON** para integração com outras ferramentas
- **CSV** para análise em planilhas
- **HTML** para relatórios visuais profissionais

### 🔍 **Análise Inteligente**
- **Detecção de recursos não utilizados**
- **Análise de potencial de custos**
- **Comparação entre scans** (diff)
- **Relatórios de segurança básicos**

### 🛡️ **Robustez**
- **Tratamento de erros** avançado
- **Permissões granulares** - continua mesmo sem acesso total
- **Multi-região** configurável
- **Filtros de serviços** personalizáveis

## 🆕 Novidades v2.0

### 🚀 **Novos Recursos AWS Suportados**
- **CloudFormation Stacks** - Infraestrutura como código
- **SNS Topics** - Notificações
- **SQS Queues** - Filas de mensagens
- **CloudWatch Alarms** - Monitoramento
- **Route53 Hosted Zones** - DNS
- **Elastic Load Balancers** - Balanceamento de carga
- **Auto Scaling Groups** - Escalabilidade automática
- **NAT Gateways** - Conectividade de rede
- **Internet Gateways** - Acesso à internet
- **ECR Repositories** - Registro de containers
- **ECS Clusters** - Orquestração de containers
- **Secrets Manager** - Gerenciamento de segredos

### 📈 **Funcionalidades Avançadas**
- **Linha de comando completa** com argumentos
- **Sistema de configuração** flexível
- **Exportação em múltiplos formatos**
- **Análise de custos e recursos não utilizados**
- **Comparação entre scans** para detectar mudanças
- **Filtros de serviços** personalizáveis

## 📋 Recursos Suportados

| Categoria | Serviços | Informações Coletadas |
|-----------|----------|----------------------|
| **💻 Compute** | EC2 Instances, Auto Scaling Groups, Elastic IPs | Tipo, status, nome, data de criação, configurações |
| **💾 Storage** | S3 Buckets, EBS Volumes | Região, tamanho, anexos, datas |
| **⚡ Serverless** | Lambda Functions | Runtime, memória, última modificação |
| **🗄️ Database** | RDS Instances, DynamoDB Tables | Engine, classe, status, contagem de itens |
| **🌐 Networking** | VPCs, Security Groups, NAT/Internet Gateways, Load Balancers | CIDR, regras, anexos, configurações |
| **🔐 Security** | IAM Users/Roles, Key Pairs, Secrets Manager | Permissões, datas de criação, último acesso |
| **📡 Application** | API Gateway, SNS Topics, SQS Queues | Tipo, configurações, estatísticas |
| **🚀 DevOps** | CloudFormation Stacks, ECR Repositories, ECS Clusters | Status, descrições, contagens |
| **📊 Monitoring** | CloudWatch Alarms | Estado, métricas, namespaces |
| **🌍 DNS** | Route53 Hosted Zones | Tipo (pública/privada), contagem de records |

## 📦 Instalação

### 1. **Pré-requisitos**
```bash
# Python 3.6+
python3 --version

# AWS CLI configurado
aws configure

# Dependências Python
pip install boto3
```

### 2. **Download dos Arquivos**
```bash
# Clone ou baixe os arquivos:
# - aws_inventory_scanner.py (arquivo principal)
# - listar_recursos_expandido.py (engine de descoberta)
# - utils.py (utilitários de exportação)
# - config.py (configurações)
```

### 3. **Configuração**
```bash
# Torne o arquivo principal executável
chmod +x aws_inventory_scanner.py

# Configure suas credenciais AWS
aws configure
```

## 🚀 Uso

### **Uso Básico**
```bash
# Scan completo com configurações padrão
python3 aws_inventory_scanner.py

# Ou se executável
./aws_inventory_scanner.py
```

### **Opções de Região**
```bash
# Scan em região específica
./aws_inventory_scanner.py --region us-west-2

# Usar perfil AWS específico
./aws_inventory_scanner.py --profile production
```

### **Filtros de Serviços**
```bash
# Scan apenas serviços específicos
./aws_inventory_scanner.py --services ec2 s3 lambda

# Excluir serviços específicos
./aws_inventory_scanner.py --exclude-services iam route53

# Listar todos os serviços disponíveis
./aws_inventory_scanner.py --list-services
```

### **Opções de Saída**
```bash
# Apenas resumo executivo
./aws_inventory_scanner.py --summary-only

# Sem emojis (para scripts)
./aws_inventory_scanner.py --no-emojis
```

## 📊 Exemplos de Uso

### **1. Scan Completo com Análise**
```bash
./aws_inventory_scanner.py --analyze --export-all
```

### **2. Monitoramento de Mudanças**
```bash
# Primeiro scan
./aws_inventory_scanner.py --export-json

# Scan posterior comparando
./aws_inventory_scanner.py --compare exports/aws_resources_20250726_120000.json
```

### **3. Auditoria de Custos**
```bash
./aws_inventory_scanner.py --services ec2 rds ebs nat_gateways --analyze
```

### **4. Relatório Executivo**
```bash
./aws_inventory_scanner.py --summary-only --export-html --output-dir reports
```

## 📤 Exportação de Dados

### **Formatos Suportados**

#### **JSON** - Para integração
```bash
./aws_inventory_scanner.py --export-json
```
```json
{
  "timestamp": "2025-07-26T06:30:00",
  "total_resources": 150,
  "resources": {
    "EC2 Instances": [
      {
        "id": "i-1234567890abcdef0",
        "extra": "t2.micro | WebServer | 2025-07-26 05:00",
        "status": "running"
      }
    ]
  }
}
```

#### **CSV** - Para planilhas
```bash
./aws_inventory_scanner.py --export-csv
```

#### **HTML** - Relatório visual
```bash
./aws_inventory_scanner.py --export-html
```

### **Exportação Múltipla**
```bash
# Todos os formatos de uma vez
./aws_inventory_scanner.py --export-all --output-dir reports
```

## 🔍 Análise de Recursos

### **Análise de Custos**
```bash
./aws_inventory_scanner.py --analyze
```

**Saída:**
```
📈 ANÁLISE DE RECURSOS AWS
============================================================

💰 Recursos que geram custos: 45
  • EC2 Instances: 5 recursos
  • RDS Instances: 2 recursos
  • NAT Gateways: 3 recursos
  • Load Balancers: 4 recursos

🗑️  Recursos potencialmente não utilizados: 12
  • Unattached Volumes: 8 recursos
  • Unassociated Eips: 4 recursos
```

### **Comparação de Scans**
```bash
./aws_inventory_scanner.py --compare previous_scan.json
```

**Saída:**
```
🔄 RELATÓRIO DE MUDANÇAS
============================================================

✅ Recursos adicionados: 3
  • EC2 Instances: 2 recursos
    - i-new1234567890
    - i-new0987654321
  • S3 Buckets: 1 recursos
    - new-backup-bucket

❌ Recursos removidos: 1
  • Lambda Functions: 1 recursos
    - old-cleanup-function
```

## ⚙️ Configuração

### **Arquivo config.py**
```python
# Região padrão
DEFAULT_REGION = 'us-east-1'

# Serviços para escanear
SERVICES_CONFIG = {
    'ec2_instances': True,
    's3_buckets': True,
    'lambda_functions': True,
    # ... outros serviços
}

# Configurações de saída
OUTPUT_CONFIG = {
    'show_executive_summary': True,
    'show_detailed_results': True,
    'use_emojis': True,
}
```

### **Personalização**
```python
# Desabilitar serviços específicos
SERVICES_CONFIG['iam_resources'] = False

# Alterar região padrão
DEFAULT_REGION = 'eu-west-1'

# Múltiplas regiões
REGIONS_TO_SCAN = ['us-east-1', 'us-west-2', 'eu-west-1']
```

## 📁 Estrutura do Projeto

```
aws-inventory-scanner/
├── aws_inventory_scanner.py      # 🎯 Arquivo principal
├── listar_recursos_expandido.py  # 🔍 Engine de descoberta
├── utils.py                      # 🛠️ Utilitários de exportação
├── config.py                     # ⚙️ Configurações
├── README.md                     # 📖 Documentação
├── exports/                      # 📤 Arquivos exportados
│   ├── aws_resources_*.json
│   ├── aws_resources_*.csv
│   └── aws_resources_*.html
└── reports/                      # 📊 Relatórios
    └── analysis_*.html
```

## 🔒 Permissões IAM Necessárias

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:Describe*",
                "s3:ListAllMyBuckets",
                "s3:GetBucketLocation",
                "lambda:ListFunctions",
                "rds:Describe*",
                "dynamodb:ListTables",
                "dynamodb:DescribeTable",
                "apigateway:GET",
                "iam:List*",
                "cloudformation:DescribeStacks",
                "sns:ListTopics",
                "sns:GetTopicAttributes",
                "sqs:ListQueues",
                "sqs:GetQueueAttributes",
                "cloudwatch:DescribeAlarms",
                "route53:ListHostedZones",
                "elasticloadbalancing:Describe*",
                "autoscaling:Describe*",
                "ecr:DescribeRepositories",
                "ecr:DescribeImages",
                "ecs:ListClusters",
                "ecs:DescribeClusters",
                "secretsmanager:ListSecrets"
            ],
            "Resource": "*"
        }
    ]
}
```

## 🚀 Funcionalidades Avançadas

### **1. Automação com Cron**
```bash
# Scan diário às 6h
0 6 * * * /path/to/aws_inventory_scanner.py --export-json --output-dir /var/log/aws-scans
```

### **2. Integração com CI/CD**
```yaml
# GitHub Actions example
- name: AWS Resource Scan
  run: |
    python3 aws_inventory_scanner.py --export-json --compare previous.json
```

### **3. Alertas de Mudanças**
```bash
# Script para alertas
./aws_inventory_scanner.py --compare last_scan.json | grep "Recursos adicionados\|Recursos removidos"
```

## 🤝 Contribuição

### **Como Contribuir**
1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/NovoServico`)
3. Commit suas mudanças (`git commit -m 'Add: Suporte ao EKS'`)
4. Push para a branch (`git push origin feature/NovoServico`)
5. Abra um Pull Request

### **Ideias para Contribuição**
- [ ] **Novos Serviços**: EKS, Fargate, ElastiCache, Redshift
- [ ] **Multi-região**: Scan automático em múltiplas regiões
- [ ] **Dashboard Web**: Interface web com Flask/Django
- [ ] **Alertas**: Integração com Slack/Teams
- [ ] **Métricas**: Integração com Prometheus/Grafana
- [ ] **Custos**: Integração com AWS Cost Explorer
- [ ] **Compliance**: Verificações de conformidade

## 📈 Roadmap

### **v2.1 (Próxima)**
- [ ] Suporte a EKS e Fargate
- [ ] Scan multi-região automático
- [ ] Dashboard web básico
- [ ] Integração com AWS Cost Explorer

### **v2.2**
- [ ] Alertas via Slack/Teams
- [ ] Análise de compliance
- [ ] Exportação para Prometheus
- [ ] API REST

### **v3.0**
- [ ] Interface web completa
- [ ] Análise de tendências
- [ ] Machine Learning para otimizações
- [ ] Integração com Terraform

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Autor

Desenvolvido por https://github.com/thomm-011 para facilitar o gerenciamento e auditoria de recursos AWS. ❤️

---

## 🆘 Suporte

### **Problemas Comuns**

**1. Erro de Credenciais**
```bash
aws configure
# ou
export AWS_PROFILE=seu-perfil
```

**2. Permissões Insuficientes**
```bash
# A ferramenta continua funcionando, apenas avisa sobre serviços sem acesso
⚠️  Sem permissão para acessar ECS Clusters
```

**3. Timeout em Regiões**
```bash
# Use uma região mais próxima
./aws_inventory_scanner.py --region us-east-1
```

**⭐ Se esta ferramenta foi útil, considere dar uma estrela no repositório!**

**🔗 Links Úteis:**
- [AWS CLI Documentation](https://docs.aws.amazon.com/cli/)
- [Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
