# Generated by Django 3.0.5 on 2020-04-30 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_profile_action'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='admin_comments',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]