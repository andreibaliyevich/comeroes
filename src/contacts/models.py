from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.core.validators import RegexValidator
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from main.model_fields import TranslatedField
from .utilities import get_store_image_path


class Store(models.Model):
    """ Store Model """
    city = models.CharField(
        max_length=64,
        choices=settings.CITIES,
        verbose_name=_('City'),
    )

    address = models.CharField(max_length=255, verbose_name=_('Address'))
    translated_address = TranslatedField('address')
    location = models.PointField(
        default=Point(0.0, 0.0),
        verbose_name=_('Location'),
    )

    meta_description = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_('Description'),
    )
    meta_keywords = models.CharField(
        blank=True,
        max_length=255,
        help_text=_('Separate keywords with commas.'),
        verbose_name=_('Keywords'),
    )
    translated_meta_description = TranslatedField('meta_description')
    translated_meta_keywords = TranslatedField('meta_keywords')

    main_image = models.ImageField(
        upload_to=get_store_image_path,
        verbose_name=_('Main image'),
        help_text=_('Recommend: 1000 x 667 px.'),
    )

    customers_phone = models.CharField(
        max_length=21,
        verbose_name=_('Phone for customers'),
    )
    support_phone = models.CharField(
        max_length=21,
        verbose_name=_('Phone for support'),
    )

    customers_email = models.EmailField(verbose_name=_('Email for customers'))
    support_email = models.EmailField(verbose_name=_('Email for support'))

    time_weekdays_start = models.TimeField(
        verbose_name=_('Start time in weekdays'))
    time_weekdays_end = models.TimeField(
        verbose_name=_('End time in weekdays'))
    time_weekend_start = models.TimeField(
        verbose_name=_('Start time in weekend'))
    time_weekend_end = models.TimeField(
        verbose_name=_('End time in weekend'))

    is_main = models.BooleanField(default=False, verbose_name=_('Main'))

    def save(self, *args, **kwargs):
        if self.is_main:
            store_list = Store.objects.all().exclude(id=self.id)
            store_list.update(is_main=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{ self.city } | { self.translated_address }'

    def get_absolute_url(self):
        return reverse('main:store_info', args=[self.id])

    class Meta:
        verbose_name = _('Store')
        verbose_name_plural = _('Stores')
        ordering = ['id']
        unique_together = ['city', 'address']


class StoreTranslation(models.Model):
    """ Store Translation Model """
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name='translations',
        verbose_name=_('Store'),
    )
    language = models.CharField(
        max_length=2,
        choices=settings.LANGUAGES[1:],
        verbose_name=_('Language'),
    )

    address = models.CharField(max_length=255, verbose_name=_('Address'))

    meta_description = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_('Description'),
    )
    meta_keywords = models.CharField(
        blank=True,
        max_length=255,
        help_text=_('Separate keywords with commas.'),
        verbose_name=_('Keywords'),
    )

    class Meta:
        verbose_name = _('Store Translation')
        verbose_name_plural = _('Store Translations')
        ordering = ['store', 'language']
        unique_together = ['store', 'language']


class StoreImage(models.Model):
    """ Store Image Model """
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        verbose_name=_('Store'),
    )
    image = models.ImageField(
        upload_to=get_store_image_path,
        verbose_name=_('Image'),
        help_text=_('Recommend: 1000 x 667 px.'),
    )

    class Meta:
        verbose_name = _('Image of Store')
        verbose_name_plural = _('Images of Store')
        ordering = ['store', 'id']


class ContactMessage(models.Model):
    """ Message Model """
    name = models.CharField(max_length=250, verbose_name=_('Name'))
    email = models.EmailField(verbose_name=_('Email'))
    phone = models.CharField(
        max_length=21,
        validators=[
            RegexValidator(
                regex=r'^(\s*)?(\+)?([- _():=+]?\d[- _():=+]?){9,16}(\s*)?$',
                message=_('Wrong format!'),
            ),
        ],
        verbose_name=_('Phone'),
    )

    subject = models.CharField(
        blank=True,
        max_length=150,
        verbose_name=_('Subject'),
    )
    content = models.TextField(verbose_name=_('Content'))
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at'),
    )

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
        ordering = ['-created_at', '-id']
