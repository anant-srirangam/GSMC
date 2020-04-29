from django.shortcuts import render,get_object_or_404,redirect
from .models import Listing
from realtors.models import Realtor
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from . import choices
from django.contrib import messages

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
    listing = get_object_or_404(Listing, pk=listing_id)
    realtor = Realtor.objects.get(name=listing.realtor)
    context = {
        'listing': listing,
        'realtor': realtor
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
    if not request.user.is_authenticated:
        return redirect('index')
    if not request.method == 'POST':
        return redirect('dashboard')
    
    if request.POST['formParam']=='0':
        context = {
            'min_experience': choices.min_experience(),
            'max_experience': choices.max_experience()
        }
        return render(request, 'listings/new_job.html', context)
    else:
        messages.success(request, 'Job reuest submitted. You will be notified once admin approves the post')
        return redirect('dashboard')



def removedListing(request, listing_id):
    if request.user.is_authenticated:
        if request.method=='POST':
            return render(request, 'listings/removed_listing.html')
        else:
            return redirect('dashboard')
    else:
        return redirect('index')


def listingAction(request):
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
            messages.success(request, 'Listing successfully archived...')
            return redirect('dashboard')
    else:
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return redirect('index')

