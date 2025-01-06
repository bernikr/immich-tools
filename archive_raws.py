
from api import api_call
from log import log

RAW_EXTENSIONS = [".rw2", ".dng"]

if __name__ == "__main__":
    files = {}
    paths = api_call("GET", "view/folder/unique-paths")
    for i, path in enumerate(paths):
        if i % 10 == 0:
            log(f"Collecting folder {i + 1}/{len(paths)}")
        assets = api_call("GET", "view/folder", data={"path": path})
        files |= {asset["originalPath"].lower(): asset["id"] for asset in filter(lambda x: not x["isArchived"], assets)}
    log(f"Found {len(files)} files")
    raws = set(filter(lambda x: x.endswith(tuple(RAW_EXTENSIONS)), files.keys()))
    log(f"Found {len(raws)} raws ({",".join(RAW_EXTENSIONS)})")
    to_archive = set(filter(lambda x: (x[:-3] + "jpg") in files, raws))  # TODO: better way to find jpgs
    log(f"Found {len(to_archive)} raws to archive")
    if to_archive:
        log("Archiving raws...")
        api_call("PUT", "assets", {"ids": [files[x] for x in to_archive], "isArchived": True})
