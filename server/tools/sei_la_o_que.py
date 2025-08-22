# sei_la_o_que.py

from server.integrations.aws_loader import AWSLoader  # ou from server.aws_loader import AWSLoader

def main():
    print("🚀 Iniciando aplicação...\n")

    # --- Configuração ---
    loader = AWSLoader(
        region_name='us-east-2',
        # profile_name='seu-perfil'  # opcional
    )

    # --- 1. Informações da conta ---
    try:
        account = loader.get_account_info()
        print(f"✅ Logado na conta AWS: {account['account_id']}")
        print(f"👤 Usuário/Role: {account['arn']}\n")
    except Exception as e:
        print(f"❌ Falha ao obter conta: {e}")
        return

    # --- 2. Listar buckets S3 ---
    try:
        buckets = loader.list_s3_buckets()
        print(f"📦 Buckets S3 encontrados ({len(buckets)}):")
        for bucket in buckets:
            print(f"  - {bucket}")
    except Exception as e:
        print(f"❌ Erro ao listar buckets S3: {e}")

    # --- 3. Listar tabelas DynamoDB ---
    try:
        tables = loader.list_dynamodb_tables()
        print(f"\n📊 Tabelas DynamoDB encontradas ({len(tables)}):")
        for table in tables:
            print(f"  - {table}")
    except Exception as e:
        print(f"❌ Erro ao listar tabelas DynamoDB: {e}")

    # --- 4. Exemplo: usar cliente S3 ---
    try:
        s3 = loader.get_client('s3')
        response = s3.list_buckets()
        print(f"\n🌍 Conexão S3 bem-sucedida. Total de buckets: {len(response['Buckets'])}")
    except Exception as e:
        print(f"❌ Falha ao usar cliente S3: {e}")


if __name__ == "__main__":
    main()