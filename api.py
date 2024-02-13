import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import boto3
import time

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém as credenciais de acesso da AWS do arquivo .env
ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
REGION = os.getenv('AWS_REGION')
BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
S3_DIRECTORY_NAME = os.getenv('S3_DIRECTORY_NAME')

# Inicializa o cliente S3
s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, region_name=REGION)

# Caminho da pasta onde as imagens estão localizadas
pasta_imagens_local = './imagens/'

# Lista de imagens na pasta
imagens = [f for f in os.listdir(pasta_imagens_local) if os.path.isfile(os.path.join(pasta_imagens_local, f))]

# Inicializa o aplicativo FastAPI
app = FastAPI()

def upload_imagem(imagem):
    try:
        # Faz o upload da imagem para o S3 dentro da pasta 'imagens'
        nome_pasta_s3 = S3_DIRECTORY_NAME
        s3.upload_file(os.path.join(pasta_imagens_local, imagem), BUCKET_NAME, nome_pasta_s3 + imagem)
        print(f'Imagem "{imagem}" enviada com sucesso para o S3.')
        return JSONResponse(content={"message": f"Imagem '{imagem}' enviada com sucesso para o S3."}, status_code=200)
    except Exception as e:
        print(f'Ocorreu um erro ao enviar a imagem para o S3: {e}')
        return JSONResponse(content={"message": f"Erro ao enviar a imagem '{imagem}' para o S3."}, status_code=500)

@app.post('/enviar-imagem')
async def enviar_imagem():
    for imagem in imagens:
        upload_imagem(imagem)
        # Espera 15 segundos antes de enviar a próxima imagem
        time.sleep(5)
    return JSONResponse(content={"message": "Todas as imagens foram enviadas com sucesso."}, status_code=200)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)