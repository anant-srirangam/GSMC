from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from realtors.models import Realtor


class Listing(models.Model):
    employer = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    gmcsJobId = models.CharField(max_length=20)
    jobId = models.CharField(max_length=20, blank=True, null=True)
    jobTitle = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    minExp = models.IntegerField(default=0)
    maxExp = models.IntegerField(default=0)
    salary = models.IntegerField(blank=True, null=True)
    jobDesc = models.TextField()
    description = models.TextField()
    is_listed = models.BooleanField(default=True)
    noOfApplies = models.IntegerField(blank=True, default=0)
    shortLists = models.IntegerField(blank=True, default=0)
    selections = models.IntegerField(blank=True, default=0)
    list_date = models.DateTimeField(default=datetime.now, blank=True)
    removeDate = models.DateTimeField(default=datetime.now, blank=True)
    removedBy = models.CharField(default='admin', blank=True, max_length=10)

