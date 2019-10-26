from rootkey import chaves_acesso
import boto3

keys = chaves_acesso()
#foto = 'paulo.jpg'

client = boto3.client('rekognition',aws_access_key_id=keys[0], aws_secret_access_key=keys[1], region_name='us-east-1')

#with open(foto, 'rb') as source_image:
  #  source_bytes = source_image.read()

#response = client.detect_labels(Image={'Bytes': source_bytes}, MaxLabels=10)

response = client.detect_labels(
    Image={
        'S3Object': {
            'Bucket': 'faces123151',
            'Name': '32643464_1722605897797514_2206263784434040832_n.jpg'}},

    MaxLabels=10,
)
print('')

response = client.compare_faces(
    SourceImage={
        'S3Object': {
            'Bucket': 'faces123151',
            'Name': '32643464_1722605897797514_2206263784434040832_n.jpg'
        }
    },
    TargetImage={
        'S3Object': {
            'Bucket': 'faces123151',
            'Name': 'paulo2.jpg',
        }
    },
)
print(response)
if not response['FaceMatches']:
    print('False')
else:
    faceMatch = response['FaceMatches']
    print('Deu Match \nSimilaridade: {}'.format(round(faceMatch[0]['Similarity'],3)))