from django.db import models

class MediaFiles(models.Model):
    LANGUAGE_CHOICES = (
        ('ar-SA', 'ar-SA'),
        ('de-DE', 'de-DE'),
        ('en-US', 'en-US'),
        ('ko-KR', 'ko-KR'),
        ('pt-BR', 'pt-BR'),
        ('en-IN', 'en-IN'),
        ('es-ES', 'es-ES'),
        ('zh-CN', 'zh-CN'),
        ('fr-CA', 'fr-CA'),
        ('it-IT', 'it-IT'),
        ('ru-RU', 'ru-RU'),
        ('hi-IN', 'hi-IN'),
        ('es-US', 'es-US'),
        ('en-AU', 'en-AU'),
        ('en-UK', 'en-UK'),
        ('fr-FR', 'fr-FR'),
        ('en-GB', 'en-GB'),
        ('ja-JP', 'ja-JP'),
        
    )
    
    bucket_name         = models.CharField(max_length=50)
    region_name         = models.CharField(max_length=20)
    object_name         = models.CharField(max_length=100)
    file_id             = models.CharField(max_length=20, unique=True)
    status_note         = models.CharField(max_length=200, default='Data Save')
    language            = models.CharField(max_length = 20, choices=LANGUAGE_CHOICES)
    job_name            = models.CharField(max_length=100, blank=True, null=True)
    json_file           = models.FileField(null=True, blank=True)
    subtitle_file       = models.FileField(null=True, blank=True)
    subtitle_complete   = models.BooleanField(default=False)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Media File'


    def __str__(self):
        return self.object_name
