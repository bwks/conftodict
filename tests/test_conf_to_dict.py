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
!
end
!'''

three_level = '''!
policy-map QOS_CATEGORIES
 class QOS_VOICE_RTP
  priority percent 20
  set ip dscp ef
 class QOS_ROUTING
  bandwidth percent 1
  set ip dscp cs6
 class QOS_MGMT
  bandwidth percent 1
  set ip dscp cs5
 class QOS_BUSINESS_APPS
  bandwidth percent 40
  set ip dscp af41
 class QOS_VIDEO_RTP
  bandwidth percent 25
  set ip dscp af31
 class QOS_SIGNALLING
  bandwidth percent 5
  set ip dscp af31
 class class-default
  set ip dscp default
  fair-queue
  random-detect
!
end
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

    def test_three_level_hierarchy_contains_list_for_second_level(self):
        from ..conf_to_dict import ConfToDict
        self.three_level = ConfToDict(three_level)
        conf_dict = self.three_level.conf_to_dict()

        self.assertIsInstance(conf_dict['policy-map QOS_CATEGORIES'], list)

