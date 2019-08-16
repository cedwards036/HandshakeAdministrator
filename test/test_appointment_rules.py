import unittest
from datetime import datetime, timedelta

from src.appointment_rules import (
    past_appointments_have_finalized_status
)
from src.rule_verification import VerificationResult


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


def format_datetime(date_time):
    return date_time.strftime('%Y-%m-%d %H:%M:%S')
