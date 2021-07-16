#!/usr/bin/env python

"""Tests for class FileSorter."""


import unittest
import uuid
import shutil

from files_to_folders.FileSorter import FileSorter

from pathlib import Path
import re

class Test_FileSorter(unittest.TestCase):
    """Tests for class FileSorter."""

    def setUp(self):
        self.path_testfolder = Path.cwd() / "tests" / "test_data"
        self.test_input_folder = self.path_testfolder / "test_input_folder"
        self.test_input_folder.mkdir(parents=True, exist_ok=True)
        self.test_output_folder = self.path_testfolder / "test_output_folder"
        self.test_output_folder.mkdir(parents=True, exist_ok=True)
        self._create_folders_and_files(self.test_input_folder)

    def _create_folders_and_files(self, input_folder:Path):
        folders = [ input_folder / str(uuid.uuid1()) for _ in range(2)]
        for folder in folders:
            folder.mkdir(parents=True)
            (folder / "test_123.txt").touch()
            (folder / "test_124.txt").touch()

    def tearDown(self):
        """Tear down test folder structure."""
        shutil.rmtree(self.path_testfolder)

    def test_regexes_have_invalid_type(self):
        """Invalid regex types raise a TypeError"""
        invalid_test_regexes = [
            [123],
            [123.123]
        ]

        for invalid_test_regex in invalid_test_regexes:
            with self.assertRaises(TypeError):
                FileSorter(invalid_test_regex)
    
    def test_regexes_have_valid_type(self):
        """Valid regex types shall raise nothing"""
        valid_test_regexes = [
            [".*"],
            [re.compile(".*")]
        ]

        for valid_test_regex in valid_test_regexes:
            try:
                FileSorter(valid_test_regex)
            except Exception as e:
                self.fail(f"No exception expected but {valid_test_regex=} raised the exception {e}.")
    
    def test_output_folder_has_invalid_type(self):
        """Invalid output folder type raises a TypeError"""
        invalid_output_folders = [
            123,
            123.123,
            [Path.cwd()]
        ]

        for invalid_output_folder in invalid_output_folders:
            with self.assertRaises(TypeError):
                FileSorter(regexes=[".*"], output_folder=invalid_output_folder)
    
    def test_output_folder_has_valid_type(self):
        """Valid output folder type raises nothing"""
        valid_output_folders = [
            Path.cwd(),
            "/"
        ]

        for valid_output_folder in valid_output_folders:
            try:
                FileSorter(regexes=[".*"], output_folder=valid_output_folder)
            except Exception as e:
                self.fail(f"No exception expected but {valid_output_folder=} raised the exception {e}.")
    
    def test_sort_function(self):
        """Valid, easy input for sort function works"""
        regexes = [r'([a-z]*)_([0-9]*).txt']
        fs = FileSorter(regexes, self.test_output_folder)
        fs.sort(list(self.test_input_folder.rglob('*.txt')))

        output_folder_files = set(file for file in self.test_output_folder.rglob('*') if file.is_file())
        correct_output_folder_structure = {
            self.test_output_folder / "test" / "124" / "test_124.txt",
            self.test_output_folder / "test" / "123" / "test_123.txt",
        }

        self.assertEqual(output_folder_files, correct_output_folder_structure)

