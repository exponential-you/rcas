import csv
import boto3
import json
import argparse

class Label:

    def __init__(self, bucket, photo):   
        self.bucket = bucket
        self.photo = photo

    def GetClient(self):
        with open ('credentials.csv', 'r') as input:
            next(input)
            reader = csv.reader(input)
            for line in reader:
                access_key_id = line[2]
                secret_access_key = line[3] 

        client = boto3.client('rekognition',
                aws_access_key_id = access_key_id,
                aws_secret_access_key = secret_access_key)
        return client

    def DetectLabel(self):
        client = self.GetClient()

        response = client.detect_labels(Image={'S3Object':{'Bucket':self.bucket,'Name':self.photo}})

        print('Detected labels for ' + self.photo)    
        for label in response['Labels']:
            print (label['Name'] + ' : ' + str(label['Confidence']))
            print (label['Parents']) 

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-b", "--bucket", type=str, required=True,
        help="S3 bucket name")
    ap.add_argument("-p", "--photo", type=str, required=True,
        help="Photo")
    args = vars(ap.parse_args())

    obj = Label(args['bucket'], args['photo'])

    obj.DetectLabel()


if __name__ == "__main__":
    main()    