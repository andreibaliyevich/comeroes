from django.contrib.gis import admin
from django.utils.translation import gettext_lazy as _
from products.models import Warehouse
from .models import Store, StoreTranslation, StoreImage, ContactMessage


class StoreTranslationInline(admin.StackedInline):
    model = StoreTranslation
    extra = 0


class StoreImageInline(admin.TabularInline):
    model = StoreImage
    extra = 0


class WarehouseInline(admin.TabularInline):
    model = Warehouse
    extra = 0


class StoreAdmin(admin.OSMGeoAdmin):
    """ Store Model for admin """
    list_display = ('__str__', 'city', 'address', 'is_main')
    list_filter = ('city',)
    save_on_top = True
    fieldsets = (
        (None, {
            'fields': (
                ('city', 'address'),
                'location',
                'main_image',
                'is_main',
            )
        }),
        (_('Metadata'), {
            'fields': ('meta_description', 'meta_keywords'),
        }),
        (_('Contacts'), {
            'fields': (
                ('customers_phone', 'support_phone'),
                ('customers_email', 'support_email'),
            ),
        }),
        (_('Working hours'), {
            'fields': (
                ('time_weekdays_start', 'time_weekdays_end'),
                ('time_weekend_start', 'time_weekend_end'),
            ),
        }),
    )
    inlines = (StoreTranslationInline, StoreImageInline, WarehouseInline)


class ContactMessageAdmin(admin.ModelAdmin):
    """ Contact Message Model for admin """
    list_display = ('name', 'email', 'phone', 'created_at')
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('created_at',)


admin.site.register(Store, StoreAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
