import re
from datetime import datetime
from typing import Union

from src.insights_fields import AppointmentFields
from src.rule_verification import make_rule


def _build_appt_status_error_message(appt: dict) -> str:
    return (f'Appointment {appt[AppointmentFields.ID]} ({_get_staff_name(appt)}, '
            f'{appt[AppointmentFields.START_DATE_TIME]}) has status '
            f'"{appt[AppointmentFields.STATUS]}"')


def _get_appt_status_error(appt: dict) -> Union[dict, None]:
    incomplete_statuses = ['approved', 'requested', 'started']
    start_time = datetime.strptime(appt[AppointmentFields.START_DATE_TIME], '%Y-%m-%d %H:%M:%S')
    if appt[AppointmentFields.STATUS] in incomplete_statuses and start_time < datetime.now():
        return {
            'id': appt[AppointmentFields.ID],
            'error_msg': _build_appt_status_error_message(appt)
        }
    else:
        return None


def _build_appt_type_error_message(appt) -> str:
    return (f'Appointment {appt[AppointmentFields.ID]} ({_get_staff_name(appt)}, '
            f'{appt[AppointmentFields.START_DATE_TIME]}) does not have an appointment type')


def _get_appt_type_missing_error(appt: dict) -> Union[dict, None]:
    if not appt[AppointmentFields.TYPE]:
        return {
            'id': appt[AppointmentFields.ID],
            'error_msg': _build_appt_type_error_message(appt)
        }
    else:
        return None


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
    return (appt[AppointmentFields.STAFF_MEMBER_FIRST_NAME].strip() + ' ' +
            appt[AppointmentFields.STAFF_MEMBER_LAST_NAME].strip())


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
