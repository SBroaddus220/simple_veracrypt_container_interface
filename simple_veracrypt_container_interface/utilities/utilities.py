#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module holds utilities used by other modules.
"""

import os
import string
import logging
from typing import Set
from pathlib import Path


# **********
# Sets up logger
logger = logging.getLogger(__name__)

# **********
def available_drive_letters() -> Set[str]:
    """Fetches a set of available drive letters for the system.

    Returns:
        Set[str]: Set of available drive letters.
    """
    logger.info("Fetching available drive letters.")
    return {letter for letter in string.ascii_uppercase if not os.path.exists(letter + ":\\")}


def is_mounted(path: Path) -> bool:
    """Checks if a path is exists and is a mount for a file system.

    Args:
        path (Path): Path to check.

    Returns:
        bool: Whether the path is mounted.
    """
    logger.info(f"Checking if path is mounted: {path}")
    return os.path.ismount(path) and path.exists()


# **********
if __name__ == "__main__":
    pass
