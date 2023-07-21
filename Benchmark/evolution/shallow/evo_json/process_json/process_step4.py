from evo_json.convert_py_json.convert_step4 import convert_step4
from evo_json.process_json.process_configuration import *
from collections import deque


def process_step4(py_json):
    """
    Converts py_json to Dealer then calls
    step4 on it
    :param py_json: list of configuration and step4
    :type py_json: PYJSON
    :return: PYJSON
    """
    dealer = convert_config_to_dealer(py_json[0])
    to_be_fed = deque(range(len(dealer.player_states)))
    [food_cards, lolocp] = convert_step4(py_json[1])
    dealer.step4(food_cards, lolocp, to_be_fed)
    return convert_dealer_to_config(dealer)



