"""

    PROJECT: flex_toolbox
    FILENAME: test_connect.py
    AUTHOR: David NAISSE
    DATE: August 13th, 2024

    DESCRIPTION: connect function testing
    
"""

from unittest import TestCase
from src._environment import Environment


class TestConnect(TestCase):

    def test_connect_valid(self):
        # ins
        env = Environment.from_env_file(environment="cs-sbx")

        try:
            env.connect()
        except:
            self.fail()
