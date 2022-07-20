from uuid import uuid4

import requests
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from core.config import settings


def generate_uuid() -> str:
    return str(uuid4())


def to_camel(string: str) -> str:
    string_split = string.split("_")
    return string_split[0] + "".join(word.capitalize() for word in string_split[1:])


def is_valid_email(email: str) -> bool:
    url = (
        f"https://api.millionverifier.com/api/v3/?api={settings.EMAIL_VERIFIER_API_KEY}"
        f"&email={email}&timeout=10"
    )
    response = requests.request("GET", url)
    return response.json().get("result") != "invalid"


def send_reset_password_email(to_email: str, reset_link: str):
    message = Mail(
        from_email=settings.SENDGRID_FROM_EMAIL,
        to_emails=to_email,
        subject="Reset your Tripari's password",
    )
    message.template_id = settings.SENDGRID_RESET_PASSWORD_TEMPLATE_ID
    message.dynamic_template_data = {"resetLink": reset_link}

    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        sg.send(message)
    except Exception as e:
        print(e)


def send_remind_trip_email(to_email: str, start_date: str, remind_link: str):
    message = Mail(
        from_email=settings.SENDGRID_FROM_EMAIL,
        to_emails=to_email,
        subject="Next trip is coming!",
    )
    message.template_id = settings.SENDGRID_REMIND_TRIP_TEMPLATE_ID
    message.dynamic_template_data = {
        "startDate": start_date,
        "remindLink": remind_link,
    }
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        sg.send(message)
    except Exception as e:
        print(e)


def send_remind_trip_email_again(to_email: str, start_date: str):
    message = Mail(
        from_email=settings.SENDGRID_FROM_EMAIL,
        to_emails=to_email,
        subject="Next trip is coming!",
    )
    message.template_id = settings.SENDGRID_REMIND_TRIP_AGAIN_TEMPLATE_ID
    message.dynamic_template_data = {
        "startDate": start_date,
    }
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        sg.send(message)
    except Exception as e:
        print(e)


def send_verify_account_email(to_email: str, verify_link: str):
    message = Mail(
        from_email=settings.SENDGRID_FROM_EMAIL,
        to_emails=to_email,
        subject="Verify your Tripari's account!",
    )
    message.template_id = settings.SENDGRID_VERIFY_ACCOUNT_TEMPLATE_ID
    message.dynamic_template_data = {"verifyLink": verify_link}
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        sg.send(message)
    except Exception as e:
        print(e)
