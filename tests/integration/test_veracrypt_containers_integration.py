#!/usr/bin/env python
# -*- coding: utf-8 -*-


""" 
Integration test cases for the VeracryptContainer class.
"""

import os
import asyncio
import unittest
from pathlib import Path
from typing import List
from parameterized import parameterized

from simple_veracrypt_container_interface.veracrypt_container import VeracryptContainer
from simple_veracrypt_container_interface.utilities.utilities import available_drive_letters, is_mounted


# ****************
# Gets environment variable for executable path
VERACRYPT_PATH = os.environ.get("VERACRYPT_PATH")
if VERACRYPT_PATH is not None:
    VERACRYPT_PATH = Path(VERACRYPT_PATH)

# ****************
@unittest.skipIf(VERACRYPT_PATH is None, "Veracrypt executable environment variable not set.")
class TestVeracryptContainerIntegration(unittest.TestCase):
    
    veracrypt_containers: List[VeracryptContainer] = [
        # (test_case_name, container_path, mount_letter, password, keyfile_path)

        ## EXFAT
        # Password only
        ("exfat_password_only",
            {
                "executable_path": VERACRYPT_PATH,
                "container_path": Path(__file__).resolve().parent / "veracrypt_volumes" / "exfat" / "password_only" / "veracrypt_volume_test_password.hc",
                "mount_letter": 'T',
                "password": "Password",
            }
        ),
        
        # Keyfile only
        ("exfat_keyfile_only",
            {
                "executable_path": VERACRYPT_PATH,
                "container_path": Path(__file__).resolve().parent / "veracrypt_volumes" / "exfat" / "keyfile_only" / "veracrypt_volume_test_keyfile.hc",
                "mount_letter": 'T',
                "keyfile_path": Path(__file__).resolve().parent / "veracrypt_volumes" / "exfat" / "keyfile_only" / "keyfile"
            }
        ),
        
        # Password and Keyfile
        ("exfat_password_and_keyfile",
            {
                "executable_path": VERACRYPT_PATH,
                "container_path": Path(__file__).resolve().parent / "veracrypt_volumes" / "exfat" / "password_and_keyfile" / "veracrypt_volume_test_password_and_keyfile.hc",
                "mount_letter": 'T',
                "password": "Password",
                "keyfile_path": Path(__file__).resolve().parent / "veracrypt_volumes" / "exfat" / "password_and_keyfile" / "keyfile"
            }
        )
    ]
    
    def tearDown(self):
        # Ensures all containers are dismounted
        if is_mounted(Path(f"{self.container.mount_letter}:\\")):
            asyncio.run(self.container.dismount(self.container.password))

    # ****************
    # Mount tests
    @parameterized.expand(veracrypt_containers)
    @unittest.skipIf(len(available_drive_letters()) == 0, "No available drive letters.")
    def test_mount_password(self, name, params):
        self.container = VeracryptContainer(**params)
        
        # Ensures that the container is currently not mounted
        if is_mounted(Path(f"{self.container.mount_letter}:\\")):
            self.container.mount_letter = available_drive_letters().pop()
        self.assertFalse(is_mounted(Path(f"{self.container.mount_letter}:\\")))

        # Mounts the container
        try:
            asyncio.run(self.container.mount())
        except Exception as e:
            self.fail(f"Mounting the container failed: {e}")
            
        # Ensures that the container is now mounted
        self.assertTrue(is_mounted(Path(f"{self.container.mount_letter}:\\")))

        # Ensures the the container dismounts
        try:
            asyncio.run(self.container.dismount())
        except Exception as e:
            self.fail(f"Dismounting the container failed: {e}")
        
        # Verify the container is no longer mounted
        self.assertFalse(is_mounted(Path(f"{self.container.mount_letter}:\\")))


# ****************
if __name__ == "__main__":
    unittest.main()
    