from celery import Celery
from celery.schedules import schedule
from dreema.helpers import getenv
import asyncio

REDIS_HOST = getenv("REDIS_HOST")
REDIS_PORT = getenv("REDIS_PORT")
REDIS_PASSWORD = getenv("REDIS_PASSWORD")
REDIS_AUTH = f":{REDIS_PASSWORD}@" if REDIS_PASSWORD else ""

# Redis DB 1 for broker, DB 2 for result backend
broker = f"redis://{REDIS_AUTH}{REDIS_HOST}:{REDIS_PORT}/1"
backend = f"redis://{REDIS_AUTH}{REDIS_HOST}:{REDIS_PORT}/1"

scheduler = Celery("dreemuni", broker=broker, backend=backend)

scheduler.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    broker_connection_max_retries=30,
)

# scheduler.conf.beat_schedule = {
#     "RepeatableJob": {
#         "task": "RepeatableJob",
#         "schedule": 60.0,  # every 10 seconds
#         "args": (),
#     },
#     # "UpdateNotf": {
#     #     "task": "UpdateNotf",
#     #     "schedule": 120.0,  # every 60 seconds
#     #     "args": (),
#     # }
# }



def runAsyncJob(coroutine):
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        # Use Thread-safe future blocking
        return asyncio.run_coroutine_threadsafe(coroutine, loop).result()
    else:
        return asyncio.run(coroutine)

from .jobs import *
