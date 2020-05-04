from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime

def user_directory_path_company(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    ext = filename.split('.')[-1]
    return 'CompanyMaster/user_{0}/logo.{1}'.format(instance.id, ext)


def user_directory_path_profile(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    ext = filename.split('.')[-1]
    return 'Employer/user_{0}/profile.{1}'.format(instance.user.id, ext)


class CompanyMaster(models.Model):
    companyName = models.CharField(max_length=200, blank=True, null=True)
    companyURL = models.TextField(max_length=2083, default=None, null=True)
    companyLogo = models.ImageField(upload_to=user_directory_path_company, default=None, null=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.BigIntegerField(blank=True, default=0)
    workEmail = models.CharField(max_length=50)
    company = models.ForeignKey(CompanyMaster, on_delete=models.DO_NOTHING, blank=True, null=True, default=0)
    designation = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    verificationToken = models.TextField(max_length=2083, blank=True)
    user_verified = models.BooleanField(default=False, blank=True)
    admin_verified = models.IntegerField(default=0, blank=True)
    action = models.CharField(max_length=30, default='newRequest')
    admin_comments = models.CharField(max_length=100, blank=True)
    profileImage = models.ImageField(upload_to=user_directory_path_profile)
    approvalDate = models.DateTimeField(blank=True,null=True)
    removeRequestDate = models.DateTimeField(blank=True,null=True)
    removeApprovalDate = models.DateTimeField(blank=True,null=True)
    request_for = models.CharField(max_length=20, blank=True,default="activation")
    posts = models.IntegerField(default=0, blank=True)
    livePosts = models.IntegerField(default=0, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class AdminActions(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    username = models.CharField(max_length=50)
    requestFor = models.CharField(max_length=20)
    adminReqAction = models.CharField(max_length=10)
    actionDate = models.DateTimeField(blank=True, default=datetime.now())
