"""

    PROJECT: flex_toolbox
    FILENAME: test_from_env_file.py
    AUTHOR: David NAISSE
    DATE: August 13th, 2024

    DESCRIPTION: from_env_file function testing
    
"""

from unittest import TestCase
from src._environment import Environment


class TestFromEnvFile(TestCase):

    def test_from_env_file_valid(self):
        # ins
        env = Environment.from_env_file(environment="cs-sbx")

        # tests
        assert env.name and env.url and env.username and env.version and env.password

    def test_from_env_file_invalid(self):
        # outs
        try:
            Environment.from_env_file(environment='does-not-exist')
            self.fail()
        except SystemExit:
            pass
        except:
            self.fail()
