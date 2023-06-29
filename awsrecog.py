## Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)

# Code has been imported from "https://docs.aws.amazon.com/rekognition/latest/dg/celebrities-video-sqs.html" 
# Start and follow steps from "https://docs.aws.amazon.com/rekognition/latest/dg/video-analyzing-with-sqs.html"


import boto3
import json
import sys
import time


class VideoDetect:

    jobId = ''

    roleArn = 'arn:aws:iam::119703509010:role/movsseservice' #This role ARN is my AWS role unique arn 
    bucket = 'movsse' # Amazon S3 bucket name that I created to store my data.
    video = ''
    startJobId = ''

    # We have to create a sqs queue and give the URL over here. 
    sqsQueueUrl = 'https://sqs.ap-south-1.amazonaws.com/119703509010/MOVSSE'

    # We also have to create a sns topic and give the URL here. 
    snsTopicArn = 'arn:aws:sns:ap-south-1:119703509010:AmazonRekognitionMOVSSE'
    processType = ''

    def __init__(self, role, bucket, video, client, rek, sqs, sns):
        self.roleArn = role
        self.bucket = bucket
        self.video = video
        self.client = client
        self.rek = rek
        self.sqs = sqs
        self.sns = sns

    def GetSQSMessageSuccess(self):

        jobFound = False
        succeeded = False

        dotLine = 0
        while jobFound == False:
            sqsResponse = self.sqs.receive_message(QueueUrl=self.sqsQueueUrl, MessageAttributeNames=['ALL'],
                                                   MaxNumberOfMessages=10)

            if sqsResponse:

                if 'Messages' not in sqsResponse:
                    if dotLine < 40:
                        print('.', end='')
                        dotLine = dotLine + 1
                    else:
                        print()
                        dotLine = 0
                    sys.stdout.flush()
                    time.sleep(5)
                    continue

                for message in sqsResponse['Messages']:
                    notification = json.loads(message['Body'])
                    rekMessage = json.loads(notification['Message'])
                    print(rekMessage['JobId'])
                    print(rekMessage['Status'])
                    if rekMessage['JobId'] == self.startJobId:
                        print('Matching Job Found:' + rekMessage['JobId'])
                        jobFound = True
                        if (rekMessage['Status'] == 'SUCCEEDED'):
                            succeeded = True

                        self.sqs.delete_message(QueueUrl=self.sqsQueueUrl,
                                                ReceiptHandle=message['ReceiptHandle'])
                    else:
                        print("Job didn't match:" +
                              str(rekMessage['JobId']) + ' : ' + self.startJobId)
                    # Delete the unknown message. Consider sending to dead letter queue
                    self.sqs.delete_message(QueueUrl=self.sqsQueueUrl,
                                            ReceiptHandle=message['ReceiptHandle'])

        return succeeded

    def StartLabelDetection(self):
        response = self.rek.start_label_detection(Video={'S3Object': {'Bucket': self.bucket, 'Name': self.video}},
                                                  NotificationChannel={'RoleArn': self.roleArn,
                                                                       'SNSTopicArn': self.snsTopicArn},
                                                  MinConfidence=90,
                                                  # Filtration options, uncomment and add desired labels to filter returned labels
                                                  # Features=['GENERAL_LABELS'],
                                                  # Settings={
                                                  # 'GeneralLabels': {
                                                  # 'LabelInclusionFilters': ['Clothing']
                                                  # }}
                                                   )

        self.startJobId = response['JobId']
        print('Start Job Id: ' + self.startJobId)

    def GetLabelDetectionResults(self):
        maxResults = 1000
        paginationToken = ''
        finished = False

        while finished == False:
            response = self.rek.get_label_detection(JobId=self.startJobId,
                                                    MaxResults=maxResults,
                                                    NextToken=paginationToken,
                                                    SortBy='TIMESTAMP')

            print('Codec: ' + response['VideoMetadata']['Codec'])
            print('Duration: ' + str(response['VideoMetadata']['DurationMillis']))
            print('Format: ' + response['VideoMetadata']['Format'])
            print('Frame rate: ' + str(response['VideoMetadata']['FrameRate']))
            print()

            for labelDetection in response['Labels']:
                label = labelDetection['Label']

                print("Timestamp: " + str(labelDetection['Timestamp']))
                print("   Label: " + label['Name'])
                print("   Confidence: " + str(label['Confidence']))
                print("   Instances:")
                for instance in label['Instances']:
                    print("      Confidence: " + str(instance['Confidence']))
                    print("      Bounding box")
                    print("        Top: " + str(instance['BoundingBox']['Top']))
                    print("        Left: " + str(instance['BoundingBox']['Left']))
                    print("        Width: " + str(instance['BoundingBox']['Width']))
                    print("        Height: " + str(instance['BoundingBox']['Height']))
                    print()
                print()

                print("Parents:")
                for parent in label['Parents']:
                    print("   " + parent['Name'])

                print("Aliases:")
                for alias in label['Aliases']:
                    print("   " + alias['Name'])

                print("Categories:")
                for category in label['Categories']:
                    print("   " + category['Name'])
                print("----------")
                print()

                if 'NextToken' in response:
                    paginationToken = response['NextToken']
                else:
                    finished = True

    def CreateTopicandQueue(self):

        millis = str(int(round(time.time() * 1000)))

        # Create SNS topic

        snsTopicName = "AmazonRekognitionExample" + millis

        topicResponse = self.sns.create_topic(Name=snsTopicName)
        self.snsTopicArn = topicResponse['TopicArn']

        # create SQS queue
        sqsQueueName = "AmazonRekognitionQueue" + millis
        self.sqs.create_queue(QueueName=sqsQueueName)
        self.sqsQueueUrl = self.sqs.get_queue_url(QueueName=sqsQueueName)['QueueUrl']

        attribs = self.sqs.get_queue_attributes(QueueUrl=self.sqsQueueUrl,
                                                AttributeNames=['QueueArn'])['Attributes']

        sqsQueueArn = attribs['QueueArn']

        # Subscribe SQS queue to SNS topic
        self.sns.subscribe(
            TopicArn=self.snsTopicArn,
            Protocol='sqs',
            Endpoint=sqsQueueArn)

        # Authorize SNS to write SQS queue
        policy = """{{
  "Version":"2012-10-17",
  "Statement":[
    {{
      "Sid":"MyPolicy",
      "Effect":"Allow",
      "Principal" : {{"AWS" : "*"}},
      "Action":"SQS:SendMessage",
      "Resource": "{}",
      "Condition":{{
        "ArnEquals":{{
          "aws:SourceArn": "{}"
        }}
      }}
    }}
  ]
}}""".format(sqsQueueArn, self.snsTopicArn)

        response = self.sqs.set_queue_attributes(
            QueueUrl=self.sqsQueueUrl,
            Attributes={
                'Policy': policy
            })

    def DeleteTopicandQueue(self):
        self.sqs.delete_queue(QueueUrl=self.sqsQueueUrl)
        self.sns.delete_topic(TopicArn=self.snsTopicArn)

    # ============== Celebrities ===============
    def StartCelebrityDetection(self):
        response=self.rek.start_celebrity_recognition(Video={'S3Object': {'Bucket': self.bucket, 'Name': self.video}},
            NotificationChannel={'RoleArn': self.roleArn, 'SNSTopicArn': self.snsTopicArn})

        self.startJobId=response['JobId']
        print('Start Job Id: ' + self.startJobId)

    def GetCelebrityDetectionResults(self,no):
        print('enetered'+str(no))
        maxResults = 1000
        paginationToken = ''
        finished = False
        celebs = []
        urls = []
        while finished == False:
            response = self.rek.get_celebrity_recognition(JobId=self.startJobId,
                                                    MaxResults=maxResults,
                                                    NextToken=paginationToken)

            # print(response['VideoMetadata']['Codec'])
            # print(str(response['VideoMetadata']['DurationMillis']))
            # print(response['VideoMetadata']['Format'])
            # print(response['VideoMetadata']['FrameRate'])
            
            for celebrityRecognition in response['Celebrities']:

                if celebrityRecognition['Celebrity']['Confidence'] > 96:

                    if str(celebrityRecognition['Celebrity']['Name']) not in celebs:
                        celebs.append(str(celebrityRecognition['Celebrity']['Name']))
                        urls.append(str(celebrityRecognition['Celebrity']['Urls']))
                    print('Celebrity: ' +
                        str(celebrityRecognition['Celebrity']['Name']) + ' Confidence: ' + str(celebrityRecognition['Celebrity']['Confidence']))
                    print('URLS: ' +str(celebrityRecognition['Celebrity']['Urls']))
                    print('Timestamp: ' + str(celebrityRecognition['Timestamp']/1000)+'seconds')
                    print()
            


            if 'NextToken' in response:
                paginationToken = response['NextToken']
            else:
                finished = True

        print(celebs)
        number = no+1
        file = open('celebs_'+str(number)+'.txt','w+')
        for idx,celeb in enumerate(celebs):
            file.write(celeb+"\n")
            file.write(urls[idx] + "\n")

        file.close()
def main():
    
    roleArn = 'arn:aws:iam::119703509010:role/movsseservice' # AWS Role ARN
    bucket = 'movsse' # S3 bucket name
    
    i = 0

    while(i<9):

        # Video names that you want to perform facial recognition
        if i==0:
            video = 'Salt_Trim.mp4' 
        else:
            video = 'Salt_Trim'+str(i)+'.mp4'
            
        session = boto3.Session(profile_name='default')
        client = session.client('rekognition')
        rek = boto3.client('rekognition')
        sqs = boto3.client('sqs')
        sns = boto3.client('sns')

        analyzer = VideoDetect(roleArn, bucket, video, client, rek, sqs, sns)
        analyzer.CreateTopicandQueue()

        analyzer.StartCelebrityDetection()
        if analyzer.GetSQSMessageSuccess() == True:
            analyzer.GetCelebrityDetectionResults(i)

        analyzer.DeleteTopicandQueue()
        i=i+1

if __name__ == "__main__":
    main()