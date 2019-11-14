import unittest

from src.constants import CareerCenters
from src.insights_fields import EventFields
from src.rule_verification import VerificationResult
from src.rules.event_rules import (
    jhu_owned_events_are_prefixed_correctly,
    events_are_invite_only_iff_not_university_wide,
    advertisement_events_are_labeled
)


class TestEventsArePrefixedCorrectly(unittest.TestCase):
    RULE_NAME = 'Events are prefixed correctly if they are owned by a career center'

    def test_with_no_data(self):
        self.assertEqual(VerificationResult(self.RULE_NAME, True),
                         jhu_owned_events_are_prefixed_correctly([]))

    def test_with_non_career_center_event(self):
        event_data = [
            {
                EventFields.ID: "4324725",
                EventFields.NAME: "McKinsey Virtual Session",
                EventFields.CAREER_CENTER: None
            },
        ]
        self.assertEqual(VerificationResult(self.RULE_NAME, True),
                         jhu_owned_events_are_prefixed_correctly(event_data))

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
        self.assertEqual(VerificationResult(self.RULE_NAME, True),
                         jhu_owned_events_are_prefixed_correctly(event_data))

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
        expected_errors = [
            'Event 5364354 (test- Drop-in Mondays HE September 9th Afternoon) should have prefix "PDCO:"',
            'Event 26895576 (TESTING Career Clinic: Job Negotiation) should have prefix "SAIS:", "SAIS DC:", "SAIS Europe:", or "HNC:"'
        ]
        self.assertEqual(VerificationResult(self.RULE_NAME, False, expected_errors),
                         jhu_owned_events_are_prefixed_correctly(event_data))

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
        expected_errors = [
            'Event 902820 (CANCELLED: Career Clinic: Job Negotiation) should have prefix "CANCELLED: PDCO:"',
            'Event 2635346 (CANCELLED: SAISLeads Retreat) should have prefix "CANCELLED: SAIS:", "CANCELLED: SAIS DC:", "CANCELLED: SAIS Europe:", or "CANCELLED: HNC:"'
        ]
        self.assertEqual(VerificationResult(self.RULE_NAME, False, expected_errors),
                         jhu_owned_events_are_prefixed_correctly(event_data))

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
        expected_errors = [
            'Event 902820 (CANCELED: PDCO: Career Clinic: Job Negotiation) should have prefix "CANCELLED: PDCO:"',
            'Event 2635346 (CAnCELEd: SAIS: SAISLeads Retreat) should have prefix "CANCELLED: SAIS:", "CANCELLED: SAIS DC:", "CANCELLED: SAIS Europe:", or "CANCELLED: HNC:"',
            'Event 3263343 (Cancelled: Peabody: Launch Event) should have prefix "CANCELLED: Peabody:"'
        ]
        self.assertEqual(VerificationResult(self.RULE_NAME, False, expected_errors),
                         jhu_owned_events_are_prefixed_correctly(event_data))

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
        expected_errors = [
            'Event 353242 (Homewoo: 2019 JumpStart STEM Diversity Forum) should have prefix "Homewood:"',
            'Event 8563254 (Cary: Drop-in Mondays HE September 9th Afternoon) should have prefix "Carey:"',
            'Event 902820 (Univ. Wide: Career Clinic: Job Negotiation) should have prefix "PDCO:"',
            'Event 2635346 (SAIS Europe SAISLeads Retreat) should have prefix "SAIS:", "SAIS DC:", "SAIS Europe:", or "HNC:"',
            'Event 526433 (N: How to Find Your First Nursing Job) should have prefix "Nursing:"',
            'Event 328092 (Strategies for Effective Professional Communication webinar) should have prefix "AAP:"',
            'Event 940935 (Homewood: LAUNCH @ Lunch) should have prefix "Peabody:"',
            'Event 5839252 (BSP: Student Activities Fair) should have prefix "BSPH:"'
        ]
        self.assertEqual(VerificationResult(self.RULE_NAME, False, expected_errors),
                         jhu_owned_events_are_prefixed_correctly(event_data))

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
        self.assertEqual(VerificationResult(self.RULE_NAME, True),
                         jhu_owned_events_are_prefixed_correctly(event_data))

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
        expected_errors = [
            'Event 526433 (N: How to Find Your First Nursing Job) should have prefix "Nursing:"',
            'Event 328092 (Strategies for Effective Professional Communication webinar) should have prefix "AAP:"',
            'Event 940935 (Homewood: LAUNCH @ Lunch) should have prefix "Peabody:"'
        ]
        self.assertEqual(VerificationResult(self.RULE_NAME, False, expected_errors),
                         jhu_owned_events_are_prefixed_correctly(event_data))


class TestEventsAreInviteOnly(unittest.TestCase):
    RULE_NAME = 'Events are invite-only if and only if they are not University-Wide or external'

    def test_no_data(self):
        self.assertEqual(VerificationResult(self.RULE_NAME, True),
                         events_are_invite_only_iff_not_university_wide([]))

    def test_non_career_center_events(self):
        event_data = [
            {
                EventFields.ID: "4324725",
                EventFields.NAME: "McKinsey Virtual Session",
                EventFields.CAREER_CENTER: None,
                EventFields.IS_INVITE_ONLY: 'No'
            },
            {
                EventFields.ID: "4625224",
                EventFields.NAME: "CIA Recruitment Event",
                EventFields.CAREER_CENTER: None,
                EventFields.IS_INVITE_ONLY: 'Yes'
            },
        ]
        self.assertEqual(VerificationResult(self.RULE_NAME, True),
                         events_are_invite_only_iff_not_university_wide(event_data))

    def test_university_wide_events(self):
        event_data = [
            {
                EventFields.ID: "6336475",
                EventFields.NAME: "University-Wide: Consulting Alumni Panel",
                EventFields.CAREER_CENTER: CareerCenters.HOMEWOOD,
                EventFields.IS_INVITE_ONLY: 'No'
            },
            {
                EventFields.ID: "9892820",
                EventFields.NAME: "University-Wide: Resume Workshop",
                EventFields.CAREER_CENTER: CareerCenters.CAREY,
                EventFields.IS_INVITE_ONLY: 'No'
            },
            {
                EventFields.ID: "8290282",
                EventFields.NAME: "University-Wide: Resume Workshop",
                EventFields.CAREER_CENTER: CareerCenters.PDCO,
                EventFields.IS_INVITE_ONLY: 'Yes'
            },
        ]
        expected_errors = ['Event 8290282 (University-Wide: Resume Workshop) should not be invite-only']
        self.assertEqual(VerificationResult(self.RULE_NAME, False, errors=expected_errors),
                         events_are_invite_only_iff_not_university_wide(event_data))

    def test_career_center_events(self):
        event_data = [
            {
                EventFields.ID: "38305945",
                EventFields.NAME: "Homewood: Consulting Alumni Panel",
                EventFields.CAREER_CENTER: CareerCenters.HOMEWOOD,
                EventFields.IS_INVITE_ONLY: 'No'
            },
            {
                EventFields.ID: "150925098",
                EventFields.NAME: "Carey: Resume Workshop",
                EventFields.CAREER_CENTER: CareerCenters.CAREY,
                EventFields.IS_INVITE_ONLY: 'No'
            },
            {
                EventFields.ID: "95739393",
                EventFields.NAME: "PDCO: Resume Workshop",
                EventFields.CAREER_CENTER: CareerCenters.PDCO,
                EventFields.IS_INVITE_ONLY: 'Yes'
            },
        ]
        expected_errors = ['Event 38305945 (Homewood: Consulting Alumni Panel) should be invite-only',
                           'Event 150925098 (Carey: Resume Workshop) should be invite-only']
        self.assertEqual(VerificationResult(self.RULE_NAME, False, errors=expected_errors),
                         events_are_invite_only_iff_not_university_wide(event_data))

    def test_cancelled_prefix_doesnt_interefere(self):
        event_data = [
            {
                EventFields.ID: "353242",
                EventFields.NAME: "CANCELLED: University-Wide: 2019 JumpStart STEM Diversity Forum",
                EventFields.CAREER_CENTER: CareerCenters.HOMEWOOD,
                EventFields.IS_INVITE_ONLY: 'Yes'
            },
            {
                EventFields.ID: "8563254",
                EventFields.NAME: "CANCELLED: Carey: Drop-in Mondays HE September 9th Afternoon",
                EventFields.CAREER_CENTER: CareerCenters.CAREY,
                EventFields.IS_INVITE_ONLY: 'Yes'
            },
            {
                EventFields.ID: "902820",
                EventFields.NAME: "CANCELLED: University-Wide: Career Clinic: Job Negotiation",
                EventFields.CAREER_CENTER: CareerCenters.PDCO,
                EventFields.IS_INVITE_ONLY: 'No'
            },
            {
                EventFields.ID: "2635346",
                EventFields.NAME: "CANCELLED: SAIS DC: SAISLeads Retreat",
                EventFields.CAREER_CENTER: CareerCenters.SAIS,
                EventFields.IS_INVITE_ONLY: 'No'
            },
        ]
        expected_errors = [
            'Event 353242 (CANCELLED: University-Wide: 2019 JumpStart STEM Diversity Forum) should not be invite-only',
            'Event 2635346 (CANCELLED: SAIS DC: SAISLeads Retreat) should be invite-only']
        self.assertEqual(VerificationResult(self.RULE_NAME, False, errors=expected_errors),
                         events_are_invite_only_iff_not_university_wide(event_data))


class TestAdvertisementsAreLabeledCorrectly(unittest.TestCase):
    RULE_NAME = '"Advertisement" events are labeled properly and have event type "Other"'

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
        expected_errors = [
            'Event 288569 (Homewood: WSE Office Hours) should be labeled "shared: advertisement"',
            'Event 331585 (Homewood: office hours with Tessa) should be labeled "shared: advertisement"'
        ]
        self.assertEqual(VerificationResult(self.RULE_NAME, False, expected_errors),
                         advertisement_events_are_labeled(event_data))

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
        self.assertEqual(VerificationResult(self.RULE_NAME, True),
                         advertisement_events_are_labeled(event_data))

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
        expected_errors = [
            'Event 288569 (Homewood: WSE Office Hours) should be labeled "shared: advertisement" and have event type "Other"',
            'Event 331585 (Homewood: office hours with Tessa) should have event type "Other"'
        ]
        self.assertEqual(VerificationResult(self.RULE_NAME, False, expected_errors),
                         advertisement_events_are_labeled(event_data))

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
        self.assertEqual(VerificationResult(self.RULE_NAME, True),
                         advertisement_events_are_labeled(event_data))
