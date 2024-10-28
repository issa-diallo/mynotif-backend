from django.core.mail import EmailMultiAlternatives


def send_mail_with_reply(
    subject,
    message,
    from_email,
    recipient_list,
    reply_to_email=None,
    fail_silently=False,
    html_message=None,
):
    mail = EmailMultiAlternatives(subject, message, from_email, recipient_list)
    if html_message:
        mail.attach_alternative(html_message, "text/html")
    if reply_to_email:
        mail.reply_to = [reply_to_email]
    return mail.send()
