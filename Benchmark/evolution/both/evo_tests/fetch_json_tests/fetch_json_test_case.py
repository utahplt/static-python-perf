import urllib.request
from evo_tests.constants import TEST_CASES_URL, JSON_FEEDING_6_DIR
from evo_tests.data_defs import *
from evo_tests.fetch_json_tests.html_parser import JSONTestCaseHTMLParser


__author__ = 'Edwin Cowart, Kevin McDonough'


# Make the directory if it doesn't exist
dir_path = make_dir(evo_tests_path, JSON_FEEDING_6_DIR)

# Grab the HTML and Parse into Files
with urllib.request.urlopen(TEST_CASES_URL) as response:
    web_page = response.read()
    parser = JSONTestCaseHTMLParser()
    parser.feed(str(web_page))

    for test_case in parser.parsed_test_cases:
        make_file(dir_path, test_case.get_in_json_filename(), test_case.in_json)
        make_file(dir_path, test_case.get_out_json_filename(), test_case.out_json)

print("\nDone")