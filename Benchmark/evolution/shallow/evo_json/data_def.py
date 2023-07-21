from evo_json.constants import *
from evolution.trait_cards.all_trait_cards import *

__author__ = 'Edwin Cowart, Kevin McDonough'

class ConvertPyJSONError(ValueError):
    """
    Represents an error in converting PyJSON
    """
    pass

PJ_Trait = str # In the Dictionary below
trait_dictionary = {
    CARNIVORE_STR: CARNIVORE_TYPE,
    AMBUSH_STR: AMBUSH_TYPE,
    BURROWING_STR: BURROWING_TYPE,
    CLIMBING_STR: CLIMBING_TYPE,
    COOPERATION_STR: COOPERATION_TYPE,
    FAT_TISSUE_STR: FAT_TISSUE_TYPE,
    FERTILE_STR: FERTILE_TYPE,
    FORAGING_STR: FORAGING_TYPE,
    HARD_SHELL_STR: HARD_SHELL_TYPE,
    HERDING_STR: HERDING_TYPE,
    HORNS_STR: HORNS_TYPE,
    LONG_NECK_STR: LONG_NECK_TYPE,
    PACK_HUNTING_STR: PACK_HUNTING_TYPE,
    SCAVENGER_STR: SCAVENGER_TYPE,
    SYMBIOSIS_STR: SYMBIOSIS_TYPE,
    WARNING_CALL_STR: WARNING_CALL_TYPE
}