from .mail import get_mail_provider
from .settings import saas_settings
from .signals import before_send_mail


def send_mail(sender, subject: str, template_id: str, recipients, **context):
    context.setdefault('site', saas_settings.SITE)
    provider = get_mail_provider('notification', 'default')
    text_message, html_message = provider.render_message(template_id, context)
    before_send_mail.send(
        sender,
        subject=subject,
        recipients=recipients,
        text_message=text_message,
        html_message=html_message,
    )
    if saas_settings.MAIL_IMMEDIATE_SEND:
        return provider.send_mail(
            subject,
            recipients,
            text_message,
            html_message,
        )
