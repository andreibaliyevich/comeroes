from django import forms
from .models import ContactMessage


class ContactMessageForm(forms.ModelForm):
    """ Contact Message Form """

    class Meta:
        model = ContactMessage
        fields = [
            'name',
            'email',
            'phone',
            'subject',
            'content',
        ]
