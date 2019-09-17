import sys
from getpass import getpass
from typing import List

from autohandshake.src.exceptions import (NoSuchElementError, InsufficientPermissionsError, InvalidPasswordError,
                                          BrowserTimeoutError, InvalidUserTypeError, InvalidEmailError)

from src.data_download_functions import (download_appointment_type_settings,
                                         download_label_settings_data,
                                         download_major_mapping,
                                         download_pending_student_requests,
                                         download_rejected_student_requests)
from src.rule_sets.daily_verification import daily_verification
from src.utils import BrowsingSession, open_config_for_editing


def get_user_selection(actions: List[dict]) -> int:
    try:
        print_action_options(actions)
        print()  # blank line for formatting
        user_selection = int(input('Select action: ')) - 1
        if not user_selection_is_valid(user_selection, actions):
            raise ValueError
        return user_selection
    except ValueError:
        print('Invalid selection. Please try again.\n')
        return get_user_selection(actions)


def print_action_options(actions):
    for i, action in enumerate(actions):
        print(f'({i + 1}) {action["name"]}')


def perform_action(actions, action_index, *args):
    action = actions[action_index]
    print(f'Performing action: "{action["name"]}"')
    filepath = action['function'](*args)
    print(f'Results saved at {filepath}')


def user_selection_is_valid(user_selection: int, actions: List[dict]) -> bool:
    return user_selection in range(0, len(actions))


def print_goodbye_message():
    print('Goodbye!')


def open_config_file(*args):
    open_config_for_editing()
    print('Any changes to the config file will take effect the next time you launch the program.')


def exit_program(*args):
    print_goodbye_message()
    sys.exit(0)


if __name__ == '__main__':
    actions = [
        {'name': 'Run Daily Rule Verification', 'function': daily_verification},
        {'name': 'Download Appointment Type Settings', 'function': download_appointment_type_settings},
        {'name': 'Download Label Settings', 'function': download_label_settings_data},
        {'name': 'Download Major Mapping', 'function': download_major_mapping},
        {'name': 'Download Pending Student Requests', 'function': download_pending_student_requests},
        {'name': 'Download Rejected Student Requests', 'function': download_rejected_student_requests},
        {'name': 'Open Config File', 'function': open_config_file},
        {'name': 'Exit Program', 'function': exit_program}
    ]

    print('HandshakeAdministrator')
    print('======================\n')
    program_is_running = True
    while program_is_running:
        do_not_restart_browser = True
        password = getpass(prompt='Please enter your Handshake password: ')
        with BrowsingSession(password) as browser:
            while do_not_restart_browser:
                try:
                    user_selection = get_user_selection(actions)
                    perform_action(actions, user_selection, browser)
                    print()  # blank line for formatting
                except SystemExit:
                    do_not_restart_browser = False
                    program_is_running = False
                except (NoSuchElementError, InsufficientPermissionsError, InvalidPasswordError, BrowserTimeoutError,
                        InvalidUserTypeError, InvalidEmailError) as e:
                    user_wants_to_try_again = input(
                        'The program encountered an error. Would you like to try again? (y / n): ').lower() == 'y'
                    if not user_wants_to_try_again:
                        print_goodbye_message()
                        program_is_running = False
                    do_not_restart_browser = False
