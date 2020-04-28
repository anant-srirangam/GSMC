from django.shortcuts import render
from listings.models import Listing
from realtors.models import Realtor
from listings import choices
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger

def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_listed=True)

    paginator = Paginator(listings, 20)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context = {
        'listings': paged_listings
    }

    context = {
        'listings': paged_listings,
        'state_choices': choices.states,
        'bedroom_choices': choices.bedrooms,
        'price_choices': choices.prices
    }
    return render(request, 'pages/index.html', context)


def about(request):
    realtors = Realtor.objects.order_by('hire_date')
    mvp_realtors = Realtor.objects.all().filter(is_mvp=True)
    context = {
        'realtors': realtors,
        'mvpRealtors': mvp_realtors
    }
    return render(request, 'pages/about.html', context)
