from django.contrib import admin
from .models import MediaFiles, TranslateFile

class CustomMediaFilesAdmin(admin.ModelAdmin):
    list_display = ('file_id', 'bucket_name', 'region_name', 'object_name', 'language', 'created_at', 'updated_at', 'subtitle_complete')
    search_fields = ('file_id', 'bucket_name', 'region_name', 'object_name', 'language', 'created_at', 'updated_at', 'subtitle_complete')

admin.site.register(MediaFiles, CustomMediaFilesAdmin)

class CustomTranslateFileAdmin(admin.ModelAdmin):
    list_display = ('media_file', 'translate_language', 'created_at', 'updated_at', 'translate_complete')
    search_fields = ('media_file', 'translate_language', 'created_at', 'updated_at', 'translate_complete')

admin.site.register(TranslateFile, CustomTranslateFileAdmin)

