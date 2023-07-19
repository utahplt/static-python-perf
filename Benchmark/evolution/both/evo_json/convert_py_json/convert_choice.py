from cardplay import *
from evo_json.convert_py_json.convert_player import convert_from_pj_player_plus
from evo_json.convert_py_json.convert_species import convert_from_pj_los
from evolution.player.player import Player
from evolution.player.iplayer import IPlayer
from evolution.player.player_state import PlayerState

def convert_choice_from_pj(py_json):
    """
    Convert the PyJSON choice to a PlayerState, and lists of before and after
    PlayerStates
    :param py_json: PyJSON Choice to be converted
    :type py_json: PyJSON
    :return: (player_state, before_player_states, after_player_states)
    :rtype: (PlayerState, [PlayerState, ...], [PlayerState, ...])
    """
    (pj_player, before_lolos, after_lolos) = py_json
    player_state = convert_from_pj_player_plus(pj_player)
    before_species_lists = [convert_from_pj_los(los) for los in before_lolos]
    after_species_lists = [convert_from_pj_los(los) for los in after_lolos]
    before_player_states = [PlayerState(1, s_list)
                            for s_list in before_species_lists]
    after_player_states = [PlayerState(1, s_list)
                           for s_list in after_species_lists]
    return player_state, before_player_states, after_player_states


def convert_to_action4(choices):
    """
    Converts the tuple of a food card choice and a list of card plays to a
    PyJSON Action4
    :param choices: (food_card_index, locp) where locp is the list of CardPlays
    :type choices: (Nat, [CardPlay, ...]
    :return: The equivalent Action4
    :rtype: PyJSON Action4
    """
    (food_card_index, locp) = choices
    logp = convert_locp(locp, cp_to_gp)
    logb = convert_locp(locp, cp_to_gb)
    lobt = convert_locp(locp, cp_to_bt)
    lort = convert_locp(locp, cp_to_rt)
    return [food_card_index, logp, logb, lobt, lort]


def convert_to_new_action4(choices):
    """
    Converts the tuple of a food card choice and a list of card plays to a
    PyJSON Action4
    :param choices: (food_card_index, locp) where locp is the list of CardPlays
    :type choices: (Nat, [CardPlay, ...]
    :return: The equivalent Action4
    :rtype: PyJSON Action4
    """
    (food_card_index, locp) = choices
    logp = convert_locp(locp, cp_to_new_gp)
    logb = convert_locp(locp, cp_to_new_gb)
    lobt = convert_locp(locp, cp_to_bt)
    lort = convert_locp(locp, cp_to_rt)
    return [food_card_index, logp, logb, lobt, lort]

def convert_locp(locp, converter):
    """
    Convert the given list of card plays using the converter
    :param locp: CardPlays to convert
    :type locp: [CardPlay, ...]
    :param converter: method to convert a CardPlay
    :type converter: CardPlay -> PyJSON or None
    :return: the list of PyJSON
    :rtype: [PyJSON, ...]
    """
    result = []
    for cp in locp:
        converted = converter(cp)
        if converted is not None:
            result.append(converted)
    return result

def cp_to_gp(cp):
    """
    Converts the given CardPlay to a GP if it is a ExchangeForPopulation, else
    returns None
    :param cp: CardPlay to be converted
    :type cp: CardPlay
    :return: GP or None
    """
    if isinstance(cp, ExchangeForPopulation):
        return ["population", cp.species_index, cp.played_card_index]
    else:
        return None

def cp_to_new_gp(cp):
    """
    Converts the given CardPlay to a GP if it is a ExchangeForPopulation, else
    returns None
    :param cp: CardPlay to be converted
    :type cp: CardPlay
    :return: GP or None
    """
    if isinstance(cp, ExchangeForPopulation):
        return [cp.species_index, cp.played_card_index]
    else:
        return None

def cp_to_gb(cp):
    """
    Converts the given CardPlay to a GB if it is a ExchangeForBodySize, else
    returns None
    :param cp: CardPlay to be converted
    :type cp: CardPlay
    :return: GB or None
    """
    if isinstance(cp, ExchangeForBodySize):
        return ["body", cp.species_index, cp.played_card_index]
    else:
        return None

def cp_to_new_gb(cp):
    """
    Converts the given CardPlay to a GB if it is a ExchangeForBodySize, else
    returns None
    :param cp: CardPlay to be converted
    :type cp: CardPlay
    :return: GB or None
    """
    if isinstance(cp, ExchangeForBodySize):
        return [cp.species_index, cp.played_card_index]
    else:
        return None

def cp_to_bt(cp):
    """
    Converts the given CardPlay to a BT if it is a ExchangeForSpecies, else
    returns None
    :param cp: CardPlay to be converted
    :type cp: CardPlay
    :return: BT or None
    """
    if isinstance(cp, ExchangeForSpecies):
        return [cp.played_card_index] + cp.loi
    else:
        return None

def cp_to_rt(cp):
    """
    Converts the given CardPlay to a RT if it is a ReplaceCards, else
    returns None
    :param cp: CardPlay to be converted
    :type cp: CardPlay
    :return: RT or None
    """
    if isinstance(cp, ReplaceCards):
        return [cp.species_index, cp.replaced_card_index, cp.played_card_index]
    else:
        return None