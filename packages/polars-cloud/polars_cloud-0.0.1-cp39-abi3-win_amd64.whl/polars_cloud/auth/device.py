"""Code for authentication using the device authorization flow."""

from __future__ import annotations

import logging
import os
import time
import webbrowser
from pathlib import Path

import requests
from platformdirs import user_config_path

from polars_cloud.auth import constants
from polars_cloud.auth.constants import (
    ACCESS_TOKEN_DEFAULT_NAME,
    AUTH_DOMAIN,
    LOGIN_AUDIENCE,
    LOGIN_CLIENT_ID,
    POLLING_INTERVAL_SECONDS_DEFAULT,
    POLLING_TIMEOUT_SECONDS_DEFAULT,
)

logger = logging.getLogger(__name__)


def login() -> None:
    """Authenticate with Polars Cloud by logging in through the browser."""
    logger.debug("logging in through browser")
    user_code, device_code, verification_url = _request_device_code()

    _open_browser(verification_url, user_code)
    token = _get_token_with_device_code(device_code)

    logger.debug("storing token")
    path = (
        Path(os.getenv(constants.ACCESS_TOKEN_PATH, user_config_path() / "polars"))
        / ACCESS_TOKEN_DEFAULT_NAME
    )

    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w") as file:
        file.write(token)


def _request_device_code() -> tuple[str, str, str]:
    """Retrieve required login information."""
    url = f"https://{AUTH_DOMAIN}/realms/Polars/protocol/openid-connect/auth/device"
    data = {"client_id": LOGIN_CLIENT_ID, "audience": LOGIN_AUDIENCE}
    headers = {"content-type": "application/x-www-form-urlencoded"}

    response = requests.post(url, data=data, headers=headers)
    response.raise_for_status()
    response_json = response.json()

    return (
        response_json["user_code"],
        response_json["device_code"],
        response_json["verification_uri_complete"],
    )


def _open_browser(url: str, user_code: str) -> None:
    """Open a web browser for the user at the specified URL."""
    webbrowser.open(url)
    print("Please complete the login process in your browser.")
    print(f"If your browser did not open automatically, please go to the URL: {url}")
    print(f"Your login code is: {user_code}")


def _get_token_with_device_code(
    device_code: str,
    interval: int | float = POLLING_INTERVAL_SECONDS_DEFAULT,
    timeout: int | float = POLLING_TIMEOUT_SECONDS_DEFAULT,
) -> str:
    """Wait until the client has logged in to receive a token."""
    url = f"https://{AUTH_DOMAIN}/realms/Polars/protocol/openid-connect/token"
    data = {
        "client_id": LOGIN_CLIENT_ID,
        "device_code": device_code,
        "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
    }
    headers = {"content-type": "application/x-www-form-urlencoded"}

    max_polls = int(timeout / interval) + 1
    for _ in range(max_polls):
        logger.debug("polling login callback for token retrieval")
        response = requests.post(url, data=data, headers=headers)
        if response.status_code < 400:
            response_json = response.json()
            return response_json["access_token"]  # type: ignore[no-any-return]

        time.sleep(interval)
    else:
        msg = "logging in has timed out. Please try again."
        logger.debug(msg)
        raise RuntimeError(msg)
