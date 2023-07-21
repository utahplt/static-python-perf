from dealer.constants import WATERINGHOLE_START, BASE_DEAL_NUMBER
from collections import deque
from evolution.species import Species
from evolution.player.player_feeding_choice import PlayerForgoAttack
from executefeed1 import NoChoice, MultipleChoices, OneChoice
from evolution.trait_cards import FertileCard
from evolution.player.iplayer import IPlayer
from evolution.player.player import Player
from dealer.deck import Deck
from evolution.timeout import TimeoutError
from evo_json.data_def import ConvertPyJSONError


class Dealer:
    """
    To represent the dealer of the game
    """

    def __init__(self, players, deck, wateringhole=WATERINGHOLE_START):
        """
        :param players: The players in the game
        :type players: [Player, ...]
        :param deck: Cards that are currently with the dealer
        :type deck: Deck
        :param wateringhole: The number of food tokens on the watering hole
        :type wateringhole: Nat
        :return: None
        """

        self.player_states = self.create_player_states(players)
        self.deck = deck
        self.wateringhole = wateringhole

    def run_game(self):
        """
        Runs a complete simulation of Evolution game
        :return: None
        """
        while self.has_enough_cards():
            self.run_turn()

    def has_enough_cards(self):
        """
        Determines if the dealer has enough cards
        :return: True if dealer has enough cards
        and false otherwise
        """
        available_cards = len(self.deck)
        needed_cards = 0

        for player in self.player_states:
            needed_cards += player.get_needed_cards()

        return needed_cards <= available_cards


    def run_turn(self):
        """
        Run the simulation of evolution
        :return: None
        """
        self.start_turn()
        [food_card_indices, lolocp] = self.get_all_card_choices()
        self.step4(food_card_indices, lolocp, deque(range(len(self.player_states))))
        self.finalize_turn()
        self.rotate_players()


    def start_turn(self):
        """
        Distributes the species boards and the cards
        over the players
        :return: None
        """
        for player_state in self.player_states:
            species_board = None
            loc = self.deck.get_n_cards(player_state.get_needed_cards())
            if not player_state.species_list:
                species_board = Species()
            player_state.hand_turn_pieces(loc, self.wateringhole, species_board)

    def get_all_card_choices(self):
        """
        Gets card choices for all player states
        :return: list of tuples containing Rest choices
        :rtype: ([Nat, ...], [[CardPlay, ...], ...])
        """
        food_card_choices = []
        card_plays = []
        for player_state in self.player_states:
            try:
                (f_c_i, c_p) = player_state.make_card_choices(self.player_states)
            except (TimeoutError, ConvertPyJSONError):
                self.kick_player(player_state)
            else:
                if not player_state.verify_card_choices((f_c_i, c_p)):
                    self.kick_player(player_state)

                else:
                    food_card_choices.append(f_c_i)
                    card_plays.append(c_p)

        return food_card_choices, card_plays

    def finalize_turn(self):
        """
        Does the clean up after a given turn
        :return: None
        """
        self.reduce_population_all()
        self.add_to_food_bag()

    def rotate_players(self):
        """
        Rotates players after the end of the turn
        :return: None
        """
        self.player_states.append(self.player_states.pop(0))

    def add_to_food_bag(self):
        """
        Adds food tokens from all species to owning players' food bag
        :return: None
        """
        self.apply_to_all_species(lambda species, p_i, s_i: self.add_food_one_species(species, p_i, s_i))

    def add_food_one_species(self, species, player_index, species_index):
        """
        Adds the food tokens from one species to owning player's food bag
        and resets the number of food tokens on that species
        :param species: the species
        :type species: Species
        :param player_index: the owning player's index
        :type player_index: Nat
        :param species_index: the species index
        :type species_index: Nat
        :return: None
        """
        player_state = self.player_states[player_index]
        player_state.food_bag += species.num_food_tokens
        species.num_food_tokens = 0


    def reduce_population(self, species_index, amount_to_reduce, player_index):
        """
        Reduces population of the species and makes the nessesairy changes as a
        result of this reduction
        :param species: The species to reduce population
        :type species: Species
        :param amount_to_reduce: amount to reduce the population
        :type amount_to_reduce: Int
        :param player_state: The state of the player who owns the species
        :type player_state: IPlayer
        :return: None
        """
        player_state = self.player_states[player_index]
        species = player_state.species_list[species_index]
        species.adjust_population(-amount_to_reduce)
        if species.is_extinct():
            player_state.species_list.pop(species_index)
            player_state.hand += self.deck.get_n_cards(2)


    def reduce_population_all(self):
        """
        Reduces the population with the nessesairy amount for all species
        :return: None
        """
        for player in self.player_states:
            player.reduce_population_all(self)

    def step4(self, food_card_indices, lolocp, to_be_fed):
        """
        Performs the 4th step of the turn
        :param food_card_indices: the the indices of the cards being played on
        the wateringhole
        :type food_card_indices: [Nat, ...]
        :param lolocp: a sequence of lists of card plays where each list
        corresponds to the player states
        :type lolocp: [[CardPlay,...],...]
        :param to_be_fed indices of the players to be fed
        :type to_be_fed: deque[Nat, ....]
        :return:
        """
        self.apply_food_cards(food_card_indices)
        self.apply_card_plays(lolocp)
        self.remove_cards(lolocp, food_card_indices)
        self.before_feeding_cycle()
        self.execute_feed_cycle(to_be_fed)

    def feed1(self, can_feed_deque):
        """
        Feed the first Player on the deque, and put them at the end if they can still feed
        Assume:
          wateringhole > 0
          len(can_feed_deque) > 0
        :param can_feed_deque: the Players who can still feed, in the order of their turns
        :type can_feed_deque: deque([Player, ...])
        :return: None
        """
        index = can_feed_deque.popleft()
        res = self.determine_choices(index)
        res.execute_feed1(can_feed_deque, self, index)


    def determine_choices(self, index):
        """
        Determines the number of choices for the player
        with the given index
        :return: Feed1Result
        """
        player_state = self.player_states[index]
        found_choices = []
        for i, species in enumerate(player_state.species_list):
            found_choices += species.get_choices_only_species(self, i)
            if len(found_choices) > 1:
                return MultipleChoices()
        if found_choices:
            return OneChoice(found_choices[0])
        else:
            return NoChoice()



    def apply_to_all_species(self, method):
        """
        Applies method to all species in all player_state
        :param method: the method to be applied to each Species
        :type method: Species, Nat, Nat -> None
        :return: None
        """
        for player_index, player_state in enumerate(self.player_states):
            player_state.apply_to_all_species(method, player_index)

    def execute_feed_cycle(self, to_be_fed):
        """
        Feeds players until wateringhole is empty or no
        more species can be fed.
        :param to_be_fed indicies of the players to be fed
        :type to_be_fed: deque[Nat, ....]
        :return: None
        """
        while self.wateringhole > 0 and len(to_be_fed) != 0:
            self.feed1(to_be_fed)

    def apply_card_plays(self, lolocp):
        """
        Apply the card plays for each PlayerState in this Dealer
        :param lolocp: a sequence of lists of card plays where each list
        corresponds to the player states
        :type lolocp: [[CardPlay,...],...]
        :return: None
        """
        for player_state, locp in zip(self.player_states, lolocp):
            for cp in locp:
                cp.apply(player_state)

    def apply_food_cards(self, food_card_indices):
        """
        Apply the given food cards to the watering hole
        :param food_card_indices: indices of the food cards to be
        added/subtracted from the watering hole
        :type food_card_indices: [Nat, ...]
        :return: None
        """
        for i, food_card_index in enumerate(food_card_indices):
            food_card = self.player_states[i].hand[food_card_index]
            self.wateringhole += food_card.get_num_tokens_as_food_card()
            self.wateringhole = max(0, self.wateringhole)

    def remove_cards(self, lolocp, food_card_indices):
        """
        Remove the cards used by the CardPlays and food cards
        :param lolocp: a sequence of lists of card plays where each list
        corresponds to the player states
        :type lolocp: [[CardPlay,...],...]
        :param food_card_indices: indices of the players food card choices
        :type food_card_indices: [Nat, ...]
        :return: None
        """
        for ps, locp, food_card_index in \
            zip(self.player_states, lolocp, food_card_indices):
            ps.remove_cards_from_hand(locp, food_card_index)

    def before_feeding_cycle(self):
        """
        Updates species automatically before the evolution cycle
        :return:
        """
        self.apply_to_all_species(
            lambda species, pi, si: species.apply_before_feeding(self, pi, si))

    def create_player_states(self, players):
        """
        Create a list of player states
        :param players: list of players
        :type players: [Player, ...]
        :return: The player states
        :rtype: [PlayerState, ...]
        """
        return [IPlayer(player, i+1) for i, player in enumerate(players)]


    def get_sorted_scores(self):
        """
        gets the score of the game in order of high to low score
        :return: [(id, info, score), ...] where id is the players id and score is
        their score and the info is the player's info
        :rtype [(Nat, String, Nat), ...]
        """
        scores = []
        for player_state in self.player_states:
            scores.append((player_state.id,
                           player_state.get_player_info(),
                           player_state.get_score()))

        return sorted(scores, key=lambda s: s[2], reverse=True)

    def kick_player(self, player_to_kick):
        """
        Kicks the given player from the game
        :type player_to_kick: IPlayer
        :return: None
        """
        self.player_states.remove(player_to_kick)


    def __repr__(self):
        return "Dealer({}, {}, {})".format(repr(self.player_states),
                                           repr(self.deck),
                                           repr(self.wateringhole))

    def __eq__(self, other):
        if not isinstance(other, Dealer):
            return False
        else:
            return self.player_states == other.player_states \
                   and self.deck == other.deck \
                   and self.wateringhole == other.wateringhole

    @staticmethod
    def make_dealer(player_states, deck, wateringhole):
        """
        Creates a dealer with the given parameters
        :param player_states: the player states
        :type player_states: [PlayerState, ...]
        :param deck: the deck
        :type deck: Deck
        :param wateringhole: the watering hole
        :type wateringhole: Nat
        :return: Dealer
        """
        players = [Player() for p in range(len(player_states))]
        dealer =  Dealer(players, deck, wateringhole)
        dealer.player_states = player_states
        return dealer
