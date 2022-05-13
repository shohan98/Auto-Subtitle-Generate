from dataclasses import field
from rest_framework.serializers import ModelSerializer, ValidationError
from subtitle.models import MediaFiles
from subtitle.utils.transcrib_action import start_transcribe


class MediaFileSerializer(ModelSerializer):
    class Meta: 
        model = MediaFiles
        fields = '__all__'

    def create(self, validate_data):

        param ={
            'region_name': validate_data.pop('region_name'),
            'bucket_name': validate_data.pop('bucket_name'),
            'object_name': validate_data.pop('object_name'),
            'file_id'    : validate_data.pop('file_id'),
            'language'   : validate_data.pop('language'),
        }
        if MediaFiles.objects.filter(object_name=param['object_name']).exists():
            raise ValidationError({'details': 'This Object is already exists.'})
        try:
            data = MediaFiles.objects.create(**param)
            data.save()
            try:
                s3_url = 'https://'+data.bucket_name+'.s3.'+data.region_name+'.amazonaws.com/'+data.object_name
                res = start_transcribe(data.bucket_name, data.region_name, s3_url, data.language)
                if res['TranscriptionJob']['TranscriptionJobName']!= 'FAILED':
                    data.status_note = 'Transcrib process start successfully.'
                    data.job_name = res['TranscriptionJob']['TranscriptionJobName']
                    data.save()
            except Exception as e:
                res={'msg': str(e)}
            return data
        except Exception as e:
            raise ValidationError({'details': str(e)})