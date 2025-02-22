"""

    PROJECT: flex_toolbox
    FILENAME: test_get_default_environment_alias.py
    AUTHOR: David NAISSE
    DATE: August 13th, 2024

    DESCRIPTION: get_default_environment_alias function testing
    
"""

from unittest import TestCase
from src._environment import Environment


class TestGetDefaultEnvironmentAlias(TestCase):

    def test_get_default_environment_alias_valid(self):
        # ins
        default_alias = Environment.get_default_environment_alias()

        # tests
        assert default_alias == 'cs-sbx'
