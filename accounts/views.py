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
from .models import user_directory_path_profile, AdminActions
from datetime import datetime
import imghdr
import os
import hashlib



def _make_hash_value(user):
        token = str(user.pk)+str(datetime.now())+str(user.is_active)
        # return token.replace('-','').replace(' ','').replace(':','').replace('.','')
        sha = hashlib.sha256()
        sha.update(token.encode())
        return sha.hexdigest()


def index(request):
    return redirect('login')


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        #regiter user
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['email']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        phone = request.POST['phone']
        workEmail = request.POST['email']
        companyName = request.POST['companyName']
        companyURL = request.POST['companyUrl']
        designation = request.POST['designation']
        location = request.POST['location']
        companyLogo = request.FILES['companyLogo']
        profileImage = request.FILES['profileImage']

        if password != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
        # if User.objects.filter(username=username,profile__admin_verified__in=[0,1] ).exists():
        #     messages.error(request, 'Username already exists')
            return redirect('register') 
        elif User.objects.filter(email=email, profile__admin_verified__in=[0,1]).exists():
            messages.error(request, 'Email already exists')
            return redirect('register') 
        elif imghdr.what(profileImage) is None:
            messages.error(request, 'Profile image file type improper')
            return redirect('register') 
        elif imghdr.what(companyLogo) is None:
            messages.error(request, 'Company logo file type improper')
            return redirect('register') 
        elif profileImage.size/1024 > 500:
            messages.error(request, 'Profile image file too big')
            return redirect('register') 
        elif companyLogo.size/1024 > 100:
            messages.error(request, 'Company logo file too big')
            return redirect('register') 
        else:
            user = User.objects.create_user(username=f"{username}__email",
                                            password=password,
                                            first_name=first_name,
                                            last_name=last_name,
                                            email=email,
                                            is_active=False)
            user.profile.phone = phone
            user.profile.workEmail = workEmail
            user.profile.companyName = companyName
            user.profile.companyURL = companyURL
            user.profile.designation = designation
            user.profile.location = location
            user.profile.companyLogo = companyLogo
            user.profile.profileImage = profileImage
            
            token = _make_hash_value(user)
            domain = get_current_site(request).domain
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            sendEmail(user=user, uid=uid, token=token, domain=domain)

            user.profile.verificationToken = token
            user.save()
            messages.success(request, 'Verification link has been sent to your registered mail. Please verify your account for login.')
            return redirect('index')
        
    else:
        return render(request, 'accounts/register.html')


def login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,
                                password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Logged in successfully')
            return redirect('dashboard')
        else:
            messages.error(request, 'Inavlid Credentials')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    if not request.user.is_authenticated:
        return get_object_or_404(User, pk=0)
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'Successfully logged out')
        return redirect('index')
    else:
        return get_object_or_404(User, pk=0)



def dashboard(request):
    if not request.user.is_authenticated:
        return get_object_or_404(User, pk=0)
    elif request.user.username == 'admin':
        return redirect('adminDashboard')
    listings = Listing.objects.order_by('-list_date').filter(employer=request.user, is_listed=True)
    paginator = Paginator(listings, 2)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context={
        'listings': paged_listings
    }
    
    return render(request, 'accounts/dashboard.html', context)


def dashboard_removed(request):
    listings = Listing.objects.order_by('-list_date').filter(employer=request.user, is_listed=False)
    print(listings.values())
    paginator = Paginator(listings, 10)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context={
        'listings': paged_listings
    }
    
    return render(request, 'accounts/dashboard_removed.html', context)


def adminDashboard(request):
    if not request.user.is_authenticated or request.user.username != 'admin':
        return get_object_or_404(User, pk=0)
    

    requests = User.objects.order_by('-date_joined').select_related('profile').filter(profile__action='newRequest')
    
    paginator = Paginator(requests, 2)
    page = request.GET.get('page')
    paged_requests = paginator.get_page(page)

    context={
        'requests': paged_requests,
        'buttonid': 1,
        'linkUrl':'adminDashboard',
        'requestType': 'pending'
    }
    return render(request, 'accounts/admin_dashboard.html', context)



def remRequestsAdminDashboard(request):
    if not request.user.is_authenticated or request.user.username != 'admin':
        return get_object_or_404(User, pk=0)
    requests = User.objects.order_by('-date_joined').select_related('profile').filter(profile__action='remRequest')
    
    paginator = Paginator(requests, 2)
    page = request.GET.get('page')
    paged_requests = paginator.get_page(page)

    context={
        'requests': paged_requests,
        'buttonid': 2,
        'linkUrl':'remRequestsAdminDashboard',
        'requestType': 'pending'
    }
    return render(request, 'accounts/admin_dashboard.html', context)


def adminApproved(request):
    if not request.user.is_authenticated or request.user.username != 'admin':
        return get_object_or_404(User, pk=0)
    

    requests = AdminActions.objects.order_by('-actionDate').filter(adminReqAction='approved', requestFor='activation')
    print(requests.values())
    paginator = Paginator(requests, 2)
    page = request.GET.get('page')
    paged_requests = paginator.get_page(page)

    context={
        'requests': paged_requests,
        'buttonid': 1,
        'linkUrl':'adminApproved',
        'requestType': 'approved'
    }
    return render(request, 'accounts/admin_actions.html', context)


def remRequestsApproved(request):
    if not request.user.is_authenticated or request.user.username != 'admin':
        return get_object_or_404(User, pk=0)
    requests = AdminActions.objects.order_by('-actionDate').filter(adminReqAction='approved', requestFor='de-activation')
    
    paginator = Paginator(requests, 2)
    page = request.GET.get('page')
    paged_requests = paginator.get_page(page)

    context={
        'requests': paged_requests,
        'buttonid': 2,
        'linkUrl':'remRequestsApproved',
        'requestType': 'approved'
    }
    return render(request, 'accounts/admin_actions.html', context)

def adminRejected(request):
    if not request.user.is_authenticated or request.user.username != 'admin':
        return get_object_or_404(User, pk=0)
    

    requests = AdminActions.objects.order_by('-actionDate').filter(adminReqAction='rejected', requestFor='activation')
    print(requests.values())
    paginator = Paginator(requests, 2)
    page = request.GET.get('page')
    paged_requests = paginator.get_page(page)

    context={
        'requests': paged_requests,
        'buttonid': 1,
        'linkUrl':'adminRejected',
        'requestType': 'rejected'
    }
    return render(request, 'accounts/admin_actions.html', context)


def remRequestsRejected(request):
    if not request.user.is_authenticated or request.user.username != 'admin':
        return get_object_or_404(User, pk=0)
    requests = AdminActions.objects.order_by('-actionDate').filter(adminReqAction='rejected', requestFor='de-activation')
    
    paginator = Paginator(requests, 2)
    page = request.GET.get('page')
    paged_requests = paginator.get_page(page)

    context={
        'requests': paged_requests,
        'buttonid': 2,
        'linkUrl':'remRequestsApproved',
        'requestType': 'rejected'
    }
    return render(request, 'accounts/admin_actions.html', context)

def adminAction(request, user_id, linkUrl):
    if request.method == 'POST':
        requestType = request.POST['requestType']
        user = User.objects.get(pk=user_id)
        
        if user.profile.request_for == 'activation':
            if requestType == 'save':
                user.username = user.email
                user.profile.admin_comments = request.POST['saveComments']
                user.profile.admin_verified = 1
                user.profile.action = 'approved'
                user.profile.approvalDate = datetime.now()
                if user.profile.user_verified:
                    user.is_active=True
                user.save()
                AdminActions.objects.create(user_id=user,
                                            username=user.username,
                                            requestFor='activation',
                                            adminReqAction='approved')
                messages.success(request, 'User approved')
                return redirect(linkUrl)
            elif requestType == 'reject':
                user.username = f"{user.id}__rejected"
                user.profile.admin_comments = request.POST['rejectComments']
                user.profile.admin_verified = 2
                user.profile.action = 'rejected'
                user.save()
                
                AdminActions.objects.create(user_id=user,
                                            username=user.email,
                                            requestFor='activation',
                                            adminReqAction='rejected')
                messages.success(request, 'User rejected')
                return redirect(linkUrl)
        elif user.profile.request_for == 'de-activation':
            if requestType == 'save':
                user.username = f"{user.id}__User_Deactivated"
                user.profile.admin_comments = request.POST['saveComments']
                user.profile.admin_verified = 1
                user.profile.action = 'approved'
                user.profile.removeApprovalDate = datetime.now()
                user.is_active=False
                user.save()
                AdminActions.objects.create(user_id=user,
                                            username=user.email,
                                            requestFor='de-activation',
                                            adminReqAction='approved')
                messages.success(request, 'User de-activated')
                return redirect(linkUrl)
            elif requestType == 'reject':
                # user.username = f"{user.id}__rejected" ----- User still active - Removal rejected
                user.profile.admin_comments = request.POST['rejectComments']
                user.profile.admin_verified = 2
                user.profile.action = 'rejected'
                user.save()
                
                AdminActions.objects.create(user_id=user,
                                            username=user.username,
                                            requestFor='de-activation',
                                            adminReqAction='rejected')
                messages.success(request, 'Removal rejected')
                return redirect(linkUrl)
    else:
        return get_object_or_404(User, pk=0)

def profile(request):
    if not request.user.is_authenticated:
        return get_object_or_404(User, pk=0)
    
    context = {
        "employer": request.user,
        'linkUrl': 'dashboard'
    }
    return render(request, 'accounts/profile.html', context)


def adminProfileView(request, user_id, linkUrl):
    if not request.user.is_authenticated or request.user.username != 'admin':
        return get_object_or_404(User, pk=0)
    employer = get_object_or_404(User, pk=user_id)
        
    context = {
            'employer': employer,
            'linkUrl': linkUrl
        }

    return render(request, 'accounts/profile.html', context)


def forgotPassword(request):
    if request.method == 'POST':
        messages.success(request, 'Password re-set link has been sent to your registered email')
        return redirect('index')
    else:
        return redirect('index')


def changeProfile(request):
    if request.method == 'POST':
        print(request.FILES)
        profileImage = request.FILES['profileImage']
        
        if profileImage.size/1024 > 2048:
            messages.error(request, 'Profile image file too big')
            return redirect('profile')
        elif imghdr.what(profileImage) is None:
            messages.error(request, 'Improper file type')
            return redirect('profile')

        os.remove(request.user.profile.profileImage.path)
        
        request.user.profile.profileImage = profileImage
        request.user.save()

        messages.success(request, 'Request has been submitted. Pending with admin for approval');
        return redirect('profile')

    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return redirect('index')



def deactivate(request):
    if request.method == 'POST':
        #
        # return redirect('profile')
        user = User.objects.get(username=request.user.username)
        user.profile.removeRequestDate = datetime.now()
        user.profile.action = 'remRequest'
        user.profile.admin_verified = 0
        user.profile.request_for = 'de-activation'
        user.save()
        messages.success(request, 'Request has been submitted. Pending with admin for approval')
        # user.update(is_active=False)
        return redirect('profile')
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return redirect('index')
        


def sendEmail(user, uid, token, domain):
    email_subject = 'Account Activation Link'
    message = render_to_string('accounts/activate_account.html', {
                'user': user,
                'domain': domain,
                'uid': uid,
                'token': token,
            })
    to_email = user.email
    email = EmailMessage(email_subject, message, to=[to_email])
    email.send()


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and token == user.profile.verificationToken and not user.profile.user_verified:
        user.profile.user_verified = True
        user.save()
        if user.profile.admin_verified == 1:
            user.is_Active=True
            user.profile.action = "UserAdded"
            message = 'Account Verified.... Please login!!!!'
            loc = 'login'
        else:
            message = 'Account Verified.... Please wait while admin approves your account'
            loc = 'index'
        
        user.save
        
        messages.success(request, message)
        return redirect(loc)
    else:
        return get_object_or_404(User, pk=0)


def getNewAddReq(request):
    requests = User.objects.order_by('-date_joined').select_related('profile').filter(profile__action='newRequest')
    
    paginator = Paginator(requests, 2)
    page = request.GET.get('page')
    paged_requests = paginator.get_page(page)

    context={
        'requests': paged_requests,
        'buttonid': 1,
        'linkUrl':'adminDashboard',
        'requestType': 'pending'
    }
    return render(request, 'accounts/newReq.html', context)