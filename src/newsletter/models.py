from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import OSUser
from .utilities import get_newsletter_path, send_newsletter


class Subscriber(models.Model):
    """ Subscriber Model """
    email = models.EmailField(unique=True, verbose_name=_('Email address'))
    confirmed = models.BooleanField(default=False, verbose_name=_('Confirmed'))

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _('Subscriber')
        verbose_name_plural = _('Subscribers')
        ordering = ['email']


class Newsletter(models.Model):
    """ Newsletter Model """
    subject = models.CharField(max_length=150, verbose_name=_('Subject'))
    text_content = models.FileField(
        upload_to=get_newsletter_path,
        verbose_name=_('Content (text)'),
    )
    html_content = models.FileField(
        upload_to=get_newsletter_path,
        verbose_name=_('Content (html)'),
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at'),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated at'),
    )

    def __str__(self):
        return f'{ self.subject } ({ self.created_at })'

    def send(self):
        user_emails = [
            user.email for user in OSUser.objects.filter(is_subscription=True)
        ]
        sub_emails = [
            sub.email for sub in Subscriber.objects.filter(confirmed=True)
        ]
        all_emails = user_emails + sub_emails

        text_content = self.text_content.read().decode('utf-8')
        html_content = self.html_content.read().decode('utf-8')

        for recipient_email in all_emails:
            send_newsletter(
                self.subject,
                text_content,
                html_content,
                recipient_email
            )

    class Meta:
        verbose_name = _('Newsletter')
        verbose_name_plural = _('Newsletters')
        ordering = ['-created_at', '-updated_at', '-id']
