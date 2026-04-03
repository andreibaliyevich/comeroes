from django.conf import settings
from django.core.validators import (
    RegexValidator,
    MinValueValidator,
    MaxValueValidator,
)
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from contacts.models import Store
from accounts.models import Address
from products.models import Product
from coupons.models import Coupon


class Order(models.Model):
    """ Order Model """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_('User'),
    )

    first_name = models.CharField(max_length=150, verbose_name=_('First name'))
    last_name = models.CharField(max_length=150, verbose_name=_('Last name'))
    email = models.EmailField(verbose_name=_('Email address'))
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

    address = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_('Address'),
    )
    store = models.ForeignKey(
        Store,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_('Store'),
    )

    coupon = models.ForeignKey(
        Coupon,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name=_('Coupon'),
    )
    discount = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
        verbose_name=_('Discount'),
    )

    total_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Total cost'),
    )

    STATUS_CHOICES = [
        ('1', _('Pending')),
        ('2', _('Failed')),
        ('3', _('Processing')),
        ('4', _('Shipped')),
        ('5', _('Completed')),
        ('6', _('Delayed')),
        ('7', _('Canceled')),
        ('8', _('Refunded')),
    ]
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default='1',
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
        return str(self.id)

    def get_absolute_url(self):
        return reverse('orders:order_detail', args=[self.id])

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
        ordering = ['-created_at', '-updated_at', '-id']


class OrderItem(models.Model):
    """ Order Item Model """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name=_('Order'),
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        verbose_name=_('Product'),
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name=_('Price'),
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name=_('Quantity'),
    )
    total_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name=_('Total price'),
    )

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = _('Ordered product')
        verbose_name_plural = _('Ordered products')
