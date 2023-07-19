import sys
import json
from evo_json.process_json.process_configuration import process_configuration


def run(file_in, file_out):
    """
    Run on the given input and output files
    :param file_in: input file-like object
    :param file_out: output file-like object
    :return: None
    """
    py_json_in = json.load(file_in)
    py_json_out = process_configuration(py_json_in)
    json.dump(py_json_out, file_out)


def main():
    run(sys.stdin, sys.stdout)


if __name__ == "__main__":
    main()