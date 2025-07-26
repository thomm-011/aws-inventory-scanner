

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/boto3-AWS-green?logo=amazon-aws" alt="boto3">
</div>


# 🗂️ aws-inventory-scanner

💡 **Por que esse projeto existe?**

Imagine um cliente que acreditava ter domínio total sobre sua infraestrutura em nuvem. Tudo estava centralizado na região sa-east-1, como era o padrão da equipe. No entanto, um pequeno deslize durante um teste fez com que uma instância EC2 fosse criada em us-east-1 — e esquecida.

Meses depois, um custo inesperado apareceu. Foi só então que descobriram essa instância rodando sozinha em uma região que nem fazia parte do dia a dia deles.

Esse script nasceu justamente para evitar esse tipo de situação. De forma simples, ele varre as regiões, identifica os recursos ativos e permite agir antes que o custo apareça.

---

Script em Python para listar recursos ativos na AWS:


<ul>
  <li><strong>EC2</strong> (instâncias)</li>
  <li><strong>S3</strong> (buckets)</li>
  <li><strong>Lambda</strong> (funções)</li>
  <li><strong>RDS</strong> (bancos de dados)</li>
  <li><strong>VPCs</strong></li>
  <li><strong>Subnets</strong></li>
  <li><strong>Security Groups</strong></li>
  <li><strong>Usuários IAM</strong></li>
  <li><strong>Roles IAM</strong></li>
  <li><strong>Policies IAM</strong></li>
  <li><strong>Elastic Load Balancers (ELB/ALB/NLB)</strong></li>
  <li><strong>CloudFront Distributions</strong></li>
  <li><strong>Route 53 Hosted Zones</strong></li>
  <li><strong>Elastic IPs (EIP)</strong></li>
  <li><strong>Network Interfaces (ENI)</strong></li>
  <li><strong>API Gateway</strong></li>
  <li><strong>WAF WebACLs</strong></li>
  <li><strong>Global Accelerator</strong></li>
  <li><strong>Direct Connect</strong></li>
  <li><strong>Transit Gateway</strong></li>
  <li><strong>NAT Gateway</strong></li>
  <li><strong>VPN Connections</strong></li>
</ul>

---

## 🚀 Pré-requisitos

- Python 3.x
- boto3 (`pip install boto3`)
- AWS CLI configurado

---

## ⚡ Como usar

<ol>
  <li>
    <strong>Configure suas credenciais AWS</strong> (caso ainda não tenha):<br>
    <pre><code>aws configure</code></pre>
  </li>
  <li>
    <strong>Instale as dependências:</strong><br>
    <pre><code>pip install boto3</code></pre>
  </li>
  <li>
    <strong>Execute o script:</strong><br>
    <pre><code>python3 listar_recursos.py</code></pre>
    <br>
    <em>Ao finalizar, os recursos serão exportados automaticamente para os arquivos <code>recursos_aws.json</code> e <code>recursos_aws.csv</code> na mesma pasta do script.</em>
  </li>
</ol>

---

<details>
<summary>O que o script faz?</summary>


O script irá listar, diretamente no terminal, os seguintes recursos da sua conta AWS:
<ul>
  <li>Instâncias <strong>EC2</strong></li>
  <li>Buckets <strong>S3</strong></li>
  <li>Funções <strong>Lambda</strong></li>
  <li>Bancos <strong>RDS</strong></li>
  <li><strong>VPCs</strong></li>
  <li><strong>Subnets</strong></li>
  <li><strong>Security Groups</strong></li>
  <li>Usuários <strong>IAM</strong></li>
  <li>Roles <strong>IAM</strong></li>
  <li>Policies <strong>IAM</strong></li>
  <li>Elastic Load Balancers (ELB/ALB/NLB)</li>
  <li>CloudFront Distributions</li>
  <li>Route 53 Hosted Zones</li>
  <li>Elastic IPs (EIP)</li>
  <li>Network Interfaces (ENI)</li>
  <li>API Gateway</li>
  <li>WAF WebACLs</li>
  <li>Global Accelerator</li>
  <li>Direct Connect</li>
  <li>Transit Gateway</li>
  <li>NAT Gateway</li>
  <li>VPN Connections</li>
</ul>

Além disso, exporta todos os dados coletados em dois formatos:
<ul>
  <li><code>recursos_aws.json</code> &mdash; formato estruturado para uso em scripts e integrações</li>
  <li><code>recursos_aws.csv</code> &mdash; formato tabular para uso em planilhas</li>
</ul>
</details>

