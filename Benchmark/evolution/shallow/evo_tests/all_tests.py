import glob
import os
import unittest
from evo_tests.data_defs import TEST_CASES_PATH, to_module_path

__author__ = 'Edwin Cowart, Kevin McDonough'

def main():

    suite = unittest.TestSuite()

    for test_file_path in glob.glob(os.path.join(TEST_CASES_PATH, 'test_*.py')):
        module_path = to_module_path(test_file_path)
        suite.addTest(unittest.defaultTestLoader.loadTestsFromName(module_path))

    unittest.TextTestRunner().run(suite)


if __name__ == "__main__":
    main()