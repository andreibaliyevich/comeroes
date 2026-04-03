from django import forms
from contacts.models import Store
from .models import Order


class OrderCreateForm(forms.ModelForm):
    """ Order Create Form """

    class Meta:
        model = Order
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'address',
            'store',
        ]

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        city_code = request.session.get('city_code')
        stores = Store.objects.filter(city=city_code)

        STORE_CHOICES = []
        STORE_CHOICES.append(('', '---------'))
        for store in stores:
            STORE_CHOICES.append((str(store.id), store.translated_address))

        self.fields['store'].choices = STORE_CHOICES
