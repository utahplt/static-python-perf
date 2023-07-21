from abc import ABCMeta
from evolution.trait_cards import HornCard
from evolution.constants import HORN_POP_REDUCTION, ATTACK_POP_REDUCTION

__author__ = 'Edwin Cowart, Kevin McDonough'


class PlayerFeedingChoice:
    """
    Represents the Feeding Choice being made by the Player
    """
    def apply_choice(self, index, dealer):
        """
        Applies the evolution choice on the player states
        """
        raise NotImplementedError('Method should not be called')

    def rotate_right(self, n, players_len):
        """
        Rotates the player index to the right by n,

        :type n: Nat
        :type players_len: Nat
        """
        return self

    def verify_self(self, player_states, own_player_state):
        """
        Verifies that this feeding choice is valid
        :type player_states: [PlayerState, ...]
        :type own_player_state: PlayerState
        :rtype: Boolean
        """
        raise NotImplementedError("Method not yet implemented")


class PlayerForgoAttack(PlayerFeedingChoice):

    def verify_self(self, player_states, own_player_state):
        return not own_player_state.has_hungry_veg()

    def __repr__(self):
        return "PlayerForgoAttack()".format()

    def __eq__(self, other):
        return isinstance(other, PlayerForgoAttack)


class PlayerFeedVegetarian(PlayerFeedingChoice):
    """
    Represents vegeterian evolution return type
    """
    def __init__(self, vegetarian_index):
        """
        :param vegetarian_index: Index of the vegeterian to feed
        :type vegetarian_index: Nat
        :return: None
        """
        self.vegetarian_index = vegetarian_index

    def get_vegetarian_index(self):
        """
        Get the Vegetarian index of this PlayerFeedVegetarian
        :return: The index of the Vegetarian you wish to feed
        :rtype: Nat
        """
        return self.vegetarian_index

    def apply_choice(self, index, dealer):
        player_state = dealer.player_states[index]
        species = player_state.get_species_at_index(self.vegetarian_index)
        species.apply_feed(dealer, index, self.vegetarian_index)

    def verify_self(self, player_states, own_player_state):
        is_hungry_veg = lambda s: s.is_hungry() and s.is_vegetarian()
        return own_player_state.verify_species(self.vegetarian_index, is_hungry_veg)

    def __eq__(self, other):
        return isinstance(other, PlayerFeedVegetarian) and \
               self.get_vegetarian_index() == other.get_vegetarian_index()

    def __repr__(self):
        return "FeedVegitarian({})".format(self.get_vegetarian_index())


class PlayerStoreFat(PlayerFeedingChoice):
    def __init__(self, species_index, num_food_to_store):
        """
         Store a number of food tokens as Fat for the Species at the given index
        :param species_index: The index of the Species
        :type species_index: Nat
        :param num_food_to_store: The amount of food being stored
        :type num_food_to_store: Nat+
        :return None
        """
        self.species_index = species_index  # type: Index
        self.num_food_to_store = num_food_to_store  # type: NaturalPlus

    def get_species_index(self):
        """
        Get the index of the Species the Food is being stored within
        :return: The index of the Species
        :rtype: Nat
        """
        return self.species_index

    def get_num_food_to_store(self):
        """ Get the amount of food you wish to store on the Species at the index
        :return: The number of food tokens to store
        :rtype: Nat+
        """
        return self.num_food_to_store

    def verify_self(self, player_states, own_player_state):
        has_fat_space = lambda s: s.fat_tissue_need() >= self.num_food_to_store
        return own_player_state.verify_species(self.species_index, has_fat_space)

    def apply_choice(self, index, dealer):
        player_state = dealer.player_states[index]
        species = player_state.get_species_at_index(self.species_index)
        species.add_stored_fat_food(self.num_food_to_store)
        dealer.wateringhole -= self.num_food_to_store

    def __repr__(self):
        return "StoreFood({}, {})".format(self.get_species_index(), self.get_num_food_to_store())

    def __eq__(self, other):
        if not isinstance(other, PlayerStoreFat):
            return False
        return self.get_species_index() == other.get_species_index() and \
               self.get_num_food_to_store() == other.get_num_food_to_store()


class PlayerAttackWithCarnivore(PlayerFeedingChoice):
    def __init__(self, your_carnivore_index, target_player_index, target_species_index):
        """ Construct an Attack with Carnivore to feed that Carnivore
        :param your_carnivore_index: The Index of your Carnivore
        :type your_carnivore_index: Nat
        :param target_player_index: The target player's index
        :type target_player_index: Nat
        :param target_species_index: The target Species of the target player
        :type target_species_index: Nat
        :return None
        """
        self.your_carnivore_index = your_carnivore_index
        self.target_player_index = target_player_index
        self.target_species_index = target_species_index

    def get_carnivore_index(self):
        """ Get your Carnivore Index
        :return: Your Carnivore's Index
        :rtype: Nat
        """
        return self.your_carnivore_index

    def get_target_player_index(self):
        """ Get the Index of the target Player
        :return: The Index of the target Player
        :rtype: Nat+
        """
        return self.target_player_index

    def get_target_species_index(self):
        """ Get the Index of the target Species
        :return: The Index of the target Species
        :rtype: Nat+
        """
        return self.target_species_index

    def apply_choice(self, index, dealer):
        attacker_state = dealer.player_states[index]
        attacker_species = attacker_state.get_species_at_index(self.your_carnivore_index)

        defender_state = dealer.player_states[self.target_player_index]
        defender_species = defender_state.get_species_at_index(self.target_species_index)

        dealer.reduce_population(self.target_species_index, ATTACK_POP_REDUCTION, self.target_player_index)

        if defender_species.has_trait(HornCard):
            dealer.reduce_population(self.your_carnivore_index, HORN_POP_REDUCTION, index)

        attacker_species.apply_feed(dealer, index, self.your_carnivore_index)
        self._apply_scavenger(dealer)


    def _apply_scavenger(self, dealer):
        """
        Apply the scavenger trait across all player states in the given dealer
        :param dealer: the dealer
        :type dealer: Dealer
        :return: None
        """
        for player_state in dealer.player_states:
            player_state.apply_scavenger(dealer)


    def verify_self(self, player_states, own_player_state):

        is_hungry_carn = lambda s: s.is_carnivore() and s.is_hungry()

        if not own_player_state.verify_species(self.your_carnivore_index, is_hungry_carn):
            return False

        if not self.target_player_index in range(len(player_states)):
            return False

        target_player = player_states[self.target_player_index]
        left_neighbor, right_neighbor = target_player.get_neighbors(self.target_species_index)
        attacker_species = own_player_state.species_list[self.your_carnivore_index]
        is_species_attackable = lambda s: s.is_attackable(attacker_species, left_neighbor, right_neighbor)

        return target_player.verify_species(self.target_species_index, is_species_attackable)


    def rotate_right(self, n, players_len):
        return PlayerAttackWithCarnivore(self.your_carnivore_index,
                                         (self.target_player_index + n) % players_len,
                                         self.target_species_index)

