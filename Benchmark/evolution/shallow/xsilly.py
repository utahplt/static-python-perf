import sys
import json
from evo_json.process_json.process_choice import process_choice


def main():
    run(sys.stdin, sys.stdout)


def run(file_in, file_out):
    py_json_in = json.load(file_in)
    py_json_out = process_choice(py_json_in)
    json.dump(py_json_out, file_out)


if __name__ == "__main__":
    main()