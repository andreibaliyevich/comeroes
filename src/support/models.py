from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Ticket(models.Model):
    """ Ticket Model """
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Members'),
    )
    subject = models.CharField(max_length=150, verbose_name=_('Subject'))

    class Category(models.TextChoices):
        WEBSITE_PROBLEM = 'WM', _('Website problem')
        COMPLAINT = 'CT', _('Complaint')
        INFO_INQUIRY = 'IY', _('Info inquiry')
        OTHER_PROBLEM = 'OM', _('Other problem')

    category = models.CharField(
        max_length=2,
        choices=Category.choices,
        default=Category.OTHER_PROBLEM,
        verbose_name=_('Category'),
    )

    class Priority(models.IntegerChoices):
        HIGH = 1, _('High')
        MEDIUM = 2, _('Medium')
        LOW = 3, _('Low')

    priority = models.IntegerField(
        choices=Priority.choices,
        default=Priority.LOW,
        verbose_name=_('Priority'),
    )

    class Status(models.IntegerChoices):
        OPEN = 0, _('Open')
        CLOSED = 1, _('Closed')

    status = models.IntegerField(
        choices=Status.choices,
        default=Status.OPEN,
        verbose_name=_('Status'),
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

    class Meta:
        verbose_name = _('Ticket')
        verbose_name_plural = _('Tickets')
        ordering = ['-updated_at', '-created_at', '-id']


class Message(models.Model):
    """ Message Model """
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        verbose_name=_('Ticket'),
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('Sender'),
    )

    content = models.TextField(verbose_name=_('Content'))
    is_viewed = models.BooleanField(default=False, verbose_name=_('Viewed'))
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at'),
    )

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
        ordering = ['created_at', 'id']
