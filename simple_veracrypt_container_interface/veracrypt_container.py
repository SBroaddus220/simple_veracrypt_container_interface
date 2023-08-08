#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module contains the VeracryptContainer class, which is used to mount and dismount Veracrypt containers.
"""

import logging
from pathlib import Path
from typing import Optional
from simple_async_command_manager.commands.command_bases import SubprocessCommand

from simple_veracrypt_container_interface.utilities import utilities, exceptions


# **********
# Sets up logger
logger = logging.getLogger(__name__)

# **********
class VeracryptContainer:
    """Represents a Veracrypt container that can be mounted and dismounted."""
    
    
    def __init__(self, executable_path: Path, container_path: Path, mount_letter: str, password: Optional[str] = None, keyfile_path: Optional[Path] = None):
        """Instantiates a new VeracryptContainer object.

        Args:
            veracrypt_executable_path (Path): Path to the Veracrypt executable.
            container_path (Path): Path to the Veracrypt container.
            mount_letter (str): Mount letter for the Veracrypt container.
            password (Optional[str], optional): Password for the Veracrypt container if there is one. Defaults to None.
            keyfile_path (Optional[Path], optional): Path to the keyfile for the Veracrypt container if there is one. Defaults to None.
        """
        self.executable_path = executable_path
        self.container_path = container_path
        self.mount_letter = mount_letter
        self.password = password
        self.keyfile_path = keyfile_path
        
        #: SubprocessCommand object to mount the Veracrypt container.
        self.subprocess_mount_command: Optional[SubprocessCommand] = None
        
        #: SubprocessCommand object to dismount the Veracrypt container.
        self.subprocess_dismount_command: Optional[SubprocessCommand] = None
        
        # Ensures executable exists
        logger.info(f"Checking if Veracrypt executable exists at `{self.executable_path}`.")
        if self.executable_path is None or not (self.executable_path.stat().st_mode & 0o111):
            raise EnvironmentError(f"Veracrypt executable not found at `{self.executable_path}`.")
        
    
    def prepare_mount_subprocess(self) -> SubprocessCommand:
        """Prepares the SubprocessCommand to mount the Veracrypt container.

        Raises:
            FileNotFoundError: If the Veracrypt container is not found.
            FileNotFoundError: If the Veracrypt keyfile is not found.
            AlreadyMountedError: If the Veracrypt container is already mounted.

        Returns:
            SubprocessCommand: SubprocessCommand object to mount the Veracrypt container.
        """
        
        if not self.container_path.exists():
            raise FileNotFoundError(f"Container at {self.container_path} not found.")
        if self.keyfile_path and not self.keyfile_path.exists():
            raise FileNotFoundError(f"Keyfile at {self.keyfile_path} not found.")
        
        if utilities.is_mounted(Path(f"{self.mount_letter}:\\")):
            raise exceptions.AlreadyMountedError(f"Drive {self.mount_letter} is already mounted.")

        logger.info(f"Preparing to mount Veracrypt container at `{self.container_path}`.")
        
        # Command to mount the Veracrypt container
        command = [
            self.executable_path,
            "/volume", self.container_path.absolute(),
            "/letter", self.mount_letter,
            "/silent",
            "/auto",
            "/quit",
        ]
        
        if self.keyfile_path:
            command.extend(["/keyfile", self.keyfile_path.absolute()])
    
        if self.password:
            command.extend(["/password", self.password])
        else:
            command.append("/tryemptypass")
        
        self.subprocess_mount_command = SubprocessCommand(command)
        
        return self.subprocess_mount_command
        
        
    async def mount(self, print_output: bool = True) -> None:
        """Mounts the Veracrypt drive.

        Args:
            print_output (bool, optional): Whether to print the output to the console. Defaults to True.
        """
        self.prepare_mount_subprocess()
        logger.info(f"Mounting Veracrypt container at `{self.container_path}`.")
        await self.subprocess_mount_command.run(print_output=print_output)
        
        
    def prepare_dismount_subprocess(self) -> SubprocessCommand:
        """Prepares the SubprocessCommand to dismount the Veracrypt container.

        Raises:
            FileNotFoundError: If the Veracrypt container is not found.
            AlreadyDismountedError: If the Veracrypt container is not mounted.

        Returns:
            SubprocessCommand: SubprocessCommand object to dismount the Veracrypt container.
        """
        if not self.container_path.exists():
            raise FileNotFoundError(f"Container at {self.container_path} not found.")
        if not utilities.is_mounted(Path(f"{self.mount_letter}:\\")):
            raise exceptions.AlreadyDismountedError(f"Drive {self.mount_letter} is not mounted.")
        
        logger.info(f"Preparing to dismount Veracrypt container at `{self.container_path}`.")
        
        # Command to dismount the Veracrypt container
        command = [
            self.executable_path,
            "/volume", self.container_path.absolute(),
            "/dismount", self.mount_letter,
            "/force",
            "/silent",
            "/quit",
        ]
        
        self.subprocess_dismount_command = SubprocessCommand(command)
        
        return self.subprocess_dismount_command
    
    
    async def dismount(self, print_output: bool = True) -> None:
        """Disounts the Veracrypt drive.

        Args:
            print_output (bool, optional): Whether to print the output to the console. Defaults to True.
        """
        self.prepare_dismount_subprocess()
        logger.info(f"Dismounting Veracrypt container at `{self.container_path}`.")
        await self.subprocess_dismount_command.run(print_output=print_output)
    
    
# **********
if __name__ == "__main__":
    pass
