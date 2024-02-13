# Projeto de Engenharia de Dados com Python na Infraestrutura AWS

Este projeto é uma demonstração de engenharia de dados utilizando Python e serviços da Amazon Web Services (AWS). Ele consiste em uma série de scripts que automatizam tarefas comuns na configuração e gerenciamento de infraestrutura na AWS, além de interagir com um banco de dados PostgreSQL e uma API FastAPI.

## Pré-requisitos

- Python 3.x
- Conta na AWS com credenciais de acesso e permissões adequadas
- Ambiente de desenvolvimento com as bibliotecas listadas no arquivo `requirements.txt`

## Estrutura de Diretórios

O projeto está estruturado da seguinte forma:

projeto-engenharia-dados/  
│  
├── infrastructure.py  
├── api.py 
├── actions.py  
├── .env  
├── imagens/  
│   ├── imagem1.jpg  
│   ├── imagem2.jpg  
│   ├── ...  
│   └── imagem10.jpg  
├── requirements.txt  
└── README.md  

- **`infrastructure.py`**: Script para configurar a infraestrutura na AWS, incluindo a criação de buckets no S3 e instâncias RDS.
- **`api.py`**: Script que define uma API utilizando o framework FastAPI para enviar imagens para o S3.
- **`actions.py`**: Script principal que interage com a API e o S3, além de inserir dados em um banco de dados PostgreSQL.
- **`.env`**: Arquivo de configuração das variáveis de ambiente, incluindo credenciais da AWS e configurações do banco de dados.
- **`imagens/`**: Pasta contendo as imagens a serem enviadas para o S3.
- **`requirements.txt`**: Arquivo contendo as dependências do projeto.
- **`README.md`**: Documentação do projeto com instruções de instalação, configuração e uso.

## Configuração

1. Clone o repositório:

git clone https://github.com/seu-usuario/data_engineer_python_project.git
cd data_engineer_python_project


2. Crie e ative um ambiente virtual:

python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass # Windows
..venv\Scripts\activate # Windows
source .venv/bin/activate # Linux/Mac


3. Instale as dependências:

pip install -r requirements.txt


4. Configure as variáveis de ambiente no arquivo `.env` conforme necessário.

## Uso

1. Inicie o servidor da API:

uvicorn api:app --log-level debug

2. Execute o script `actions.py` para interagir com a API e inserir dados no banco de dados.

3. Verifique os resultados no banco de dados PostgreSQL.

## Tecnologias Utilizadas

- Python
- AWS (S3, RDS)
- FastAPI
- PostgreSQL

Este projeto visa demonstrar uma aplicação prática de engenharia de dados na nuvem utilizando tecnologias populares e de fácil integração. Se você tiver alguma dúvida ou sugestão, não hesite em entrar em contato!
