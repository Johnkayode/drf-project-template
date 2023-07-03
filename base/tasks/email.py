import logging
import os
import typing

from celery import shared_task, Task
from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import get_template, render_to_string


@shared_task(bind=True, name="base.tasks.send_email")
def send_email(
    self: Task,
    subject: str,
    template_name: str,
    recipients: typing.List[str],
    context: typing.Optional[dict] = None,
    sender: str = settings.DEFAULT_FROM_EMAIL,
    pdf: typing.Optional[str]=None,
    reply_to: str = "",
    text_template_name: str = "",
):
    message = get_template(template_name).render(context)
    mail = EmailMultiAlternatives(
        subject=subject,
        body=message,
        from_email=sender,
        to=recipients,
        reply_to=[reply_to],
    )

    mail.attach_alternative(message, "text/html")
    _send = mail.send()
    return {
        "status": "successful",
        "message": "Email sent successfully",
        "recipients": recipients,
        "count": _send,
    }
