from django.db.models import Count, Sum, Q
from .models import Message


def support_context(request):
    """ Support context """
    if request.user.is_authenticated:
        messages_count = Message.objects.filter(
            ~Q(sender=request.user),
            ticket__members=request.user,
            is_viewed=False,
        ).count()

        context = {
            'messages_count': messages_count,
        }
    else:
        context = {
            'messages_count': 0,
        }
    return context
