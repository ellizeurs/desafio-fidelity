import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

NADA_CONSTA = 'Não existem informações disponíveis para os parâmetros informados.'
CONSTA01 = 'Processos encontrados'
CONSTA02 = 'Audiências'
FILTRO = 0
EXECUTAVEL = 'C:/Users/teste/OneDrive/Documentos/'

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')