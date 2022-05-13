from .pytranscrib import Transcrib
from .pysubtitle import Subtitle
from django.conf import settings
from subtitle.models import MediaFiles
import os

def start_transcribe(bucket, region, s3_url, ln):
	transcrib = Transcrib(bucket, region)
	response = transcrib.transcribjob(s3_url, ln)
	return response
        
def check_job_status(job_name):
	t = Transcrib()
	res = t.getTranscriptionJobStatus(job_name)
	if res['TranscriptionJob']['TranscriptionJobStatus']=='COMPLETED':
		data = MediaFiles.objects.get(job_name=job_name)
		if not os.path.exists(os.path.join(settings.BASE_DIR, 'media')):
			os.mkdir(os.path.join(settings.BASE_DIR, 'media'))

		if not os.path.exists(os.path.join(settings.BASE_DIR, 'media', data.file_id)):
			os.mkdir(os.path.join(settings.BASE_DIR, 'media', data.file_id))

		if not data.json_file:
			json_file = t.getTranscript(data.object_name, res['TranscriptionJob']['Transcript']['TranscriptFileUri'], os.path.join(settings.BASE_DIR, 'media', data.file_id, '/'))
			res['json_file']=json_file
			if json_file['status']:
				data.json_file = json_file['jsonfile'].split('media/')[-1]
		# if not data.subtitle_file:
		sub = Subtitle(data.json_file.path)
		print(settings.BASE_DIR)
		subtitle_file = sub.subtitle(data.object_name, 'srt', str(settings.BASE_DIR)+'/media/'+data.file_id+'/')
		res['subtitle_file']=subtitle_file
		if subtitle_file['status']:
			data.subtitle_file=subtitle_file['srt_file'].split('media/')[-1]
		
		data.save()

	return res

