# Generated by Django 3.0.5 on 2020-05-04 12:01

import candidates.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidates', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidateactions',
            name='resume',
            field=models.FileField(null=True, upload_to=candidates.models.user_directory_path),
        ),
    ]