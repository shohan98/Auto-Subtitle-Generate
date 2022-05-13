from xml.etree.ElementInclude import include
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AllMediaData, CheckJobStatus

r = DefaultRouter()

r.register('media-data', AllMediaData, basename='media_data')
urlpatterns = [
    path('check-job-status/', CheckJobStatus.as_view()),
    path('', include(r.urls))
]