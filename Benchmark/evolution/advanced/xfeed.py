import sys
import json
from evo_json.convert_py_json.convert_feeding import *
from evolution.feeding import *

__author__ = 'Edwin Cowart, Kevin McDonough'


def main():
    process_json_feeding_7(sys.stdin, sys.stdout)

def process_json_feeding_7(file_in, file_out):
    """
    Process the evolution according to HW-7 Specs """
    py_json_in = json.load(file_in)
    try:
        feeding = convert_from_pj_feeding(py_json_in)
    except ValueError as e:
        # Error converting the PyJSON to a evolution; ill formed
        raise e

    player_feeding_choice = feeding.player_choose_feeding()

    if player_feeding_choice is not None:
        py_json_out = convert_player_feeding_choice_to_pj(player_feeding_choice)
        json.dump(py_json_out, file_out)

if __name__ == "__main__":
    main()
