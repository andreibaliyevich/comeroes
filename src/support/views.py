from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import render, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView
from .forms import TicketForm, MessageForm
from .models import Ticket


class SupportView(TemplateView):
    """ Support page """
    template_name = 'support/support.html'


@login_required
def tickets(request):
    """ Tickets """
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST)
        message_form = MessageForm(request.POST)

        if ticket_form.is_valid() and message_form.is_valid():
            new_ticket = ticket_form.save()
            new_ticket.members.add(request.user)

            new_message = message_form.save(commit=False)
            new_message.ticket = new_ticket
            new_message.sender = request.user
            new_message.save()

            ticket_form = TicketForm()
            message_form = MessageForm()
    else:
        ticket_form = TicketForm()
        message_form = MessageForm()

    objects = request.user.ticket_set.annotate(
        msg_not_viewed_count=Count('message',
            filter=(
                ~Q(message__sender=request.user)
                & Q(message__is_viewed=False)
            )
        )
    )

    paginator = Paginator(objects, 8)
    page_number = request.GET.get('page', 1)
    objects_page = paginator.get_page(page_number)

    context = {
        'ticket_form': ticket_form,
        'message_form': message_form,
        'objects_page': objects_page,
    }
    return render(request, 'support/tickets.html', context)


@login_required
def ticket_detail(request, t_id):
    """ Ticket Detail """
    ticket = get_object_or_404(Ticket, id=t_id)

    if request.user in ticket.members.all():
        if request.method == 'POST' and ticket.status == ticket.Status.OPEN:
            message_form = MessageForm(request.POST)

            if message_form.is_valid():
                new_message = message_form.save(commit=False)
                new_message.ticket = ticket
                new_message.sender = request.user
                new_message.save()

                if request.POST.get('close-ticket'):
                    ticket.status = ticket.Status.CLOSED
                    ticket.save(update_fields=['status', 'updated_at'])
                else:
                    ticket.save(update_fields=['updated_at'])

                message_form = MessageForm()
        else:
            ticket.message_set.filter(
                ~Q(sender=request.user) & Q(is_viewed=False)
            ).update(is_viewed=True)

            message_form = MessageForm()

        context = {
            'ticket': ticket,
            'message_form': message_form,
        }
        return render(request, 'support/ticket_detail.html', context)
    else:
        raise Http404
