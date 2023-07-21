from evo_json.convert_py_json.convert_species_fields import *
from evolution.Species import Species
from evolution.data_defs import *

__author__ = 'Edwin Cowart, Kevin McDonough'


"""----------- PyJSON Species <-> Species -----------"""


"""
PJ_Species = List[PyJSON]  # of format [PJ_Food, PJ_Body, PJ_Pop, PJ_Traits]
"""

def is_pj_species(value):
    """ Is the given value a PyJSON Species?
    :param value: The value being checked
    :type value: Any
    :return: True if the given value is a PyJSON Species
    :rtype: Boolean
    """
    return is_list_with_len(value, PJ_SPECIES_LEN)


def convert_from_pj_species(species):
    """ Convert the given PyJSON Species to a Species
    :param species: The PyJSON Species being converted
    :type Species: PyJSON
    :return: The equivalent Species
    :rtype: Species
    """
    if not is_pj_species(species):
        raise ValueError("convert_species: Invalid PyJSON Species")

    return Species(convert_from_pj_food(species[0]),
                   convert_from_pj_body(species[1]),
                   convert_from_pj_pop(species[2]),
                   convert_from_pj_traits(species[3]))


def convert_to_pj_species(species):
    """ Convert the given Species to a PyJSON Species
    :param species: The Species being converted
    :type species: Species
    :return: The equivalent Species in PyJSON
    :rtype: PyJSON
    """
    if not isinstance(species, Species):
        raise ValueError("convert_species: Invalid Species")

    return [convert_to_pj_food(species.num_food_tokens),
            convert_to_pj_body(species.body_size),
            convert_to_pj_pop(species.population),
            convert_to_pj_traits(species.get_active_cards())]


"""----------- PyJSON OptSpecies <-> Optional[Species] -----------"""


"""
PJ_OptSpecies = PyJSON  # one of False or PJ_Species
"""

def is_pj_opt_species(value):
    """
    Is the given value a PyJSON OptSpecies?
    :param value: The value being checked
    :type value: Any
    :return: True if the given value is a PyJSON OptSpecies
    :rtype: Boolean
    """
    return (value == PJ_OPT) or is_pj_species(value)


def convert_from_pj_opt_species(pj_opt_species):
    """
     Convert the given PyJSON OptSpecies to a Optional Species
    :param species: The PyJSON OptSpecies being converted
    :type species: PJ_OptSpecies
    :return: The Optional Species
    :rtype: Species or None
    """
    if pj_opt_species == PJ_OPT:
        return None
    else:
        return convert_from_pj_species(pj_opt_species)


def convert_to_pj_opt_species(opt_species):
    """ Convert the given Optional Species to a PyJSON OptSpecies
    :param species: The Optional Species being converted
    :type species: Species or None
    :return: The PyJSON OptSpecies
    :rtype: PJ_OptSpecies

    OptSpecies is either Species or False
    """
    if opt_species is None:
        return PJ_OPT
    else:
        return convert_to_pj_species(opt_species)


"""----------- PyJSON Species+ <-> Species -----------"""


"""
PJ_Species_Plus = List[PyJSON]  # of format [PJ_Food, PJ_Body, PJ_Pop, PJ_Traits, PJ_Fat_Food]
"""

def is_pj_species_plus(value):
    """ Is the given value a PyJSON Species+?
    :param value: The value being checked
    :type value: Any
    :return: True if the given value is a PyJSON Species+
    :rtype: Boolean
    """
    return is_list_with_len(value, PJ_SPECIES_PLUS_LEN)


def convert_from_pj_species_plus(pj_species):
    """ Convert the given PyJSON Species+ to a Species
    :param pj_species: The PyJSON Species+ being converted
    :type pj_species: PyJSON
    :return: The equivalent Species
    :rtype: Species
    """
    if is_list_with_len(pj_species, PJ_SPECIES_LEN):
        return convert_from_pj_species(pj_species)
    if not is_list_with_len(pj_species, PJ_SPECIES_PLUS_LEN):
        raise ValueError("convert_from_pj_species_plus: Invalid PyJSON Species+: " + repr(pj_species))

    species = convert_from_pj_species(pj_species[:-1])

    species.add_stored_fat_food(convert_from_pj_fat_food(pj_species[PJ_SPECIES_LEN]))
    return species


def convert_to_pj_species_plus(species):
    """
    Convert the given Species to a PyJSON Species+
    :param species: The Species being converted
    :type species: Species
    :return: The equivalent PyJSON Species+
    :rtype: PyJSON

    Species+ = [food, body, population, traits, fat-food]
    """

    base_species = convert_to_pj_species(species)
    fat_food = species.get_fat_tissue_food()
    if fat_food > 0:
        base_species.append(convert_to_pj_fat_food(fat_food))
    return base_species


"""----------- PyJSON LOS <-> List[Species] -----------"""


def is_pj_los(value):
    """ Is the given value a PyJSON Listof Species+?
    :param value: The value being checked
    :type value: Any
    :return: True if the given value is a PyJSON Listof Species+
    :rtype: Boolean
    """
    return isinstance(value, list)


def convert_from_pj_los(py_los):
    """ Convert PyJSON LOS into a List of Species
    :param py_los: The  PyJSON LOS being converted
    :type py_los: PyJSON
    :return: The resulting List of Species
    :rtype: [Species, ...]
    """
    if not is_pj_los(py_los):
        raise ValueError("convert_species_plus_list: Invalid PyJSON LOS ")

    return [convert_from_pj_species_plus(py_species_plus) for py_species_plus in py_los]


def convert_to_pj_los(species_list):
    """ Convert List of Species into a PyJSON LOS
    :param species_plus_list: The  List of Species being converted
    :type species_plus_list:
    :return: The resulting PyJSON PyJSON LOS
    :rtype: PyJSON
    """
    if not is_list_of(species_list, Species):
        raise ValueError("convert_species_plus_list: Invalid List[Species]")

    return [convert_to_pj_species_plus(species) for species in species_list]
