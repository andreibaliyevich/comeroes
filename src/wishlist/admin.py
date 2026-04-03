from django.contrib import admin
from .models import Wish


class WishAdmin(admin.ModelAdmin):
    """ Wish Model for admin """
    list_display = ('id', 'user', 'product', 'created_at')
    list_filter = ('user', 'product')
    readonly_fields = ('created_at',)


admin.site.register(Wish, WishAdmin)
