from evo_json.constants import ID_STR, CARDS_STR
from evo_json.convert_py_json.convert_player_fields import *
from evo_json.convert_py_json.convert_species import convert_from_pj_los, \
    convert_to_pj_los, convert_from_pj_loc
from evolution.data_defs import *
from evolution.player.iplayer import IPlayer
from evolution.player.player import Player
from evolution.player.player_state import PlayerState
__author__ = 'Edwin Cowart, Kevin McDonough'

def is_pj_player(value):
    """ Is the given value a PJ_Player?
    :param value: The value being checked
    :type value: Any
    :return: True if the given value is a PJ_Player, False otherwise
    :rtype: Boolean
    """
    return is_list_with_len(value, 3)


def convert_from_pj_player(pj_player):
    """ Convert the given PJ_Player to a PlayerState
    :param player_state: The player state in PyJSON
    :type player_state: PJ_Player
    :return: The PlayerState
    :rtype: IPlayer
    """
    if not is_pj_player(pj_player):
        raise ValueError("convert_from_pj_player: Invalid PyJSON Player")

    return IPlayer(Player(),
                       convert_from_id(pj_player[0]),
                       convert_from_pj_player_species(pj_player[1]),
                       convert_from_bag(pj_player[2]))


def convert_to_pj_player(player_state):
    """ Convert the given PlayerState to a PJ_Player
    :param player_state: The PlayerState
    :type player_state: IPlayer
    :return: The equivalent player in PyJSON
    :rtype: PJ_Player
    """
    if not isinstance(player_state, IPlayer):
        raise ValueError("convert_to_pj_player: Invalid PlayerState")

    return [convert_to_pj_id(player_state.get_id()),
            convert_to_pj_player_species(player_state.get_all_species()),
            convert_to_pj_bag(player_state.get_food_bag())]


def is_pj_player_plus(value):
    """
    :param value: The value to be checked
    :type value: Any
    :return: whether or not the value is a PJ Player+
    :rtype: bool
    """
    return isinstance(value, list) and len(value) == 4 or len(value) == 3


def convert_from_pj_player_plus(py_json):
    """
    Converts the given PyJSON Player+ to an Iplayer
    :param py_json: The PyJSON to be converted
    :type py_json: PyJSON
    :return: the equivalent Iplayer
    :rtype: IPlayer
    """
    if is_pj_player(py_json):
        return convert_from_pj_player(py_json)

    base_player = convert_from_pj_player(py_json[:3])
    [field_name, json_hand] = py_json[3]
    if field_name == CARDS_STR:
        base_player.hand = convert_from_pj_loc(json_hand)
    return base_player


'''----------- PyJSON LOP <-> List[PlayerState] -----------'''

'''
PJ_LOP = List[PJ_Player]
'''


def is_pj_lop(value):
    """ Is the given value a PJ_LOP
    :param value: The value being checked
    :type value: Any
    :return: True if the value is a PJ_LOP, False otherwise
    :rtype: Boolean
    """
    return isinstance(value, list)


def convert_from_pj_lop(pj_lop):
    """ Convert the given PJ_LOP to a List[PlayerState]
    :param pj_lop: The PJ_LOP
    :type pj_lop: PJ_LOP
    :return: The equivalent list of player states
    :rtype: [PlayerState, ...]
    """
    if not is_pj_lop(pj_lop):
        raise ValueError("convert_from_pj_lop: Invalid PyJSON LOP")

    return [convert_from_pj_player(pj_player) for pj_player in pj_lop]


def convert_to_pj_lop(player_states):
    """
    Convert the given list of player states to a PJ_LOP
    :param player_states: The list of player states to be converted
    :type player_states: [PlayerState, ...]
    :return: The quivalent list of players in PyJSON
    :rtype: PJ_LOP
    """
    if not isinstance(client_player_list, list):
        raise ValueError("convert_species_plus_list: Invalid PyJSON LOS")

    return [convert_to_pj_player(player_state) for player_state in
            player_states]


def convert_from_pj_lop_plus(py_json):
    """
    Convert the given list of Player+ to a list of IPlayers
    :param py_json: The list of Player+
    :type py_json: [Player+, ...]
    :rtype: IPlayer
    """
    if not isinstance(py_json, list):
        raise ValueError()

    return [convert_from_pj_player_plus(player) for player in py_json]


def convert_to_pj_player_plus(player_state):
    """
    Converts the given PlayerState to a PyJSON Player+
    :param player_state: The PlayerState to be converted
    :type player_state: IPlayer
    :return: Player+
    :rtype: PyJSON
    """
    base_player = convert_to_pj_player(player_state)
    if player_state.hand != []:
        base_player.append([CARDS_STR, convert_to_pj_loc(player_state.hand)])
    return base_player


def convert_to_pj_lop_plus(lops):
    """
    Converts the list of PlayerStates to an LOP+
    :param lops: The PlayerStates to be converted
    :type lops: [PlayerState, ...]
    :return: The LOP+
    :rtype: PyJSON
    """
    return [convert_to_pj_player_plus(ps) for ps in lops]


def convert_to_pj_player_start(player_state, wh):
    """
    Converts the given playerState to PyJSON
    for the start message
    :type player_state: IPlayer
    :type wh: Nat
    :rtype: PyJson
    """
    return [wh,
            player_state.food_bag,
            convert_to_pj_los(player_state.species_list),
            convert_to_pj_loc(player_state.hand)]


def convert_from_pj_player_start(py_json):
    """
    Conver the given PyJSON into a PlayerState
    :param py_json: PyJSON to convert
    :return: equivalent PlayerState
    :rtype: (IPlayer, wh)
    """
    if not(isinstance(py_json, list) and len(py_json) == 4):
        raise ConvertPyJSONError("Cannot convert Action4")
    [wh, pj_food, pj_species, pj_hand] = py_json
    species_list = convert_from_pj_los(pj_species)
    hand = convert_from_pj_loc(pj_hand)
    return PlayerState(1, species_list, pj_food, hand), wh


########################################################


def convert_lop_to_lob(player_states):
    """
    Converts the given list of PlayerStates to a PyJSON List of Boards
    :param player_states: the player states to be converted
    :type player_states: [PlayerState, ...]
    :return: The eqivalent LOB
    :rtype: PyJSON
    """
    return [convert_to_pj_los(ps.species_list) for ps in player_states]


def convert_lob_to_lop(lob):
    """
    Converts the given list of Boards to a list of Players
    :param lob: The list of boards
    :type lob: [Boards, ...]
    :return: the equivalent list of player states
    :rtype: [PlayerState, ...]
    """
    species_lists = [convert_from_pj_los(boards) for boards in lob]
    return [PlayerState(1, sl) for sl in species_lists]


