import sys

from src.data_download_functions import (download_appointment_type_settings,
                                         download_label_settings_data,
                                         download_major_mapping,
                                         download_pending_student_requests,
                                         download_rejected_student_requests)
from src.rule_sets.daily_verification import daily_verification
from src.utils import BrowsingSession


def print_action_options(actions):
    for i, action in enumerate(actions):
        print(f'({i + 1}) {action["name"]}')


def perform_action(actions, action_index, *args):
    action = actions[action_index]
    print(f'Performing action: "{action["name"]}"')
    filepath = action['function'](*args)
    print(f'Results saved at {filepath}')


def exit_program(*args):
    print('Goodbye!')
    sys.exit(0)


if __name__ == '__main__':

    actions = [
        {'name': 'Run Daily Rule Verification', 'function': daily_verification},
        {'name': 'Download Appointment Type Settings', 'function': download_appointment_type_settings},
        {'name': 'Download Label Settings', 'function': download_label_settings_data},
        {'name': 'Download Major Mapping', 'function': download_major_mapping},
        {'name': 'Download Pending Student Requests', 'function': download_pending_student_requests},
        {'name': 'Download Rejected Student Requests', 'function': download_rejected_student_requests},
        {'name': 'Exit Program', 'function': exit_program}
    ]

    print('HandshakeAdministrator')
    print('======================\n')
    program_is_running = True
    while program_is_running:
        do_not_restart_browser = True
        with BrowsingSession() as browser:
            while do_not_restart_browser:
                try:
                    print_action_options(actions)
                    print()  # blank line for formatting
                    user_selection = int(input('Select action: ')) - 1
                    perform_action(actions, user_selection, browser)
                    print()  # blank line for formatting
                except SystemExit:
                    do_not_restart_browser = False
                    program_is_running = False
                except:
                    do_not_restart_browser = False
