'''
A Nat is an int >= 0

A Nat+ is a Nat > 0
'''

def is_natural(value):
    """
    Is the given value a Nat?
    :param value: value to check
    :type value: Any
    :return: True if the value is a Nat, False otherwise
    :rtype: bool
    """
    return is_int_greater_or_equal_to(0, value)


def is_index(value):
    """ Is the given value an index?
    :param value: value to check
    :type value: Any
    :return: True if the value is an Index, False otherwise
    :rtype: bool
    """
    return is_natural(value)


def is_natural_plus(value):
    """ Is the given value a Nat+
    :param value: value to check
    :type value: Any
    :return: True if the value is a Nat, False otherwise
    :rtype: bool
    """
    return isinstance(value, int) and value >= 1


def is_int_greater_or_equal_to(min_val, value):
    """ Is th given value an int greater than or equal to the given minimum value?
    :param min_val: The minimum value
    :type min_val: int
    :param value: The value being checked
    :type value: Any
    :return: True if the value is an int greater than or equal to the given minimum value, False otherwise
    :rtype: bool
    """
    return isinstance(value, int) and min_val <= value


def is_int_in_inclusive_range(value, min_value, max_value):
    """ Is the given value an int in the range [min_value, max_value]
    :param value: value being checked
    :type value: Any
    :param min_value: minimum allowed int
    :type min_value: int
    :param max_value: maximum allowed int
    :type max_value: int
    :return: True if the value is int on given range, False otherwise
    :rtype: bool
    """
    return isinstance(value, int) and (value in range(min_value, max_value + 1))


def is_list_with_len(value, length) -> bool:
    """ Is the given value a list of the given length?
    :param value: The value to check
    :type value: Any
    :param length: The length being checked for
    :type length: Nat
    :return: True if the value is a list of the length
    :rtype: bool
    """
    return isinstance(value, list) and len(value) == length


def is_list_with_max_len(value, length):
    """ Is the list of given length or less?
    :param value: The value being checked
    :type value: Any
    :param length: The length being checked
    :type length: Nat
    :return: True if the list is of the length or less, False otherwise
    :rtype: bool
    """
    return isinstance(value, list) and len(value) <= length


def is_list_with_len_and_first(value, length, first_val):
    """ Is the given value a list of the given length and the given first value
    :param value: The value being checked
    :type value: Any
    :param length: The length of the list
    :type length: Nat
    :param first_val: The first value
    :type first_val: Any
    :return: True if the value is a list of the length with the first value
    :rtype: bool
    """
    return is_list_with_len(value, length) and value and (length > 0 and value[0] == first_val)


def is_list_of(value, elem_type):
    """ Is the given value a list where each element is the elem_type
    :param value: The value being checked
    :type value: Any
    :param elem_type: The element type
    :type elem_type: type
    :return: True is the value is a list and each element in the list is of the given type, False otherwise
    :rtype: bool
    """
    return isinstance(value, list) and all(isinstance(elem, elem_type) for elem in value)


def is_list_of_valid_elem(value, elem_validator):
    """ Is the given value a list whose each element is checked by elem_check to be True?
    :param value: The value being checked
    :type value: Any
    :param elem_validator: The element checker
    :type elem_validator: Any -> bool
    :return: True if the given value is a list whose every element is checked, False otherwise
    :rtype: bool
    """
    return isinstance(value, list) and all(elem_validator(elem) for elem in value)


def is_list_of_nat(value):
    """
    Is the given value a list where each element is a natural number?
    :param value: The value being checked
    :type value: Any
    :rtype: bool
    :return: bool
    """
    return isinstance(value, list) and all(is_natural(elem) for elem in value)

