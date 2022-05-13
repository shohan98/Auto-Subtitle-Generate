from django.db import models
from .s3_objects import MediaFiles
class TranslateFile(models.Model):
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

    media_file = models.ForeignKey(MediaFiles, on_delete=models.CASCADE)
    translate_language = models.CharField(max_length = 20, choices=LANGUAGE_CHOICES)
    status_note         = models.CharField(max_length=200, default='Translate Data Save')
    translated_json_file = models.FileField(null=True, blank=True)
    translated_subtitle_file = models.FileField(null=True, blank=True)
    translate_complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):

        return self.media_file.object_name
