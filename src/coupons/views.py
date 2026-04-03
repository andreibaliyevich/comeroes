from django.contrib import messages
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST
from .forms import CouponApllyForm
from .models import Coupon


@require_POST
def coupon_apply(request):
    """ Coupon application """
    coupon_aplly_form = CouponApllyForm(request.POST)

    if coupon_aplly_form.is_valid():
        coupon_code = coupon_aplly_form.cleaned_data['code']
        datetime_now = timezone.now()

        try:
            coupon = Coupon.objects.get(
                code__iexact=coupon_code,
                valid_from__lte=datetime_now,
                valid_to__gte=datetime_now,
                is_active=True,
            )
        except Coupon.DoesNotExist:
            messages.error(request, _('Coupon is not valid.'))
        else:
            request.session['coupon_id'] = coupon.id
            message = _('Coupon has been successfully applied.')
            messages.success(request, message)

    return redirect('cart:cart_detail')
