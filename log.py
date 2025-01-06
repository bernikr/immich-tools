import inspect
from datetime import datetime
from pathlib import Path


def log(msg: str) -> None:
    frame = inspect.stack()[1]
    print(f"{datetime.now()} [{Path(frame.filename).name}:{frame.lineno}] {msg}")  # noqa: DTZ005
