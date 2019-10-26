from rootkey import chaves_acesso
import boto3


class Rekognition:
    def __init__(self):
        self.keys = chaves_acesso()
        self.client = boto3.client('rekognition', aws_access_key_id=self.keys[0], aws_secret_access_key=self.keys[1],
                                   region_name='us-east-1')

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
        return  response

    def rekog_text(self, id_img):  # Pega o texto das imagens
        response = self.client.detect_text(
            Image={
                'S3Object': {
                    'Bucket': 'family-acess-grant',
                    'Name': id_img
                }
            }
        )
        return response
