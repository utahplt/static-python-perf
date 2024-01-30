from evo_json.convert_py_json.convert_species import *
from evolution.situation import Situation
from evolution.data_defs import is_list_with_len

__author__ = 'Edwin Cowart, Kevin McDonough'

"""----------- PyJSON Situation <-> Situation -----------"""

"""
PJ_Situation = List[PyJSON]  # of format [PJ_Species, PJ_Species, PJ_OptSpecies, PJ_OptSpecies]
"""

def is_pj_situation(value):
    """ Is the given value a PyJSON Situation
    :param value: The value being checked
    :type value: Any
    :return: True if the given value is a PyJSON Situation
    :rtype: Boolean
    """
    return is_list_with_len(value, 4)


def convert_from_py_situation(situation):
    """ Convert the given PyJSON Situation to a Situation
    :param situation: The given PyJSON Situation
    :type situation: PJ_Situation
    :return: The resulting Situation
    :rtype: Situation
    """
    if not is_pj_situation(situation):
        raise ValueError("convert_situation: Invalid PyJSON Situation")

    return Situation(convert_from_pj_species(situation[0]),
                     convert_from_pj_species(situation[1]),
                     convert_from_pj_opt_species(situation[2]),
                     convert_from_pj_opt_species(situation[3]), )


def convert_to_py_situation(situation):
    """ Convert the given Situation to a PyJSON Situation
    :param situation: The given Situation
    :type situation: Situation
    :return: The resulting PyJSON Situation
    :rtype: PJ_Situation

    Situation = [Species, Species, OptSpecies, OptSpecies]
    """
    if not isinstance(situation, Situation):
        raise ValueError("convert_situation: Invalid Situation")

    return [convert_to_pj_species(situation.attacker),
            convert_to_pj_species(situation.defender),
            convert_to_pj_opt_species(situation.defender_left_neighbor),
            convert_t0_pj_opt_species(situation.defender_right_neighbor)]
