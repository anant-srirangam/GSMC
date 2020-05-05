from django.db import models
from listings.models import Listing
from datetime import datetime


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    ext = filename.split('.')[-1]
    return f'Candidate/candidate_{instance.candidate.id}/listing_{instance.listing.id}/resume.{ext}'


class Candidate(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=50, unique=True)
    phone = models.BigIntegerField()
    blacklisted = models.BooleanField(default=False, blank=True)
    noOfApplies = models.IntegerField(default=1, blank=True)
    noOfOffers = models.IntegerField(default=0, blank=True)


class CandidateActions(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.DO_NOTHING)
    listing = models.ForeignKey(Listing, on_delete=models.DO_NOTHING)
    resume = models.FileField(upload_to=user_directory_path, null=True)
    applyDate = models.DateTimeField(default=datetime.now, blank=True)
    rejectDate = models.DateTimeField(null=True, blank=True)
    shortlistDate = models.DateTimeField(null=True, blank=True)
    selectionDate = models.DateTimeField(null=True, blank=True)
    workflowLevel = models.CharField(max_length=12, default='apply', blank=True)
