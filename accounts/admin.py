from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ['first_name', 'last_name', 'email', 'username', 'last_login', 'date_joined']
    list_display_links = ['first_name', 'email']
    ordering = ['-date_joined']
    readonly_fields = ['date_joined', 'last_login']
    

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    
admin.site.register(Account, AccountAdmin)