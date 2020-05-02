# Generated by Django 3.0.5 on 2020-05-01 12:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='removeDate',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='listing',
            name='remvedBy',
            field=models.CharField(blank=True, default='admin', max_length=10),
        ),
        migrations.AlterField(
            model_name='listing',
            name='is_listed',
            field=models.BooleanField(default=True),
        ),
    ]
