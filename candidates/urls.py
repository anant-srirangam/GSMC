from django.urls import path
from . import views


urlpatterns = [
    path('apply/<int:listing_id>', views.applyListing, name='applyListing')
]