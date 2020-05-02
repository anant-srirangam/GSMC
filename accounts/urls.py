from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='accountsIndex'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('admin/dashboard', views.adminDashboard, name='adminDashboard'),
    path('admin/dashboard/approvedRequests', views.adminApproved, name='adminApproved'),
    path('admin/dashboard/approvedRequests/removals', views.remRequestsApproved, name='remRequestsApproved'),
    path('admin/dashboard/rejectedRequests', views.adminRejected, name='adminRejected'),
    path('admin/dashboard/rejectedRequests/removals', views.remRequestsRejected, name='remRequestsRejected'),
    path('admin/dashboard/removalRequests', views.remRequestsAdminDashboard, name='remRequestsAdminDashboard'),
    path('admin/dashboard/dashboardAction/<int:user_id>/<str:linkUrl>', views.adminAction, name='adminAction'),
    path('dashboard/active', views.dashboard, name='dashboardActive'),
    path('dashboard/removed', views.dashboard_removed, name='dashboardRemoved'),
    path('profile', views.profile, name='profile'),
    path('adminProfileView/<int:user_id>/<str:linkUrl>', views.adminProfileView, name='adminProfileView'),
    path('login/forgotPassword', views.forgotPassword, name='forgotPassword'),
    path('changeProfile', views.changeProfile, name='changeProfile'),
    path('deactivate', views.deactivate, name='deactivate'),
    path('admin/dashboard/newReq', views.getNewAddReq, name='getNewReq'),
    path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate')
]