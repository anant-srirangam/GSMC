# Generated by Django 3.0.5 on 2020-05-04 08:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0003_auto_20200501_1821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='list_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 5, 4, 14, 10, 49, 635618)),
        ),
        migrations.AlterField(
            model_name='listing',
            name='removeDate',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 5, 4, 14, 10, 49, 635618)),
        ),
    ]
