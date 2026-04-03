from os.path import splitext
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.signing import Signer
from django.template.loader import render_to_string
from django.utils import timezone


signer = Signer()


def send_activation_email(user):
    """ Send activation email to user """
    context = {
        'SITE_NAME': settings.SITE_NAME,
        'SITE_HOST': settings.SITE_HOST,
        'sign': signer.sign(user.email),
    }

    subject = render_to_string('email/signup_activation_subject.txt', context)
    text_content = render_to_string(
        'email/signup_activation_email_text.html',
        context,
    )
    html_content = render_to_string(
        'email/signup_activation_email.html',
        context,
    )

    email = EmailMultiAlternatives(
        subject,
        text_content,
        settings.EMAIL_HOST_USER,
        [user.email],
    )
    email.attach_alternative(html_content, 'text/html')
    email.send(fail_silently=False)


def get_user_avatar_path(instance, filename):
    """ Get path of avatar """
    path_name = timezone.now().strftime('%Y/%m/%d/%H%M%S%f')
    file_ext = splitext(filename)[1].lower()
    return f'avatars/{ path_name }{ file_ext }'
