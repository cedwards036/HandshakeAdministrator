from datetime import datetime

from src.rule_verification import make_rule


##########################
# HELPER/SUB-FUNCTIONS
##########################

def _get_appt_status_error(appt: dict):
    incomplete_statuses = ['approved', 'requested', 'started']
    start_time = datetime.strptime(appt['appointments.start_date_time'], '%Y-%m-%d %H:%M:%S')
    if appt['appointments.status'] in incomplete_statuses and start_time < datetime.now():
        return _build_appt_status_error_string(appt)
    else:
        return None


def _build_appt_status_error_string(appt: dict) -> str:
    return (f'Appointment {appt["appointments.id"]} ({_get_staff_name(appt)}, '
            f'{appt["appointments.start_date_time"]}) has status '
            f'"{appt["appointments.status"]}"')


def _get_appt_type_missing_error(appt: dict) -> str:
    if not appt['appointment_type_on_appointments.name']:
        return (f'Appointment {appt["appointments.id"]} ({_get_staff_name(appt)}, '
                f'{appt["appointments.start_date_time"]}) does not have an appointment type')


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
