#!/usr/bin/env python

"""Tests for `files_to_folders` package."""


import unittest
from click.testing import CliRunner

from files_to_folders import cli

from pathlib import Path

class Test_CLI(unittest.TestCase):
    def test_command_line_interface(self):
        """Test if the CLI starts properly."""
        runner = CliRunner()
        result = runner.invoke(cli.main, ['--regexes', '.*', Path.cwd().as_posix(),])
        assert result.exit_code == 0
