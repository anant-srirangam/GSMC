# Generated by Django 3.0.5 on 2020-05-04 12:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_auto_20200504_1742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminactions',
            name='actionDate',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 5, 4, 17, 52, 19, 424131)),
        ),
    ]