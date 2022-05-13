from rest_framework.response import Response as RestResponse
from rest_framework import  viewsets, views 
from subtitle.models import MediaFiles
from subtitle.serializers import MediaFileSerializer

from subtitle.utils.transcrib_action import check_job_status

class AllMediaData(viewsets.ModelViewSet):
    serializer_class  = MediaFileSerializer
    queryset = MediaFiles.objects.all()

    
class CheckJobStatus(views.APIView):
    def get_object(self):
        file_id = self.request.data.get('file_id')
        try:
            q = MediaFiles.objects.get(file_id=file_id)
            return q
        except MediaFiles.DoesNotExist:
            return None

    def post(self, request):
        q = self.get_object()
        if q:
            res = check_job_status(q.job_name)
            status = 1
        else:
            res = 'No file found!'
            status = 0
        return RestResponse({'status': status,'JobStatus': res})

    def get(self, request):
        return RestResponse({'msg': 'Hello Everyone!'})
    