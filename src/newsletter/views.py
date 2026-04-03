from django.contrib import messages
from django.core.signing import BadSignature
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST
from accounts.models import OSUser
from .models import Subscriber
from .utilities import signer, send_confirm_email


@require_POST
def subscriber_add(request):
    """ Adding a subscriber """
    sub_email = request.POST.get('sub_email')
    msg_success = _('To complete your subscription, you need to confirm your email.')
    msg_info = _('You are already subscribed to our newsletter.')

    try:
        user = OSUser.objects.get(email=sub_email)
    except OSUser.DoesNotExist:
        try:
            subscriber = Subscriber.objects.get(email=sub_email)
        except Subscriber.DoesNotExist:
            Subscriber.objects.create(email=sub_email)
            send_confirm_email(sub_email)
            messages.success(request, msg_success)
        else:
            if subscriber.confirmed:
                messages.info(request, msg_info)
            else:
                send_confirm_email(sub_email)
                messages.success(request, msg_success)
    else:
        if user.is_subscription:
            messages.info(request, msg_info)
        else:
            send_confirm_email(sub_email)
            messages.success(request, msg_success)
    finally:
        next_page = request.META.get('HTTP_REFERER', '/')
        return redirect(next_page)


def subscriber_confirm(request, sign):
    """ Confirm a subscriber """
    try:
        sub_email = signer.unsign(sign)
        user = OSUser.objects.get(email=sub_email)
    except BadSignature:
        messages.error(request, _('The confirm of an email was unsuccessful.'))
    except OSUser.DoesNotExist:
        try:
            subscriber = Subscriber.objects.get(email=sub_email)
        except Subscriber.DoesNotExist:
            messages.error(request, _('Email has been removed from subscriptions.'))
        else:
            if subscriber.confirmed:
                messages.info(request, _('The email was confirm earlier.'))
            else:
                subscriber.confirmed = True
                subscriber.save(update_fields=['confirmed'])
                messages.success(request, _('You have successfully subscribed to our newsletter.'))
    else:
        if user.is_subscription:
            messages.info(request, _('The email was confirm earlier.'))
        else:
            user.is_subscription = True
            user.save(update_fields=['is_subscription'])
            messages.success(request, _('You have successfully subscribed to our newsletter.'))
    finally:
        return redirect('main:index')


def subscriber_delete(request, sign):
    """ Delete a subscriber """
    try:
        sub_email = signer.unsign(sign)
        user = OSUser.objects.get(email=sub_email)
    except BadSignature:
        messages.error(request, _('The delete of an email was unsuccessful.'))
    except OSUser.DoesNotExist:
        try:
            subscriber = Subscriber.objects.get(email=sub_email)
        except Subscriber.DoesNotExist:
            messages.info(request, _('Email has been removed from subscriptions earlier.'))
        else:
            subscriber.delete()
            messages.success(request, _('Email has been removed from subscriptions.'))
    else:
        if user.is_subscription:
            user.is_subscription = False
            user.save(update_fields=['is_subscription'])
            messages.success(request, _('Email has been removed from subscriptions.'))
        else:
            messages.info(request, _('Email has been removed from subscriptions earlier.'))
    finally:
        return redirect('main:index')
