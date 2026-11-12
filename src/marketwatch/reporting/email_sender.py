from __future__ import annotations

import smtplib
import ssl
from email.message import EmailMessage


def send_email(
    smtp_host: str,
    smtp_port: int,
    smtp_username: str,
    smtp_password: str,
    email_to: str,
    email_from: str,
    subject: str,
    html: str,
) -> None:
    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = email_from
    message["To"] = email_to
    message.set_content("Your email client does not support HTML.")
    message.add_alternative(html, subtype="html")

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(smtp_username, smtp_password)
        server.send_message(message)
