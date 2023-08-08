#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script showcases how commands can be wrapped and added to the command queue using an event handler.
Set proper values for the variables used to initialize the VERACRYPT_CONTAINER instance below before running this script.
"""

import logging
import asyncio
from pathlib import Path

# Adds package to path
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from simple_veracrypt_container_interface.veracrypt_container import VeracryptContainer
from simple_veracrypt_container_interface.utilities.exceptions import AlreadyDismountedError, AlreadyMountedError

VERACRYPT_CONTAINER = VeracryptContainer(
    executable_path = Path(f"path/to/veracrypt.exe"),
    container_path = Path(f"path/to/veracrypt_container.hc"),
    mount_letter = "T",
    password = "Password",
)

# **********
# Sets up logger
logger = logging.getLogger(__name__)

PROGRAM_LOG_FILE_PATH = Path(__file__).resolve().parent.parent / "program_log.txt"

LOGGER_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,  # Doesn't disable other loggers that might be active
    "formatters": {
        "default": {
            "format": "[%(levelname)s][%(funcName)s] | %(asctime)s | %(message)s",
        },
        "simple": {  # Used for console logging
            "format": "[%(levelname)s][%(funcName)s] | %(message)s",
        },
    },
    "handlers": {
        "logfile": {
            "class": "logging.FileHandler",  # Basic file handler
            "formatter": "default",
            "level": "INFO",
            "filename": PROGRAM_LOG_FILE_PATH.as_posix(),
            "mode": "a",
            "encoding": "utf-8",
        },
        "console_stdout": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "level": "DEBUG",
            "stream": "ext://sys.stdout",
        },
        "console_stderr": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "level": "ERROR",
            "stream": "ext://sys.stderr",
        },
    },
    "root": {  # Simple program, so root logger uses all handlers
        "level": "DEBUG",
        "handlers": [
            "logfile",
            "console_stdout",
            "console_stderr",
        ]
    }
}


# **********
async def mount_veracrypt_container():
    """Attempts to mount the VeraCrypt container. If the container is already mounted, the function will continue."""
    try:
        await VERACRYPT_CONTAINER.mount()
    except AlreadyMountedError:
        logger.warning(f"Veracrypt container at {VERACRYPT_CONTAINER.container_path} is already mounted. Continuing...")


async def dismount_veracrypt_container():
    """Attempts to dismount the VeraCrypt container. If the container is already dismounted, the function will continue."""
    try:
        await VERACRYPT_CONTAINER.dismount()
    except AlreadyDismountedError:
        logger.warning(f"Veracrypt container at {VERACRYPT_CONTAINER.container_path} is already dismounted. Continuing...")


# **********
if __name__ == "__main__":
    import logging.config
    logging.disable(logging.DEBUG)
    logging.config.dictConfig(LOGGER_CONFIG)
    asyncio.run(mount_veracrypt_container())
    