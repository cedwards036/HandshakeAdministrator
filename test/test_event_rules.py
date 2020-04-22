import unittest
from datetime import datetime, timedelta

from src.constants import CareerCenters
from src.insights_fields import EventFields
from src.rules.event_rules import (
    jhu_owned_events_are_prefixed_correctly,
    _build_event_prefix_error_message,
    events_are_invite_only_iff_not_university_wide,
    _build_invite_only_error_message,
    advertisement_events_are_labeled,
    _build_ad_error_message,
    past_events_do_not_have_virtual_event_type
)
from test.common import assertContainsErrorIDs, assertIsVerified


class TestEventsArePrefixedCorrectly(unittest.TestCase):

    def test_with_no_data(self):
        assertIsVerified(self, jhu_owned_events_are_prefixed_correctly([]))

    def test_with_non_career_center_event(self):
        event_data = [
            {
                EventFields.ID: "4324725",
                EventFields.NAME: "McKinsey Virtual Session",
                EventFields.CAREER_CENTER: None
            },
        ]
        assertIsVerified(self, jhu_owned_events_are_prefixed_correctly(event_data))

    def test_university_wide_is_valid(self):
        event_data = [
            {
                EventFields.ID: "353242",
                EventFields.NAME: "University-Wide: 2019 JumpStart STEM Diversity Forum",
                EventFields.CAREER_CENTER: CareerCenters.HOMEWOOD
            },
            {
                EventFields.ID: "8563254",
                EventFields.NAME: "University-Wide: Drop-in Mondays HE September 9th Afternoon",
                EventFields.CAREER_CENTER: CareerCenters.CAREY
            },
            {
                EventFields.ID: "902820",
                EventFields.NAME: "University-Wide: Career Clinic: Job Negotiation",
                EventFields.CAREER_CENTER: CareerCenters.PDCO
            },
        ]
        assertIsVerified(self, jhu_owned_events_are_prefixed_correctly(event_data))

    def test_test_prefix_is_valid(self):
        event_data = [
            {
                EventFields.ID: "3463254",
                EventFields.NAME: "Test: 2019 JumpStart STEM Diversity Forum",
                EventFields.CAREER_CENTER: CareerCenters.HOMEWOOD
            },
            {
                EventFields.ID: "5364354",
                EventFields.NAME: "test- Drop-in Mondays HE September 9th Afternoon",
                EventFields.CAREER_CENTER: CareerCenters.PDCO
            },
            {
                EventFields.ID: "26895576",
                EventFields.NAME: "TESTING Career Clinic: Job Negotiation",
                EventFields.CAREER_CENTER: CareerCenters.SAIS
            },
        ]
        assertContainsErrorIDs(self, ['5364354', '26895576'], jhu_owned_events_are_prefixed_correctly(event_data))

    def test_cancelled_prefix_is_valid(self):
        event_data = [
            {
                EventFields.ID: "353242",
                EventFields.NAME: "CANCELLED: University-Wide: 2019 JumpStart STEM Diversity Forum",
                EventFields.CAREER_CENTER: CareerCenters.HOMEWOOD
            },
            {
                EventFields.ID: "8563254",
                EventFields.NAME: "CANCELLED: Carey: Drop-in Mondays HE September 9th Afternoon",
                EventFields.CAREER_CENTER: CareerCenters.CAREY
            },
            {
                EventFields.ID: "902820",
                EventFields.NAME: "CANCELLED: Career Clinic: Job Negotiation",
                EventFields.CAREER_CENTER: CareerCenters.PDCO
            },
            {
                EventFields.ID: "2635346",
                EventFields.NAME: "CANCELLED: SAISLeads Retreat",
                EventFields.CAREER_CENTER: CareerCenters.SAIS
            },
        ]
        assertContainsErrorIDs(self, ['902820', '2635346'], jhu_owned_events_are_prefixed_correctly(event_data))

    def test_canceled_misspelling_gives_helpful_feedback(self):
        event_data = [
            {
                EventFields.ID: "902820",
                EventFields.NAME: "CANCELED: PDCO: Career Clinic: Job Negotiation",
                EventFields.CAREER_CENTER: CareerCenters.PDCO
            },
            {
                EventFields.ID: "2635346",
                EventFields.NAME: "CAnCELEd: SAIS: SAISLeads Retreat",
                EventFields.CAREER_CENTER: CareerCenters.SAIS
            },
            {
                EventFields.ID: "3263343",
                EventFields.NAME: "Cancelled: Peabody: Launch Event",
                EventFields.CAREER_CENTER: CareerCenters.PEABODY
            }
        ]
        assertContainsErrorIDs(self, ['902820', '2635346', '3263343'], jhu_owned_events_are_prefixed_correctly(event_data))

    def test_with_one_of_each_bad_event(self):
        event_data = [
            {
                EventFields.ID: "353242",
                EventFields.NAME: "Homewoo: 2019 JumpStart STEM Diversity Forum",
                EventFields.CAREER_CENTER: CareerCenters.HOMEWOOD
            },
            {
                EventFields.ID: "8563254",
                EventFields.NAME: "Cary: Drop-in Mondays HE September 9th Afternoon",
                EventFields.CAREER_CENTER: CareerCenters.CAREY
            },
            {
                EventFields.ID: "902820",
                EventFields.NAME: "Univ. Wide: Career Clinic: Job Negotiation",
                EventFields.CAREER_CENTER: CareerCenters.PDCO
            },
            {
                EventFields.ID: "2635346",
                EventFields.NAME: "SAIS Europe SAISLeads Retreat",
                EventFields.CAREER_CENTER: CareerCenters.SAIS
            },
            {
                EventFields.ID: '526433',
                EventFields.NAME: 'N: How to Find Your First Nursing Job',
                EventFields.CAREER_CENTER: CareerCenters.NURSING
            },
            {
                EventFields.ID: '328092',
                EventFields.NAME: 'Strategies for Effective Professional Communication webinar',
                EventFields.CAREER_CENTER: CareerCenters.AAP
            },
            {
                EventFields.ID: '940935',
                EventFields.NAME: 'Homewood: LAUNCH @ Lunch',
                EventFields.CAREER_CENTER: CareerCenters.PEABODY
            },
            {
                EventFields.ID: '5839252',
                EventFields.NAME: 'BSP: Student Activities Fair',
                EventFields.CAREER_CENTER: CareerCenters.BSPH
            }
        ]
        expected_error_ids = ['353242', '8563254', '902820', '2635346', '526433', '328092', '940935', '5839252']
        assertContainsErrorIDs(self, expected_error_ids, jhu_owned_events_are_prefixed_correctly(event_data))

    def test_with_one_of_each_correct_event(self):
        event_data = [
            {
                EventFields.ID: "288569",
                EventFields.NAME: "Homewood: 2019 JumpStart STEM Diversity Forum",
                EventFields.CAREER_CENTER: CareerCenters.HOMEWOOD
            },
            {
                EventFields.ID: "331585",
                EventFields.NAME: "Carey: Drop-in Mondays HE September 9th Afternoon",
                EventFields.CAREER_CENTER: CareerCenters.CAREY
            },
            {
                EventFields.ID: "333931",
                EventFields.NAME: "PDCO: Career Clinic: Job Negotiation",
                EventFields.CAREER_CENTER: CareerCenters.PDCO
            },
            {
                EventFields.ID: "2938025",
                EventFields.NAME: "SAIS: Online Webinar",
                EventFields.CAREER_CENTER: CareerCenters.SAIS
            },
            {
                EventFields.ID: "317809",
                EventFields.NAME: "SAIS DC: SAISLeads Retreat",
                EventFields.CAREER_CENTER: CareerCenters.SAIS
            },
            {
                EventFields.ID: "288213",
                EventFields.NAME: "SAIS Europe: SAISLeads Retreat",
                EventFields.CAREER_CENTER: CareerCenters.SAIS
            },
            {
                EventFields.ID: "288213",
                EventFields.NAME: "SAIS ALL: Webinar",
                EventFields.CAREER_CENTER: CareerCenters.SAIS
            },
            {
                EventFields.ID: '239094',
                EventFields.NAME: 'HNC: Group Coaching Appointment 3',
                EventFields.CAREER_CENTER: CareerCenters.SAIS
            },
            {
                EventFields.ID: '249995',
                EventFields.NAME: 'Nursing: How to Find Your First Nursing Job',
                EventFields.CAREER_CENTER: CareerCenters.NURSING
            },
            {
                EventFields.ID: '217543',
                EventFields.NAME: 'AAP: Strategies for Effective Professional Communication webinar',
                EventFields.CAREER_CENTER: CareerCenters.AAP
            },
            {
                EventFields.ID: '264029',
                EventFields.NAME: 'Peabody: LAUNCH @ Lunch',
                EventFields.CAREER_CENTER: CareerCenters.PEABODY
            },
            {
                EventFields.ID: '198116',
                EventFields.NAME: 'BSPH: Student Activities Fair',
                EventFields.CAREER_CENTER: CareerCenters.BSPH
            }
        ]
        assertIsVerified(self, jhu_owned_events_are_prefixed_correctly(event_data))

    def test_with_all_event_types(self):
        event_data = [
            {
                EventFields.ID: "288569",
                EventFields.NAME: "Homewood: 2019 JumpStart STEM Diversity Forum",
                EventFields.CAREER_CENTER: CareerCenters.HOMEWOOD
            },
            {
                EventFields.ID: "331585",
                EventFields.NAME: "Carey: Drop-in Mondays HE September 9th Afternoon",
                EventFields.CAREER_CENTER: CareerCenters.CAREY
            },
            {
                EventFields.ID: "333931",
                EventFields.NAME: "PDCO: Career Clinic: Job Negotiation",
                EventFields.CAREER_CENTER: CareerCenters.PDCO
            },
            {
                EventFields.ID: '526433',
                EventFields.NAME: 'N: How to Find Your First Nursing Job',
                EventFields.CAREER_CENTER: CareerCenters.NURSING
            },
            {
                EventFields.ID: '328092',
                EventFields.NAME: 'Strategies for Effective Professional Communication webinar',
                EventFields.CAREER_CENTER: CareerCenters.AAP
            },
            {
                EventFields.ID: '940935',
                EventFields.NAME: 'Homewood: LAUNCH @ Lunch',
                EventFields.CAREER_CENTER: CareerCenters.PEABODY
            },
            {
                EventFields.ID: "83257925",
                EventFields.NAME: "Deloitte Virtual Session",
                EventFields.CAREER_CENTER: None
            },
            {
                EventFields.ID: "4324725",
                EventFields.NAME: "McKinsey Virtual Session",
                EventFields.CAREER_CENTER: None
            },
            {
                EventFields.ID: "12980293",
                EventFields.NAME: "Google On-Site",
                EventFields.CAREER_CENTER: None
            },
        ]
        assertContainsErrorIDs(self, ['526433', '328092', '940935'], jhu_owned_events_are_prefixed_correctly(event_data))

    def test_prefix_error_message_with_single_prefix(self):
        event = {
            EventFields.ID: '328092',
            EventFields.NAME: 'Strategies for Effective Professional Communication webinar',
            EventFields.CAREER_CENTER: CareerCenters.AAP
        }
        expected = 'Event 328092 (Strategies for Effective Professional Communication webinar) should have prefix "AAP:"'
        self.assertEqual(expected, _build_event_prefix_error_message(event, ['AAP:']))

    def test_prefix_error_message_with_multiple_prefixes(self):
        event = {
            EventFields.ID: '437858',
            EventFields.NAME: 'SAIS Europe Vienna Career trek 2020: OPEC',
            EventFields.CAREER_CENTER: CareerCenters.SAIS
        }
        expected = 'Event 437858 (SAIS Europe Vienna Career trek 2020: OPEC) should have prefix "SAIS:", "SAIS DC:", "SAIS Europe:", or "HNC:"'
        self.assertEqual(expected, _build_event_prefix_error_message(event, ['SAIS:', 'SAIS DC:', 'SAIS Europe:', 'HNC:']))


class TestEventsAreInviteOnly(unittest.TestCase):
    IN_THE_FUTURE = (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S')
    IN_THE_PAST = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S')

    def test_no_data(self):
        assertIsVerified(self, events_are_invite_only_iff_not_university_wide([]))

    def test_non_career_center_events(self):
        event_data = [
            {
                EventFields.ID: "4324725",
                EventFields.NAME: "McKinsey Virtual Session",
                EventFields.CAREER_CENTER: None,
                EventFields.IS_INVITE_ONLY: 'No',
                EventFields.START_DATE_TIME: self.IN_THE_FUTURE
            },
            {
                EventFields.ID: "4625224",
                EventFields.NAME: "CIA Recruitment Event",
                EventFields.CAREER_CENTER: None,
                EventFields.IS_INVITE_ONLY: 'Yes',
                EventFields.START_DATE_TIME: self.IN_THE_FUTURE
            },
        ]
        assertIsVerified(self, events_are_invite_only_iff_not_university_wide(event_data))

    def test_university_wide_events(self):
        event_data = [
            {
                EventFields.ID: "6336475",
                EventFields.NAME: "University-Wide: Consulting Alumni Panel",
                EventFields.CAREER_CENTER: CareerCenters.HOMEWOOD,
                EventFields.IS_INVITE_ONLY: 'No',
                EventFields.START_DATE_TIME: self.IN_THE_FUTURE
            },
            {
                EventFields.ID: "9892820",
                EventFields.NAME: "University-Wide: Resume Workshop",
                EventFields.CAREER_CENTER: CareerCenters.CAREY,
                EventFields.IS_INVITE_ONLY: 'No',
                EventFields.START_DATE_TIME: self.IN_THE_FUTURE
            },
            {
                EventFields.ID: "8290282",
                EventFields.NAME: "University-Wide: Resume Workshop",
                EventFields.CAREER_CENTER: CareerCenters.PDCO,
                EventFields.IS_INVITE_ONLY: 'Yes',
                EventFields.START_DATE_TIME: self.IN_THE_FUTURE
            },
        ]
        assertContainsErrorIDs(self, ['8290282'], events_are_invite_only_iff_not_university_wide(event_data))

    def test_career_center_events(self):
        event_data = [
            {
                EventFields.ID: "38305945",
                EventFields.NAME: "Homewood: Consulting Alumni Panel",
                EventFields.CAREER_CENTER: CareerCenters.HOMEWOOD,
                EventFields.IS_INVITE_ONLY: 'No',
                EventFields.START_DATE_TIME: self.IN_THE_FUTURE
            },
            {
                EventFields.ID: "150925098",
                EventFields.NAME: "Carey: Resume Workshop",
                EventFields.CAREER_CENTER: CareerCenters.CAREY,
                EventFields.IS_INVITE_ONLY: 'No',
                EventFields.START_DATE_TIME: self.IN_THE_FUTURE
            },
            {
                EventFields.ID: "95739393",
                EventFields.NAME: "PDCO: Resume Workshop",
                EventFields.CAREER_CENTER: CareerCenters.PDCO,
                EventFields.IS_INVITE_ONLY: 'Yes',
                EventFields.START_DATE_TIME: self.IN_THE_FUTURE
            },
        ]
        assertContainsErrorIDs(self, ['38305945', '150925098'], events_are_invite_only_iff_not_university_wide(event_data))

    def test_cancelled_prefix_doesnt_interefere(self):
        event_data = [
            {
                EventFields.ID: "353242",
                EventFields.NAME: "CANCELLED: University-Wide: 2019 JumpStart STEM Diversity Forum",
                EventFields.CAREER_CENTER: CareerCenters.HOMEWOOD,
                EventFields.IS_INVITE_ONLY: 'Yes',
                EventFields.START_DATE_TIME: self.IN_THE_FUTURE
            },
            {
                EventFields.ID: "8563254",
                EventFields.NAME: "CANCELLED: Carey: Drop-in Mondays HE September 9th Afternoon",
                EventFields.CAREER_CENTER: CareerCenters.CAREY,
                EventFields.IS_INVITE_ONLY: 'Yes',
                EventFields.START_DATE_TIME: self.IN_THE_FUTURE
            },
            {
                EventFields.ID: "902820",
                EventFields.NAME: "CANCELLED: University-Wide: Career Clinic: Job Negotiation",
                EventFields.CAREER_CENTER: CareerCenters.PDCO,
                EventFields.IS_INVITE_ONLY: 'No',
                EventFields.START_DATE_TIME: self.IN_THE_FUTURE
            },
            {
                EventFields.ID: "2635346",
                EventFields.NAME: "CANCELLED: SAIS DC: SAISLeads Retreat",
                EventFields.CAREER_CENTER: CareerCenters.SAIS,
                EventFields.IS_INVITE_ONLY: 'No',
                EventFields.START_DATE_TIME: self.IN_THE_FUTURE
            },
        ]
        assertContainsErrorIDs(self, ['353242', '2635346'], events_are_invite_only_iff_not_university_wide(event_data))

    def test_ignores_past_events(self):
        event_data = [
            {
                EventFields.ID: "38305945",
                EventFields.NAME: "Homewood: Consulting Alumni Panel",
                EventFields.CAREER_CENTER: CareerCenters.HOMEWOOD,
                EventFields.IS_INVITE_ONLY: 'No',
                EventFields.START_DATE_TIME: self.IN_THE_PAST
            },
            {
                EventFields.ID: "150925098",
                EventFields.NAME: "Carey: Resume Workshop",
                EventFields.CAREER_CENTER: CareerCenters.CAREY,
                EventFields.IS_INVITE_ONLY: 'No',
                EventFields.START_DATE_TIME: self.IN_THE_PAST
            },
        ]
        assertIsVerified(self, events_are_invite_only_iff_not_university_wide(event_data))

    def test_invite_only_error_message(self):
        event = {
            EventFields.ID: "353242",
            EventFields.NAME: "A Fun Event",
        }
        should_expected = 'Event 353242 (A Fun Event) should be invite-only'
        shouldnt_expected = 'Event 353242 (A Fun Event) should not be invite-only'
        self.assertEqual(should_expected, _build_invite_only_error_message(event, True))
        self.assertEqual(shouldnt_expected, _build_invite_only_error_message(event, False))


class TestAdvertisementsAreLabeledCorrectly(unittest.TestCase):

    def test_rule_flags_homewood_office_hours_events(self):
        event_data = [
            {
                EventFields.ID: "288569",
                EventFields.NAME: "Homewood: WSE Office Hours",
                EventFields.CAREER_CENTER: CareerCenters.HOMEWOOD,
                EventFields.EVENT_TYPE: 'Other',
                EventFields.LABELS_LIST: ''
            },
            {
                EventFields.ID: "331585",
                EventFields.NAME: "Homewood: office hours with Tessa",
                EventFields.CAREER_CENTER: CareerCenters.HOMEWOOD,
                EventFields.EVENT_TYPE: 'Other',
                EventFields.LABELS_LIST: 'hwd: stem'
            },
            {
                EventFields.ID: "333931",
                EventFields.NAME: "Homewood: Job Negotiation Workshop",
                EventFields.CAREER_CENTER: CareerCenters.HOMEWOOD,
                EventFields.EVENT_TYPE: 'Workshop',
                EventFields.LABELS_LIST: ''
            },
        ]
        assertContainsErrorIDs(self, ['288569', '331585'], advertisement_events_are_labeled(event_data))

    def test_with_multiple_labels(self):
        event_data = [
            {
                EventFields.ID: "331585",
                EventFields.NAME: "Homewood: office Hours with Tessa",
                EventFields.CAREER_CENTER: CareerCenters.HOMEWOOD,
                EventFields.EVENT_TYPE: 'Other',
                EventFields.LABELS_LIST: 'hwd: stem, shared: advertisement, hwd: virtual'
            }
        ]
        assertIsVerified(self, advertisement_events_are_labeled(event_data))

    def test_rule_flags_events_with_wrong_event_type(self):
        event_data = [
            {
                EventFields.ID: "288569",
                EventFields.NAME: "Homewood: WSE Office Hours",
                EventFields.CAREER_CENTER: CareerCenters.HOMEWOOD,
                EventFields.EVENT_TYPE: 'Group Appointment',
                EventFields.LABELS_LIST: ''
            },
            {
                EventFields.ID: "331585",
                EventFields.NAME: "Homewood: office hours with Tessa",
                EventFields.CAREER_CENTER: CareerCenters.HOMEWOOD,
                EventFields.EVENT_TYPE: 'Workshop',
                EventFields.LABELS_LIST: 'shared: advertisement'
            },
        ]
        assertContainsErrorIDs(self, ['288569', '331585'], advertisement_events_are_labeled(event_data))

    def test_doesnt_flag_non_homewood_office_hours(self):
        event_data = [
            {
                EventFields.ID: "331585",
                EventFields.NAME: "PDCO: Office Hours",
                EventFields.CAREER_CENTER: CareerCenters.PDCO,
                EventFields.EVENT_TYPE: 'Workshop',
                EventFields.LABELS_LIST: ''
            },
        ]
        assertIsVerified(self, advertisement_events_are_labeled(event_data))

    def test_ad_error_message(self):
        event = {
            EventFields.ID: "288569",
            EventFields.NAME: "Homewood: WSE Office Hours",
            EventFields.CAREER_CENTER: CareerCenters.HOMEWOOD,
            EventFields.EVENT_TYPE: 'Group Appointment',
            EventFields.LABELS_LIST: ''
        }
        expected = 'Event 288569 (Homewood: WSE Office Hours) should be labeled "shared: advertisement" and have event type "Other"'
        self.assertEqual(expected, _build_ad_error_message(event))


class TestPastEventsDoNotHaveVirtualEventType(unittest.TestCase):
    IN_THE_FUTURE = (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S')
    IN_THE_PAST = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S')

    def test_events_without_the_virtual_event_type_are_ok(self):
        events = [{
            EventFields.ID: "666484",
            EventFields.NAME: '',
            EventFields.CAREER_CENTER: CareerCenters.HOMEWOOD,
            EventFields.EVENT_TYPE: 'Info Session',
            EventFields.START_DATE_TIME: self.IN_THE_PAST
        }]
        assertIsVerified(self, past_events_do_not_have_virtual_event_type(events))

    def test_future_events_are_ok(self):
        events = [{
            EventFields.ID: "119437",
            EventFields.NAME: '',
            EventFields.CAREER_CENTER: CareerCenters.HOMEWOOD,
            EventFields.EVENT_TYPE: 'Virtual Session',
            EventFields.START_DATE_TIME: self.IN_THE_FUTURE
        }]
        assertIsVerified(self, past_events_do_not_have_virtual_event_type(events))

    def test_past_external_events_are_ok(self):
        events = [{
            EventFields.ID: "119437",
            EventFields.NAME: '',
            EventFields.CAREER_CENTER: None,
            EventFields.EVENT_TYPE: 'Virtual Session',
            EventFields.START_DATE_TIME: self.IN_THE_PAST
        }]
        assertIsVerified(self, past_events_do_not_have_virtual_event_type(events))

    def test_past_jhu_events_with_virtual_event_type_are_not_ok(self):
        events = [{
            EventFields.ID: '354987',
            EventFields.NAME: 'Homewood: Deloitte Info Session',
            EventFields.CAREER_CENTER: CareerCenters.HOMEWOOD,
            EventFields.EVENT_TYPE: 'Virtual Session',
            EventFields.START_DATE_TIME: self.IN_THE_PAST
        }]
        result = past_events_do_not_have_virtual_event_type(events)
        assertContainsErrorIDs(self, ['354987'], result)
        self.assertEqual('Event 354987 (Homewood: Deloitte Info Session) should not have the "Virtual Session" event type', result.errors[0]['error_msg'])
