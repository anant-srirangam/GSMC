from django.shortcuts import render,get_object_or_404,redirect
from .models import Listing
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from datetime import datetime
from urllib.parse import urlparse
from .choices import *

def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return redirect('index')
    # listings = Listing.objects.order_by('-list_date').filter(is_listed=True)

    # paginator = Paginator(listings, 6)
    # page = request.GET.get('page')
    # paged_listings = paginator.get_page(page)

    # context = {
    #     'listings': paged_listings
    # }
    # return render(request, 'listings/listings.html', context)


def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id, is_listed=True)
    
    if 'HTTP_REFERER' in request.META:
        linkUrl = request.META['HTTP_REFERER']
    else:
        if request.user.is_authenticated:
            linkUrl = reverse('dashboard')
        else:
            linkUrl = reverse('index')
    context = {
        'listing': listing,
        'linkUrl': linkUrl,
        'time':datetime.now()
    }
    return render(request, 'listings/job_listing.html', context)


def search(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    print(urlparse(request.build_absolute_uri()))
    listings = Listing.objects.order_by('-list_date').filter(is_listed=True)
    
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            listings = listings.filter(description__icontains=keywords)

    if 'company' in request.GET:
        keywords = request.GET['company']
        if keywords and keywords != 'Company (All)':
            listings = listings.filter(employer__profile__company=keywords)

    if 'jobTitle' in request.GET:
        keywords = request.GET['jobTitle']
        if keywords and keywords != "Job Title (All)":
            listings = listings.filter(jobTitle__iexact=keywords)

    if 'minExp' in request.GET:
        keywords = request.GET['minExp']
        if keywords and keywords != "Min Exp (All)":
            listings = listings.filter(minExp__gte=keywords)

    if 'maxExp' in request.GET:
        keywords = request.GET['maxExp']
        if keywords and keywords != "Max Exp (All)":
            listings = listings.filter(maxExp__lte=keywords)


   
    paginator = Paginator(listings, 2)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context = {
        'listings': paged_listings,
        'minExpList': getMinExpList(),
        'maxExpList': getMaxExpList(),
        'companyList': getCompanyList(),
        'jobTitleList':getJobTitleList(),
        'values': request.GET
    }

    return render(request, 'listings/search.html', context)


def newJob(request):
    if not request.user.is_authenticated :
        return redirect('index')

    if request.user.username == 'admin':
        return redirect('adminDashboard')
    
    company = request.user.profile.company.companyName.split(' ')[0][:3]
    now = datetime.now()

    context = {
            'min_experience': min_experience(),
            'max_experience': max_experience(),
            'gmcsJobId': f"{request.user.id}_{company.upper()}{now.year}{now.month}{now.day}"
        }
    return render(request, 'listings/new_job.html', context)
    


def removedListing(request, listing_id):
    if request.user.is_authenticated:
        listing = get_object_or_404(Listing, pk=listing_id)

        context = {
            'listing':listing
        }
        return render(request, 'listings/removed_listing.html', context)
    else:
        return redirect('index')


def listingAction(request, listing_id):
    if request.method == 'POST':
        listing = Listing.objects.get(pk=listing_id)
        listing.removeDate = datetime.now()
        listing.removedBy = 'user'
        listing.is_listed = False
        listing.save()

        user = User.objects.get(pk=request.user.id)

        user.profile.livePosts = user.profile.livePosts-1
        
        user.save()
        
        messages.success(request, 'Listing successfully archived...')
        return redirect(request.POST['linkUrl'])
    else:
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return redirect('index')


def addJob(request):
    if request.method != 'POST':
        return get_object_or_404(User, pk=0)

    gmcsJobId = request.POST['gmcsJobId']
    jobId = request.POST['JobId']
    jobTitle = request.POST['JobTitle']
    location = request.POST['Location']
    minExp = request.POST['min_experience']
    maxExp = request.POST['max_experience']
    salary = request.POST['Salary']
    jobDesc = request.POST['JobDescription']

    description = jobDesc + f"\n\n {jobTitle} | {minExp} years | {maxExp} years | {location} | {salary}"

    if minExp>maxExp or maxExp == 0:
        messages.error(request, 'Invalid maximum experience')
        return redirect('newJob')

    employer = User.objects.get(pk=request.user.id)
    listing = Listing.objects.create(employer=employer,
                                    gmcsJobId=gmcsJobId,
                                    jobId=jobId,
                                    jobTitle=jobTitle,
                                    location=location,
                                    minExp=minExp,
                                    maxExp=maxExp,
                                    salary=salary,
                                    jobDesc=jobDesc,
                                    description=description)
    listing.gmcsJobId = f"{gmcsJobId}{listing.id}"
    listing.save()

    user = User.objects.get(pk=request.user.id)

    user.profile.posts = user.profile.posts+1
    user.profile.livePosts = user.profile.livePosts+1

    user.save()
    messages.success(request, 'Job listing made live')
    return redirect('dashboard')