import unittest
from datetime import datetime, timedelta

from src.rule_verification import VerificationResult
from src.rules.appointment_rules import (
    past_appointments_have_finalized_status,
    all_appointments_have_a_type,
    parse_status_error_str
)


class TestAppointmentStatusCompleted(unittest.TestCase):
    RULE_NAME = 'No past appointments are marked as "approved", "requested", or "started"'

    def test_with_no_data(self):
        self.assertEqual(VerificationResult(self.RULE_NAME, True),
                         past_appointments_have_finalized_status([]))

    def test_future_appointments_are_fine(self):
        tomorrow_start_time = datetime.now() + timedelta(days=1)
        tomorrow_end_time = tomorrow_start_time + timedelta(minutes=30)
        next_month_start_time = datetime.now() + timedelta(weeks=4)
        next_month_end_time = next_month_start_time + timedelta(minutes=30)
        appt_data = [
            {
                "appointments.id": "6352432",
                "appointments.start_date_time": format_datetime(tomorrow_start_time),
                "appointments.end_date_time": format_datetime(tomorrow_end_time),
                "appointments.status": "approved",
                "staff_member_on_appointments.first_name": "Alex",
                "staff_member_on_appointments.last_name": "Vanderbildt"
            },
            {
                "appointments.id": "18536335",
                "appointments.start_date_time": format_datetime(next_month_start_time),
                "appointments.end_date_time": format_datetime(next_month_end_time),
                "appointments.status": "approved",
                "staff_member_on_appointments.first_name": "Mary",
                "staff_member_on_appointments.last_name": "Smith"
            },
        ]
        self.assertEqual(VerificationResult(self.RULE_NAME, True),
                         past_appointments_have_finalized_status(appt_data))

    def test_completed_past_appointments_are_fine(self):
        appt_data = [
            {
                "appointments.id": "6352432",
                "appointments.start_date_time": "2018-05-28 15:30:00",
                "appointments.end_date_time": "2018-05-28 16:00:00",
                "appointments.status": "completed",
                "staff_member_on_appointments.first_name": "Alex",
                "staff_member_on_appointments.last_name": "Vanderbildt"
            },
            {
                "appointments.id": "18536335",
                "appointments.start_date_time": "2015-12-08 10:00:00",
                "appointments.end_date_time": "2015-12-08 10:30:00",
                "appointments.status": "cancelled",
                "staff_member_on_appointments.first_name": "Mary",
                "staff_member_on_appointments.last_name": "Smith"
            },
            {
                "appointments.id": "18536335",
                "appointments.start_date_time": "2008-02-08 10:00:00",
                "appointments.end_date_time": "2008-02-08 10:30:00",
                "appointments.status": "no_show",
                "staff_member_on_appointments.first_name": "Jack",
                "staff_member_on_appointments.last_name": "Heizer"
            },
            {
                "appointments.id": "18536335",
                "appointments.start_date_time": "2017-12-08 11:00:00",
                "appointments.end_date_time": "2017-12-01 11:30:00",
                "appointments.status": "declined",
                "staff_member_on_appointments.first_name": "Ella",
                "staff_member_on_appointments.last_name": "Barns"
            },
        ]
        self.assertEqual(VerificationResult(self.RULE_NAME, True),
                         past_appointments_have_finalized_status(appt_data))

    def test_incomplete_past_appointments(self):
        appt_data = [
            {
                "appointments.id": "6352432",
                "appointments.start_date_time": "2018-05-28 15:30:00",
                "appointments.end_date_time": "2018-05-28 16:00:00",
                "appointments.status": "approved",
                "staff_member_on_appointments.first_name": "Alex",
                "staff_member_on_appointments.last_name": "Vanderbildt"
            },
            {
                "appointments.id": "290392059",
                "appointments.start_date_time": "2015-12-08 10:00:00",
                "appointments.end_date_time": "2015-12-08 10:30:00",
                "appointments.status": "started",
                "staff_member_on_appointments.first_name": "Mary",
                "staff_member_on_appointments.last_name": "Smith"
            },
            {
                "appointments.id": "18536335",
                "appointments.start_date_time": "2016-08-19 13:00:00",
                "appointments.end_date_time": "2016-08-19 13:30:00",
                "appointments.status": "completed",
                "staff_member_on_appointments.first_name": "Jess",
                "staff_member_on_appointments.last_name": "Walker"
            },
        ]
        expected_errors = [
            'Appointment 6352432 (Alex Vanderbildt, 2018-05-28 15:30:00) has status "approved"',
            'Appointment 290392059 (Mary Smith, 2015-12-08 10:00:00) has status "started"'
        ]
        self.assertEqual(VerificationResult(self.RULE_NAME, False, errors=expected_errors),
                         past_appointments_have_finalized_status(appt_data))


class TestAppointmentHasType(unittest.TestCase):
    RULE_NAME = 'All appointments have an associated appointment type'

    def test_with_no_data(self):
        self.assertEqual(VerificationResult(self.RULE_NAME, True),
                         all_appointments_have_a_type([]))

    def test_appointments_with_a_type_are_fine(self):
        appt_data = [
            {
                "appointments.id": "6352432",
                "appointments.start_date_time": "2018-05-28 15:30:00",
                "appointments.end_date_time": "2018-05-28 16:00:00",
                "appointments.status": "approved",
                "staff_member_on_appointments.first_name": "Alex",
                "staff_member_on_appointments.last_name": "Vanderbildt",
                "appointment_type_on_appointments.name": "Resume Review Type"
            },
            {
                "appointments.id": "18536335",
                "appointments.start_date_time": "2016-08-19 13:00:00",
                "appointments.end_date_time": "2016-08-19 13:30:00",
                "appointments.status": "approved",
                "staff_member_on_appointments.first_name": "Mary",
                "staff_member_on_appointments.last_name": "Smith",
                "appointment_type_on_appointments.name": "Interview Prep Type"
            },
        ]
        self.assertEqual(VerificationResult(self.RULE_NAME, True),
                         all_appointments_have_a_type(appt_data))

    def test_appointments_without_a_type(self):
        appt_data = [
            {
                "appointments.id": "6352432",
                "appointments.start_date_time": "2018-05-28 15:30:00",
                "appointments.end_date_time": "2018-05-28 16:00:00",
                "appointments.status": "approved",
                "staff_member_on_appointments.first_name": "Alex",
                "staff_member_on_appointments.last_name": "Vanderbildt",
                "appointment_type_on_appointments.name": ""
            },
            {
                "appointments.id": "18536335",
                "appointments.start_date_time": "2016-08-19 13:00:00",
                "appointments.end_date_time": "2016-08-19 13:30:00",
                "appointments.status": "approved",
                "staff_member_on_appointments.first_name": "Mary",
                "staff_member_on_appointments.last_name": "Smith",
                "appointment_type_on_appointments.name": None
            },
        ]
        expected_errors = [
            'Appointment 6352432 (Alex Vanderbildt, 2018-05-28 15:30:00) does not have an appointment type',
            'Appointment 18536335 (Mary Smith, 2016-08-19 13:00:00) does not have an appointment type'
        ]
        self.assertEqual(VerificationResult(self.RULE_NAME, False, errors=expected_errors),
                         all_appointments_have_a_type(appt_data))


class TestErrorStringParser(unittest.TestCase):

    def test_status_error_parser(self):
        test_strs = [
            'Appointment 4124582 (MaryAnn Riegelman, 2019-07-23 15:00:00) has status "approved"',
            'Appointment 4167709 (Jenn Leard- Consulting, 2019-08-14 16:30:00) has status "started"',
            'Appointment 4383184 (Roni White, 2019-09-19 14:00:00) has status "approved"'
        ]

        expected = [
            {'id': '4124582', 'url': 'https://app.joinhandshake.com/appointments/4124582',
             'staff_name': 'MaryAnn Riegelman', 'datetime': datetime(2019, 7, 23, 15), 'status': 'approved'},
            {'id': '4167709', 'url': 'https://app.joinhandshake.com/appointments/4167709',
             'staff_name': 'Jenn Leard- Consulting', 'datetime': datetime(2019, 8, 14, 16, 30), 'status': 'started'},
            {'id': '4383184', 'url': 'https://app.joinhandshake.com/appointments/4383184', 'staff_name': 'Roni White',
             'datetime': datetime(2019, 9, 19, 14), 'status': 'approved'}
        ]
        actual = [parse_status_error_str(error_str) for error_str in test_strs]
        self.assertEqual(expected, actual)

def format_datetime(date_time):
    return date_time.strftime('%Y-%m-%d %H:%M:%S')
