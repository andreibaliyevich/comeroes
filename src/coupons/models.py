from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Coupon(models.Model):
    """ Coupon Model """
    code = models.CharField(max_length=64, unique=True, verbose_name=_('Code'))
    valid_from = models.DateTimeField(verbose_name=_('Valid with'))
    valid_to = models.DateTimeField(verbose_name=_('Valid until'))
    discount = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100),
        ],
        verbose_name=_('Discount'),
    )
    is_active = models.BooleanField(default=True, verbose_name=_('Active'))

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = _('Coupon')
        verbose_name_plural = _('Coupons')
