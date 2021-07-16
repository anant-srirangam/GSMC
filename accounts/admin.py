from django.contrib import admin
from .models import Profile, CompanyMaster, AdminActions


class AccountsAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'user',
                    'workEmail',
                    'user_verified',
                    'admin_verified',
                    'action',
                    'request_for')
    list_display_links = ('id',
                        'user',
                        'workEmail')
    list_filter = ('user_verified','admin_verified','user','workEmail','phone')
    search_fields = ('workEmail','phone','designation')
    list_per_page = 25

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'companyName',
                    'companyURL',
                    'companyLogo')
    list_display_links = ('id',
                    'companyName',
                    'companyURL',
                    'companyLogo')
    search_fields = ('companyName','companyURL')
    list_per_page = 25

class AdminActionsAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'username',
                    'requestFor',
                    'adminReqAction',
                    'actionDate')
    list_display_links = ('id',
                    'username',)
    list_filter = ('requestFor','adminReqAction','actionDate')
    search_fields = ('username',)
    list_per_page = 25

admin.site.register(AdminActions, AdminActionsAdmin)
admin.site.register(CompanyMaster, CompanyAdmin)
admin.site.register(Profile, AccountsAdmin)