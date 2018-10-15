from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.utils.translation import gettext, gettext_lazy as _

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = [
        'username',
        'full_name',
        'original',
        'bio',
    ]
    list_display = [
        'username',
        'date_joined',
        'is_staff'
    ]

