import unittest
from datetime import datetime, timedelta

from src.insights_fields import AppointmentFields
from src.rules.appointment_rules import (
    past_appointments_have_finalized_status,
    all_appointments_have_a_type,
    parse_status_error_str,
    _build_appt_type_error_message,
    _build_appt_status_error_message
)
from test.common import assertIsVerified, assertContainsErrorIDs


class TestAppointmentStatusCompleted(unittest.TestCase):
    RULE_NAME = 'No past appointments are marked as "approved", "requested", or "started"'

    def test_with_no_data(self):
        assertIsVerified(self, past_appointments_have_finalized_status([]))

    def test_future_appointments_are_fine(self):
        tomorrow_start_time = datetime.now() + timedelta(days=1)
        tomorrow_end_time = tomorrow_start_time + timedelta(minutes=30)
        next_month_start_time = datetime.now() + timedelta(weeks=4)
        next_month_end_time = next_month_start_time + timedelta(minutes=30)
        appt_data = [
            {
                AppointmentFields.ID: "6352432",
                AppointmentFields.START_DATE_TIME: format_datetime(tomorrow_start_time),
                AppointmentFields.END_DATE_TIME: format_datetime(tomorrow_end_time),
                AppointmentFields.STATUS: "approved",
                AppointmentFields.STAFF_MEMBER_FIRST_NAME: "Alex",
                AppointmentFields.STAFF_MEMBER_LAST_NAME: "Vanderbildt"
            },
            {
                AppointmentFields.ID: "18536335",
                AppointmentFields.START_DATE_TIME: format_datetime(next_month_start_time),
                AppointmentFields.END_DATE_TIME: format_datetime(next_month_end_time),
                AppointmentFields.STATUS: "approved",
                AppointmentFields.STAFF_MEMBER_FIRST_NAME: "Mary",
                AppointmentFields.STAFF_MEMBER_LAST_NAME: "Smith"
            },
        ]
        assertIsVerified(self, past_appointments_have_finalized_status(appt_data))

    def test_completed_past_appointments_are_fine(self):
        appt_data = [
            {
                AppointmentFields.ID: "6352432",
                AppointmentFields.START_DATE_TIME: "2018-05-28 15:30:00",
                AppointmentFields.END_DATE_TIME: "2018-05-28 16:00:00",
                AppointmentFields.STATUS: "completed",
                AppointmentFields.STAFF_MEMBER_FIRST_NAME: "Alex",
                AppointmentFields.STAFF_MEMBER_LAST_NAME: "Vanderbildt"
            },
            {
                AppointmentFields.ID: "18536335",
                AppointmentFields.START_DATE_TIME: "2015-12-08 10:00:00",
                AppointmentFields.END_DATE_TIME: "2015-12-08 10:30:00",
                AppointmentFields.STATUS: "cancelled",
                AppointmentFields.STAFF_MEMBER_FIRST_NAME: "Mary",
                AppointmentFields.STAFF_MEMBER_LAST_NAME: "Smith"
            },
            {
                AppointmentFields.ID: "18536335",
                AppointmentFields.START_DATE_TIME: "2008-02-08 10:00:00",
                AppointmentFields.END_DATE_TIME: "2008-02-08 10:30:00",
                AppointmentFields.STATUS: "no_show",
                AppointmentFields.STAFF_MEMBER_FIRST_NAME: "Jack",
                AppointmentFields.STAFF_MEMBER_LAST_NAME: "Heizer"
            },
            {
                AppointmentFields.ID: "18536335",
                AppointmentFields.START_DATE_TIME: "2017-12-08 11:00:00",
                AppointmentFields.END_DATE_TIME: "2017-12-01 11:30:00",
                AppointmentFields.STATUS: "declined",
                AppointmentFields.STAFF_MEMBER_FIRST_NAME: "Ella",
                AppointmentFields.STAFF_MEMBER_LAST_NAME: "Barns"
            },
        ]
        assertIsVerified(self, past_appointments_have_finalized_status(appt_data))

    def test_incomplete_past_appointments(self):
        appt_data = [
            {
                AppointmentFields.ID: "6352432",
                AppointmentFields.START_DATE_TIME: "2018-05-28 15:30:00",
                AppointmentFields.END_DATE_TIME: "2018-05-28 16:00:00",
                AppointmentFields.STATUS: "approved",
                AppointmentFields.STAFF_MEMBER_FIRST_NAME: "Alex",
                AppointmentFields.STAFF_MEMBER_LAST_NAME: "Vanderbildt"
            },
            {
                AppointmentFields.ID: "290392059",
                AppointmentFields.START_DATE_TIME: "2015-12-08 10:00:00",
                AppointmentFields.END_DATE_TIME: "2015-12-08 10:30:00",
                AppointmentFields.STATUS: "started",
                AppointmentFields.STAFF_MEMBER_FIRST_NAME: "Mary",
                AppointmentFields.STAFF_MEMBER_LAST_NAME: "Smith"
            },
            {
                AppointmentFields.ID: "18536335",
                AppointmentFields.START_DATE_TIME: "2016-08-19 13:00:00",
                AppointmentFields.END_DATE_TIME: "2016-08-19 13:30:00",
                AppointmentFields.STATUS: "completed",
                AppointmentFields.STAFF_MEMBER_FIRST_NAME: "Jess",
                AppointmentFields.STAFF_MEMBER_LAST_NAME: "Walker"
            },
        ]
        expected_errors = [
            'Appointment 6352432 (Alex Vanderbildt, 2018-05-28 15:30:00) has status "approved"',
            'Appointment 290392059 (Mary Smith, 2015-12-08 10:00:00) has status "started"'
        ]
        assertContainsErrorIDs(self, ['6352432', '290392059'], past_appointments_have_finalized_status(appt_data))

    def test_type_error_message(self):
        appt = {
            AppointmentFields.ID: "6352432",
            AppointmentFields.START_DATE_TIME: "2018-05-28 15:30:00",
            AppointmentFields.END_DATE_TIME: "2018-05-28 16:00:00",
            AppointmentFields.STATUS: "approved",
            AppointmentFields.STAFF_MEMBER_FIRST_NAME: "Alex",
            AppointmentFields.STAFF_MEMBER_LAST_NAME: "Vanderbildt"
        }
        expected = 'Appointment 6352432 (Alex Vanderbildt, 2018-05-28 15:30:00) has status "approved"'
        self.assertEqual(expected, _build_appt_status_error_message(appt))


class TestAppointmentHasType(unittest.TestCase):
    RULE_NAME = 'All appointments have an associated appointment type'

    def test_with_no_data(self):
        assertIsVerified(self, all_appointments_have_a_type([]))

    def test_appointments_with_a_type_are_fine(self):
        appt_data = [
            {
                AppointmentFields.ID: "6352432",
                AppointmentFields.START_DATE_TIME: "2018-05-28 15:30:00",
                AppointmentFields.END_DATE_TIME: "2018-05-28 16:00:00",
                AppointmentFields.STATUS: "approved",
                AppointmentFields.STAFF_MEMBER_FIRST_NAME: "Alex",
                AppointmentFields.STAFF_MEMBER_LAST_NAME: "Vanderbildt",
                AppointmentFields.TYPE: "Resume Review Type"
            },
            {
                AppointmentFields.ID: "18536335",
                AppointmentFields.START_DATE_TIME: "2016-08-19 13:00:00",
                AppointmentFields.END_DATE_TIME: "2016-08-19 13:30:00",
                AppointmentFields.STATUS: "approved",
                AppointmentFields.STAFF_MEMBER_FIRST_NAME: "Mary",
                AppointmentFields.STAFF_MEMBER_LAST_NAME: "Smith",
                AppointmentFields.TYPE: "Interview Prep Type"
            },
        ]
        assertIsVerified(self, all_appointments_have_a_type(appt_data))

    def test_appointments_without_a_type(self):
        appt_data = [
            {
                AppointmentFields.ID: "6352432",
                AppointmentFields.START_DATE_TIME: "2018-05-28 15:30:00",
                AppointmentFields.END_DATE_TIME: "2018-05-28 16:00:00",
                AppointmentFields.STATUS: "approved",
                AppointmentFields.STAFF_MEMBER_FIRST_NAME: "Alex",
                AppointmentFields.STAFF_MEMBER_LAST_NAME: "Vanderbildt",
                AppointmentFields.TYPE: ""
            },
            {
                AppointmentFields.ID: "18536335",
                AppointmentFields.START_DATE_TIME: "2016-08-19 13:00:00",
                AppointmentFields.END_DATE_TIME: "2016-08-19 13:30:00",
                AppointmentFields.STATUS: "approved",
                AppointmentFields.STAFF_MEMBER_FIRST_NAME: "Mary",
                AppointmentFields.STAFF_MEMBER_LAST_NAME: "Smith",
                AppointmentFields.TYPE: None
            },
        ]
        assertContainsErrorIDs(self, ['6352432', '18536335'], all_appointments_have_a_type(appt_data))

    def test_type_error_message(self):
        appt = {
            AppointmentFields.ID: "6352432",
            AppointmentFields.START_DATE_TIME: "2018-05-28 15:30:00",
            AppointmentFields.END_DATE_TIME: "2018-05-28 16:00:00",
            AppointmentFields.STATUS: "approved",
            AppointmentFields.STAFF_MEMBER_FIRST_NAME: "Alex",
            AppointmentFields.STAFF_MEMBER_LAST_NAME: "Vanderbildt",
            AppointmentFields.TYPE: ""
        }
        expected = 'Appointment 6352432 (Alex Vanderbildt, 2018-05-28 15:30:00) does not have an appointment type'
        self.assertEqual(expected, _build_appt_type_error_message(appt))


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
