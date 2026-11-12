from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    fred_api_key: str
    email_to: str
    email_from: str
    smtp_host: str
    smtp_port: int
    smtp_username: str
    smtp_password: str


def load_settings() -> Settings:
    required = [
        "FRED_API_KEY",
        "EMAIL_TO",
        "EMAIL_FROM",
        "SMTP_HOST",
        "SMTP_USERNAME",
        "SMTP_PASSWORD",
    ]
    missing = [name for name in required if not os.getenv(name)]
    if missing:
        raise EnvironmentError(
            f"Missing environment variables: {', '.join(missing)}"
        )

    return Settings(
        fred_api_key=os.environ["FRED_API_KEY"],
        email_to=os.environ["EMAIL_TO"],
        email_from=os.environ["EMAIL_FROM"],
        smtp_host=os.environ["SMTP_HOST"],
        smtp_port=int(os.getenv("SMTP_PORT", "587")),
        smtp_username=os.environ["SMTP_USERNAME"],
        smtp_password=os.environ["SMTP_PASSWORD"],
    )
