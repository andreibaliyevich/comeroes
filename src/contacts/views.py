from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.utils.translation import gettext_lazy as _
from .models import Store, ContactMessage
from .forms import ContactMessageForm


def contacts(request):
    """ Contacts """
    main_store = get_object_or_404(Store, is_main=True)
    other_stores = Store.objects.filter(is_main=False)

    if request.method == 'POST':
        contact_message_form = ContactMessageForm(request.POST)

        if contact_message_form.is_valid():
            contact_message_form.save()
            contact_message_form = ContactMessageForm()
            messages.success(request, _('Thank you for your message.'))
    else:
        contact_message_form = ContactMessageForm()

    context = {
        'main_store': main_store,
        'other_stores': other_stores,
        'contact_message_form': contact_message_form,
    }
    return render(request, 'contacts/contacts.html', context)


def store_detail(request, s_id):
    """ Store detail """
    store = get_object_or_404(Store, id=s_id)
    store_images = store.storeimage_set.all()

    context = {
        'store': store,
        'store_images': store_images,
    }
    return render(request, 'contacts/store_detail.html', context)
