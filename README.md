# aws-inventory-scanner

## Descrição
Script em Python para listar recursos ativos na AWS (EC2, S3, Lambda, RDS e usuários IAM) usando boto3.

## Pré-requisitos
- Python 3.x
- boto3 (`pip install boto3`)
- AWS CLI configurado (NUNCA inclua chaves no código!)

## Como usar

1. **Configure suas credenciais AWS** (se ainda não fez):
   ```sh
   aws configure
   ```
   Preencha com sua Access Key, Secret Key, região e formato de saída. As credenciais ficam salvas localmente (~/.aws/credentials) e NÃO devem ser incluídas no código.

2. **Salve o script**
   - O script está no arquivo `listar_recursos.py`.

3. **Instale as dependências**
   ```sh
   pip install boto3
   ```

4. **Execute o script**
   ```sh
   python listar_recursos.py
   ```

## Segurança
- **NUNCA** inclua suas chaves de acesso (aws_access_key_id, aws_secret_access_key) no código ou em repositórios.
- Use sempre o `aws configure` para gerenciar credenciais.

---
Este projeto não armazena nem exibe dados sensíveis. Use com responsabilidade.

