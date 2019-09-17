import json
import os
import subprocess
import sys
from csv import DictWriter
from datetime import datetime
from getpass import getuser
from typing import List

from autohandshake import HandshakeSession

CONFIG_DIR = f'{os.environ.get("USERPROFILE")}\\.handshake_administrator'
CONFIG_FILE_NAME = 'config.json'
CONFIG_FILEPATH = f'{CONFIG_DIR}\\{CONFIG_FILE_NAME}'


def _create_default_config():
    username = getuser()
    config = {
        "handshake_url": "https://jhu.joinhandshake.com",
        "handshake_email": f"{username}@jhu.edu",
        "download_dir": f"C:\\Users\\{username}\\Downloads"
    }
    if not (os.path.exists(CONFIG_DIR) and os.path.isdir(CONFIG_DIR)):
        os.mkdir(CONFIG_DIR)
    if not (os.path.exists(CONFIG_FILEPATH) and os.path.isfile(CONFIG_FILEPATH)):
        with open(CONFIG_FILEPATH, 'w') as file:
            json.dump(config, file)


def load_config():
    """
    Load the configuration file
    :return: a dict of config values
    """
    _create_default_config()
    with open(CONFIG_FILEPATH, 'r') as file:
        return json.load(file)


def open_config_for_editing():
    """
    Open the config file in the default text editor for manual editing.
    """
    subprocess.run(['start', CONFIG_FILEPATH], check=True, shell=True)


config = load_config()

class BrowsingSession(HandshakeSession):
    """
    A wrapper class around HandshakeSession that always logs into the account
    specified in the config file.
    """

    def __init__(self, password, max_wait_time=300):
        super().__init__(config['handshake_url'], config['handshake_email'],
                         password=password, download_dir=config['download_dir'],
                         max_wait_time=max_wait_time, chromedriver_path=_get_chromedriver_path())


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


def create_filepath_in_download_dir(filename: str) -> str:
    """
    Given a filename, append it to the download dir to create a full file path

    :param filename: the filename to concatenate with the download dir
    :return: the full filepath
    """
    return os.path.join(config['download_dir'], filename)


def get_datestamped_filename(filename: str) -> str:
    """
    Get a filename (minus extension) with the current datetime stamp appended onto it

    :param filename: the "base" name of the file, without any extensions
    :type filename: str
    :return: the base filename concatenated to the current datetime stamp
    """
    return f'{filename}_{format_datetime_for_filename(datetime.now())}'


def format_datetime_for_filename(dt: datetime) -> str:
    """
    Format a datetime into a string suitable for use in a file name

    :param dt: the datetime to format
    :type dt: datetime
    :return: a string representation of the datetime suitable for a file name
    """
    return dt.strftime('%Y-%m-%dT%H-%M-%S')


def write_to_file(text: str, file_path):
    """Write the given string to a file at the given filepath"""
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text)
    except FileNotFoundError as e:
        print(f'Unable to write results to file. {str(e)}')


def read_and_delete_json(filepath: str) -> List[dict]:
    """
    Read the given json file into a list of dicts, then delete the file

    :param filepath: the filepath of the json file to read
    :return: a list of dicts representing the json data
    """
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    os.remove(filepath)
    return data


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


def _get_chromedriver_path() -> str:
    if getattr(sys, 'frozen', False):
        # executed as a bundled exe, the driver is in the extracted folder
        return os.path.join(sys._MEIPASS, "src", "chromedriver.exe")
    else:
        # executed as a simple script, the driver should be in `PATH`
        return "./chromedriver.exe"
