import boto3
import datetime
from botocore.exceptions import ClientError
import requests
from django.conf import settings
    
class Transcrib:
    def __init__(self, Bucket=settings.S3_BUCKET, region_name=settings.AWS_REGION, 
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_ACCESS_KEY):

        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region_name = region_name
        self.bucket = Bucket
        self.now = datetime.datetime.now()
        self.timestamp = datetime.datetime.timestamp(self.now)
        if self.aws_secret_access_key==None or self.aws_access_key_id==None:
            self.transcribe =  boto3.client(
                        'transcribe',
                )
        else:
            self.transcribe = boto3.client(
                                'transcribe',
                                aws_access_key_id=self.aws_access_key_id,
                                aws_secret_access_key=self.aws_secret_access_key,
                                region_name = self.region_name
                        )
    def getTranscriptionJobStatus(self, jobName):
    
        response = self.transcribe.get_transcription_job( TranscriptionJobName=jobName )
        return response
    

    # purpose: get and return the transcript structure given the provided uri
    def getTranscript(self, FileName, transcriptURI , SaveJsonLocation=''):
        # Get the resulting Transcription Job and store the JSON response in transcript
        status = 1
        msg = ''
        jsonfile=''
        try:
            result = requests.get( transcriptURI )
            jsonfile = SaveJsonLocation+'{}.json'.format(FileName)
            create_json = open(jsonfile,'w')
            create_json.write(result.text)
        except Exception as e:
            status = 0
            msg = str(e)
        return {'status': status, 'msg':msg, 'jsonfile' :jsonfile}  
    
    
    def transcribjob(self, S3MediaURL, language, ShowSpeakerLabels=True, MaxSpeakerLabels=10, ChannelIdentification=False):
        
        # Set up the full uri for the bucket and media file
        self.File = S3MediaURL.split('/')[-1].split('.')
        self.job_name = self.File[0]+str(self.timestamp)
        # Use the uuid functionality to generate a unique job name.  Otherwise, the Transcribe service will return an error
        response = self.transcribe.start_transcription_job(
            TranscriptionJobName=self.job_name,
            Media={'MediaFileUri': S3MediaURL},
            MediaFormat=self.File[-1],
            LanguageCode=language,
            Settings={
                'ShowSpeakerLabels': ShowSpeakerLabels,
                'MaxSpeakerLabels': MaxSpeakerLabels,
                'ChannelIdentification': ChannelIdentification
            }
        
        )
        
        # jsonfile = self.getTranscript(res['TranscriptionJob']['Transcript']['TranscriptFileUri'])
        # return the response structure found in the Transcribe Documentation
        return response
    
    

    
    
