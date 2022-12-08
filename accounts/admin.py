from django.contrib.auth.admin import UserAdmin, admin
from accounts.models import Account
from django.contrib import admin
from django.contrib.auth import get_user_model
from accounts.forms import AccountCreateForm


@admin.register(Account)
class AccountAdmin(UserAdmin):
    model = Account
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_active', 'last_login', 'date_joined',)
    list_display_links = list_display[:4]
    readonly_fields = ('last_login', 'date_joined',)
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    add_fieldsets = (
        *UserAdmin.add_fieldsets, (
            'Пользовательские поля', {
                'fields': (
                    'phone',
                )
            }
        )
    )
    fieldsets = (
        *UserAdmin.fieldsets, (
            'Пользовательские поля', {
                'fields': (
                    'phone',
                )
            }
        )
    )
