"""
Test for conf_to_dict
"""
import unittest


class TestConfToDict(unittest.TestCase):

    def setUp(self):
        from ..conf_to_dict import ConfToDict
        self.c = ConfToDict('tests/test.txt', from_file=True)

    def test_initialization_with_correct_file_returns_a_list_of_config(self):
        self.assertIsInstance(self.c.config, list)
