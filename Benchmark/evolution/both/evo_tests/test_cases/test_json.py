__author__ = 'Edwin Cowart, Kevin McDonough'

import glob
import io
import os
import unittest
import xattack
import xfeed
import xstep
import xstep4
import xsilly
from evo_tests.constants import *
from evo_tests.data_defs import remove_white_space, evo_tests_path

SKIP_FILES = []


def is_skip_file(filename):
    """ Should the given file be skipped over for testing
    :param filename: The file's name
    :type filename: String
    :return: True if the given file should be skipped, false otherwise
    :rtype: Boolean
    """
    filename_len = len(filename)
    for skip_name in SKIP_FILES:
        skip_name_len = len(skip_name)
        if (skip_name_len <= filename_len) and (
            skip_name == filename[-skip_name_len:]):
            return True

    return False


class Test_JSON(unittest.TestCase):
    def _test_json_in_directory(self, dir_name, process_json_function):
        """ Test the processed json in_files against their expected results
        :param dir_name: The name of the directory containing the json files
        :type dir_name: String
        :param process_json_function: The json in_file processor function
        :type process_json_function: json->json
        :return None
        """
        num_tests_run = 0
        for in_filename in glob.glob(
                os.path.join(evo_tests_path, dir_name, '*-' + IN_JSON)):
            # Skip Condition
            if is_skip_file(in_filename):
                continue

            in_file = open(in_filename)
            out_file = io.StringIO()

            try:
                process_json_function(in_file, out_file)
            except Exception as e:
                print("\n" + in_filename + "\n")
                raise e

            actual_out_str = out_file.getvalue()

            expected_out_filename = in_filename.replace(IN_JSON, OUT_JSON)
            expected_out_file = open(expected_out_filename)
            excepted_out_str = expected_out_file.read()  # str

            with self.subTest():
                self.assertEqual(remove_white_space(excepted_out_str),
                                 remove_white_space(actual_out_str), in_filename)

            in_file.close()
            out_file.close()

            num_tests_run += 1
        self.assertNotEqual(num_tests_run, 0, "No test files loaded")

    def test_situation(self):
        self._test_json_in_directory(JSON_SITUATION_DIR,
                                     xattack.process_json_situation)

    def test_feeding_7(self):
        self._test_json_in_directory(JSON_FEEDING_7_DIR,
                                     xfeed.process_json_feeding_7)

    def test_config(self):
        self._test_json_in_directory(JSON_CONFIG_DIR,
                                     xstep.run)

    def test_step4(self):
        self._test_json_in_directory(JSON_STEP4_DIR,
                                     xstep4.run)

    def test_silly_choice(self):
        self._test_json_in_directory(JSON_SILLY_CHOICE_DIR,
                                     xsilly.run)

if __name__ == '__main__':
    unittest.main()
