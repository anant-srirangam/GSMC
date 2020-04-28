from django.shortcuts import render,get_object_or_404
from .models import Listing
from realtors.models import Realtor
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from . import choices

def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_listed=True)

    paginator = Paginator(listings, 6)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context = {
        'listings': paged_listings
    }
    return render(request, 'listings/listings.html', context)


def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    realtor = Realtor.objects.get(name=listing.realtor)
    context = {
        'listing': listing,
        'realtor': realtor
    }
    return render(request, 'listings/listing.html', context)


def search(request):
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
