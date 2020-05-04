from django.shortcuts import render,redirect
from listings.models import Listing
from realtors.models import Realtor
from accounts.models import CompanyMaster
from listings.choices import *
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger


def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    listings = Listing.objects.order_by('-list_date').filter(is_listed=True)

    paginator = Paginator(listings, 2)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context = {
        'listings': paged_listings,
        'minExpList': getMinExpList(),
        'maxExpList': getMaxExpList(),
        'companyList': getCompanyList(),
        'jobTitleList':getJobTitleList()
    }
    return render(request, 'pages/index.html', context)


def about(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    realtors = Realtor.objects.order_by('hire_date')
    mvp_realtors = Realtor.objects.all().filter(is_mvp=True)
    context = {
        'realtors': realtors,
        'mvpRealtors': mvp_realtors
    }
    return render(request, 'pages/about.html', context)
