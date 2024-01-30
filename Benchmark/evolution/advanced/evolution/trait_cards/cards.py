from abc import ABCMeta
from evolution.constants import PLAYER_STARTING_FOOD_TOKENS, TRAIT_CARD_MIN_FOOD_TOKENS, TRAIT_CARD_MAX_FOOD_TOKENS, CARNIVORE_MIN_FOOD_TOKENS, CARNIVORE_MAX_FOOD_TOKENS, ATTACK_POP_REDUCTION, FAT_TISSUE_STARTING_FOOD, HARD_SHELL_OFFSET, DEFAUlT_FEED_AMOUNT, FORAGING_FOOD_ADDED, HORN_POP_REDUCTION, COOP_EXTRA_FOOD, FERTILE_POP_INC, SPECIES_START_FOOD, SPECIES_START_POP, SPECIES_EXTINCTION_POP, SPECIES_MAX_POP, SPECIES_START_BODY_SIZE, SPECIES_MIN_BODY_SIZE, SPECIES_MAX_BODY_SIZE, SPECIES_MAX_TRAITS_PER_SPECIES, TRAIT_CARD_DEFAULT_FOOD_TOKENS, TRAIT_CARD_DEFAULT_DESC, MIN_BOARD_FOOD_TOKENS, GEN_TRAIT_CARD_STORED_FOOD, DEFAULT_WATER_HOLE, FORAGING_FEED_ORDERING, COOP_FEED_ORDERING, FERTILE_ORDERING, LONG_NECK_ORDERING, DEFAULT_FEED_ORDERING
from evolution.data_defs import is_natural, is_index, is_natural_plus, is_int_greater_or_equal_to, is_int_in_inclusive_range, is_list_with_len, is_list_with_max_len, is_list_with_len_and_first, is_list_of, is_list_of_valid_elem, is_list_of_nat
from evolution.situation_flag import SituationFlag


"""
PlayedCard is one of:
- TraitCard
- FaceDownCard
"""

class TraitCard:

    def __init__(self, num_tokens_as_food_card=TRAIT_CARD_DEFAULT_FOOD_TOKENS, description=TRAIT_CARD_DEFAULT_DESC):
        """
        Construct a TraitCard with its number of food tokens on the card
        :param num_tokens_as_food_card: The number of food tokens on the card
        :type num_tokens_as_food_card: int
        :param description:     The description on the card
        :type description: String
        :return: None
        """
        self.num_tokens_as_food_card = TRAIT_CARD_MIN_FOOD_TOKENS
        self.set_num_tokens_as_food_card(num_tokens_as_food_card)
        self.description = TRAIT_CARD_DEFAULT_DESC
        self.set_description(description)

    @classmethod
    def make_list_of_cards(cls):
        """
        Creates a list of all possible cards
        for this trait
        :return: all the cards
        :rtype: [TraitCard, ...]
        """
        min_val = cls.get_min()
        max_val = cls.get_max()
        return [cls(i) for i in range(min_val, max_val+1)]


    def get_num_tokens_as_food_card(self):
        """ Get the number of food tokens as a food card
        :return: The number of food tokens as a food card
        :rtype: int
        """
        return self.num_tokens_as_food_card

    def set_num_tokens_as_food_card(self, num_tokens_as_food_card):
        """ Set the Number of Food Tokens
        :param num_tokens_as_food_card: The new number_of_tokens
        :type num_tokens_as_food_card: int
        :raise: ValueError if sent invalid value
        :return: None
        """
        if not isinstance(num_tokens_as_food_card, int) or \
            num_tokens_as_food_card < TRAIT_CARD_MIN_FOOD_TOKENS or \
            num_tokens_as_food_card > TRAIT_CARD_MAX_FOOD_TOKENS:

            raise ValueError(self.__class__.__name__ + " - set_number_of_food_tokens: Number of Food Tokens must be " +
                             "in range [" + str(TRAIT_CARD_MIN_FOOD_TOKENS) + ", " + str(TRAIT_CARD_MAX_FOOD_TOKENS) +
                             "]")
        self.num_tokens_as_food_card = num_tokens_as_food_card

    def get_description(self):
        """
        Get the description
        :return: The description
        :rtype: String
        """
        return self.description

    def set_description(self, description):
        """ Set the description
        :param description: The new description
        :type description: String
        :return: None
        """
        if isinstance(description, str):
            self.description = description
        else:
            raise ValueError("TraitCard - set_description: Set the description")

    def blocks_attack(self,
                      defender,
                      attacker,
                      defenders_left_neighbor=None,
                      defenders_right_neighbor=None,
                      owner_flag=None):
        """ Does this TraitCard block attacks from a given attacker and the defenders neighbors
        :param defender: The defending Species
        :type defender: feeding.Species.Species
        :param attacker: The attacking Carnivore
        :type attacker: feeding.Species.Species
        :param defenders_left_neighbor: The defender's left neighbor
        :type defenders_left_neighbor: feeding.Species.Species or None
        :param defenders_right_neighbor: The defender's right neighbor
        :type defenders_right_neighbor: feeding.Species.Species or None
        :param owner_flag: The owner of this Trait
        :type owner_flag: SituationFlag or None
        :return: True if this blocks attacks from the given attacker, False otherwise
        :rtype: bool

        Behavioral contracts:
        owner_flag = DEFENDER_RIGHT_NEIGHBOR_FLAG => defenders_right_neighbor is not None
        owner_flag = DEFENDER_LEFT_NEIGHBOR_FLAG  => defenders_left_neighbor  is not None
        """
        return False

    def mod_owner_body_size(self, owner, owner_current_body_size, owner_flag=None):
        """ Modify the owner Species' body_size
        :param owner: The owner Species
        :type owner: feeding.Species.Species
        :param owner_current_body_size: The owner's current body_size
        :type owner_current_body_size: Nat
        :param owner_flag: The owner's situation flag
        :type owner_flag: SituationFlag or None
        :return: The Modified Body Size of the Owner
        :rtype: Nat
        """
        return owner_current_body_size

    def on_feed(self, dealer, player_index, species_index):
        """
        Performs the actions of this trait on a evolution
        :param wateringhole: the wateringhole
        :type wateringhole: Nat
        :param species_list: owning player's list of species
        :type species_list: [Species, ...]
        :param index: Index of this card's owning species
        :type index: Int
        :param traits: traits to be triggered
        :type traits: [TraitCard ...]
        :return: updated wateringhole
        :rtype: Nat
        """
        return

    def apply_before_feeding(self, dealer, player_index, species_index):
        """
        Applies needed changes to the game
        :param dealer: the dealer of the game
        :type dealer: Dealer
        :param player_index: the index of the player who owns species
        :type player_index: Nat
        :param species_index: this species' index
        :type species_index: Nat
        :return: None
        """
        return

    def get_food_stored(self):
        """
        Gets the number of food tokens stored on this card
        :return: the number of food tokens stored
        :rtype: Nat
        """
        return 0

    def fat_tissue_need(self, owner_body_size):
        """ How many tokens of food can this TraitCard store?
        :param owner_body_size: body size of the owning Species
        :type owner_body_size: Nat
        :rtype: Nat
        """
        return 0

    def add_stored_fat_food(self, stored_fat_food, owner_body_size):
        """ Set the stored fat food which is always GEN_TRAIT_CARD_STORED_FOOD for Non-FatTissueCards
        :param stored_fat_food: The amount of food you wish to store
        :type stored_fat_food: Nat
        :param owner_body_size: The owner's body size
        :type owner_body_size: Nat
        :return: The new self.food
        :rtype: Nat
        """
        if not (is_natural(stored_fat_food) and is_natural(owner_body_size) and stored_fat_food <= owner_body_size):
            raise ValueError("TraitCard - add_stored_fat_food: 0 <= stored_fat_food <= owner_body_size")

        return 0

    def can_store_fat(self, owner_body_size):
        """
        Is this trait card capable of storing food as fat?
        :param owner_body_size: body size of the owning Species
        :type owner_body_size: Nat
        :return: True if this Species can store fat, False otherwise
        :rtype: Boolean
        """
        return self.fat_tissue_need(owner_body_size) > 0

    def get_name(self):
        raise NotImplementedError('Method not yet implemented on ' +
                                  str(self.__class__.__name__))

    def get_on_feed_ordering(self):
        """
        Gets the ordering in which to apply this trait on a evolution
        :return: number representing it's position in the ordering
        :rtype: int
        """
        return DEFAULT_FEED_ORDERING

    @classmethod
    def get_min(cls):
        """
        Gets the minimum value allowed on this card
        :return: Int
        """
        return TRAIT_CARD_MIN_FOOD_TOKENS

    @classmethod
    def get_max(cls):
        """
        Gets the maximum value allowed on this card
        :return: Int
        """
        return TRAIT_CARD_MAX_FOOD_TOKENS

    @staticmethod
    def is_trait_card(val):
        """
        Is val a TraitCard?
        :param val: the value
        :type val: any
        :return: true if val is a TraitCard and
        False otherwise.
        :rtype: Boolean
        """
        return isinstance(val, TraitCard)


    def __eq__(self, other):
        return isinstance(other, TraitCard) and \
               (self.num_tokens_as_food_card == other.num_tokens_as_food_card)
