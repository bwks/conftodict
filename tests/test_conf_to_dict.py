"""
Test for conf_to_dict
"""
import unittest

config = '''!
hostname TSTR01
!
boot-start-marker
boot-end-marker
!
!
logging buffered 16384
!'''


class TestConfToDict(unittest.TestCase):

    def setUp(self):
        from ..conf_to_dict import ConfToDict
        self.c = ConfToDict('tests/test.txt', from_file=True)

    def test_constructor_with_config_as_string_builds_a_list_of_config(self):
        from ..conf_to_dict import ConfToDict
        self.sc = ConfToDict(config)
        self.assertIsInstance(self.sc.config, list)

    def test_initialization_with_correct_file_builds_a_list_of_config(self):
        self.assertIsInstance(self.c.config, list)

    def test_initialization_with_non_existent_file_raises_file_not_found_error(self):
        from ..conf_to_dict import ConfToDict
        self.assertRaises(FileNotFoundError, ConfToDict, 'tests/no_file.txt', from_file=True)

    def test_no_elements_in_config_list_from_file_startswith_comments_or_new_line_chars(self):
        for i in self.c.config:
            self.assertIsNot(i, (i.startswith('!') or i.startswith(' !\n') or i.startswith('\n')))

    def test_no_elements_in_config_list_from_string_startswith_comments_or_new_line_chars(self):
        from ..conf_to_dict import ConfToDict
        self.sc = ConfToDict(config)
        for i in self.sc.config:
            self.assertIsNot(i, (i.startswith('!') or i == ' !' or i == ''))
