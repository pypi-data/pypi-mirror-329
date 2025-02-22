import os

import requests
from requests.auth import HTTPBasicAuth

from ..utils import api_base_url


def build_token_payload(token: str, duration: int, **kwargs) -> dict:
    student_id = kwargs.get("student_id", None)
    assignment = kwargs.get("assignment", None)

    jhub_user = os.getenv("JUPYTERHUB_USER")
    if jhub_user is None:
        raise ValueError("JupyterHub user not found")

    payload = {
        "value": token,
        "duration": duration,
        "requester": jhub_user,
    }

    if student_id:
        payload["student_id"] = student_id
    if assignment:
        payload["assignment"] = assignment

    return payload


def add_token(token: str, duration: int = 20, **kwargs) -> None:
    """
    Sends a POST request to mint a token
    """

    if not api_base_url:
        raise ValueError("Environment variable for API URL not set")
    url = api_base_url.rstrip("/") + "/tokens"

    payload = build_token_payload(token=token, duration=duration, **kwargs)

    # Dummy credentials for HTTP Basic Auth
    auth = HTTPBasicAuth("user", "password")

    # Add a custom header, for potential use in authorization
    headers = {"x-jhub-user": payload["requester"]}

    response = requests.post(url=url, json=payload, headers=headers, auth=auth)

    # Print response
    print(f"Status code: {response.status_code}")

    try:
        print(f"Response: {response.json()}")
    except ValueError:
        print(f"Response: {response.text}")
