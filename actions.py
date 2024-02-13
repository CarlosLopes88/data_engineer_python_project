import requests
from dotenv import load_dotenv
import boto3
import psycopg2
import os

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém as credenciais de acesso da AWS e do banco de dados do arquivo .env
ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
REGION = os.getenv('AWS_REGION')
BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
S3_DIRECTORY_NAME = os.getenv('S3_DIRECTORY_NAME')
DB_INSTANCE_IDENTIFIER = os.getenv('DB_INSTANCE_IDENTIFIER')
DB_NAME = os.getenv('DB_NAME')
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# Chama a API para enviar as imagens para o S3
url_fastapi = 'http://127.0.0.1:8000/enviar-imagem'
response = requests.post(url_fastapi)

# Verificar se a solicitação foi bem-sucedida
if response.status_code == 200:
    print("Envio de imagens concluído com sucesso!")
else:
    print("Erro ao enviar imagens:", response.text)

# Inicializa o cliente S3
s3 = boto3.resource(service_name='s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, region_name=REGION)

# Leitura dos objetos do bucket
for object_s3 in s3.Bucket(BUCKET_NAME).objects.filter(Prefix=S3_DIRECTORY_NAME):
    if object_s3.key.endswith('jpg') or object_s3.key.endswith('JPG'):
        filename = os.path.basename(object_s3.key).replace('.jpg', '').replace('.JPG', '')  # Remove a extensão .jpg do nome do arquivo
        print(f'Imagem encontrada: {filename}') # Aqui você pode salvar o ID da imagem (filename) e o nome da imagem em uma lista ou em uma estrutura de dados que você preferir

# Verifica se as credenciais foram carregadas corretamente
if not all([ACCESS_KEY, SECRET_KEY, REGION]):
    raise ValueError("Alguma(s) credencial(ais) não foi(foram) encontrada(s).")

# Inicializa o cliente RDS
try:
    rds_client = boto3.client('rds', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, region_name=REGION)
    print("Cliente RDS inicializado com sucesso!")
except Exception as e:
    print("Erro ao inicializar o cliente RDS:", e)

def get_rds_instance_host(db_instance_identifier):
    try:
        # Obtém informações sobre a instância RDS
        response = rds_client.describe_db_instances(DBInstanceIdentifier=DB_INSTANCE_IDENTIFIER)
        if 'DBInstances' in response and response['DBInstances']:
            # A instância RDS foi encontrada, então retorna o host
            return response['DBInstances'][0]['Endpoint']['Address']
        else:
            print(f"Não foi possível encontrar a instância RDS com o identificador '{DB_INSTANCE_IDENTIFIER}'.")
            return None
    except Exception as e:
        print(f"Erro ao obter o host da instância RDS '{DB_INSTANCE_IDENTIFIER}':", e)
        return None

# Captura o host da instância RDS
HOST = get_rds_instance_host(DB_INSTANCE_IDENTIFIER)
if HOST:
    print(f"Host da instância RDS '{DB_INSTANCE_IDENTIFIER}': {HOST}")
else:
    print("Falha ao obter o host da instância RDS.")

# Constrói a string de conexão com o banco de dados
connection_string = f"dbname='{DB_NAME}' user='{DB_USERNAME}' host='{HOST}' password='{DB_PASSWORD}'"

try:
    # Conecta ao banco de dados
    connection = psycopg2.connect(connection_string)
    print("Conexão com o banco de dados estabelecida com sucesso!")

    # Cria uma tabela para armazenar os dados das imagens
    create_table_query = """
    CREATE TABLE IF NOT EXISTS public.imagens (
        id SERIAL PRIMARY KEY,
        image_name VARCHAR(255) NOT NULL
    );
    """
    cursor = connection.cursor()
    cursor.execute(create_table_query)
    connection.commit()
    print("Tabela 'imagens' criada com sucesso!")

    # Insere os dados das imagens na tabela
    for object_s3 in s3.Bucket(BUCKET_NAME).objects.filter(Prefix=S3_DIRECTORY_NAME):
        if object_s3.key.endswith('jpg') or object_s3.key.endswith('JPG'):
            image_id = os.path.basename(object_s3.key).replace('.jpg', '').replace('.JPG', '')
            image_name = os.path.basename(object_s3.key)
            insert_query = "INSERT INTO imagens (image_name) VALUES (%s)"
            cursor.execute(insert_query, (image_name,))
            connection.commit()
            print(f"Dados da imagem '{image_name}' inseridos na tabela 'imagens'.")

    # Consulta para verificar se os dados foram salvos com sucesso
    select_query = "SELECT * FROM imagens;"
    try:
        cursor.execute(select_query)
        records = cursor.fetchall()
        print("Registros na tabela 'imagens':")
        for row in records:
            print(row)
    except Exception as e:
        print("Erro ao executar consulta de seleção:", e)

    # Fecha a conexão
    cursor.close()
    connection.close()
    print("Conexão com o banco de dados fechada.")
except Exception as e:
    print("Erro ao conectar ao banco de dados:", e)
