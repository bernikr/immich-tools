from __future__ import annotations

import asyncio
import importlib
import logging
import os
import pkgutil
from typing import TYPE_CHECKING

from init import run

if TYPE_CHECKING:
    from types import ModuleType

VERSION = os.getenv("VERSION", "dev")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)-30s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


def import_submodules(package: str | ModuleType) -> dict[str, ModuleType]:
    if isinstance(package, str):
        package = importlib.import_module(package)
    results = {}
    for _, name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = package.__name__ + "." + name
        try:
            results[full_name] = importlib.import_module(full_name)
        except ModuleNotFoundError:
            continue
        if is_pkg:
            results.update(import_submodules(full_name))
    return results


modules = import_submodules("scripts")
logger.info("Loaded %i modules: %s", len(modules), ", ".join(modules.keys()))


if __name__ == "__main__":
    logger.info(f"Starting immich-tools version {VERSION}")
    asyncio.run(run())
