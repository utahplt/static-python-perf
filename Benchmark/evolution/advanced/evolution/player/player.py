from collections import namedtuple
from evolution.data_defs import is_list_of, is_natural
from evolution.player.player_state import PlayerState
from evolution.player.player_feeding_choice import PlayerAttackWithCarnivore
from evolution.player.player_feeding_choice import PlayerStoreFat
from evolution.player.player_feeding_choice import PlayerForgoAttack
from evolution.player.player_feeding_choice import PlayerFeedVegetarian
from evolution.player.species_keys import SpeciesPickKey, SpeciesFeedType, \
    SpeciesOrderKey

from exchange_for_population import ExchangeForPopulation
from exchange_for_species import ExchangeForSpecies


class Player:
    def __init__(self):
        """
        :return: None
        """
        self.player_state = None

    def start(self, player_state, wh):
        """
        updates the player state
        :type: player_state: PlayerState
        :param wh: watering hole
        :type wh: Nat
        :return: None
        """
        self.player_state = player_state

    def get_card_choices(self, c, d):
        """
        Gets the card choices from the players
        :param c: the states of the players before this player
        :type c: [PlayerState, ...]
        :param d: the states of the players after this player
        :type d: [PlayerState, ...]
        :return: A tuple containing Rest choices
        :rtype: (Nat, [CardPlay, ...])
        """
        s_hand = self.player_state.sorted_hand()
        food_card_index = self.get_hand_index(s_hand.pop(0))
        card_plays = []
        card_plays.append(
            ExchangeForSpecies(self.get_hand_index(s_hand.pop(0)),
                               [self.get_hand_index(s_hand.pop(0))]))
        if s_hand:
            card_plays.append(
                ExchangeForPopulation(self.get_hand_index(s_hand.pop(0)),
                                      len(self.player_state.species_list)))

        return food_card_index, card_plays

    def get_hand_index(self, card):
        """
        Get the index of the given card in this player's hand
        :param card: the card
        :type card: TraitCard
        :return: Nat
        """
        return self.player_state.hand.index(card)

    def choose_feeding(self, watering_hole, other_players, own_player):
        """
        Choose the next species for this player to feed. Must have at least 2 choices for feedings.
        :param watering_hole: the number of tokens at the watering hole
        :type watering_hole: Nat+
        :param players: the states of all players in the game (not including this player)
        :type players: [PlayerState, ...]
        :param own_player: This player's state
        :type own_player: PlayerState
        :return: The player's evolution choice
        :rtype: PlayerFeedingChoice or None
        """

        all_players_states = other_players + [own_player]
        own_index = len(other_players)
        own_species = own_player.get_all_species()

        best_species_key = max(
            SpeciesPickKey(species, own_index, all_players_states) for species
            in own_species)
        best_species = best_species_key.species
        best_species_index = own_species.index(best_species)
        best_species_feed_type = best_species_key.feed_type

        if best_species_feed_type is SpeciesFeedType.STORE_FAT:
            return PlayerStoreFat(best_species_index,
                                  min(best_species.fat_tissue_need(),
                                      watering_hole))
        if best_species_feed_type is SpeciesFeedType.FEEDABLE_VEG:
            return PlayerFeedVegetarian(best_species_index)
        if best_species_feed_type is SpeciesFeedType.FEEDABLE_CARN:
            return self.choose_target(best_species_index, all_players_states,
                                      own_index)
        if best_species_feed_type is SpeciesFeedType.FORGO_ATTACK:
            return PlayerForgoAttack()
        else:
            return None

    def choose_target(self, carn_index, players, own_index):
        """
        Choose the target of this Player's Carnivore at the given index in this Player's species boards
        :param carn_index: The index of the attacking Carnivore in this Player's species boards
        :type carn_index: Nat
        :param players: the other players in the game
        :type players: [PlayerState, ...]
        :param own_index: This players index in the given array of player states
        :type own_index: Nat
        :return: The attack that the aforementioned Carnivore will execute
        :rtype: PlayerAttackWithCarnivore
        """
        carn_species = players[own_index].get_all_species()[carn_index]
        BestInfo = namedtuple('BestInfo', ['key', 'p_index', 's_index'])
        best = None  # type: None or BestInfo

        for player_index, player in enumerate(players):
            if player_index == own_index:
                continue
            player_species = player.get_all_species()
            player_best_species_index, player_best_speices_key = \
                carn_species.best_attack_on_player(player_species,
                                                   SpeciesOrderKey)
            if (player_best_speices_key is not None) and \
                    ((best is None) or (player_best_speices_key > best.key)):
                best = BestInfo(player_best_speices_key, player_index,
                                player_best_species_index)
        if best is None:
            raise ValueError(
                "choose_target: Given carnivore had no valid target among players.")

        return PlayerAttackWithCarnivore(carn_index, best.p_index, best.s_index)


    def get_player_info(self):
        """
        Gets the player info
        :return: String
        """
        return "player info"

    @staticmethod
    def index_2d(players, species):
        for i, player in enumerate(players):
            if species in player.species_list:
                return (i, player.species_list.index(species))

    def __eq__(self, other):
        return isinstance(other, Player)


