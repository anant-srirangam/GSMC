# Generated by Django 3.0.5 on 2020-05-04 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidates', '0003_auto_20200504_1742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='noOfApplies',
            field=models.IntegerField(blank=True, default=1),
        ),
    ]
