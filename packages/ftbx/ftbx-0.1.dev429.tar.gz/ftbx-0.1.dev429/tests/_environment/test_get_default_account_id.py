"""

    PROJECT: flex_toolbox
    FILENAME: test_get_default_account_id.py
    AUTHOR: David NAISSE
    DATE: August 13th, 2024

    DESCRIPTION: get_default_account_id function testing
    
"""

from unittest import TestCase
from src._environment import Environment


class TestGetDefaultAccountId(TestCase):

    def test_get_default_account_id_valid(self):
        # ins
        env = Environment.from_env_file(environment='cs-sbx')

        # outs
        acc_id = env.get_default_account_id() 

        # tests
        assert acc_id == 203
