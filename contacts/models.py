from django.db import models
from datetime import datetime

class Contact(models.Model):
    userType = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    message = models.TextField(blank=True)
    contact_date = models.DateTimeField(default=datetime.now)
    def __str__(self):
        return self.name