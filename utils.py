from uuid import uuid4

import requests

from core.config import settings


def generate_uuid() -> str:
    return str(uuid4())


def to_camel(string: str) -> str:
    string_split = string.split("_")
    return string_split[0] + "".join(word.capitalize() for word in string_split[1:])


def is_valid_email(email: str) -> bool:
    url = "https://api.reacher.email/v0/check_email"
    headers = {"Authorization": settings.REACHER_API_KEY}
    payload = {"to_email": email}
    response = requests.post(url, json=payload, headers=headers)

    return response.json().get("is_reachable") != "invalid"
