from django.contrib import admin
from .models import Listing


class ListingAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'is_listed',
                    'gsmcJobId',
                    'jobId',
                    'jobTitle',
                    'employer',
                    'location'
                    )
    list_display_links = ('id',
                        'gsmcJobId',
                        'jobId',)
    list_filter = ('gsmcJobId','employer','location','is_listed')
    list_editable = ('is_listed',)
    search_fields = ('gsmcJobId','jobTitle','location')
    list_per_page = 25

admin.site.register(Listing, ListingAdmin)

