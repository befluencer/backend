"""

Use:
    serves as the entry point for the application
    Runs uvicorn as the main server and parse all
    information required to index.py for processing
"""

import sys
import uvicorn
from dreema.helpers import getenv

# autoparse function arguments to the the config
def autoParse():
    result = {"port": int(getenv('RUNNING_PORT')), "reload": True, "log_level": "debug", "host": "127.0.0.1"}
    for arg in sys.argv[1:]:
        split = arg.split("=")
        if len(split) < 2:
            continue

        result[f"{split[0]}"] = split[1]
    return result


if __name__ == "__main__":
    parser = autoParse()
    config = uvicorn.run(
        "index:app",
        port=int(getenv('RUNNING_PORT')),
        host='0.0.0.0',
        workers=4,
        reload=parser['reload'],
        log_level=parser["log_level"],
    )


# COMMAND TO START CELERY
# celery -A dreema.scheduler.setup.scheduler worker --loglevel=info
# celery -A dreema.scheduler.setup.scheduler beat --loglevel=info
