from evolution.species import Species
from evolution.constants import PLAYER_STARTING_FOOD_TOKENS
from dealer.constants import BASE_DEAL_NUMBER
from evolution.data_defs import is_natural_plus, is_list_of, is_natural
from evolution.trait_cards import TraitCard
from evolution.timeout import timeout



class PlayerState:
    """
    To represent the state of the player
    """
    def __init__(self, id, species_list=None,
                 food_bag=PLAYER_STARTING_FOOD_TOKENS, hand=None):
        """ Create a new player-state made for clients, with the given
        number of food tokens and the given list of Species
        :param id: The id number of the player
        :type id: Nat+
        :param species_list: the list of Species owned by the Player
        :type species_list: [Species, ...]
        :param food_bag: the number of tokens in the food bag
        :type food_bag: Nat+
        :param hand: This Player's initial hand
        :type hand: [TraitCard, ...]
        :return: None
        """
        if not is_natural_plus(id):
            raise ValueError(
                "__init__: Player Id must be a positive Natural, got: " + str(
                    id))
        if not (is_list_of(species_list, Species) or species_list is None):
            raise ValueError(
                "__init__: Species List is not a valid list of Species: " + repr(
                    species_list))
        if not is_natural(food_bag):
            raise ValueError(
                "__init__: The food bag must be a Natural, got: " + str(
                    food_bag))
        if not (is_list_of(hand, TraitCard) or hand is None):
            raise ValueError(
                "__init__: Invalid Hand, must be a List of TraitCards")

        self.id = id
        self.food_bag = food_bag
        self.species_list = [] if species_list is None else species_list
        self.hand = [] if hand is None else hand


    def sorted_hand(self):
        """
        Gets the hand of this player, sorted by trait name and then food tokens
        :return: Sorted hand
        :rtype: [TraitCard, ...]
        """
        by_number = sorted(self.hand,
                           key=lambda tc: tc.num_tokens_as_food_card)
        return sorted(by_number, key=lambda tc: tc.get_name())


    def get_id(self):
        """
        Get the id of this Player
        :return: The id of this Player
        :rtype: Nat+
        """
        return self.id

    def get_food_bag(self):
        """ Get the number of food tokens in this Player's food bag
        :return: number of food tokens
        :rtype: Nat
        """
        return self.food_bag

    def get_all_species(self):
        """ Get All the Species of this Player
        :return: A list of this Player's species. Guaranteed non-empty
        :rtype: [Species, ...]
        """
        return self.species_list

    def get_num_species(self):
        """
        Get the number of Species
        :return: The number of Species
        """
        return len(self.get_all_species())

    def get_species_at_index(self, index):
        """ Get the species at the given index
        :param index: The Index of the Species
        :type index: Nat
        :return: The Species at the given IndexOfSpecies or raise IndexError
        :rtype: Species
        """
        if 0 <= index < len(self.species_list):
            return self.species_list[index]
        return None

    def has_hungry_veg(self):
        """
        Checks if this player has any hungry vegeterians
        :return: True if player has hungry vegeterians
        and false otherwise
        :rtype: boolean
        """
        return all(self.verify_species(i, Species.is_hungry) for i in range(len(self.species_list)))

    def get_needed_cards(self):
        """
        Gets the cards needed by this
        player for the turn
        :return: number of cards
        :rtype: Nat
        """
        if len(self.species_list) == 0:
            return BASE_DEAL_NUMBER+1
        else:
            return BASE_DEAL_NUMBER + len(self.species_list)

    def get_neighbors(self, index):
        """
        Gets the neighbors of species with the given index
        :param index: index of the species
        :type index: Nat
        :return: The left and right neighbors
        :rtype: (Species, Species)
        """
        return self.get_species_at_index(index-1), self.get_species_at_index(index+1)
