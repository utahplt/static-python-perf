from evo_json.constants import ID_STR, SPECIES_STR, BAG_STR
from evo_json.convert_py_json.convert_species import *
from evolution.data_defs import *
from evolution.player.iplayer import IPlayer

__author__ = 'Edwin Cowart, Kevin McDonough'


"""----------- PyJSON Player id filed <-> Natural -----------"""


def is_pj_id(value):
    """
    IS the given value a PJ_Id?
    :param value: The value being checked
    :type value: Any
    :return: True if given value is a PJ_Id, False otherwise
    :rtype: Boolean
    """
    return is_list_with_len(value, 2) and (value[0] == ID_STR) and is_natural_plus(value[1])

def convert_from_id(pj_id):
    """
    Convert the given PJ_ID to a NaturalPlus id
    :param id: The PJ_Id being converted
    :type id: PJ_Id
    :return: The resulting NaturalPlus id
    :rtype: Nat+
    """
    if not is_pj_id(pj_id):
        raise ValueError("convert_from_id: Invalid PyJSON Id: " + repr(pj_id))

    return pj_id[1]


def convert_to_pj_id(id_nat_plus):
    """ Convert the given NaturalPlus id to a PJ_ID
    :param id_nat_plus: The NaturalPlus id being converted
    :type id_nat_plus: Nat+
    :return: The resulting PJ_Id
    :rtype: PJ_Id
    """
    if not is_natural_plus(id_nat_plus):
        raise ValueError("convert_to_pj_id: Not given Natural+")

    return [ID_STR, id_nat_plus]


"""----------- PyJSON Player species <-> List[Species] -----------"""


"""
PJ_Player_Species = List[PyJSON] # of format ["species", PJ_LOS]
"""

def is_pj_player_species(value):
    """ Is the given value a PJ_Player_Species
    :param value: The value being checked
    :type value: Any
    :return: True if value is a PJ_Player_Species, False otherwise
    :rtype: Boolean
    """
    return is_list_with_len(value, 2) and (value[0] == SPECIES_STR) and isinstance(value[1], list)

def convert_from_pj_player_species(pjp_species):
    """ Convert the given PJ_Player_Species to a List[Species]
    :param pjp_species: PJ_Player_Species
    :type pjp_species: PJ_Player_Species
    :return: The equivalent list of species
    :rtype: [Species, ...]
    """
    if not is_pj_player_species(pjp_species):
        raise ValueError("convert_from_pj_player_species: Invalid PyJSON Player Species")

    return convert_from_pj_los(pjp_species[1])


def convert_to_pj_player_species(species_list):
    """ Convert the given List[Species] a PJ_Player_Species
    :param species_list: The list of species to be converted
    :type species_list: [Species, ...]
    :return: The equivalent player list of species in PyJSON
    :rtype: PJ_Player_Species
    """

    return [SPECIES_STR, convert_to_pj_los(species_list)]


def is_pj_bag(value):
    """ IS the given value a PJ_ID?
    :param value: The value being checked
    :type value: Any
    :return: True if given value is a PJ_ID, False otherwise
    :rtype: Boolean
    """
    return is_list_with_len(value, 2) and (value[0] == BAG_STR) and is_natural(value[1])

def convert_from_bag(pj_bag):
    """ Convert the given PJ_Bag to a Natural
    :param pj_bag: The PJ_Bag being converted
    :type pj_bag: PJ_Bag
    :return: The equivalent natural number in Python
    :rtype: Nat
    """
    if not is_pj_bag(pj_bag):
        raise ValueError("convert_from_bag: Invalid PyJSON Bag")

    return pj_bag[1]


def convert_to_pj_bag(bag_nat):
    """ Convert the given food bag count to a PJ_Bag
    :param bag_nat: The natural number bag being converted
    :type bag_nat: Nat
    :return: The resulting PJ_Bag
    :rtype: PJ_Bag
    """
    if not is_natural(bag_nat):
        raise ValueError("convert_to_pj_bag: Not given Natural")

    return [BAG_STR, bag_nat]