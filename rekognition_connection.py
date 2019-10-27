from time import sleep

from botocore.exceptions import NoCredentialsError
from rootkey import chaves_acesso
import boto3


class Rekognition:
    def __init__(self):
        self.keys = chaves_acesso()
        self.client = boto3.client('rekognition', aws_access_key_id=self.keys[0], aws_secret_access_key=self.keys[1],
                                   region_name='us-east-1')
        self.s3 = boto3.client('s3', aws_access_key_id=self.keys[0], aws_secret_access_key=self.keys[1],
                               region_name='us-east-1')
        self.topicArn = "arn:aws:sns:us-east-1:704853567767:video-teste"
        self.roleArn = "arn:aws:iam::704853567767:role/serviceRekognition"
        self.queueUrl = "https://sqs.us-east-1.amazonaws.com/704853567767/rekognitionQueue"

    def rekog_labels(self, src_img):  # Pega informações das imagens Ex: Homem, Sorrindo, Idade 30-40 anos, etc...
        response = self.client.detect_labels(
            Image={
                'S3Object': {
                    'Bucket': 'source-faces',
                    'Name': src_img}},

            MaxLabels=10
        )
        return response

    def rekog_matchfaces(self, src_img, trg_img):  # Compara Imagens
        response = self.client.compare_faces(
            SourceImage={
                'S3Object': {
                    'Bucket': 'source-faces',
                    'Name': src_img}},

            TargetImage={
                'S3Object': {
                    'Bucket': 'target-faces',
                    'Name': trg_img
                }
            },
        )
        return response

    def rekog_text(self, id_img):  # Pega o texto das imagens
        response = self.client.detect_text(
            Image={
                'S3Object': {
                    'Bucket': 'family-access-grant',
                    'Name': id_img
                }
            }
        )
        return response

    def upload(self, foto_idoso, nome_idoso, flag, foto_parente='sem foto', nome_parente="sem parente"):
        if flag == 'pessoa_perdida':
            try:
                self.client.upload_file(foto_idoso, 'source-faces', nome_idoso)
                self.client.upload_file(foto_parente, 'family-access-grant', nome_parente)
                return 'Upload com sucesso'

            except FileNotFoundError:
                return "Arquivo nao encontrado"

            except NoCredentialsError:
                return "Credenciais inválida"

        if flag == 'cad_pessoa':
            try:
                self.client.upload_file(foto_idoso, 'target-source', nome_idoso)
                return 'upload com sucesso'

            except FileNotFoundError:
                return "Arquivo nao encontrado"

            except NoCredentialsError:
                return "Credenciais inválida"

    def video_face_rekog(self):
        #for key in self.s3.list_objects(Bucket='video-bucket-teste')['Contents']:
         #   foto_target = key['Key']
          #  print(foto_target)

        response = self.client.start_face_detection(
            Video={
                'S3Object': {
                    'Bucket': 'source-faces',
                    'Name': 'video1.mp4'
                }},
            NotificationChannel={
                'SNSTopicArn': self.topicArn,
                'RoleArn': self.roleArn
            })
        print(response)

        return response

    def face_detect(self, JobId):
        face_detect = self.client.get_face_detection(
            JobId=JobId,
            MaxResults=10
        )
        return face_detect