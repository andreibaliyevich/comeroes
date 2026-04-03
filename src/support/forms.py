from django import forms
from .models import Ticket, Message


class TicketForm(forms.ModelForm):
    """ Ticket Form """

    class Meta:
        model = Ticket
        fields = [
            'subject',
            'category',
            'priority',
        ]


class MessageForm(forms.ModelForm):
    """ Message Form """

    class Meta:
        model = Message
        fields = [
            'content',
        ]
