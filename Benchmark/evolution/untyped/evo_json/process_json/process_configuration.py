from collections import deque
from dealer.dealer import Dealer
from dealer.deck import Deck
from evolution.player.player import Player
from evo_json.convert_py_json.convert_player import convert_from_pj_lop_plus, \
    convert_to_pj_lop_plus
from evo_json.convert_py_json.convert_trait import convert_from_pj_loc, \
    convert_to_pj_loc


def process_configuration(pyjson_config):
    """
    Processes a PyJSON Configuration by calling feed1 once
    :param pyjson_config: the Configuration to be updated
    :type pyjson_config: PyJSON
    :return: the updated Configuration
    :rtype: PyJSON
    """
    dealer = convert_config_to_dealer(pyjson_config)
    dealer.feed1(deque(range(len(dealer.player_states))))
    return convert_dealer_to_config(dealer)


def convert_config_to_dealer(pyjson_config):
    """
    Converts a PyJSON configuration to a Dealer
    :param pyjson_config: the Configuration
    :type pyjson_config: PyJSON
    :return: the dealer from the given configuration
    :rtype: Dealer
    """
    player_states = convert_from_pj_lop_plus(pyjson_config[0])
    deck = Deck(convert_from_pj_loc(pyjson_config[2]))
    wateringhole = pyjson_config[1]
    return Dealer.make_dealer(player_states, deck, wateringhole)


def convert_dealer_to_config(dealer):
    """
    Converts a Dealer to a PyJSON Configuration
    :param dealer: the dealer to be converted
    :type dealer: Dealer
    :return: The Configuration of the Dealer
    :rtype: PyJSON
    """
    lop = convert_to_pj_lop_plus(dealer.player_states)
    wateringhole = dealer.wateringhole
    loc = convert_to_pj_loc(dealer.deck.loc)
    return [lop, wateringhole, loc]
