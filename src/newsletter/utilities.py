from os.path import splitext
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.signing import Signer
from django.template.loader import render_to_string
from django.utils import timezone


signer = Signer()


def send_confirm_email(sub_email):
    """ Send confirm email to user """
    context = {
        'SITE_NAME': settings.SITE_NAME,
        'SITE_HOST': settings.SITE_HOST,
        'sign': signer.sign(sub_email),
    }

    subject = render_to_string('email/subscriber_confirm_subject.txt')
    text_content = render_to_string(
        'email/subscriber_confirm_content_text.html',
        context,
    )
    html_content = render_to_string(
        'email/subscriber_confirm_content.html',
        context,
    )

    email = EmailMultiAlternatives(
        subject,
        text_content,
        settings.EMAIL_HOST_USER,
        [sub_email],
    )
    email.attach_alternative(html_content, 'text/html')
    email.send(fail_silently=False)


def send_newsletter(subject, text_content, html_content, recipient_email):
    """ Send newsletter to user """
    context = {
        'SITE_NAME': settings.SITE_NAME,
        'SITE_HOST': settings.SITE_HOST,
        'sign': signer.sign(recipient_email),
    }

    text_content = text_content + (
        render_to_string('email/newsletter_footer_text.html', context)
    )
    html_content = html_content + (
        render_to_string('email/newsletter_footer.html', context)
    )

    email = EmailMultiAlternatives(
        subject,
        text_content,
        settings.EMAIL_HOST_USER,
        [recipient_email],
    )
    email.attach_alternative(html_content, 'text/html')
    email.send(fail_silently=False)


def get_newsletter_path(instance, filename):
    """ Get path of newsletter """
    path_name = timezone.now().strftime('%Y/%m/%d/%H%M%S%f')
    file_ext = splitext(filename)[1].lower()
    return f'newsletter/{ path_name }{ file_ext }'
