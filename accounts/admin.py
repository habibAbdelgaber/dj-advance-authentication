from django.contrib import admin
from django.contrib.auth.admin import  UserAdmin
from .models import Account

class AccountAdmin(UserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'username', 'date_joined', 'is_active']
    list_filter = ()
    fieldsets = ()
    filter_horizontal = ()

    list_display_links = ['email', 'first_name', 'last_name', 'username']

    ordering = ('-date_joined',)

    readonly_fields = ('date_joined', 'last_login')

admin.site.register(Account, AccountAdmin)
