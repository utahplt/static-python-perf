from evo_json.convert_py_json.convert_player import *
from evo_json.data_def import ConvertPyJSONError


def convert_to_pj_state(watering_hole, other_players, own_player):
    """
    Converts the given information into a PyJSON State
    :param watering_hole: tokens on the watering hole
    :type watering_hole: Nat
    :param other_players: other player states
    :type other_players: [PlayerState, ...]
    :param own_player: The current player
    :type own_player: PlayerState
    :return: the equivalent PyJSON State
    :rtype: PyJSON
    """
    return [own_player.food_bag,
            convert_to_pj_los(own_player.species_list),
            convert_to_pj_loc(own_player.hand),
            watering_hole,
            convert_lop_to_lob(other_players)]


def convert_from_pj_state(pj_state):
    """
    Converts the given PyJSON State to the player state, watering hole
    and other player states
    :param pj_state: The PyJSON State
    :type pj_state: PyJSON State
    :return: (watering_hole, other_players, own_player)
    :rtype: (Nat, [PlayerState, ...], PlayerState)
    """
    if not(isinstance(pj_state, list) and len(pj_state) == 5):
        raise ConvertPyJSONError("Cannot convert Action4")

    [pj_food, pj_species, pj_hand, wh, other_lob] = pj_state

    species_list = convert_from_pj_los(pj_species)
    hand = convert_from_pj_loc(pj_hand)

    own_player_state = PlayerState(1, species_list, pj_food, hand)
    other_player_states = convert_lob_to_lop(other_lob)

    return wh, other_player_states, own_player_state
