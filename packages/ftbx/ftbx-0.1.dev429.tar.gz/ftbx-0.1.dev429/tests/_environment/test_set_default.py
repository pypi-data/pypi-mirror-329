"""

    PROJECT: flex_toolbox
    FILENAME: test_set_default.py
    AUTHOR: David NAISSE
    DATE: August 13th, 2024

    DESCRIPTION: set_default function testing
    
"""

from unittest import TestCase
from src._environment import Environment


class TestSetDefault(TestCase):

    def test_set_default_valid(self):
        # ins
        env = Environment.from_env_file(environment="cs-sbx")

        # outs
        env.set_default()

        # tests
        assert Environment.get_default_environment_alias() == "cs-sbx"
