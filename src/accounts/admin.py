from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import OSUser, Address


class AddressInline(admin.TabularInline):
    model = Address


class OSUserAdmin(admin.ModelAdmin):
    """ Advanced User Model for admin """
    list_display = (
        'email',
        'last_visit',
        'last_login',
        'date_joined',
    )
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_subscription', 'is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {
            'fields': ('email',),
        }),
        (_('Personal info'), {
            'fields': (
                ('first_name', 'last_name'),
                'avatar',
                'phone',
                'date_of_birth',
                'is_subscription',
            ),
        }),
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            ),
        }),
        (_('Important dates'), {
            'fields': ('last_visit', 'last_login', 'date_joined'),
        }),
    )
    filter_horizontal = ('groups', 'user_permissions')
    readonly_fields = ('last_visit', 'last_login', 'date_joined')
    inlines = (AddressInline,)


admin.site.register(OSUser, OSUserAdmin)
