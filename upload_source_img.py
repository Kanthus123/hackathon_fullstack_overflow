import csv
import boto3 
import config

ACCESS_KEY_ID = config.config['access_key_id']
SECRET_ACCESS_KEY = config.config['secret_access_key']


#foto = 'felipe_oculos.jpg'

def upload(foto):
    s3 = boto3.client('s3', 
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=SECRET_ACCESS_KEY,
        region_name='us-east-1')

    try:
        s3.upload_file(foto, 'face-lab-source', 'foto')
        print('upload com sucesso')
        return True
    except FileNotFoundError:
        print("Arquivo nao encontrado")
        return False
    except NoCredentialsError:
        print("Credenciais invalida")
        return False