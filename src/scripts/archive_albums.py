import logging
import os
from operator import itemgetter

from common.api import api_call
from init import schedule

ARCHIVE_ALBUMS = os.getenv("ARCHIVE_ALBUMS", "").split(",")
DO_NOT_ARCHIVE = os.getenv("DO_NOT_ARCHIVE")

logger = logging.getLogger(__name__)
log = logger.info


@schedule(15)  # every 15 minutes
def main() -> None:
    log("Starting archiving")

    do_not_archive: list[str] = []
    if DO_NOT_ARCHIVE:
        album_info = api_call("GET", f"albums/{DO_NOT_ARCHIVE}")
        do_not_archive.extend(map(itemgetter("id"), album_info["assets"]))
        log(f"Found {len(do_not_archive)} assets that are safe from archiving")

        to_unarchive = list(map(itemgetter("id"), filter(itemgetter("isArchived"), album_info["assets"])))
        if to_unarchive:
            log(f"Found {len(to_unarchive)} assets that are already archived, but should be safe")
            log("Unarchiving assets...")
            api_call("PUT", "assets", {"ids": to_unarchive, "isArchived": False})

    to_archive: list[str] = []
    for album_id in ARCHIVE_ALBUMS:
        album_info = api_call("GET", f"albums/{album_id}")
        to_archive.extend(map(itemgetter("id"), filter(lambda x: not x["isArchived"], album_info["assets"])))
    to_archive = list(set(to_archive) - set(do_not_archive))
    log(f"Found {len(to_archive)} new assets to archive")
    if to_archive:
        log("Archiving assets...")
        api_call("PUT", "assets", {"ids": to_archive, "isArchived": True})
