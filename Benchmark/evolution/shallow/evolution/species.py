from evolution.constants import PLAYER_STARTING_FOOD_TOKENS, TRAIT_CARD_MIN_FOOD_TOKENS, TRAIT_CARD_MAX_FOOD_TOKENS, CARNIVORE_MIN_FOOD_TOKENS, CARNIVORE_MAX_FOOD_TOKENS, ATTACK_POP_REDUCTION, FAT_TISSUE_STARTING_FOOD, HARD_SHELL_OFFSET, DEFAUlT_FEED_AMOUNT, FORAGING_FOOD_ADDED, HORN_POP_REDUCTION, COOP_EXTRA_FOOD, FERTILE_POP_INC, SPECIES_START_FOOD, SPECIES_START_POP, SPECIES_EXTINCTION_POP, SPECIES_MAX_POP, SPECIES_START_BODY_SIZE, SPECIES_MIN_BODY_SIZE, SPECIES_MAX_BODY_SIZE, SPECIES_MAX_TRAITS_PER_SPECIES, TRAIT_CARD_DEFAULT_FOOD_TOKENS, TRAIT_CARD_DEFAULT_DESC, MIN_BOARD_FOOD_TOKENS, GEN_TRAIT_CARD_STORED_FOOD, DEFAULT_WATER_HOLE, FORAGING_FEED_ORDERING, COOP_FEED_ORDERING, FERTILE_ORDERING, LONG_NECK_ORDERING, DEFAULT_FEED_ORDERING
from evolution.data_defs import is_natural, is_index, is_natural_plus, is_int_greater_or_equal_to, is_int_in_inclusive_range, is_list_with_len, is_list_with_max_len, is_list_with_len_and_first, is_list_of, is_list_of_valid_elem, is_list_of_nat
from evolution.situation_flag import SituationFlag
from evolution.trait_cards import TraitCard, ScavengerCard, CarnivoreCard, FatTissueCard
from evolution.player.player_feeding_choice import PlayerAttackWithCarnivore, \
    PlayerFeedVegetarian, PlayerForgoAttack, PlayerStoreFat
from evolution.util import type_comparator, of_type_comparator, any_duplicates, does_list_contain


class Species:
    def __init__(self,
                 num_food_tokens=SPECIES_START_FOOD,
                 body_size=SPECIES_START_BODY_SIZE,
                 population=SPECIES_START_POP,
                 played_cards=None):
        """
        :param num_food_tokens: Number of food tokens fed to the species
        :type num_food_tokens: Nat
        :param body_size: Body size of the species
        :type body_size: Nat
        :param population: Population of the species
        :type population: Nat
        :param played_cards: Trait cards on the species
        :type played_cards: [PlayedCard, ...] or None
        :return: None
        """
        self.set_population(population)
        self.set_body_size(body_size)
        self.set_num_food_tokens(num_food_tokens)
        self.set_cards([] if played_cards is None else played_cards)

    def set_num_food_tokens(self, num_food_tokens):
        """ Set the Number of food tokens
        :param num_food_tokens: Number of food tokens
        :type num_food_tokens: Nat
        :raise: ValueError if invalid input
        :return: None
        """
        if not isinstance(num_food_tokens, int) or\
            num_food_tokens < MIN_BOARD_FOOD_TOKENS or\
            num_food_tokens > self.population:
            raise ValueError('Invalid number %s' % num_food_tokens)
        self.num_food_tokens = num_food_tokens

    def get_cards(self):
        """
         Gets all the Face Up Cards and the empty Face Down Cards
        :return: The all played cards on this boards
        :rtype: [PlayedCard, ...]
        """
        return self.played_cards

    def get_active_cards(self):
        """
         Get the currently active traits of this Species
        :return: The currently active traits of this Species
        :rtype: [TraitCard, ...]
        """
        active_cards = []  # type:  List[TraitCard]
        for played_card in self.played_cards:
            if isinstance(played_card, TraitCard):
                active_cards.append(played_card)

        return active_cards

    def get_population(self, owner_flag=None):
        """ Get the population of the Species
        :param owner_flag: flag indicating this Species role when the population size is being checked
        :type owner_flag: SituationFlag or None
        :return: The population of the Species
        :rtype: Nat
        """
        return self.population

    def set_cards(self, played_cards):
        if not isinstance(played_cards, list) or len(played_cards) > SPECIES_MAX_TRAITS_PER_SPECIES:
            raise ValueError("set_cards: Must send in a list of length of " +
                              str(SPECIES_MAX_TRAITS_PER_SPECIES) + " or less")
        if not all(TraitCard.is_trait_card(card) for card in played_cards):
            raise ValueError("set_cards: All elements must be a TraitCard or FaceDownCard")

        if any_duplicates(played_cards, type_comparator):
            raise ValueError("Species - set_cards: Duplicate TraitCards are not permitted")

        self.played_cards = played_cards


    def set_population(self, population):
        """ Set the population of this Species to the given population
        :param population: The new population
        :type population: Nat
        :raise: ValueError if given population is invalid
        :return: None
        """
        if not is_int_in_inclusive_range(population, SPECIES_EXTINCTION_POP, SPECIES_MAX_POP):
            raise ValueError(
                    "Species - set_population: Population must be an int in range [" +
                    str(SPECIES_EXTINCTION_POP) + ", " + str(SPECIES_MAX_POP) + "]")
        self.population = population


    def get_choices_only_species(self, dealer, self_index):
        """
        Returns the possible evolution choices for the species as if it is the only species
        that can feed.
        :param dealer: the game configuration
        :type dealer: Dealer
        :param self_index: this species's index
        :type self_index: Nat
        :return: The possible evolution choice for this species
        :rtype: [PlayerFeedingChoice, ...]
        """
        choices = []
        if self.is_hungry():
            if self.is_vegetarian():
                choices.append(PlayerFeedVegetarian(self_index))
            else:
                choices += self.get_carnivore_choices(dealer, self_index)

        if self.is_fat_species() and self.fat_tissue_need() > 0:
            difference = min(dealer.wateringhole, self.fat_tissue_need())
            choices.append(PlayerStoreFat(self_index, difference))
        return choices

    def get_carnivore_choices(self, dealer, self_index):
        """
        Returns the possible evolution choices for a carnivore species
        :param dealer: The dealer
        :type dealer: Dealer
        :param self_index: index of this species on it's owning PlayerState
        :type self_index: Nat
        :return: The possible carnivore evolution choices for this species
        """
        choices = []

        for player_i, player_state in enumerate(dealer.player_states):
            player_species = player_state.species_list
            for defender_i, defender in enumerate(player_species):
                right_neighbor = player_species[defender_i + 1] if defender_i + 1 < len(player_species) else None
                left_neighbor = player_species[defender_i - 1] if defender_i - 1 >= 0 else None
                if defender.is_attackable(self, right_neighbor, left_neighbor):
                    choices.append(PlayerAttackWithCarnivore(self_index, player_i, defender_i))
        if choices:
            choices.append(PlayerForgoAttack())
        return choices

    def adjust_population(self, amount):
        """
        Changes the population of this species by the given amount
        :param amount: number to reduce this species population by
        :type amount: int
        :return: None
        """
        self.set_population(self.population + amount)
        self.num_food_tokens = min(self.num_food_tokens, self.population)

    def get_body_size(self, owner_flag=None):
        """ Get the integer body size of this Species
        :param owner_flag: flag indicating this Species role when the body size is being checked
        :type owner_flag: SituationFlag or None
        :return: Get the body size of this Species
        :rtype: Nat
        """
        body_size = self.body_size
        for trait in self.get_active_cards():
            body_size = trait.mod_owner_body_size(self, body_size, owner_flag)
        return body_size

    def set_body_size(self, body_size):
        """
        Set the body_size of this Species to the given body_size
        :param body_size: The new body_size
        :type body_size: Nat
        :raise: ValueError if invalid given body_size is invalid
        :return: None
        """
        if not isinstance(body_size, int) or \
           body_size < SPECIES_MIN_BODY_SIZE or\
           body_size > SPECIES_MAX_BODY_SIZE:
            raise ValueError
        self.body_size = body_size



    def add_stored_fat_food(self, stored_fat_food):
        """
         Store the given Amount of fat food on your Fat Token
        :param stored_fat_food: The fat you wish to store
        :type stored_fat_food: Nat+
        :return: None
        """
        if not (is_natural(stored_fat_food) and stored_fat_food <= self.get_body_size()):
            raise ValueError("Species - add_stored_fat_food: Invalid stored_fat_food : {}. Must be between {} and {}."
                             .format(stored_fat_food, 0, self.get_body_size()))

        [trait.add_stored_fat_food(stored_fat_food, self.body_size) for trait in self.get_active_cards()]

    def is_extinct(self):
        """
        Is this Species Extinct?
        :return: True if this Species is Extinct, False Otherwise
        :rtype: bool
        """
        return self.population <= SPECIES_EXTINCTION_POP

    def has_trait(self, trait_type):
        """ Does this Species have the given TraitCard type
        :param trait_type: The TraitCard type being checked for
        :return: True if this Species has the given TraitCard type, False otherwise
        :rtype: bool
        """
        return does_list_contain(self.get_active_cards(), trait_type, of_type_comparator)

    def is_hungry(self):
        """
        Is this Species hungry?
        :return: True if this Species is hungry, False otherwise
        :rtype: Boolean
        """
        return self.num_food_tokens < self.population

    def how_hungry(self):
        """
        How hungry is this Species, its population - how many have been fed this turn
        :return: The number of members of this Species left to be fed
        :rtype: Nat
        """
        return self.population - self.num_food_tokens

    def is_done_feeding(self):
        """ Is this Species done evolution?
        :return: True if this Species is done evolution, False Otherwise
        :rtype: Boolean
        """
        return not self.is_hungry()

    def is_attackable(self, attacker, defenders_left_neighbor=None, defenders_right_neighbor=None):
        """ Can the given attacker attack the given defender given the defender's left and right neighbors?
        :param attacker: The attacking Carnivore
        :type attacker: Species
        :param defenders_left_neighbor: The defender's left neighbor
        :type defenders_left_neighbor: Species or None
        :param defenders_right_neighbor: The defender's right neighbor
        :type defenders_right_neighbor: Species or None
        :return: True if the defender is attackable by the attacker, False otherwise
        :rtype: Boolean
        """
        return not self is attacker and \
               not self._attacks_blocked(attacker, defenders_left_neighbor, defenders_right_neighbor)

    def can_attack_player(self, player_species):
        """
        Can this species attack any of the opponent's species as given in the list, assuming this is a Carnivore
        :param player_species: list of the opponent's species boards from left to right
        :type player_species: [Species, ...]
        :return: True if this species can attack one or more of the given species, false otherwise
        :rtype: Boolean
        """
        return self.best_attack_on_player(player_species, lambda x: 0)[0] is not None

    def best_attack_on_player(self, player_species, key):
        """
        Gets the best attack this species can manage on the given list of a player's species
        :param player_species: The list of species of the player being attacked, in left->right order
        :type player_species: [Species, ...]
        :param key: The key used to compare the species, greater than is better
        :type key: Species -> T
        :return: (Index, key) of the largest attackable species or None if no attack is possible
        :rtype: (Nat or None, T)
        """
        best_species_key = None
        best_species_index = None

        last_species = None
        for index, cur_species in enumerate(player_species):
            next_species = None if (index + 1) >= len(player_species) else player_species[index + 1]
            if cur_species.is_attackable(self, last_species, next_species):
                cur_species_key = key(cur_species)
                if best_species_key is None or cur_species_key > best_species_key:
                    best_species_key = cur_species_key
                    best_species_index = index
            last_species = cur_species
        return best_species_index, best_species_key

    def can_store_fat(self):
        """ Can this species store food in its fat?
        :return: True if this species is able to store food in fat, False otherwise
        """
        return self.fat_tissue_need() > 0

    def fat_tissue_need(self):
        """ Get the Fat Tissue need of this Species
        :return: The Fat Tissue need of this Species
        :rtype: Nat
        """
        return max([card.fat_tissue_need(self.body_size) for card in self.get_active_cards()], default=0)

    def get_fat_tissue_food(self):
        """
        :return: The number of food tokens on this Species FatTissueCard if it has one
        :rtype: Nat
        """
        return max([card.get_food_stored() for card in self.get_active_cards()], default=0)

    def _attacks_blocked(self, attacker, defenders_left_neighbor= None, defenders_right_neighbor=None):
        """ Are attacks from the given attacker blocked by given defender or by the defender's left and right neighbors?
        :param attacker:                 The attacking Carnivore
        :type attacker: Species
        :param defenders_left_neighbor:  The defender's left neighbor
        :type defenders_left_neighbor: Species or None
        :param defenders_right_neighbor: The defender's right neighbor
        :type defenders_right_neighbor: Species or None
        :return: True if the defender is unattackable by the attacker, False otherwise
        :rtype: Boolean
        """
        return any(Species._any_traits_blocks_attacks(self, attacker, defenders_left_neighbor,
                                                      defenders_right_neighbor, owner_flag)
                   for owner_flag in SituationFlag)


    def is_carnivore(self):
        """
        Is the given self a Carnivore?
        :return: True if the self is a Carnivore, False otherwise
        """
        return isinstance(self, Species) and self.has_trait(CarnivoreCard)

    def is_extant_carnivore(self):
        """
        Is the given self an extant carnivore
        :return: True if the self is a Extant Carnivore, False otherwise
        """
        return Species.is_extant_species(self) and self.has_trait(CarnivoreCard)

    def is_vegetarian(self):
        """
        Is the given self a Vegetarian?
        :return: True if the self is a Vegetarian, False otherwise
        """
        return isinstance(self, Species) and not self.has_trait(CarnivoreCard)

    def is_fat_species(self):
        """
        Is the given self a Fat Species?
        :return: True if the self is a Carnivore, False otherwise
        """
        return isinstance(self, Species) and self.has_trait(FatTissueCard)


    def apply_before_feeding(self, dealer, player_index, species_index):
        """
        Applies the steps needed before evolution to the game
        :param dealer:  the dealer of the game
        :type dealer: Dealer
        :param player_index: index of player who owns this species
        :type player_index: Nat
        :param species_index: this species' index
        :type species_index: Nat
        :return: None
        """
        traits = self.get_sorted_traits()
        for trait in traits:
            trait.apply_before_feeding(dealer, player_index, species_index)

    def apply_feed(self, dealer, player_index, species_index, ignored_traits=[]):
        """
        Updates this species based on evolution
        :param wateringhole: The wateringhole
        :type wateringhole: int
        :param species_list: The species list of the owning player
        :type species_list: [Species, ...]
        :param index: The index of this species in species_list
        :type index: int
        :param ignored_traits: Traits not to apply evolution on
        :type ignored_traits: [TraitCard, ...]
        :return: The resulting wateringhole
        :rtype: int
        """
        taken_food = min(DEFAUlT_FEED_AMOUNT, dealer.wateringhole, self.population - self.num_food_tokens)
        self.num_food_tokens += taken_food
        dealer.wateringhole -= taken_food
        if taken_food > 0:
            traits = self.get_sorted_traits()
            traits_to_trigger = [trait for trait in traits if trait not in ignored_traits]
            return self.trigger_on_feed(dealer, player_index, species_index, traits_to_trigger)

    def trigger_on_feed(self, dealer, player_index, species_index, traits):
        """
        Triggers the actions that happen after a evolution
        :param wateringhole: The wateringhole
        :type wateringhole: int
        :param species_list: The species list
        :type species_list: [Species, ...]
        :param index: The index of this species in species_list
        :type index: int
        :param traits: traits to trigger
        :type traits: [TraitCard, ...]
        :return: None
        """
        for trait in traits:
            trait.on_feed(dealer, player_index, species_index)

    def apply_scanvenger(self, dealer, player_index, species_index):
        """
        Feed this Species if it has the scavenger trait
        :param wateringhole: the wateringhole
        :type wateringhole: Nat
        :param species_list: The species list
        :type species_list: [Species, ...]
        :param index: Index of the species
        :type index: int
        :return: Watering hole
        """
        if self.has_trait(ScavengerCard):
            self.apply_feed(dealer, player_index, species_index)

    def get_sorted_traits(self):
        """
        Sorts the list of traits for this species
        in the order they should be applied
        during the evolution
        :return: List of sorted traits
        :rtype: [TraitCard, ...]
        """
        traits = self.get_active_cards()
        return sorted(traits, key=lambda trait: trait.get_on_feed_ordering())

    @staticmethod
    def _any_traits_blocks_attacks(defender, attacker,
                                   defenders_left_neighbor=None,
                                   defenders_right_neighbor=None,
                                   owner_flag=SituationFlag.DEFENDER):
        """ Are attacks from the given attacker blocked by the traits of flagged owner
        :param defender: The defending Species
        :type defender: Species
        :param attacker: The attacking Carnivore
        :type attacker: Species
        :param defenders_left_neighbor:  The defender's left neighbor
        :type defenders_right_neighbor: Species or None
        :param defenders_right_neighbor: The defender's right neighbor
        :type defenders_left_neighbor: species or None
        :param owner_flag: The flag which tells you whose traits are being looked at for blocking
        :return: True if the defender is unattackable by the attacker given the flagged owner's traits, False otherwise
        :rtype: Booleam
        """
        owner_species = Species.get_owner_species(defender, attacker, defenders_left_neighbor,
                                                  defenders_right_neighbor,
                                                  owner_flag)

        if owner_species is None:
            return False
        else:
            return any(trait.blocks_attack(defender, attacker, defenders_left_neighbor,
                                           defenders_right_neighbor, owner_flag)
                       for trait in owner_species.get_active_cards())

    @staticmethod
    def get_owner_species(defender,
                          attacker,
                          defenders_left_neighbor= None,
                          defenders_right_neighbor= None,
                          owner_flag = None):
        """ Get the owner corresponding to the owner_flag given all participants
        :param defender:                 The defending Species
        :type defender: Species
        :param attacker:                 The attacking Carnivore
        :type attacker: Species
        :param defenders_left_neighbor:  The defender's left neighbor
        :type defenders_left_neighbor: Species orNone
        :param defenders_right_neighbor: The defender's right neighbor
        :type defenders_right_neighbor: Species or None
        :param owner_flag:               The flag which tells you whose traits are being looked at for blocking
        :type owner_flag: SituationFlag
        :return: The owner Species or None if no valid owner
        :rtype: Species or None
        """
        if owner_flag is SituationFlag.ATTACKER:
            return attacker
        elif owner_flag is SituationFlag.DEFENDER:
            return defender
        elif owner_flag is SituationFlag.DEFENDER_L_NEIGHBOR:
            return defenders_left_neighbor
        elif owner_flag is SituationFlag.DEFENDER_R_NEIGHBOR:
            return defenders_right_neighbor
        else:
            return None

    @staticmethod
    def is_opt_species(value):
        """ Is the given self a valid Optional Species
        :param value: The self being checked
        :type value: Any
        :return: True if the self is a valid Optional Species, False otherwise
        :rtype: Boolean
        """
        return (value is None) or isinstance(value, Species)

    @staticmethod
    def is_extant_species(value):
        """ Is the given self a valid extant Species
        :param value: The self being checked
        :type value: Any
        :return: True if the self is a valid and extant, False otherwise
        :rtype: Boolean
        """
        return isinstance(value, Species) and not value.is_extinct()

    @staticmethod
    def is_opt_extant_species(value):
        """ Is the given self a valid extant Optional Species
        :param value: The self being checked
        :type value: Any
        :return: True if the self is a valid and extant, False otherwise
        :rtype: Boolean
        """
        return (value is None) or (isinstance(value, Species) and not value.is_extinct())

    def __eq__(self, other):
        if not isinstance(other, Species):
            return False

        return (self.body_size == other.body_size) and \
               (self.population == other.population) and \
               (self.num_food_tokens == other.num_food_tokens) and \
               (self.played_cards == other.played_cards)

    def __repr__(self):
        return "Species({},{},{},{})".format(self.num_food_tokens, self.body_size,
                                             self.population, self.get_active_cards())
