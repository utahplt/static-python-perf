from evolution.feeding import *
from evolution.player.player_feeding_choice import *
from evolution.data_defs import is_list_with_len
from evo_json.data_def import ConvertPyJSONError
from evo_json.convert_py_json.convert_player import convert_from_pj_player, convert_from_pj_lop, convert_to_pj_player, \
    convert_to_pj_lop
from evolution.data_defs import *
from evolution.player.player_feeding_choice import *

from evo_json.convert_py_json.convert_species import convert_to_pj_species_plus

__author__ = 'Edwin Cowart, Kevin McDonough'

"""
PJ_Feeding = List[PyJSON] # of format [PJ_Player, PJ_Watering_Hole, List[PJ_Player]]
"""
def is_pj_feeding(value):
    """
    Is the given value a PJ_Feeding
    :param value: The value
    :type value: Any
    :return: True if value is a PJ_Feeding, False otherwise
    """
    return is_list_with_len(value, 3)

def convert_from_pj_feeding(pj_feeding):
    """
    Convert the given PJ_Feeding to Feeding
    :param evolution: type of the evolution to be converted
    :type evolution: PJ_Feeding
    :return: The Feeding class equivalent of pj_feeding
    :rtype: Feeding
    """
    if not is_pj_feeding(pj_feeding):
        raise ValueError("convert_from_pj_feeding: Invalid PyJSON Feeding")

    return Feeding(convert_from_pj_player(pj_feeding[0]),
                   pj_feeding[1],
                   convert_from_pj_lop(pj_feeding[2]))

def convert_player_feeding_choice_to_pj(player_feeding_choice):
    """
    Converts the given player evolution choice into the equivalent PyJSON
    :param player_feeding_choice: The player evolution choice to be converted
    :type player_feeding_choice: PlayerFeedingChoice
    :return: The equivalent PyJSON
    :type: PyJSON
    """
    if isinstance(player_feeding_choice, PlayerForgoAttack):
        return False
    if isinstance(player_feeding_choice, PlayerFeedVegetarian):
        return player_feeding_choice.vegetarian_index
    if isinstance(player_feeding_choice, PlayerStoreFat):
        return [player_feeding_choice.species_index,
                player_feeding_choice.num_food_to_store]
    if isinstance(player_feeding_choice, PlayerAttackWithCarnivore):
        return [player_feeding_choice.your_carnivore_index,
                player_feeding_choice.target_player_index,
                player_feeding_choice.target_species_index]

def convert_from_pj_feeding_choice(py_json):
    """
    Converts the given PyJSON into a PlayerFeedingChoice
    :param py_json: the PyJSON to convert
    :type py_json: PyJSON
    :return: the equivalent PlayerFeedingChoice
    :rtype: PlayerFeedingChoice
    """
    if py_json is False:
        return PlayerForgoAttack()
    elif is_natural(py_json):
        return convert_from_pj_veg_choice(py_json)
    elif is_list_of_nat(py_json):
        if len(py_json) == 2:
            return convert_from_pj_fat_choice(py_json)
        elif len(py_json) == 3:
            return convert_from_pj_carn_choice(py_json)
    raise ConvertPyJSONError("Error converting player feeding choice")

def convert_from_pj_veg_choice(pj_species_index):
    """
    Convert the given PyJSON species index into a PlayerFeedVegetarian
    :param pj_species_index: the PyJSON species index to convert
    :type pj_species_index: PyJSON
    :return: the equivalent PlayerFeedVegetarian
    :rtype: PlayerFeedVegetarian
    """
    return PlayerFeedVegetarian(pj_species_index)


def convert_from_pj_fat_choice(py_json):
    """
    Convert the given py_json into a PlayerFeedVegetarian
    :param py_json: the PyJSON to convert
    :type py_json: PyJSON
    :return: the equivalent PlayerFeedVegetarian
    :rtype: PlayerFeedVegetarian
    """
    [species_index, fat_to_store] = py_json
    if not is_natural_plus(fat_to_store):
        raise ConvertPyJSONError("Error Converting Fat Tissue Choice")
    return PlayerStoreFat(species_index, fat_to_store)


def convert_from_pj_carn_choice(py_json):
    """
    Convert the given PyJSON into a PlayerAttackWithCarnivore
    :param py_json: PyJSON to convert
    :type py_json: PyJSON
    :return: the equivalent choice
    :rtype: PlayerAttackWithCarnivore
    """
    [attacker_index, target_player_index, target_species_index] = py_json
    return PlayerAttackWithCarnivore(attacker_index,
                                     target_player_index,
                                     target_species_index)


def convert_to_pj_feeding(feeding):
    """
    Convert the given Feeding to PJ_Feeding
    :param feeding: The evolution to be converted
    :type feeding: Feeding
    :return: The equivalent PJ_Feeding
    :rtype: PJ_Feeding
    """
    if not isinstance(feeding, FeedingChoice):
        raise ValueError("convert_to_pj_feeding: Invalid Feeding")

    return [convert_to_pj_player(feeding.player_state),
            feeding.watering_hole,
            convert_to_pj_lop(feeding.other_player_states)]
