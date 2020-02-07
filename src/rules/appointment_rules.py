from datetime import datetime
from typing import Union, Callable

from src.insights_fields import AppointmentFields
from src.rule_verification import make_rule


def _build_appt_status_error_message(appt: dict) -> str:
    return (f'Appointment {appt[AppointmentFields.ID]} ({_get_staff_name(appt)}, '
            f'{appt[AppointmentFields.START_DATE_TIME]}) status should be one of "completed", "cancelled", or "no-show"')


def _get_appt_status_error(appt: dict) -> Union[dict, None]:
    incomplete_statuses = ['approved', 'requested', 'started']
    start_date_time = _parse_date_time(appt[AppointmentFields.START_DATE_TIME])
    if appt[AppointmentFields.STATUS] in incomplete_statuses and start_date_time < datetime.now():
        return _extract_error_data_from_appt(appt, _build_appt_status_error_message)
    else:
        return None


def _parse_date_time(date_time_str: str) -> datetime:
    return datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')


def _build_appt_type_error_message(appt) -> str:
    return (f'Appointment {appt[AppointmentFields.ID]} ({_get_staff_name(appt)}, '
            f'{appt[AppointmentFields.START_DATE_TIME]}) does not have an appointment type')


def _get_appt_type_missing_error(appt: dict) -> Union[dict, None]:
    if not appt[AppointmentFields.TYPE]:
        return _extract_error_data_from_appt(appt, _build_appt_type_error_message)
    else:
        return None


def _extract_error_data_from_appt(appt: dict, error_msg_func: Callable[[dict], str]) -> dict:
    return {
        'id': appt[AppointmentFields.ID],
        'start_date_time': _parse_date_time(appt[AppointmentFields.START_DATE_TIME]),
        'staff_last_name': appt[AppointmentFields.STAFF_MEMBER_LAST_NAME],
        'staff_first_name': appt[AppointmentFields.STAFF_MEMBER_FIRST_NAME],
        'url': f'https://app.joinhandshake.com/appointments/{appt[AppointmentFields.ID]}',
        'error_msg': error_msg_func(appt)
    }

##########################
# HELPER/SUB-FUNCTIONS
##########################

def _get_staff_name(appt: dict) -> str:
    return (appt[AppointmentFields.STAFF_MEMBER_FIRST_NAME].strip() + ' ' +
            appt[AppointmentFields.STAFF_MEMBER_LAST_NAME].strip())


######################
# RULES
######################

past_appointments_have_finalized_status = make_rule(
    'No past appointments are marked as "approved", "requested", or "started"',
    'appt_wrong_status',
    _get_appt_status_error
)

all_appointments_have_a_type = make_rule(
    'All appointments have an associated appointment type',
    'appt_missing_type',
    _get_appt_type_missing_error
)
