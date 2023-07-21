import sys
import json
from evo_json.process_json.process_step4 import process_step4


def main():
    run(sys.stdin, sys.stdout)


def run(in_file, out_file):
    in_pyjson = json.load(in_file)
    out_pyjson = process_step4(in_pyjson)
    json.dump(out_pyjson, out_file)


if __name__ == "__main__":
    main()