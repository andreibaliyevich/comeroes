from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from products.models import Product


class Wish(models.Model):
    """ Wish Model """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        verbose_name=_('Product'),
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at'),
    )

    class Meta:
        verbose_name = _('Wish')
        verbose_name_plural = _('Wishes')
        ordering = ['-created_at', '-id']
        unique_together = ['user', 'product']
