from easy_thumbnails.fields import ThumbnailerImageField
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import OSUserManager
from .utilities import get_user_avatar_path


class OSUser(AbstractBaseUser, PermissionsMixin):
    """ User Model """
    email = models.EmailField(unique=True, verbose_name=_('Email address'))

    first_name = models.CharField(
        blank=True,
        max_length=150,
        verbose_name=_('First name'),
    )
    last_name = models.CharField(
        blank=True,
        max_length=150,
        verbose_name=_('Last name'),
    )

    avatar = ThumbnailerImageField(
        null=True,
        blank=True,
        upload_to=get_user_avatar_path,
        resize_source={
            'size': (300, 300),
            'crop': 'smart',
            'autocrop': True,
            'quality': 100,
        },
        verbose_name=_('Avatar'),
    )
    phone = models.CharField(
        blank=True,
        max_length=21,
        validators=[
            RegexValidator(
                regex=r'^(\s*)?(\+)?([- _():=+]?\d[- _():=+]?){9,16}(\s*)?$',
                message=_('Wrong format!'),
            ),
        ],
        verbose_name=_('Phone'),
    )
    date_of_birth = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Date of Birth'),
    )
    is_subscription = models.BooleanField(
        default=True,
        verbose_name=_('Is subscription'),
    )

    is_active = models.BooleanField(default=False, verbose_name=_('Active'))
    is_staff = models.BooleanField(
        default=False,
        verbose_name=_('Staff status'),
    )
    is_superuser = models.BooleanField(
        default=False,
        verbose_name=_('Superuser status'),
    )

    last_visit = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('Last visit'),
    )
    last_login = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('Last login'),
    )
    date_joined = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('Date joined'),
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = OSUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.first_name and self.last_name:
            return f'{ self.first_name } { self.last_name }'
        else:
            return None

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['email']


class Address(models.Model):
    """ Address Model """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
    )

    locality = models.CharField(max_length=64, verbose_name=_('Locality'))
    street_house = models.CharField(
        max_length=128,
        verbose_name=_('Street, House'),
    )
    porch = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name=_('Porch'),
    )
    level = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name=_('Level'),
    )
    apt_office = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name=_('Apt / office'),
    )
    is_primary = models.BooleanField(
        default=False,
        verbose_name=_('Is Primary'),
    )

    def save(self, *args, **kwargs):
        if self.is_primary:
            addresses_list = Address.objects.filter(
                user=self.user).exclude(id=self.id)
            addresses_list.update(is_primary=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f'{ self.locality }, { self.street_house }, '
            f'{ self.porch }, { self.level }, { self.apt_office }'
        )

    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')
        ordering = ['id']
