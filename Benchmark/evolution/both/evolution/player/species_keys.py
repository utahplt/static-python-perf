import enum
from functools import total_ordering

from evolution.player.iplayer import IPlayer
from evolution.species_types import *


class SpeciesFeedType(enum.Enum):
    """ Represents the different types of feedings that can be picked,
    with their value representing the priority (higher number = higer priority)
    """
    STORE_FAT = 3
    FEEDABLE_VEG = 2
    FEEDABLE_CARN = 1
    FORGO_ATTACK = 0
    UNFEEDABLE = -1


@total_ordering
class SpeciesPickKey:
    def __init__(self, species, owning_player_index, players):
        """
        :param species: The species to be compared
        :type species: feeding.Species.Species
        :param owning_player_index: The index of the species owning Player in players
        :type owning_player_index: Nat
        :param players: The states of all the players in the game
        :type players: [PlayerState, ...]
        :return None
        """
        self.species = species
        self.feed_type = get_species_feed_type(self.species, owning_player_index, players)

    def __gt__(self, other):
        """
        :param other: The key to be compared to this
        :type other: SpeciesPickKey
        """
        if self.feed_type is not other.feed_type:
            return self.feed_type.value > other.feed_type.value
        if self.feed_type is SpeciesFeedType.STORE_FAT:
            return FatOrderKey(self.species) > FatOrderKey(other.species)
        if self.feed_type in (SpeciesFeedType.FEEDABLE_CARN, SpeciesFeedType.FEEDABLE_VEG):
            return SpeciesOrderKey(self.species) > SpeciesOrderKey(other.species)
        return False

    def __eq__(self, other):
        """
        :param other: The key to be compared to this
        :type other: SpeciesPickKey
        """
        if self.feed_type is not other.feed_type:
            return False
        # at this point we know Rest keys are the same
        if self.feed_type is SpeciesFeedType.STORE_FAT:
            return FatOrderKey(self.species) == FatOrderKey(other.species)
        if self.feed_type in (SpeciesFeedType.FEEDABLE_CARN, SpeciesFeedType.FEEDABLE_VEG):
            return SpeciesOrderKey(self.species) == SpeciesOrderKey(other.species)
        # Rest must be unfeedable
        return True


def get_species_feed_type(species, owning_player_index, players):
    """
    Gets the evolution type of species
    :param species: the species
    :type species: feeding.Species.Species
    :param owning_player_index: the player owning species
    :type owning_player_index: IPlayer
    :param players: the opponents of the player
    :type players: [PlayerState, ...]
    :return: The type of evolution
    :rtype: SpeciesFeedType
    """
    if species.can_store_fat():
        return SpeciesFeedType.STORE_FAT
    elif species.is_hungry():
        if is_vegetarian(species):
            return SpeciesFeedType.FEEDABLE_VEG
        # Checks if any of the items in the list are true
        owning_player = players[owning_player_index]
        if any(species.can_attack_player(player.get_all_species())
               for player in players if player is not owning_player):
            return SpeciesFeedType.FEEDABLE_CARN
        if species.can_attack_player(owning_player.get_all_species()):
            return SpeciesFeedType.FORGO_ATTACK

    return SpeciesFeedType.UNFEEDABLE

@total_ordering
class SpeciesOrderKey():
    """
    Represents the ordering of the species.
    Ordering is defined as:
    starting with the (plain) population attribute,
    followed by the food that the species has been
    fed so far, and finally the (plain) body size.
    """
    def __init__(self, species):
        """
        :param species:
        :type species:
        :return: None
        """
        self.species = species

    def __eq__(self, other):
        """
        Is this species of this key equal to the species of the other key?
        :param other:
        :return:
        """
        return self.species.population == other.species.population and \
               self.species.body_size == other.species.body_size and \
               self.species.num_food_tokens == other.species.num_food_tokens

    def __gt__(self, other):
        return self.species.population > other.species.population or\
               (self.species.population == other.species.population and
                self.species.num_food_tokens > other.species.num_food_tokens) or \
               (self.species.population == other.species.population and
                self.species.num_food_tokens == other.species.num_food_tokens
                and self.species.body_size > other.species.body_size)


@total_ordering
class FatOrderKey:
    def __init__(self, species: Species):
        self.species = species

    def __gt__(self, other):
        return self.species.fat_tissue_need() > other.species.fat_tissue_need() or \
               (self.species.fat_tissue_need() == other.species.fat_tissue_need() and
                (SpeciesOrderKey(self.species) > SpeciesOrderKey(other.species)))

    def __eq__(self, other):
        return self.species.fat_tissue_need() == other.species.fat_tissue_need() and \
               (SpeciesOrderKey(self.species) == SpeciesOrderKey(other.species))
