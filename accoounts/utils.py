from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import PermissionDenied
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def detect_user(user):
    if user.role == 1:
        redirectUrl = "vendor_dashboard"
    elif user.role == 2:
        redirectUrl = "customer_dashboard"
    elif user.role == None and user.is_superadmin:
        redirectUrl = "/admin"
    return redirectUrl


def check_role_vendor(user):
    print("USER :", user.role, user.role == 1)
    if user.role == 1:
        return True
    raise PermissionDenied


def check_role_customer(user):
    print("USER :", user.role)
    if user.role == 2:
        return True
    raise PermissionDenied


def send_email(request, user, status):
    current_site = get_current_site(request)
    if status == "send_verification_email":
        mail_subject = "Please activate your account"
        message = render_to_string(
            "accounts/emails/account_verification_email.html",
            {
                "user": user,
                "domain": current_site,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": default_token_generator.make_token(user),
            },
        )
    elif status == "send_reset_password_email":
        mail_subject = "Reset Your Password"
        message = render_to_string(
            "accounts/emails/reset_password_email.html",
            {
                "user": user,
                "domain": current_site,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": default_token_generator.make_token(user),
            },
        )
    to_email = user.email
    mail = EmailMessage(
        subject=mail_subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[to_email],
    )
    mail.content_subtype = "html"

    mail.send()


def send_notification(mail_subject, mail_template, context):

    message = render_to_string(mail_template, context)
    to_email = context.get("user").email
    mail = EmailMessage(
        subject=mail_subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[to_email],
    )
    mail.content_subtype = "html"

    mail.send()
