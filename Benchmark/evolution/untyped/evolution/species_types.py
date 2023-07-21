from evolution.species import Species
from evolution.trait_cards import CarnivoreCard, FatTissueCard

__author__ = 'Edwin Cowart, Kevin McDonough'


def is_carnivore(value):
    """ Is the given value a Carnivore?
    :param value: The value being checked
    :type value: Any
    :return: True if the value is a Carnivore, False otherwise
    """
    return isinstance(value, Species) and value.has_trait(CarnivoreCard)

def is_extant_carnivore(value):
    """ Is the given value an extant carnivore
    :param value: The value being checked
    :type value: Any
    :return: True if the value is a Extant Carnivore, False otherwise
    """
    return Species.is_extant_species(value) and value.has_trait(CarnivoreCard)

def is_vegetarian(value):
    """ Is the given value a Vegetarian?
    :param value: The value being checked
    :type value: Any
    :return: True if the value is a Vegetarian, False otherwise
    """
    return isinstance(value, Species) and not value.has_trait(CarnivoreCard)

def is_fat_species(value):
    """ Is the given value a Fat Species?
    :param value: The value being checked
    :type value: Any
    :return: True if the value is a Carnivore, False otherwise
    """
    return isinstance(value, Species) and value.has_trait(FatTissueCard)
