from evolution.player.player import Player
from evo_json.convert_py_json.convert_choice import convert_choice_from_pj, \
    convert_to_action4


def process_choice(py_json):
    """
    Process the silly-player choice made for the PyJSON choice
    :param py_json: PyJSON Choice to be processed
    :type py_json: PyJSON
    :return: The PyJSON Action4 response
    :rtype: PyJSON
    """
    (ps, before_ps, after_ps) = convert_choice_from_pj(py_json)
    silly_player = Player()
    #harness for silly player, which did not include wateringhole
    silly_player.start(ps, 0)
    choices = silly_player.get_card_choices(before_ps, after_ps)
    return convert_to_action4(choices)
