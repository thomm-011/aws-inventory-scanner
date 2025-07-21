

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/boto3-AWS-green?logo=amazon-aws" alt="boto3">
</div>

# 🗂️ aws-inventory-scanner

Script em Python para listar recursos ativos na AWS:

<ul>
  <li><strong>EC2</strong></li>
  <li><strong>S3</strong></li>
  <li><strong>Lambda</strong></li>
  <li><strong>RDS</strong></li>
  <li><strong>Usuários IAM</strong></li>
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
  </li>
</ol>

---

<details>
<summary>O que o script faz?</summary>

O script irá listar recursos <strong>EC2</strong>, <strong>S3</strong>, <strong>Lambda</strong>, <strong>RDS</strong> e <strong>usuários IAM</strong> da sua conta AWS diretamente no terminal.

</details>

