# Generated by Django 3.0.5 on 2020-05-03 09:05

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20200503_1331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminactions',
            name='actionDate',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 5, 3, 14, 35, 11, 708324)),
        ),
        migrations.AlterField(
            model_name='profile',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.CompanyMaster'),
        ),
    ]
