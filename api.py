import os
from http import HTTPStatus

import requests
from dotenv import load_dotenv

load_dotenv()
IMMICH_API_KEY = os.getenv("IMMICH_API_KEY")
IMMICH_URL = os.getenv("IMMICH_URL")


class APIError(Exception):
    pass


def api_call(method: str, endpoint: str, data: dict | None = None) -> dict:
    res = requests.request(
        method,
        IMMICH_URL + "/api/" + endpoint,
        headers={"x-api-key": IMMICH_API_KEY},
        json=data,
        timeout=5,
        )
    status = HTTPStatus(res.status_code)
    if not status.is_success:
        msg = f"API call failed: {res.status_code} {res.reason}"
        raise APIError(msg)
    if status == HTTPStatus.NO_CONTENT:
        return {}
    return res.json()
