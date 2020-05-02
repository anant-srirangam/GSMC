from django.shortcuts import render,get_object_or_404,redirect
from .models import Listing
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from django.urls import reverse
from . import choices
from django.contrib import messages
from django.contrib.auth.models import User
from datetime import datetime

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
        'linkUrl': linkUrl
    }
    return render(request, 'listings/job_listing.html', context)


def search(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    listings = Listing.objects.order_by('-list_date').filter(is_listed=True)
    
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            listings = listings.filter(description__icontains=keywords)

    if 'city' in request.GET:
        keywords = request.GET['city']
        if keywords:
            listings = listings.filter(city__iexact=keywords)

    if 'state' in request.GET:
        keywords = request.GET['state']
        if keywords and keywords != "State (Any)":
            listings = listings.filter(state__iexact=keywords)

    if 'bedrooms' in request.GET:
        keywords = request.GET['bedrooms']
        if keywords and keywords != "Bedrooms (Any)":
            listings = listings.filter(bedrooms__iexact=keywords)

    if 'price' in request.GET:
        keywords = request.GET['price']
        if keywords and keywords != "Max Price (Any)":
            listings = listings.filter(price__lte=keywords)

   
    paginator = Paginator(listings, 3)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    
    context = {
        'listings': paged_listings,
        'state_choices': choices.states,
        'bedroom_choices': choices.bedrooms,
        'price_choices': choices.prices,
        'values': request.GET
    }


    return render(request, 'listings/search.html', context)


def newJob(request):
    if not request.user.is_authenticated :
        return redirect('index')

    if request.user.username == 'admin':
        return redirect('adminDashboard')
    
    company = request.user.profile.companyName.split(' ')[0][:3]
    now = datetime.now()

    context = {
            'min_experience': choices.min_experience(),
            'max_experience': choices.max_experience(),
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
    fileTypes = [
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/pdf'
    ]
    if request.method == 'POST':
        if request.POST['requestType'] == 'apply':
            resume = request.FILES['resume']
            if resume.content_type not in fileTypes:
                messages.error(request, 'Invalid file type')
                return redirect('listing',7)
            if resume.size/1024 > 20:
                messages.error(request, 'file too big')
                return redirect('listing',7)
            messages.success(request, 'Successfully applied...')
            return redirect('listing',7)
        elif request.POST['requestType'] == 'remove':
            listing = Listing.objects.get(pk=listing_id)
            listing.removeDate = datetime.now()
            listing.removedBy = 'user'
            listing.is_listed = False
            listing.save()
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

    messages.success(request, 'Post request sent for admin approval')
    return redirect('dashboard')