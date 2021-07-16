from django.contrib import admin
from .models import Contact


class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 
                    'userType',
                    'name',
                    'email',
                    'phone',
                    'contact_date')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('userType','contact_date')
    list_per_page = 25

admin.site.register(Contact, ContactAdmin)