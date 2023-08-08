#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module contains custom exceptions for the package.
"""

# **********
class AlreadyMountedError(Exception):
    """Raised when a container, file system, or drive is already mounted."""
    pass


class AlreadyDismountedError(Exception):
    """Raised when a container, file system, or drive is already dismounted."""
    pass


# **********
if __name__ == "__main__":
    pass
