from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordResetView,
    PasswordResetConfirmView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.core.signing import BadSignature
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from newsletter.models import Subscriber
from .forms import SignupForm, UserProfileForm, AddressForm
from .models import OSUser, Address
from .utilities import signer, send_activation_email


def signin(request):
    """ Sign In """
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        next_page = request.POST['next']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, _('You are logged in!'))

            if next_page:
                return redirect(next_page)
            else:
                return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            messages.error(request, _('Invalid email or password!'))
            context = {
                'email': email,
                'password': password,
                'next': next_page,
            }
            return render(request, 'accounts/signin.html', context)
    else:
        next_page = request.GET.get('next', '')
        context = {
            'next': next_page,
        }
        return render(request, 'accounts/signin.html', context)


@login_required
def signout(request):
    """ Sign Out """
    logout(request)
    messages.success(request, _('Logged out successfully!'))
    return redirect(settings.LOGOUT_REDIRECT_URL)


def signup(request):
    """ Sign Up """
    if request.method == 'POST':
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            send_activation_email(user)
            messages.success(request, _('Register User Done. Check your email.'))
            return redirect('main:index')
    else:
        signup_form = SignupForm()

    context = {
        'signup_form': signup_form,
    }
    return render(request, 'accounts/signup.html', context)


def signup_activate(request, sign):
    """ User Sign Up Activate """
    try:
        email = signer.unsign(sign)
    except BadSignature:
        messages.error(request, _('The activation of a user was unsuccessful.'))
        return redirect('main:index')

    user = get_object_or_404(OSUser, email=email)

    if user.is_active:
        messages.info(request, _('A user with this name was activated earlier.'))
        return redirect('main:index')
    else:
        user.is_active = True
        user.save(update_fields=['is_active'])

        try:
            subscriber = Subscriber.objects.get(email=user.email)
        except Subscriber.DoesNotExist:
            pass
        else:
            subscriber.delete()

        login(request, user)
        messages.success(request, _('Your account has been successfully activated.'))
        return redirect('accounts:profile')


class OSPasswordResetView(SuccessMessageMixin, PasswordResetView):
    """ Password Reset """
    extra_email_context = {
        'SITE_NAME': settings.SITE_NAME,
        'SITE_HOST': settings.SITE_HOST,
    }
    template_name = 'accounts/password_reset.html'
    subject_template_name = 'email/password_reset_subject.txt'
    email_template_name = 'email/password_reset_email_text.html'
    html_email_template_name = 'email/password_reset_email.html'
    success_url = reverse_lazy('main:index')
    success_message = _('Password Reset Done. Check your email.')


class OSPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    """ Password Reset Confirm """
    template_name = 'accounts/password_reset_confirm.html'
    post_reset_login = True
    post_reset_login_backend = 'django.contrib.auth.backends.ModelBackend'
    success_url = reverse_lazy('main:index')
    success_message = _('Password Reset Complete. New password set.')


class OSPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    """ Password Change """
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('accounts:profile')
    success_message = _('Your password has been changed.')


@login_required
def profile(request):
    """ Profile info """
    user = get_object_or_404(OSUser, id=request.user.id)

    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, request.FILES, instance=user)

        if user_form.is_valid():
            user = user_form.save()
            user_form = UserProfileForm(instance=user)
            messages.success(request, _('Your profile information has been changed.'))
    else:
        user_form = UserProfileForm(instance=user)

    context = {
        'user_form': user_form,
    }
    return render(request, 'accounts/account_profile.html', context)


@login_required
def profile_delete(request):
    """ User Profile Delete """
    user = get_object_or_404(OSUser, id=request.user.id)

    if request.method == 'POST':
        logout(request)
        user.delete()
        messages.success(request, _('Your account has been deleted.'))
        return redirect(settings.LOGOUT_REDIRECT_URL)
    else:
        return render(request, 'accounts/account_profile_delete.html')


@login_required
def addresses(request):
    """ Addresses """
    if request.method == 'POST':
        address_form = AddressForm(request.POST)

        if address_form.is_valid():
            new_address = address_form.save(commit=False)
            new_address.user = request.user
            new_address.save()
            address_form = AddressForm()
    else:
        address_form = AddressForm()

    addresses_list = request.user.address_set.all()

    context = {
        'addresses_list': addresses_list,
        'address_form': address_form,
    }
    return render(request, 'accounts/account_addresses.html', context)


@login_required
def address_change(request, address_id):
    """ Change Address """
    address = get_object_or_404(Address, id=address_id)

    if address.user.id == request.user.id:
        if request.method == 'POST':
            address_form = AddressForm(request.POST, instance=address)
            if address_form.is_valid():
                address_form.save()
                return redirect('accounts:addresses')
        else:
            address_form = AddressForm(instance=address)

        context = {
            'address_id': address.id,
            'address_form': address_form,
        }
        return render(request, 'accounts/account_address_change.html', context)
    else:
        raise Http404


@login_required
def address_delete(request, address_id):
    """ Delete Address """
    address = get_object_or_404(Address, id=address_id)
    if address.user.id == request.user.id:
        address.delete()
        return redirect('accounts:addresses')
    else:
        raise Http404
