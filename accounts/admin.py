from django.contrib import admin
from .models import Profile


class AccountsAdmin(admin.ModelAdmin):
    list_display = ('workEmail',)

admin.site.register(Profile, AccountsAdmin)