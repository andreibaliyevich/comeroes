from django import forms
from django.contrib.auth import password_validation
from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import OSUser, Address
from .validators import MinSizeImageValidator


class SignupForm(forms.ModelForm):
    """ Sign Up Form """
    email = forms.EmailField(label=_('Email address'), required=True)

    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput,
        required=True,
    )
    password2 = forms.CharField(
        label=_('Confirm password'),
        widget=forms.PasswordInput,
        required=True,
    )

    is_subscription = forms.BooleanField(
        label=_('Subscribe me to Newsletter'),
        widget=forms.widgets.CheckboxInput(
            attrs={'class': 'custom-control-input'}),
        required=False,
    )

    class Meta:
        model = OSUser
        fields = [
            'email',
            'password1',
            'password2',
            'is_subscription',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_subscription'].initial = True

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                _("Passwords don't match."),
                code='password_mismatch',
            )
        password_validation.validate_password(password2)
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    """ User Profile Form """
    avatar = forms.ImageField(
        label=_('Avatar'),
        validators=[
            validators.FileExtensionValidator(
                allowed_extensions=('jpg', 'png')),
            MinSizeImageValidator(300, 300),
        ],
        error_messages={
            'invalid_extension': _('This file format is not supported.')},
    )

    first_name = forms.CharField(label=_('First name'), required=False)
    last_name = forms.CharField(label=_('Last name'), required=False)

    email = forms.EmailField(label=_('Email address'), required=False)
    phone = forms.CharField(
        label=_('Phone'),
        min_length=9,
        max_length=21,
        required=False,
    )

    BIRTH_YEAR_CHOICES = [i for i in range(1970, 2011)]
    BIRTH_MONTH_CHOICES = {
        1: _('January'),
        2: _('February'),
        3: _('March'),
        4: _('April'),
        5: _('May'),
        6: _('June'),
        7: _('July'),
        8: _('August'),
        9: _('September'),
        10: _('October'),
        11: _('November'),
        12: _('December'),
    }
    date_of_birth = forms.DateField(
        label=_('Date of Birth'),
        widget=forms.widgets.SelectDateWidget(
            months=BIRTH_MONTH_CHOICES,
            years=BIRTH_YEAR_CHOICES),
        required=False,
    )

    is_subscription = forms.BooleanField(
        label=_('Subscribe me to Newsletter'),
        widget=forms.widgets.CheckboxInput(
            attrs={'class': 'custom-control-input'}),
        required=False,
    )

    class Meta:
        model = OSUser
        fields = [
            'avatar',
            'first_name',
            'last_name',
            'email',
            'phone',
            'date_of_birth',
            'is_subscription',
        ]


class AddressForm(forms.ModelForm):
    """ Address Form """

    class Meta:
        model = Address
        fields = [
            'locality',
            'street_house',
            'porch',
            'level',
            'apt_office',
            'is_primary',
        ]
        labels = {
            'is_primary': _('Make this address primary'),
        }
        widgets = {
            'is_primary': forms.widgets.CheckboxInput(
                attrs={'class': 'custom-control-input'}),
        }
