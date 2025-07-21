

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/boto3-AWS-green?logo=amazon-aws" alt="boto3">
</div>

# 🗂️ aws-inventory-scanner

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
    <pre><code>python listar_recursos.py</code></pre>
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
</ul>

Além disso, exporta todos os dados coletados em dois formatos:
<ul>
  <li><code>recursos_aws.json</code> &mdash; formato estruturado para uso em scripts e integrações</li>
  <li><code>recursos_aws.csv</code> &mdash; formato tabular para uso em planilhas</li>
</ul>
</details>

