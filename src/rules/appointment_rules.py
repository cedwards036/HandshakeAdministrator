import re
from datetime import datetime

from src.rule_verification import make_rule


def _get_appt_status_error(appt: dict):
    def _build_appt_status_error_string(appt: dict) -> str:
        return (f'Appointment {appt["appointments.id"]} ({_get_staff_name(appt)}, '
                f'{appt["appointments.start_date_time"]}) has status '
                f'"{appt["appointments.status"]}"')

    incomplete_statuses = ['approved', 'requested', 'started']
    start_time = datetime.strptime(appt['appointments.start_date_time'], '%Y-%m-%d %H:%M:%S')
    if appt['appointments.status'] in incomplete_statuses and start_time < datetime.now():
        return _build_appt_status_error_string(appt)
    else:
        return None


def _get_appt_type_missing_error(appt: dict) -> str:
    if not appt['appointment_type_on_appointments.name']:
        return (f'Appointment {appt["appointments.id"]} ({_get_staff_name(appt)}, '
                f'{appt["appointments.start_date_time"]}) does not have an appointment type')


##########################
# HELPER/SUB-FUNCTIONS
##########################


def parse_status_error_str(status_error_str: str) -> dict:
    """
    Parse an appointment status error into a dictionary.

    :param status_error_str: the error string to parse
    :return: a dictionary with fields for appt id, Handshake url, staff name, appt
             datetime, and appt status
    """

    def parse_datetime_str(datetime_str: str) -> datetime:
        return datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')

    regex = '^Appointment ([0-9]+) \((.+), (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\) has status \"([a-z]+)\"$'
    try:
        parsed_fields = re.match(regex, status_error_str).groups()
        return {
            'id': parsed_fields[0],
            'url': f'https://app.joinhandshake.com/appointments/{parsed_fields[0]}',
            'staff_name': parsed_fields[1],
            'datetime': parse_datetime_str(parsed_fields[2]),
            'status': parsed_fields[3]
        }
    except AttributeError:
        raise ValueError(f'Invalid error str: "{status_error_str}"')



def _get_staff_name(appt: dict) -> str:
    return (appt['staff_member_on_appointments.first_name'].strip() + ' ' +
            appt['staff_member_on_appointments.last_name'].strip())


######################
# RULES
######################

past_appointments_have_finalized_status = make_rule(
    'No past appointments are marked as "approved", "requested", or "started"',
    _get_appt_status_error
)

all_appointments_have_a_type = make_rule(
    'All appointments have an associated appointment type',
    _get_appt_type_missing_error
)
