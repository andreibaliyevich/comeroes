from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Subscriber, Newsletter


def send_newsletters(modeladmin, request, queryset):
    """ Send Newsletters for admin """
    for newsletter in queryset:
        newsletter.send()
    modeladmin.message_user(request, _('Newsletters sent to all subscribers'))
send_newsletters.short_description = _('Send selected Newsletters to all subscribers')


class SubscriberAdmin(admin.ModelAdmin):
    """ Subscriber Model for admin """
    list_display = ('email', 'confirmed')
    list_filter = ('confirmed',)


class NewsletterAdmin(admin.ModelAdmin):
    """ Newsletter Model for admin """
    list_display = ('__str__', 'created_at', 'updated_at')
    actions = (send_newsletters,)


admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(Newsletter, NewsletterAdmin)
