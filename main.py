import os
from http import HTTPStatus
from operator import itemgetter

import requests
from dotenv import load_dotenv

load_dotenv()
IMMICH_API_KEY = os.getenv("IMMICH_API_KEY")
IMMICH_URL = os.getenv("IMMICH_URL")
ARCHIVE_ALBUMS = os.getenv("ARCHIVE_ALBUMS", "").split(",")


def api_call(method: str, endpoint: str, data: dict | None = None) -> dict:
    res = requests.request(
        method,
        IMMICH_URL + "/api/" + endpoint,
        headers={"x-api-key": IMMICH_API_KEY},
        json=data,
        timeout=5,
    )
    if res.status_code == HTTPStatus.NO_CONTENT:
        return {}
    return res.json()


def main() -> None:
    to_archive = []
    for album_id in ARCHIVE_ALBUMS:
        album_info = api_call("GET", f"albums/{album_id}")
        to_archive.extend(map(itemgetter("id"), filter(lambda x: not x["isArchived"], album_info["assets"])))
    if to_archive:
        api_call("PUT", "assets", {"ids": to_archive, "isArchived": True})


if __name__ == "__main__":
    main()
