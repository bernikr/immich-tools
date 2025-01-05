import os
from operator import itemgetter

from api import api_call

ARCHIVE_ALBUMS = os.getenv("ARCHIVE_ALBUMS", "").split(",")


if __name__ == "__main__":
    to_archive = []
    for album_id in ARCHIVE_ALBUMS:
        album_info = api_call("GET", f"albums/{album_id}")
        to_archive.extend(map(itemgetter("id"), filter(lambda x: not x["isArchived"], album_info["assets"])))
    if to_archive:
        api_call("PUT", "assets", {"ids": to_archive, "isArchived": True})
