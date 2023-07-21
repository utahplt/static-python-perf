from evolution.species import Species
from evolution.constants import PLAYER_STARTING_FOOD_TOKENS
from dealer.constants import BASE_DEAL_NUMBER
from evolution.data_defs import is_natural_plus, is_list_of, is_natural
from evolution.trait_cards import TraitCard
from evolution.timeout import timeout
from evolution.player.player_state import PlayerState

class IPlayer(PlayerState):
    """
    To represent the internal state of the player
    """
    def __init__(self, player, id, species_list=None,
                 food_bag=PLAYER_STARTING_FOOD_TOKENS, hand=None):
        super().__init__(id, species_list, food_bag, hand)
        self.player = player

    def update_player(self, wh):
        """
        Updates the player with this player state and the given watering hole
        :param wh: wateringhole
        :type wh: Nat
        :return: None
        """
        self.player.start(self, wh)


    def get_player_info(self):
        return self.player.get_player_info()

    @timeout()
    def choose_feeding(self, wateringhole, player_states):
        """
        Returns the feeding choice the player associated with
        this player state
        :type wateringhole: Nat
        :type player_states: [PlayerState, ...]
        :return: FeedingChoice
        """
        own_index = player_states.index(self)
        external_players = [p.make_external_player_state() for p in player_states]
        modified_external_p = external_players[own_index+1:] + external_players[:own_index]

        feeding_choice = self.player.choose_feeding(wateringhole, modified_external_p, self)
        return feeding_choice.rotate_right(own_index+1, len(player_states))

    def remove_cards_from_hand(self, locp, food_card_index):
        """
        Remove the cards used by the CardPlays and food
        :param locp: a sequence of lists of card plays where each list
        corresponds to the player states
        :type locp: [[CardPlay,...],...]
        :param food_card_index: index of the player's food card choices
        :type food_card_index: Nat
        :return: None
        """
        to_remove = [food_card_index]
        for cp in locp:
            to_remove += cp.get_card_indices()
        self.remove_cards_with_indices(to_remove)

    def remove_cards_with_indices(self, loi):
        """
        Remove the cards in this player's hand with the given indices
        :param loi: list of indices of cards to be removed
        :type loi: [Nat, ...]
        :return:
        """
        for i in sorted(loi, reverse=True):
            del self.hand[i]

    def apply_scavenger(self, dealer):
        """
        Apply the scavenger trait to all species in this player state
        :param wateringhole: the wateringhole
        :type wateringhole: Nat
        :return: the resulting wateringhole
        :rtype: Nat
        """
        player_index = dealer.player_states.index(self)
        for index, species in enumerate(self.species_list):
            species.apply_scanvenger(dealer, player_index, index)

    def apply_to_all_species(self, method, player_index):
        """
        Applies method to all Species in this PlayerState
        :param method: the method to be applied to each Species
        :type method: Species Nat Nat -> None
        :return: None
        """
        for species_index, species in enumerate(self.species_list):
            method(species, player_index, species_index)

    def reduce_population_all(self, dealer):
        """
        Reduces population of all species of this player
        :type dealer: Dealer
        :return: None
        """
        species_to_be_removed = []

        for species in self.species_list:
            species.population = species.num_food_tokens
            if species.is_extinct():
                species_to_be_removed.append(species)

        for species in species_to_be_removed:
            self.species_list.remove(species)
            self.hand += dealer.deck.get_n_cards(2)


    @timeout()
    def make_card_choices(self, player_states):
        """
        choose food card to put on the wateringhole, and
        card plays
        :param player_states: the player states
        :type player_states: [PlayerState...]
        :return: A tuple containing Rest choices
        :rtype: (Nat, [CardPlay, ...])
        """
        external_players = [p.make_external_player_state() for p in player_states]
        self_index = player_states.index(self)
        c = external_players[:self_index]
        d = external_players[self_index+1:]
        card_choices = self.player.get_card_choices(c, d)
        return card_choices

    def verify_card_choices(self, choices):
        """
        Verifies card choices
        :param choices: card choices
        :type choices: (Nat, [CardPlay, ...])
        :return: None
        :raise: ValueError
        """
        (food_card_index, card_plays) = choices
        self.verify_index(food_card_index, self.hand)
        for i,  card_play in enumerate(card_plays):
            if not card_play.verify_self(self, food_card_index, card_plays[:i]):
                return False
        return True


    def verify_index(self, index, a_list):
        """
        Verifies that index is valid in a_list
        :param index: The food card index
        :type a_list [x, ...]
        :return: Boolean
        """
        return 0 <= index < len(a_list)

    def verify_species(self, species_index, predicate):
        """
        Verify that there's a species with species_index and that it
         satisfies the predicate
        :type species_index: Nat
        :type predicate: Species -> boolean
        :rtype: boolean
        """
        return self.verify_index(species_index, self.species_list) and \
               predicate(self.species_list[species_index])

    def hand_turn_pieces(self, list_of_cards, wh, species_board=None):
        """
        Hands the players the list of cards and an optional
        species board
        :type list_of_cards: [TraitCard, ...]
        :type species_board: [Species, ...]
        :param wh: wateringhole
        :type wh: Nat
        :return: None
        """
        self.hand += list_of_cards
        if species_board:
            self.species_list.append(species_board)
        self.update_player(wh)

    def make_external_player_state(self):
        return PlayerState(self.id, self.species_list)

    def get_score(self):
        """
        Get the score for this playerstate
        :return: the score
        :rtype: int
        """
        return self.food_bag + self.get_pop_score() + self.get_trait_score()

    def get_pop_score(self):
        """
        Gets the score of this player state from species population
        :return: score from species population
        :rtype: int
        """
        return sum(s.population for s in self.species_list)

    def get_trait_score(self):
        """
        Gets the score of this player from trait cards on species
        :return: the score
        :rtype: int
        """
        return sum(len(s.played_cards) for s in self.species_list)

    def validate_species_index(self, species_index, card_plays):
        """
        Validates that species_index will be valid in self.species_list
        after card_plays are applied
        :type species_index:
        :param card_plays: Cards played so far in the turn
        :type card_plays: [CardPlay, ...]
        :rtype: Boolean
        """
        species_count = sum(card_play.num_species_created() for card_play in card_plays) +\
                        len(self.species_list)

        return species_index in range(0, species_count)

    def validate_species_trait_index(self, species_index, trait_index, card_plays):
        """
        Validates the trait put on the species will be valid in self.species_list
        after card_plays are applied (if the species will exist in the player's hand)
        :type species_index: Nat
        :param card_plays: Cards played so far in the turn
        :type card_plays: [CardPlay, ...]
        :rtype: Boolean
        """
        species_trait_count = [len(species.played_cards) for species in self.species_list]

        for card_play in card_plays:
            species_trait_count = card_play.update_trait_counts(species_trait_count)

        return trait_index in range(species_trait_count[species_index])

    def validate_trait_cards_indicies(self, species_card_indices):
        """
        Ensures that the list of indicies of cards to add on the species
        is valid
        :param species_card_indices: The indies of cards to be added on the ew
        species
        :type species_card_indices: [Nat, ...]
        :rtype: boolean
        """
        species_card_types = [type(self.hand[i]) for i in species_card_indices]
        return len(species_card_types) == len(set(species_card_types))

