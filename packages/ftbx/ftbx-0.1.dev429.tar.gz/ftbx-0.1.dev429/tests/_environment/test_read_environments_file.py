"""

    PROJECT: flex_toolbox
    FILENAME: test_read_environments_file.py
    AUTHOR: David NAISSE
    DATE: August 13th, 2024

    DESCRIPTION: read_environments_file function testing
    
"""

from unittest import TestCase
from src._environment import Environment


class TestReadEnvironmentsFile(TestCase):

    def test_read_environments_file_valid(self):
        # ins
        env = Environment.read_environments_file()

        # tests
        assert isinstance(env, dict) and 'environments' in env
