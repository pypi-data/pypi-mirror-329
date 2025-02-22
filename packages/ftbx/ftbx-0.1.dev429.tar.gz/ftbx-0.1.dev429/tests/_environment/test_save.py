"""

    PROJECT: flex_toolbox
    FILENAME: test_save.py
    AUTHOR: David NAISSE
    DATE: August 13th, 2024

    DESCRIPTION: save function testing
    
"""

from unittest import TestCase
from src._environment import Environment


class TestSave(TestCase):

    def test_save_valid(self):
        # ins
        env = Environment.from_env_file(environment="cs-sbx")

        # outs
        env.save()
        saved_env = Environment.from_env_file(environment="cs-sbx")

        # tests
        for e in [env, saved_env]:
            e.__dict__.pop('session')
            e.__dict__.pop('consul')
            e.__dict__.pop('database')
            e.__dict__.pop('rabbitmq')
        assert env.__dict__ == saved_env.__dict__
