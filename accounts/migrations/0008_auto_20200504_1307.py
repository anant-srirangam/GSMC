# Generated by Django 3.0.5 on 2020-05-04 07:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20200503_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminactions',
            name='actionDate',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 5, 4, 13, 7, 30, 32329)),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.BigIntegerField(blank=True, default=0),
        ),
    ]
