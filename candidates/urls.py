from django.urls import path
from . import views


urlpatterns = [
    path('apply/<int:listing_id>', views.applyListing, name='applyListing'),
    path('admin/dashboard', views.adminDashboard, name='candidateAdminDashboard'),
    path('admin/dashboard/shortlisted', views.candidateShortlist, name='candidateShortlist'),
    path('admin/dashboard/selected', views.candidateSelect, name='candidateSelect'),
    path('admin/dashboard/rejected', views.candidateReject, name='candidateReject'),
    path('admin/dashboard/candidateListing/<int:listing_id>/<int:action_id>/<str:status>', views.candidateListing, name='candidateListing'),
    path('admin/dashboard/shortListCandidate/<int:action_id>', views.shortListCandidate, name='shortListCandidate'),
    path('admin/dashboard/selectCandidate/<int:action_id>', views.selectCandidate, name='selectCandidate'),
    path('admin/dashboard/rejectCandidate/<int:action_id>', views.rejectCandidate, name='rejectCandidate'),
    path('admin/dashboard/blackListCandidate/<int:action_id>', views.blackListCandidate, name='blackListCandidate'),
    path('admin/dashboard/candidateLeft/<int:action_id>', views.candidateLeft, name='candidateLeft'),
    path('admin/dashboard/search/<str:requestType>', views.searchCandidate, name='searchCandidate')
    
]