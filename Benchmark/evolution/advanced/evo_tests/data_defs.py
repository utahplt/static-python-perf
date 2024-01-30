import os
import sys
from evo_tests.constants import TEST_CASES_DIR

__author__ = 'Edwin Cowart, Kevin McDonough'


evo_tests_path = os.path.dirname(os.path.realpath(__file__))

project_path = evo_tests_path + os.sep + os.pardir
sys.path.insert(0, project_path)

TEST_CASES_PATH = evo_tests_path + os.sep + TEST_CASES_DIR


def to_module_path(path: str, proj_path: str=project_path) -> str:
    """ Convert the given file-system path to a python module path
    :param path: The full file or directory path of the path which is being converted to a module path
    :param proj_path: The project path that contains the file
    :return: The module path
    """
    rel_path = os.path.relpath(path, proj_path)
    module_path = rel_path.split(".")[0]  # Removes .py
    module_path = module_path.replace(os.sep, ".")
    return module_path


def make_dir(parent_path: str, dir_name: str) -> str:
    """ Make the a directory at the given parent directory's path
    :param parent_path: The parent directory
    :param dir_name: The name of the directory
    :return: The full path of the directory
    """
    dir_path = parent_path + os.sep + dir_name
    try:
        os.stat(dir_path)
        print("\nDir Exists: " + dir_path)
    except FileNotFoundError:
        os.mkdir(dir_path)
        print("\nMake Dir: " + dir_path)

    return dir_path


def make_file(dir_path: str, file_name: str, write_data: str) -> str:
    """ Make a new file with the given name at the given directory location and write the given data to it
    :param dir_path: The directory path
    :param file_name: The file name
    :param write_data: The data being writen
    :return: The full path of the file
    """
    file_path = dir_path + os.sep + file_name

    print("Making File : " + file_name + " : With Data:")
    out_file = open(file_path, "w+")

    write_data = remove_white_space(write_data)
    print(write_data + "\n")
    out_file.write(write_data)

    return file_path


def remove_white_space(string):
    """ Removes white space from the given string
    :param string: The string in question
    :return: The resulting string without whitespace
    """
    string = string.replace('\\n', ' ')
    string = string.replace('\\t', ' ')
    return "".join(string.split())
