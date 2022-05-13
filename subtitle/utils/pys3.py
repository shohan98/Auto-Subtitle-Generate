import boto3
from botocore.exceptions import ClientError
import moviepy.editor as mp
from django.conf import settings
class Awss3:
    def __init__(self, region_name=settings.AWS_REGION, 
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_ACCESS_KEY):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region_name = region_name
        if self.aws_secret_access_key==None or self.aws_access_key_id==None:
            self.s3 =  boto3.client(
                        's3',
                )
        else:
            self.s3 =  boto3.client(
                                's3',
                                aws_access_key_id=self.aws_access_key_id,
                                aws_secret_access_key=self.aws_secret_access_key,
                                region_name = self.region_name
                        )
        
# =============================================================================
#         
# =============================================================================
    def s3_bucketlist(self):
        buckets = self.s3.list_buckets()
        bucket_list = []
        for bucket in buckets['Buckets']:
            bucket_list.append(bucket["Name"])
        return bucket_list
    
# =============================================================================
#     
# =============================================================================
    def create_bucket(self, bucket_name):
        """Create an S3 bucket in a specified region

        If a region is not specified, the bucket is created in the S3 default
        region (ap-southeast-1).
    
        :param bucket_name: Bucket to create
        :param region: String region to create bucket in, e.g., 'us-west-2'
        :return: True if bucket created, else False
        """
    
        # Create bucket
        try:
            location = {'LocationConstraint': self.region_name}
            self.s3.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
        except ClientError as e:
            return e
        return bucket_name
# =============================================================================
#     
# =============================================================================
    
    def video2audio(self, FileLocation, AudioFIleName, AudioFileFormat='wav', AudioFileLocation=''):
        try:
            clip = mp.VideoFileClip(FileLocation)
            audio_file = AudioFileLocation + AudioFIleName + '.' + AudioFileFormat
            clip.audio.write_audiofile(audio_file)
            return {'status':'Audio write Successfully.', 'filename':audio_file}
        except:
            return {'status':'Audio write failed. Please check your video file.', 'filename':''}
       
# =============================================================================
#         
# =============================================================================
    def upload_file(self, FileLocation, FIleName, Bucket=settings.S3_BUCKET):
        try:
            extension = FileLocation.split('.')[-1]
        except:
            return {'status':'File extension is not right', 'json_file':'','filename': FileLocation, 's3_url':'', 's3_region':''}
        try :
            NewFile = FIleName + '.' + extension
            self.s3.upload_file(FileLocation, Bucket, NewFile)
            return {'status':'S3 Upload Success', 'filename': NewFile, 
                    's3_url':'s3://'+Bucket+'/'+ NewFile, 's3_region':self.region_name}
        except:
            
            return {'status':'S3 Upload Failed', 'json_file':'','filename': NewFile, 's3_url':'', 's3_region':''}
      
# =============================================================================
#     
# =============================================================================
    def delete_bucket(self, ExpectedBucketOwner='', Bucket=settings.S3_BUCKET):
        try:
            self.s3.delete_bucket(
            Bucket=Bucket,
            ExpectedBucketOwner=ExpectedBucketOwner
            )
            return True
        except ClientError as e:
            return e
    
        
    def file_list(self, bucket_name):
        files = []
        s3_client = boto3.Session(
                    aws_access_key_id=self.aws_access_key_id,
                    aws_secret_access_key=self.aws_secret_access_key,
                    region_name = self.region_name,
                    )

        s3 = s3_client.resource('s3')

        content = s3.Bucket(bucket_name)
        for my_bucket_object in content.objects.all():
            files.append(my_bucket_object.key)
        return files

    def download__file(self, file_name, bucket_name):
        s3_client = boto3.client(
                    's3',
                    aws_access_key_id=self.aws_access_key_id,
                    aws_secret_access_key=self.aws_secret_access_key,
                    region_name = self.region_name,
                    )
        s3_client.download_file(bucket_name, file_name, file_name)
