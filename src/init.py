from collections.abc import Awaitable, Callable

from apscheduler import AsyncScheduler
from apscheduler.abc import Trigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

scheduler = AsyncScheduler()

Job = Callable[[], Awaitable[None] | None]

_scheduled_jobs: list[tuple[Job, Trigger]] = []


def schedule[T: Job](trigger: Trigger | str | int) -> Callable[[T], T]:
    if isinstance(trigger, str):
        trigger = CronTrigger.from_crontab(trigger)
    elif isinstance(trigger, int):
        trigger = IntervalTrigger(minutes=trigger)

    def decorator(func: T) -> T:
        _scheduled_jobs.append((func, trigger))
        return func

    return decorator


async def run() -> None:
    async with scheduler:
        for func, trigger in _scheduled_jobs:
            await scheduler.add_schedule(func, trigger)
    await scheduler.run_until_stopped()
