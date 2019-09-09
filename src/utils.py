import json
import os
from csv import DictWriter
from typing import List

from autohandshake import HandshakeSession


class BrowsingSession(HandshakeSession):
    """
    A wrapper class around HandshakeSession that always logs into the account
    specified in the config file.
    """

    def __init__(self, max_wait_time=300):
        config = load_config()
        super().__init__(config['handshake_url'], config['handshake_email'], max_wait_time=max_wait_time)


def load_config():
    """
    Load the configuration file
    :return: a dict of config values
    """
    config_file_path = f'{os.environ.get("USERPROFILE")}\\.handshake_administrator\\config.json'
    with open(config_file_path, 'r') as file:
        return json.load(file)


def to_csv(list_of_dicts: List[dict], file_path: str):
    """
    Write the given list of dicts to a csv at the given file path.

    The dictionaries should have a uniform structure, i.e. they should be parsable
    into the rows of the csv, with the keys equivalent to column names.

    :param list_of_dicts: the list to write to a file
    :type list_of_dicts: list
    :param file_path: the file path at which to create the file
    :type file_path: str
    """

    keys = list_of_dicts[0].keys()
    with open(file_path, 'w', encoding='utf-8') as output_file:
        dict_writer = DictWriter(output_file, keys, lineterminator='\n')
        dict_writer.writeheader()
        dict_writer.writerows(list_of_dicts)


def print_and_write_to_file(text: str, file_path):
    """Write the given string to a file at the given filepath"""
    print(text)
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text)
        print(f'Report successfully written to file at {file_path}')
    except FileNotFoundError as e:
        print(f'Unable to write results to file. {str(e)}')


def create_or_list_from(items: list) -> str:
    """
    Create a string like '"item1", "item2", or "item3"' from a list of items.
    """
    if len(items) == 0:
        return ''
    elif len(items) == 1:
        return f'"{items[0]}"'
    elif len(items) == 2:
        return f'"{items[0]}" and "{items[1]}"'
    else:
        return _create_or_statement_from(items)


def _create_or_statement_from(items):
    result = '"'
    result += '", "'.join(items[:-1])
    result += f'", or "{items[-1]}"'
    return result
