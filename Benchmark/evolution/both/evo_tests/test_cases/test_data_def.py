import unittest

from evolution.data_defs import *
from evolution.util import eq_comparator, is_comparator, type_comparator, of_type_comparator, any_duplicates, \
    does_list_contain

__author__ = 'Edwin Cowart, Kevin McDonough'


class TestDataDefs(unittest.TestCase):
    def test_is_natural(self):
        self.assertFalse(is_natural(-1))
        self.assertFalse(is_natural(""))
        self.assertFalse(is_natural(None))
        self.assertFalse(is_natural([]))
        self.assertTrue(is_natural(0))
        self.assertTrue(is_natural(1))
        self.assertTrue(is_natural(100))
        self.assertTrue(is_natural(3434))

    def test_is_index(self):
        self.assertFalse(is_index(-1))
        self.assertFalse(is_index(""))
        self.assertFalse(is_index(None))
        self.assertFalse(is_index([]))
        self.assertTrue(is_index(0))
        self.assertTrue(is_index(1))
        self.assertTrue(is_index(100))
        self.assertTrue(is_index(3434))

    def test_is_natural_plus(self):
        self.assertFalse(is_natural_plus(-1))
        self.assertFalse(is_natural_plus(""))
        self.assertFalse(is_natural_plus(None))
        self.assertFalse(is_natural_plus([]))
        self.assertFalse(is_natural_plus(0))
        self.assertTrue(is_natural_plus(1))
        self.assertTrue(is_natural_plus(100))
        self.assertTrue(is_natural_plus(3434))

    def test_is_int_greater_or_equal_to(self):
        self.assertFalse(is_int_greater_or_equal_to(-2, ""))
        self.assertFalse(is_int_greater_or_equal_to(-1, []))
        self.assertTrue(is_int_greater_or_equal_to(-2, 0))
        self.assertTrue(is_int_greater_or_equal_to(-1, 0))
        self.assertTrue(is_int_greater_or_equal_to(0, 0))
        self.assertTrue(is_int_greater_or_equal_to(0, 1))
        self.assertTrue(is_int_greater_or_equal_to(1, 1))
        self.assertTrue(is_int_greater_or_equal_to(1, 2))
        self.assertFalse(is_int_greater_or_equal_to(0, ""))
        self.assertTrue(is_int_greater_or_equal_to(-3, -1))

    def test_is_int_in_inclusive_range(self):
        self.assertFalse(is_int_in_inclusive_range([], 0,0))
        self.assertFalse(is_int_in_inclusive_range("", 0,0))
        self.assertTrue(is_int_in_inclusive_range(0,0,0))
        self.assertTrue(is_int_in_inclusive_range(-1,-1,1))
        self.assertFalse(is_int_in_inclusive_range(-2,-1,1))
        self.assertTrue(is_int_in_inclusive_range(0,-1,1))
        self.assertTrue(is_int_in_inclusive_range(1,-1,1))
        self.assertFalse(is_int_in_inclusive_range(2,-1,1))

    def test_is_list_with_len(self):
        self.assertFalse(is_list_with_len(2, -1))
        self.assertFalse(is_list_with_len("", -1))
        self.assertFalse(is_list_with_len([], -1))
        self.assertTrue(is_list_with_len([], 0))
        self.assertFalse(is_list_with_len([], 1))
        self.assertFalse(is_list_with_len([1], 0))
        self.assertTrue(is_list_with_len([1], 1))
        self.assertFalse(is_list_with_len([1], 2))
        self.assertFalse(is_list_with_len([1, 2], 1))
        self.assertTrue(is_list_with_len([1, 2], 2))
        self.assertFalse(is_list_with_len([1, 2], 3))

    def test_is_list_with_max_len(self):
        self.assertFalse(is_list_with_max_len("", 0))
        self.assertFalse(is_list_with_max_len(2, 0))
        self.assertTrue(is_list_with_max_len([], 0))
        self.assertTrue(is_list_with_max_len([], 1))
        self.assertTrue(is_list_with_max_len([], 2))
        self.assertFalse(is_list_with_max_len([1], 0))
        self.assertTrue(is_list_with_max_len([1], 1))
        self.assertTrue(is_list_with_max_len([1], 2))
        self.assertTrue(is_list_with_max_len([1], 3))
        self.assertFalse(is_list_with_max_len([1, 2], 0))
        self.assertFalse(is_list_with_max_len([1, 2], 1))
        self.assertTrue(is_list_with_max_len([1, 2], 2))
        self.assertTrue(is_list_with_max_len([1, 2], 3))

    def test_is_list_with_len_and_first(self):
        self.assertFalse(is_list_with_len_and_first("", 2, ""))
        self.assertFalse(is_list_with_len_and_first([1, 2], 2, ""))
        self.assertFalse(is_list_with_len_and_first([["h", "ello"], 2, 3], 3, "h"))

    def test_is_list_of(self):
        self.assertFalse(is_list_of("", str))
        self.assertTrue(is_list_of([], str))
        self.assertTrue(is_list_of(["", "2343242", "234"], str))
        self.assertFalse(is_list_of(["", 12321, "234"], str))

    def test_is_list_of_valid_elem(self):
        self.assertFalse(is_list_of_valid_elem("", is_natural))
        self.assertTrue(is_list_of_valid_elem([], is_natural))
        self.assertFalse(is_list_of_valid_elem([""], is_natural))
        self.assertFalse(is_list_of_valid_elem(["", 3434], is_natural))
        self.assertTrue(is_list_of_valid_elem([1232, 3434], is_natural))

    def test_eq_comparator(self):
        self.assertFalse(eq_comparator(1, ""))
        self.assertTrue(eq_comparator(1, 1))
        self.assertTrue(eq_comparator("", ""))
        self.assertFalse(eq_comparator(1, None))
        self.assertFalse(eq_comparator(None, ""))
        self.assertTrue(eq_comparator(None, None))
        self.assertTrue(eq_comparator([""], [""]))

    def test_is_comparator(self):
        self.assertFalse(is_comparator(1, ""))
        self.assertTrue(is_comparator(1, 1))
        self.assertTrue(is_comparator("", ""))
        self.assertFalse(is_comparator(1, None))
        self.assertFalse(is_comparator(None, ""))
        self.assertTrue(is_comparator(None, None))
        self.assertFalse(is_comparator([""], [""]))

    def test_type_comparator(self):
        self.assertFalse(type_comparator(1, ""))
        self.assertTrue(type_comparator(1, 1))
        self.assertTrue(type_comparator("", ""))
        self.assertFalse(type_comparator(1, None))
        self.assertFalse(type_comparator(None, ""))
        self.assertTrue(type_comparator(None, None))
        self.assertTrue(type_comparator([""], [""]))

    def test_of_type_comparator(self):
        self.assertFalse(of_type_comparator(1, str))
        self.assertTrue(of_type_comparator(1, int))
        self.assertTrue(of_type_comparator("", str))
        self.assertFalse(of_type_comparator(1, None))
        self.assertFalse(of_type_comparator(None, str))
        self.assertFalse(of_type_comparator(None, None))
        self.assertTrue(of_type_comparator([""], list))


    def test_any_duplicates_eq(self):
        self.assertFalse(any_duplicates([]))
        self.assertFalse(any_duplicates([1]))
        self.assertFalse(any_duplicates([1, 2]))
        self.assertFalse(any_duplicates([1, 2, 3]))
        self.assertTrue(any_duplicates([1, 2, 1]))
        self.assertTrue(any_duplicates([1, 1, 3]))
        self.assertTrue(any_duplicates([1, 1, 1]))
        self.assertTrue(any_duplicates([[None], [None], 1]))

    def test_any_duplicates_is(self):
        self.assertFalse(any_duplicates([], is_comparator))
        self.assertFalse(any_duplicates([1], is_comparator))
        self.assertFalse(any_duplicates([1, 2], is_comparator))
        self.assertFalse(any_duplicates([1, 2, 3], is_comparator))
        self.assertTrue(any_duplicates([1, 2, 1], is_comparator))
        self.assertTrue(any_duplicates([1, 1, 3], is_comparator))
        self.assertTrue(any_duplicates([1, 1, 1], is_comparator))
        self.assertTrue(any_duplicates(["", "", 1], is_comparator))
        self.assertTrue(any_duplicates([None, None, 1], is_comparator))
        self.assertFalse(any_duplicates([[None], [None], 1], is_comparator))

    def test_any_duplicates_type(self):
        self.assertFalse(any_duplicates([], type_comparator))
        self.assertFalse(any_duplicates([1], type_comparator))
        self.assertTrue(any_duplicates([1, 2], type_comparator))
        self.assertFalse(any_duplicates([1, ""], type_comparator))
        self.assertTrue(any_duplicates([1, 2, 3], type_comparator))
        self.assertTrue(any_duplicates([1, 2, 1], type_comparator))
        self.assertTrue(any_duplicates([1, 1, 3], type_comparator))
        self.assertTrue(any_duplicates([1, 1, 1], type_comparator))
        self.assertTrue(any_duplicates(["", "", 1], type_comparator))
        self.assertFalse(any_duplicates(["", None, 1], type_comparator))
        self.assertTrue(any_duplicates([None, None, 1], type_comparator))
        self.assertTrue(any_duplicates([[None], [None], 1], type_comparator))

    def test_does_list_contain_eq(self):
        self.assertFalse(does_list_contain([], 1))
        self.assertTrue(does_list_contain([1, 2], 1))
        self.assertTrue(does_list_contain([1, 2], 2))
        self.assertFalse(does_list_contain(["1", "31415"], 1))
        self.assertFalse(does_list_contain([1, 2], 0))
        self.assertTrue(does_list_contain([None], None))
        self.assertTrue(does_list_contain([[]], []))

    def test_does_list_contain_is(self):
        self.assertFalse(does_list_contain([], 1), is_comparator)
        self.assertTrue(does_list_contain([1, 2], 1, is_comparator))
        self.assertTrue(does_list_contain([1, 2], 2, is_comparator))
        self.assertFalse(does_list_contain(["1", "31415"], 1, is_comparator))
        self.assertFalse(does_list_contain([1, 2], 0, is_comparator))
        self.assertTrue(does_list_contain([None], None, is_comparator))
        self.assertFalse(does_list_contain([[]], [], is_comparator))

    def test_does_list_contain_type(self):
        self.assertFalse(does_list_contain([], 1), type_comparator)
        self.assertTrue(does_list_contain([1, 2], 1, type_comparator))
        self.assertTrue(does_list_contain([1, 2], 2, type_comparator))
        self.assertFalse(does_list_contain(["1", "31415"], 1, type_comparator))
        self.assertTrue(does_list_contain([1, 2], 0, type_comparator))
        self.assertTrue(does_list_contain([None], None, type_comparator))
        self.assertTrue(does_list_contain([[]], [], type_comparator))

    def test_does_list_contain_of_type(self):
        self.assertFalse(does_list_contain([], None), of_type_comparator)
        self.assertFalse(does_list_contain([], int), of_type_comparator)
        self.assertFalse(does_list_contain([1, 2], str, of_type_comparator))
        self.assertTrue(does_list_contain([1, 2], int, of_type_comparator))
        self.assertFalse(does_list_contain(["1", "31415"], int, of_type_comparator))
        self.assertFalse(does_list_contain([1, 2], list, of_type_comparator))
        self.assertFalse(does_list_contain([None], None, of_type_comparator))
        self.assertTrue(does_list_contain([[]], list, of_type_comparator))




if __name__ == '__main__':
    unittest.main()
