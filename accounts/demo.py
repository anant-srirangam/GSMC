
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.files.storage import FileSystemStorage
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from listings.models import Listing
from .models import user_directory_path_profile, AdminActions, CompanyMaster, Profile
from datetime import datetime
import imghdr
import os
import hashlib

def sendEmail():
    email_subject = 'Account Activation Link'
    message = render_to_string('accounts/activate_account.html', {
                'user': 'Anant',
                'domain': 'localhost:8000',
                'uid': 12345,
                'token': 'test',
            })
    to_email = 'annukumar07@gmail.com)'
    email = EmailMessage(email_subject, message, to=[to_email])
    email.send()

sendEmail()