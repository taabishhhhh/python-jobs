from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import format_html

from .models import *


class CoreUserAdmin(UserAdmin):
    list_display = (
        'id', 'login_as', 'email', 'date_joined',
        'last_login', 'is_staff', 'is_active', 'password'
    )
    list_filter = (
        'is_staff', 'is_superuser', 'is_active', 'groups',
        ('date_joined', DateRangeFilter),
        ('last_login', DateRangeFilter),
    )
    search_fields = (
        'id', 'username', 'email', 'date_joined',
        'last_login', 'is_staff', 'is_active', 'password'
    )
    ordering = ('-id',)

    def login_as(self, obj):
        return format_html(
            '<a href="%s" target="_blank">%s</a>' % (
                reverse('impersonate-start', args=[obj.id]), obj.username)
        )

    login_as.allow_tags = True
    login_as.short_description = 'Login as'
    login_as.admin_order_field = 'username'


admin.site.unregister(User)
admin.site.register(User, CoreUserAdmin)
