import boto3
from dotenv import load_dotenv
import os
from api import *  # Importa o módulo 'api'

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém as credenciais de acesso da AWS do arquivo .env
ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
REGION = os.getenv('AWS_REGION')
BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
DB_INSTANCE_IDENTIFIER = os.getenv('DB_INSTANCE_IDENTIFIER')
DB_NAME = os.getenv('DB_NAME') 
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_SG = os.getenv('DB_SG')

# Verifica se as credenciais foram carregadas corretamente
if not all([ACCESS_KEY, SECRET_KEY, REGION, BUCKET_NAME]):
    raise ValueError("Alguma(s) credencial(ais) não foi(foram) encontrada(s).")

# Inicializa o cliente S3
try:
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, region_name=REGION)
    print("Cliente S3 inicializado com sucesso!")
except Exception as e:
    print("Erro ao inicializar o cliente S3:", e)

# Inicializa o cliente RDS
try:
    rds_client = boto3.client('rds', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, region_name=REGION)
    print("Cliente RDS inicializado com sucesso!")
except Exception as e:
    print("Erro ao inicializar o cliente RDS:", e)

def criar_bucket(bucket_name):
    try:
        # Verifica se o bucket já existe
        response = s3.list_buckets()
        existing_buckets = [bucket['Name'] for bucket in response['Buckets']]
        if bucket_name not in existing_buckets:
            # O bucket não existe, então cria o bucket
            s3.create_bucket(Bucket=bucket_name)
            print(f'Bucket "{bucket_name}" criado com sucesso!')
        else:
            print(f'O bucket "{bucket_name}" já existe.')
    except Exception as e:
        print(f'Ocorreu um erro ao criar o bucket: {e}')

def criar_pasta(bucket_name, pasta_nome):
    try:
        # Verifica se a pasta já existe
        response = s3.list_objects(Bucket=bucket_name, Prefix=pasta_nome)
        if 'Contents' not in response:
            # A pasta não existe, então cria a pasta
            s3.put_object(Bucket=bucket_name, Key=f"{pasta_nome}/")
            print(f'Pasta "{pasta_nome}" criada com sucesso dentro do bucket "{bucket_name}".')
        else:
            print(f'A pasta "{pasta_nome}" já existe dentro do bucket "{bucket_name}".')
    except Exception as e:
        print(f'Ocorreu um erro ao criar a pasta: {e}')

def create_rds_instance(db_instance_identifier, db_name, db_username, db_password, db_instance_class='db.t3.micro'):
    # Crie uma conexão com o serviço RDS
    rds_client = boto3.client('rds')
    
    # Configurações para o banco de dados
    db_instance_settings = {
        'DBInstanceIdentifier': DB_INSTANCE_IDENTIFIER,  # Identificador único para a instância do banco de dados
        'DBName': DB_NAME,  # Nome do banco de dados a ser criado
        'Engine': 'postgres',  # Tipo de motor de banco de dados (PostgreSQL)
        'DBInstanceClass': db_instance_class,  # Classe de instância do banco de dados (tamanho da instância)
        'MasterUsername': DB_USERNAME,  # Nome de usuário mestre para o banco de dados
        'MasterUserPassword': DB_PASSWORD,  # Senha do usuário mestre para o banco de dados
        'AllocatedStorage': 20,  # Espaço de armazenamento alocado para a instância do banco de dados (em GB)
        'BackupRetentionPeriod': 0,  # Período de retenção de backup em dias (0 para desativar o backup automático)
        'MultiAZ': False,  # Indica se a instância do banco de dados é de alta disponibilidade multi-zona
        'StorageType': 'gp2',  # Tipo de armazenamento (SSD)
        'EngineVersion': '15.5',  # Versão do PostgreSQL
        'PubliclyAccessible': True,  # Define se a instância do banco de dados pode ser acessada publicamente
        'EnablePerformanceInsights': False,  # Indica se o monitoramento do Performance Insights está habilitado (False para desativar)
        'VpcSecurityGroupIds': [DB_SG]  # Substitua pelo ID do seu novo grupo de segurança da VPC
    }
    
    # Cria a instância RDS
    response = rds_client.create_db_instance(**db_instance_settings)
    
    return response

# Testando a criação do bucket
criar_bucket(BUCKET_NAME)

# Testando a criação da pasta
criar_pasta(BUCKET_NAME, 'imagens')

# Chame a função para criar a instância RDS
response = create_rds_instance(DB_INSTANCE_IDENTIFIER, DB_NAME, DB_USERNAME, DB_PASSWORD)

# Exiba o resultado da criação da instância RDS
print("instância RDS criada com sucesso!")
