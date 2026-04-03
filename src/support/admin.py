from django.contrib import admin
from .models import Ticket, Message


class MessageInline(admin.TabularInline):
    """ Message in line for TicketAdmin """
    model = Message
    extra = 0


class TicketAdmin(admin.ModelAdmin):
    """ Ticket Model for admin """
    list_display = ('__str__', 'category', 'priority', 'status')
    list_filter = ('category', 'priority', 'status')
    readonly_fields = ('created_at', 'updated_at')
    inlines = (MessageInline,)


admin.site.register(Ticket, TicketAdmin)
