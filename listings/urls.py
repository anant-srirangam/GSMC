from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='listings'),
    path('<int:listing_id>', views.listing, name='listing'),
    path('search', views.search, name='searchListing'),
    path('search', views.search, name='searchListing'),
    path('NewJob', views.newJob, name='newJob'),
    path('listingAction', views.listingAction, name='listingAction'), 
    path('removedListings/<int:listing_id>', views.removedListing, name='removedListing')
]