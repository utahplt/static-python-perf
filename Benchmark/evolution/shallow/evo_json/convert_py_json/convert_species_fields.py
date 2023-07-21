from evo_json.constants import FOOD_STR, BODY_STR, POP_STR, TRAITS_STR, FAT_FOOD_STR, PJ_FIELD_LEN
from evo_json.convert_py_json.convert_trait import *
from evolution.data_defs import is_list_of, is_list_with_len, is_natural


__author__ = 'Edwin Cowart, Kevin McDonough'


"""----------- PyJSON Species food field <-> Natural -----------"""


"""
PJ_Food = List[PyJSON] # of the format ["food", Natural]
"""


def is_pj_food(value):
    """ Is the given value a PyJSON Food?
    :param value: The value being checked
    :type value: Any
    :return: True the given value a PyJSON Food, False otherwise
    :rtype: Boolean
    """
    return is_list_with_len(value, PJ_FIELD_LEN) and (value[0] == FOOD_STR) and is_natural(value[1])


def convert_from_pj_food(pj_food):
    """ Convert the given PyJSON Food int a Natural
    :param pj_food: The PyJSON Food being converted
    :type pj_food: PJ_Food
    :return: The resulting Natural
    :rtype: Natural
    """
    if not is_pj_food(pj_food):
        raise ValueError("convert_from_pj_food: Invalid PyJSON Food: " + repr(pj_food))

    return pj_food[1]


def convert_to_pj_food(food_nat):
    """
     Convert the given Natural into a PyJSON food
    :param food_nat: The Natural
    :type food_nat: Nat
    :return: The PyJSON Food
    :rtype: PJ_Food

    food = [\"food\", Natural]
    """
    if not (is_natural(food_nat)):
        raise ValueError("convert_to_pj_food: Invalid Natural")

    return [FOOD_STR, food_nat]


"""----------- PyJSON Species body field <-> Natural -----------"""


"""
PJ_Body = List[PyJSON] # of format ["body", Natural]
"""

def is_pj_body(value):
    """ Is the given value a PyJSON Body?
    :param value: The value being checked
    :type value: Any
    :return: True the given value a PyJSON Body, False otherwise
    :rtype: Boolean
    """
    return is_list_with_len(value, PJ_FIELD_LEN) and (value[0] == BODY_STR) and is_natural(value[1])


def convert_from_pj_body(pj_body):
    """ Convert the given PyJSON Body into a Natural
    :param pj_body: The PyJSON Body being converted
    :type pj_body: PJ_Body
    :return: The resulting Natural
    :rtype: Nat
    """
    if not is_pj_body(pj_body):
        raise ValueError("convert_from_pj_body: Invalid PyJSON Body = [\"body\", Natural]")

    return pj_body[1]


def convert_to_pj_body(body_nat):
    """ Convert the given Natural into a PyJSON Body
    :param body_nat: The body size to be converted
    :type body_nat: Nat
    :return: PyJSON Body
    :rtype: PJ_Body
    """
    if not (is_natural(body_nat)):
        raise ValueError("convert_to_pj_body: Invalid Natural")

    return [BODY_STR, body_nat]


"""----------- PyJSON Species population field <-> Natural -----------"""


"""
PJ_Pop = List[PyJSON] # of format ["body", Natural]
"""

def is_pj_pop(value):
    """ Is the given value a PyJSON Population?
    :param value: The value being checked
    :type value: Any
    :return: True the given value a PyJSON Population, False otherwise
    :rtype: Boolean
    """
    return is_list_with_len(value, PJ_FIELD_LEN) and (value[0] == POP_STR) and is_natural(value[1])


def convert_from_pj_pop(pj_pop):
    """ Convert the given PyJSON Population into a Natural
    :param pj_pop: The PyJSON Population being converted
    :type pj_pop: PJ_Pop
    :return: The equivalent natural number
    :rtype: Nat
    """
    if not is_pj_pop(pj_pop):
        raise ValueError("convert_from_pj_population: Invalid PyJSON Population = [\"population\", Natural]")

    return pj_pop[1]


def convert_to_pj_pop(pop_nat):
    """ Convert the given population count into a PyJSON Population
    :param pop_nat: The natural number being converted
    :type pop_nat: Nat
    :return: The PyJSON Population
    :rtype: PJ_Pop
    """
    if not is_natural(pop_nat):
        raise ValueError("convert_to_pj_population: Invalid Natural")

    return [POP_STR, pop_nat]


"""----------- PyJSON Species traits field <-> List[TraitCard] -----------"""


"""
PJ_Traits = List[PyJSON] # of format ["traits", PJ_LOT]
"""

def is_pj_traits(value):
    """ Is the given value a PyJSON Traits?
    :param value: The value being checked
    :type value: Any
    :return: True the given value a PyJSON Traits, False otherwise
    :rtype: Boolean
    """
    return is_list_with_len(value, PJ_FIELD_LEN) and (value[0] == TRAITS_STR) and is_pj_lot(value[1])



def convert_from_pj_traits(pj_traits):
    """ Convert the given PyJSON Traits to a List of TraitCards
    :param pj_traits: The PyJSON Traits being converted
    :type pj_traits: PJ_Traits
    :return: The resulting List of TraitCards
    :rtype: [TraitCard, ...]
    """
    if not is_pj_traits(pj_traits):
        raise ValueError("convert_traits: Invalid PyJSON Traits: " + repr(pj_traits))

    return convert_from_pj_lot(pj_traits[1])


def convert_to_pj_traits(traits_list):
    """ Convert the given List of TraitCards to a PyJSON Traits
    :param traits_list: The List of TraitCards traits being converted
    :type traits_list: [TraitCard, ...]
    :return: The resulting PyJSON Traits
    :rtype: PJ_Traits
    """
    if not is_list_of(traits_list, TraitCard):
        raise ValueError("convert_traits: Invalid List[TraitCard]")

    return [TRAITS_STR, convert_to_pj_lot(traits_list)]


"""----------- PyJSON Species fat-food field <-> Natural -----------"""


"""
PJ_Fat_Food = List[PyJSON] # of format ["fat-food", Natural]
"""

def is_pj_fat_food(value):
    """ Is the given value a PyJSON Fat-Food?
    :param value: The value being checked
    :type value: Any
    :return: True the given value a PyJSON Fat-Food, False otherwise
    :rtype: Boolean
    """
    return is_list_with_len(value, PJ_FIELD_LEN) and (value[0] == FAT_FOOD_STR) and is_natural(value[1])


def convert_from_pj_fat_food(pj_fat_food):
    """ Convert the given PyJSON Fat-Food to a Natural
    :param pj_fat_food: The PyJSON Fat-Food being converted
    :type pj_fat_food: PJ_FatFood
    :return: The resulting Natural
    :rtype: Natural
    """
    if not is_pj_fat_food(pj_fat_food):
        raise ValueError("convert_fat_food: Invalid PyJSON Fat-Food = [\"fat-food\", Natural]")
    return pj_fat_food[1]


def convert_to_pj_fat_food(fat_food_nat):
    """ Convert the given Natural to a PyJSON PJ_Fat_Food
    :param fat_food_nat: The Natural being converted
    :type fat_food_nat: Nat
    :return: The resulting PyJSON PJ_Fat_Food
    :rtype: PJ_Fat_Food

    fat-food = [\"fat-food\", Natural]
    """
    if not is_natural(fat_food_nat):
        raise ValueError("convert_fat_food: Invalid Natural]")
    return [FAT_FOOD_STR, fat_food_nat]
