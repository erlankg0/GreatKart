from django.contrib.auth.admin import UserAdmin, admin
from accounts.models import Account
from django.contrib import admin
from django.contrib.auth import get_user_model

user = get_user_model()

admin.site.register(user)

# @admin.register(Account)
# class AccountAdmin(UserAdmin):
#     list_display = ('email', 'username', 'first_name', 'last_name', 'is_active', 'last_login', 'date_joined',)
#     list_display_links = list_display[:4]
#     readonly_fields = ('last_login', 'date_joined',)
#     ordering = ('-date_joined',)
#     filter_horizontal = ()
#     list_filter = ()
#     fieldsets = ()
