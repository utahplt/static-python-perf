from evo_json.data_def import *
from evo_json.constants import *
from evolution.data_defs import is_list_of_valid_elem, is_list_of
from evolution.constants import CARNIVORE_MIN_FOOD_TOKENS, \
    CARNIVORE_MAX_FOOD_TOKENS

__author__ = 'Edwin Cowart, Kevin McDonough'

"""----------- PyJSON Trait <-> TraitCard -----------"""


def is_pj_trait(value):
    """ Is the given value a PJ_Trait?
    :param value: The value being checked
    :type value: Any
    :return: True if value is a PJ_TRAIT, False otherwise
    :rtype: Boolean
    """
    return isinstance(value, str) and (value in trait_dictionary.keys())


def convert_from_py_trait(pj_trait):
    """ Convert the given PyJSON Trait to a TraitCard
    :param pj_trait: The PyJSON Trait being converted
    :type pj_trait: PJ_Trait
    :return: The resulting TraitCard
    :rtype: TraitCard
    """
    if not is_pj_trait(pj_trait):
        raise ValueError(
            "convert_from_py_trait: Invalid PyJSON Trait: " + repr(pj_trait))

    return trait_dictionary[pj_trait]()


def convert_to_py_trait(trait_card):
    """ Convert the given TraitCard to a PyJSON Trait
    :param trait_card: The TraitCard being converted
    :type trait_card: TraitCard
    :return: The resulting PyJSON Trait
    :rtype: PJ_Trait
    """
    if not isinstance(trait_card, TraitCard):
        raise ValueError("convert_to_py_trait: Invalid TraitCard")

    for key, trait_card_subtype in trait_dictionary.items():
        if isinstance(trait_card, trait_card_subtype):
            return key

    # Should not be Reached
    raise ValueError(
        "convert_to_py_trait: Invalid TraitCard, must be subtype which is one of:" +
        "\"" + "\", \"".join(trait_dictionary.values()) + "\"")


def convert_from_pj_card(py_json):
    """
    Convertes the given PJ Card to a TraitCard
    :param py_json: The Card to be converted
    :type py_json: PyJSON
    :return: The equivalent TraitCard
    :rtype: TraitCard
    """
    if not isinstance(py_json, list) or len(py_json) != 2:
        raise ValueError("Invalid food card.")

    if not (CARNIVORE_MIN_FOOD_TOKENS <=
                py_json[0] <= CARNIVORE_MAX_FOOD_TOKENS):
        raise ValueError("Food value out of range.")

    base_card = convert_from_py_trait(py_json[1])
    base_card.num_tokens_as_food_card = py_json[0]
    return base_card


def convert_to_pj_card(trait_card):
    """
    Convert the given TraitCard to a PyJSON Card
    :param trait_card: The TraitCard to be converted
    :type trait_card: TraitCard
    :return: Card
    :rtype: PyJSON
    """
    return [trait_card.num_tokens_as_food_card, convert_to_py_trait(trait_card)]


"""----------- PyJSON LOT <-> List[TraitCard] -----------"""

"""
PJ_LOT = List[PJ_Trait]
"""


def is_pj_lot(value):
    """ Is the given value a Py_LOT
    :param value: The value being checked
    :type value: Any
    :return: True if the value is a Py_LOT, False otherwise
    :rtype: Boolean
    """
    return isinstance(value, list)


def convert_from_pj_lot(py_lot):
    """ Convert the given PyJSON LOT to a List of TraitCard
    :param py_lot: The PyJSON LOT being converted
    :type py_lot: PJ_LOT
    :return: The resulting List of TraitCard
    :rtype: [TraitCard, ...]
    """
    if not is_pj_lot(py_lot):
        raise ValueError("convert_from_lot:  Invalid PyJSON LOT")

    return [convert_from_py_trait(py_trait) for py_trait in py_lot]


def convert_to_pj_lot(trait_card_list):
    """ Convert the given List of TraitCard to a
    :param trait_card_list: The List of TraitCard being converted
    :type trait_card_list: [TraitCard, ...]
    :return: The resulting LOT
    :rtype: PJ_LOT
    """
    if not is_list_of(trait_card_list, TraitCard):
        raise ValueError("convert_to_py_lot: Invalid List[TraitCard]")

    return [convert_to_py_trait(trait_card) for trait_card in trait_card_list]


def convert_from_pj_loc(pj_loc):
    """
    Convert the given LOC to a list of TraitCards
    :param pj_loc: List of Cards to convert to TraitCards
    :type pj_loc: PyJSON
    :return: the list of trait cards
    :rtype: [TraitCard, ...]
    """
    if not isinstance(pj_loc, list):
        raise ValueError("List of cards must be a list")

    return [convert_from_pj_card(card) for card in pj_loc]


def convert_to_pj_loc(lotc):
    """
    Convert the given list of TraitCards to an LOC
    :param lotc: The TraitCards to be converted
    :type lotc: [TraitCard, ...]
    :return: The LOC
    :rtype: PyJSON
    """
    return [convert_to_pj_card(tc) for tc in lotc]
