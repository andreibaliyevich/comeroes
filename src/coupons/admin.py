from django.contrib import admin
from .models import Coupon


class CouponAdmin(admin.ModelAdmin):
    """ Coupon Model for admin """
    list_display = ('code', 'valid_from', 'valid_to', 'discount', 'is_active')
    list_filter = ('discount', 'is_active')
    search_fields = ('code',)


admin.site.register(Coupon, CouponAdmin)
