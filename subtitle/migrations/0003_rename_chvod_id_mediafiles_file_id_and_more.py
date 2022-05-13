# Generated by Django 4.0.4 on 2022-04-17 08:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('subtitle', '0002_mediafiles_chvod_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mediafiles',
            old_name='chvod_id',
            new_name='file_id',
        ),
        migrations.AddField(
            model_name='mediafiles',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mediafiles',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='translatefile',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='translatefile',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]