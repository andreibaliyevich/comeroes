from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    """ Order Model for admin """
    list_display = ('id', 'status', 'created_at', 'updated_at')
    list_filter = ('status',)
    readonly_fields = ('created_at', 'updated_at')
    inlines = (OrderItemInline,)


admin.site.register(Order, OrderAdmin)

