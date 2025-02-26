#!/usr/bin/env python3
"""
 support functions

 Copyright (c) 2023 ROX Automation - Jev Kuznetsov
"""
import asyncio
import logging
import os
from functools import wraps
from pathlib import Path
from typing import Any, Coroutine

import can
import cantools
import coloredlogs  # type: ignore

LOG_FORMAT = "%(asctime)s [%(name)s] %(filename)s:%(lineno)d - %(message)s"
TIME_FORMAT = "%H:%M:%S.%f"

DEFAULT_DBC = "odrive-cansimple-0.6.10"


def get_axis_id(msg: can.Message) -> int:
    """get axis id from message"""
    return msg.arbitration_id >> 5


def extract_ids(can_id: int) -> tuple[int, int]:
    """get axis_id and cmd_id from can_id"""
    cmd_id = can_id & 0x1F  # Extract lower 5 bits for cmd_id
    axis_id = can_id >> 5  # Shift right by 5 bits to get axis_id
    return axis_id, cmd_id


# pylint: disable=import-outside-toplevel
def get_dbc(name: str = DEFAULT_DBC):
    """get the cantools database"""

    # get relative path to db file
    dbc_path = Path(__file__).parent / f"dbc/{name}.dbc"

    return cantools.database.load_file(dbc_path.as_posix())


def get_dbc_path(name: str = DEFAULT_DBC) -> Path:
    """get the path to the dbc file"""
    return Path(__file__).parent / f"dbc/{name}.dbc"


def run_main_async(
    coro: Coroutine[Any, Any, None], silence_loggers: list[str] | None = None
) -> None:
    """convenience function to avoid code duplication"""
    loglevel = os.environ.get("LOGLEVEL", "INFO").upper()
    coloredlogs.install(level=loglevel, fmt=LOG_FORMAT)
    logging.info(f"Log level set to {loglevel}")

    if silence_loggers:
        for logger in silence_loggers:
            logging.info(f"Silencing logger: {logger}")
            logging.getLogger(logger).setLevel(logging.CRITICAL)

    try:
        asyncio.run(coro)
    except KeyboardInterrupt:
        pass
    except ExceptionGroup as group:
        logging.error("ExceptionGroup caught")
        for e in group.exceptions:  # pylint: disable=not-an-iterable
            logging.exception(f"Caught exception: {e}", exc_info=e)
    except asyncio.CancelledError:
        logging.error("Cancelled")

    except Exception as e:
        logging.error(f"Crashed with {e},  type: {type(e)}", exc_info=e)


def async_timeout(timeout: float = 1.0):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await asyncio.wait_for(func(*args, **kwargs), timeout)
            except asyncio.TimeoutError:
                func_name = func.__name__
                # Include the function name in the error message
                raise TimeoutError(f"{func_name} timed out after {timeout} seconds")

        return wrapper

    return decorator
