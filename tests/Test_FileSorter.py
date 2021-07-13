#!/usr/bin/env python

"""Tests for class FileSorter."""


import unittest

from files_to_folders.FileSorter import FileSorter

from pathlib import Path
import re

class Test_FileSorter(unittest.TestCase):
    """Tests for class FileSorter."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

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
