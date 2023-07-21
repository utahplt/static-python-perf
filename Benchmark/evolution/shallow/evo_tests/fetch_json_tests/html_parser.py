from html.parser import HTMLParser
from evo_tests.fetch_json_tests.html_tags import HTML_Tag
from evo_tests.fetch_json_tests.html_test_case import JSONTestCase

__author__ = 'Edwin Cowart, Kevin McDonough'


""" HW-6 JSON Test HTML Format
<h2>test_name</h2>
<p>
    <pre>in_data</pre>
    <pre>\n</pre>
    <pre>out_data</pre>
</p>
"""


class JSONTestCaseHTMLParser(HTMLParser):
    """ A class for parsing JSONTestCases from HTML according to their current formatting
    """

    def __init__(self, parsed_test_cases=None, cur_test_case=None):
        """ Construct a JSON Test Case HTML Parser
        :param parsed_test_cases: The list of full parse test cases
        :type parsed_test_cases: [JsonTestCase, ...] or None
        :param cur_test_case: The current test case
        :type cur_test_case: [JsonTestCase,...] or None
        """
        HTMLParser.__init__(self)
        self.parsed_test_cases = [] if parsed_test_cases is None else parsed_test_cases # type: List[JSONTestCase]
        self.cur_test_case = JSONTestCase() if cur_test_case is None else cur_test_case # type: JSONTestCase
        self.last_start_tag = None  # type: Optional[HTML_Tag]
        self.skip_next_pre = False

    def handle_starttag(self, tag: str, attrs):
        """ Handle the start tag by finishing the current test case if it is complete and set the last start tag
        :param tag: The tag in question
        :param attrs: The attributes
        """
        self.checkout_cur_test_case()
        self.last_start_tag = tag

    def handle_endtag(self, tag: str):
        pass

    def handle_data(self, data: str):
        """ Handle the given data if it is within a <h2> or <pre> and fits the current test case
        :param data: The data
        """
        if HTML_Tag.is_h2(self.last_start_tag) and not self.cur_test_case.has_name():
            self.cur_test_case.name = data
        elif HTML_Tag.is_pre(self.last_start_tag):
            if not self.cur_test_case.has_in_json():
                self.cur_test_case.in_json = data
                self.skip_next_pre = True
            elif self.skip_next_pre:
                self.skip_next_pre = False
            elif not self.cur_test_case.has_out_json():
                self.cur_test_case.out_json = data

    def checkout_cur_test_case(self):
        """ If the current test case is complete then checkout the test case by placing it in the parse test cases list
        and resets the current test case to a new one.
        :return: True if the current test case is complete, False otherwise
        """
        if self.cur_test_case.is_complete():
            self.parsed_test_cases.append(self.cur_test_case)
            self.cur_test_case = JSONTestCase()
            return True
        else:
            return False

