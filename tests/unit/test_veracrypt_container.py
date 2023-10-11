#!/usr/bin/env python
# -*- coding: utf-8 -*-


""" 
Test cases for the VeracryptContainer class.
"""

import asyncio
from pathlib import Path

import unittest
from unittest import mock
from unittest.mock import AsyncMock, MagicMock, PropertyMock

from simple_veracrypt_container_interface.veracrypt_container import VeracryptContainer

# ****************
class TestVeracryptSetup(unittest.TestCase):
    
    # ****************
    def setUp(self):
        
        # Mocks the Veracrypt executable
        self.VERACRYPT_PATH = MagicMock(spec=Path)
        type(self.VERACRYPT_PATH).stat = PropertyMock(return_value=MagicMock(st_mode=0o700))
    
        # Generic container instance
        container_path = Path('/fake/path')
        mount_letter = 'Z'
        self.veracrypt_container = VeracryptContainer(self.VERACRYPT_PATH, container_path, mount_letter)
    
    
    # ****************
    # Prepare mount subprocess tests
    def test_prepare_mount_subprocess_command_setup(self):
        # Arrange
        expected_command = [
            self.VERACRYPT_PATH,
            "/volume", self.veracrypt_container.container_path.absolute(),
            "/letter", self.veracrypt_container.mount_letter,
            "/silent",
            "/auto",
            "/quit",
            "/tryemptypass",
        ]

        with mock.patch('asyncio.create_subprocess_exec', new=mock.MagicMock()) as mock_subprocess, \
            mock.patch('pathlib.Path.exists', return_value=True), \
            mock.patch('simple_veracrypt_container_interface.utilities.utilities.is_mounted', return_value=False):
            # Act
            command = self.veracrypt_container.prepare_mount_subprocess()

            # Assert
            self.assertEqual(command, expected_command)
    
    
    def test_prepare_mount_subprocess_incorrect_container_path(self):
        # Arrange
        with mock.patch('pathlib.Path.exists', return_value=False):
            # Act & Assert
            with self.assertRaises(FileNotFoundError):
                self.veracrypt_container.prepare_mount_subprocess()


    def test_prepare_mount_subprocess_idempotence(self):
        # Arrange
        with mock.patch('pathlib.Path.exists', return_value=True), \
            mock.patch('asyncio.create_subprocess_exec', new=mock.MagicMock()), \
            mock.patch('simple_veracrypt_container_interface.utilities.utilities.is_mounted', return_value=False):

            # Act
            command1 = self.veracrypt_container.prepare_mount_subprocess()
            command2 = self.veracrypt_container.prepare_mount_subprocess()

            # Assert
            self.assertEqual(command1, command2)
    
    
    # ****************
    # Mount tests
    def test_mount_method(self):
        # Arrange
        with mock.patch('simple_veracrypt_container_interface.utilities.utilities.run_command', return_value=None) as mock_run_command, \
            mock.patch('pathlib.Path.exists', return_value=True), \
            mock.patch('asyncio.create_subprocess_exec', new=mock.MagicMock()), \
            mock.patch('simple_veracrypt_container_interface.utilities.utilities.is_mounted', return_value=False):
            # Act
            asyncio.run(self.veracrypt_container.mount())

            # Assert
            mock_run_command.assert_called_once()
    
    
    def test_mount_method_prepares_subprocess(self):
        # Arrange
        mock_subprocess_command = mock.MagicMock()
        mock_subprocess_command.__iter__.return_value = iter([])  # Mocks iterable property of command
        
        # Manually sets the attribute to the required value to simulate prepare sync subprocess call
        def side_effect():
            self.veracrypt_container.subprocess_mount_command = mock_subprocess_command
            return mock_subprocess_command

        with mock.patch('simple_veracrypt_container_interface.utilities.utilities.run_command', return_value=None) as mock_run_command, \
            mock.patch('pathlib.Path.exists', return_value=True), \
            mock.patch.object(VeracryptContainer, 'prepare_mount_subprocess', side_effect=side_effect) as mock_prepare_mount_subprocess, \
            mock.patch('simple_veracrypt_container_interface.utilities.utilities.is_mounted', return_value=False):

            # Act
            asyncio.run(self.veracrypt_container.mount())

            # Assert
            mock_prepare_mount_subprocess.assert_called_once()
            mock_run_command.assert_called_once()


    # ****************
    # Prepare dismount subprocess test
    def test_prepare_dismount_subprocess_command_setup(self):
        
        # Arrange
        expected_command = [
            self.VERACRYPT_PATH,
            "/volume", self.veracrypt_container.container_path.absolute(),
            "/dismount", self.veracrypt_container.mount_letter,
            "/force",
            "/silent",
            "/quit",
        ]

        with mock.patch('asyncio.create_subprocess_exec', new=mock.MagicMock()) as mock_subprocess, \
            mock.patch('pathlib.Path.exists', return_value=True), \
            mock.patch('simple_veracrypt_container_interface.utilities.utilities.is_mounted', return_value=True):
            # Act
            command = self.veracrypt_container.prepare_dismount_subprocess()

            # Assert
            self.assertEqual(command, expected_command)
    
    
    def test_prepare_dismount_subprocess_incorrect_container_path(self):
        # Arrange
        with mock.patch('pathlib.Path.exists', return_value=False):
            # Act & Assert
            with self.assertRaises(FileNotFoundError):
                self.veracrypt_container.prepare_dismount_subprocess()


    def test_prepare_dismount_subprocess_idempotence(self):
        # Arrange
        with mock.patch('pathlib.Path.exists', return_value=True), \
            mock.patch('asyncio.create_subprocess_exec', new=mock.MagicMock()), \
            mock.patch('simple_veracrypt_container_interface.utilities.utilities.is_mounted', return_value=True):

            # Act
            command1 = self.veracrypt_container.prepare_dismount_subprocess()
            command2 = self.veracrypt_container.prepare_dismount_subprocess()

            # Assert
            self.assertEqual(command1, command2)
    
    # ****************
    # Mount tests
    def test_dismount_method(self):
        # Arrange
        with mock.patch('simple_veracrypt_container_interface.utilities.utilities.run_command', return_value=None) as mock_run_command, \
            mock.patch('pathlib.Path.exists', return_value=True), \
            mock.patch('asyncio.create_subprocess_exec', new=mock.MagicMock()), \
            mock.patch('simple_veracrypt_container_interface.utilities.utilities.is_mounted', return_value=True):
            # Act
            asyncio.run(self.veracrypt_container.dismount())

            # Assert
            mock_run_command.assert_called_once()
    
    
    def test_dismount_method_prepares_subprocess(self):
        # Arrange
        mock_subprocess_command = mock.MagicMock()
        mock_subprocess_command.__iter__.return_value = iter([])  # Mocks iterable property of command

        # Manually sets the attribute to the required value to simulate prepare sync subprocess call
        def side_effect():
            self.veracrypt_container.subprocess_dismount_command = mock_subprocess_command
            return mock_subprocess_command

        with mock.patch('simple_veracrypt_container_interface.utilities.utilities.run_command', return_value=None) as mock_run_command, \
            mock.patch('pathlib.Path.exists', return_value=True), \
            mock.patch.object(VeracryptContainer, 'prepare_dismount_subprocess', side_effect=side_effect) as mock_prepare_dismount_subprocess:

            # Act
            asyncio.run(self.veracrypt_container.dismount())

            # Assert
            mock_prepare_dismount_subprocess.assert_called_once()
            mock_run_command.assert_called_once()



# ****************
if __name__ == '__main__':
    unittest.main()