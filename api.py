import os
from typing import Any

import httpx

IMMICH_API_KEY = os.getenv("IMMICH_API_KEY", "")
IMMICH_URL = os.getenv("IMMICH_URL", "")


class APIError(Exception):
    pass


def api_call(method: str, endpoint: str, data: dict[Any, Any] | None = None) -> dict[Any, Any]:
    res = httpx.request(
        method,
        IMMICH_URL + "/api/" + endpoint,
        headers={"x-api-key": IMMICH_API_KEY},
        json=data if method != "GET" else None,
        params=data if method == "GET" else None,
    )
    if not res.is_success:
        msg = f"API call failed: {res.status_code} {res.reason_phrase}"
        raise APIError(msg)
    if res.status_code == httpx.codes.NO_CONTENT:
        return {}
    return res.json()  # type: ignore[no-any-return]
