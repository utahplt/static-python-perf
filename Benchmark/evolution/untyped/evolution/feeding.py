from evolution.data_defs import *
from evolution.species_types import *
from evolution.player.iplayer import IPlayer
from evolution.player.player import Player
from evolution.player.player_feeding_choice import *

__author__ = 'Edwin Cowart, Kevin McDonough'


class Feeding:
    """
    Represents a Feeding where a Player must choose one of its Species to feed
    """
    def __init__(self, player_state, watering_hole, other_player_states):
        """
        Construct a Feeding
        :param player_state: The state of the player choosing the evolution
        :type player_state: IPlayer
        :param watering_hole: The number of food tokens in the watering hole
        :type watering_hole: int
        :param other_player_states:
        :type other_player_states: [Player, ...]
        :return: None
        """
        if not isinstance(player_state, IPlayer):
            raise ValueError("Feeding - constructor: Invalid PlayerState as player_state")
        elif not is_natural_plus(watering_hole):
            raise ValueError("Feeding - constructor: Invalid NaturalPlus as watering_hole")
        elif not is_list_of(other_player_states, IPlayer):
            raise ValueError("Feeding - constructor: Invalid List[PlayerState] as other_player_states")

        self.player_state = player_state                # type: PlayerState
        self.player = Player()                          # type: Player
        self.watering_hole = watering_hole              # type: NaturalPlus
        self.other_player_states = other_player_states  # type: List[PlayerState]


    def player_choose_feeding(self):
        """
         Tell the player to choice their feeder
        :return: The Feeding Choice of the Player
        :rtype: PlayerFeedingChoice or None
        """
        return self.player.choose_feeding(self.watering_hole,
                                          self.other_player_states,
                                          self.player_state)

