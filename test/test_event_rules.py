import unittest

from src.constants import CareerCenters
from src.event_rules import jhu_owned_events_are_prefixed_correctly
from src.verification_report import VerificationResult


class TestEventsArePrefixedCorrectly(unittest.TestCase):
    RULE_NAME = 'Events are prefixed correctly if they are owned by a career center'

    def test_with_no_data(self):
        self.assertEqual(VerificationResult(self.RULE_NAME, True),
                         jhu_owned_events_are_prefixed_correctly([]))

    def test_with_non_career_center_event(self):
        event_data = [
            {
                'events.id': "4324725",
                'events.name': "McKinsey Virtual Session",
                'career_center_on_events.name': None
            },
        ]
        self.assertEqual(VerificationResult(self.RULE_NAME, True),
                         jhu_owned_events_are_prefixed_correctly(event_data))

    def test_university_wide_is_valid(self):
        event_data = [
            {
                'events.id': "353242",
                'events.name': "University-Wide: 2019 JumpStart STEM Diversity Forum",
                'career_center_on_events.name': CareerCenters.HOMEWOOD
            },
            {
                'events.id': "8563254",
                'events.name': "University-Wide: Drop-in Mondays HE September 9th Afternoon",
                'career_center_on_events.name': CareerCenters.CAREY
            },
            {
                'events.id': "902820",
                'events.name': "University-Wide: Career Clinic: Job Negotiation",
                'career_center_on_events.name': CareerCenters.PDCO
            },
        ]
        self.assertEqual(VerificationResult(self.RULE_NAME, True),
                         jhu_owned_events_are_prefixed_correctly(event_data))

    def test_cancelled_prefix_is_valid(self):
        event_data = [
            {
                'events.id': "353242",
                'events.name': "CANCELLED: University-Wide: 2019 JumpStart STEM Diversity Forum",
                'career_center_on_events.name': CareerCenters.HOMEWOOD
            },
            {
                'events.id': "8563254",
                'events.name': "CANCELLED: Carey: Drop-in Mondays HE September 9th Afternoon",
                'career_center_on_events.name': CareerCenters.CAREY
            },
            {
                'events.id': "902820",
                'events.name': "CANCELLED: Career Clinic: Job Negotiation",
                'career_center_on_events.name': CareerCenters.PDCO
            },
            {
                'events.id': "2635346",
                'events.name': "CANCELLED: SAISLeads Retreat",
                'career_center_on_events.name': CareerCenters.SAIS
            },
        ]
        expected_errors = [
            'Event 902820 (CANCELLED: Career Clinic: Job Negotiation) should have prefix "CANCELLED: PDCO:"',
            'Event 2635346 (CANCELLED: SAISLeads Retreat) should have prefix "CANCELLED: SAIS DC:", "CANCELLED: SAIS Europe:", or "CANCELLED: HNC:"'
        ]
        self.assertEqual(VerificationResult(self.RULE_NAME, False, expected_errors),
                         jhu_owned_events_are_prefixed_correctly(event_data))

    def test_with_one_of_each_bad_event(self):
        event_data = [
            {
                'events.id': "353242",
                'events.name': "Homewoo: 2019 JumpStart STEM Diversity Forum",
                'career_center_on_events.name': CareerCenters.HOMEWOOD
            },
            {
                'events.id': "8563254",
                'events.name': "Cary: Drop-in Mondays HE September 9th Afternoon",
                'career_center_on_events.name': CareerCenters.CAREY
            },
            {
                'events.id': "902820",
                'events.name': "Univ. Wide: Career Clinic: Job Negotiation",
                'career_center_on_events.name': CareerCenters.PDCO
            },
            {
                'events.id': "2635346",
                'events.name': "SAIS Europe SAISLeads Retreat",
                'career_center_on_events.name': CareerCenters.SAIS
            },
            {
                'events.id': '526433',
                'events.name': 'N: How to Find Your First Nursing Job',
                'career_center_on_events.name': CareerCenters.NURSING
            },
            {
                'events.id': '328092',
                'events.name': 'Strategies for Effective Professional Communication webinar',
                'career_center_on_events.name': CareerCenters.AAP
            },
            {
                'events.id': '940935',
                'events.name': 'Homewood: LAUNCH @ Lunch',
                'career_center_on_events.name': CareerCenters.PEABODY
            },
            {
                'events.id': '5839252',
                'events.name': 'BSP: Student Activities Fair',
                'career_center_on_events.name': CareerCenters.BSPH
            }
        ]
        expected_errors = [
            'Event 353242 (Homewoo: 2019 JumpStart STEM Diversity Forum) should have prefix "Homewood:"',
            'Event 8563254 (Cary: Drop-in Mondays HE September 9th Afternoon) should have prefix "Carey:"',
            'Event 902820 (Univ. Wide: Career Clinic: Job Negotiation) should have prefix "PDCO:"',
            'Event 2635346 (SAIS Europe SAISLeads Retreat) should have prefix "SAIS DC:", "SAIS Europe:", or "HNC:"',
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
                'events.id': "288569",
                'events.name': "Homewood: 2019 JumpStart STEM Diversity Forum",
                'career_center_on_events.name': CareerCenters.HOMEWOOD
            },
            {
                'events.id': "331585",
                'events.name': "Carey: Drop-in Mondays HE September 9th Afternoon",
                'career_center_on_events.name': CareerCenters.CAREY
            },
            {
                'events.id': "333931",
                'events.name': "PDCO: Career Clinic: Job Negotiation",
                'career_center_on_events.name': CareerCenters.PDCO
            },
            {
                'events.id': "317809",
                'events.name': "SAIS DC: SAISLeads Retreat",
                'career_center_on_events.name': CareerCenters.SAIS
            },
            {
                'events.id': "288213",
                'events.name': "SAIS Europe: SAISLeads Retreat",
                'career_center_on_events.name': CareerCenters.SAIS
            },
            {
                'events.id': '239094',
                'events.name': 'HNC: Group Coaching Appointment 3',
                'career_center_on_events.name': CareerCenters.SAIS
            },
            {
                'events.id': '249995',
                'events.name': 'Nursing: How to Find Your First Nursing Job',
                'career_center_on_events.name': CareerCenters.NURSING
            },
            {
                'events.id': '217543',
                'events.name': 'AAP: Strategies for Effective Professional Communication webinar',
                'career_center_on_events.name': CareerCenters.AAP
            },
            {
                'events.id': '264029',
                'events.name': 'Peabody: LAUNCH @ Lunch',
                'career_center_on_events.name': CareerCenters.PEABODY
            },
            {
                'events.id': '198116',
                'events.name': 'BSPH: Student Activities Fair',
                'career_center_on_events.name': CareerCenters.BSPH
            }
        ]
        self.assertEqual(VerificationResult(self.RULE_NAME, True),
                         jhu_owned_events_are_prefixed_correctly(event_data))

    def test_with_all_event_types(self):
        event_data = [
            {
                'events.id': "288569",
                'events.name': "Homewood: 2019 JumpStart STEM Diversity Forum",
                'career_center_on_events.name': CareerCenters.HOMEWOOD
            },
            {
                'events.id': "331585",
                'events.name': "Carey: Drop-in Mondays HE September 9th Afternoon",
                'career_center_on_events.name': CareerCenters.CAREY
            },
            {
                'events.id': "333931",
                'events.name': "PDCO: Career Clinic: Job Negotiation",
                'career_center_on_events.name': CareerCenters.PDCO
            },
            {
                'events.id': '526433',
                'events.name': 'N: How to Find Your First Nursing Job',
                'career_center_on_events.name': CareerCenters.NURSING
            },
            {
                'events.id': '328092',
                'events.name': 'Strategies for Effective Professional Communication webinar',
                'career_center_on_events.name': CareerCenters.AAP
            },
            {
                'events.id': '940935',
                'events.name': 'Homewood: LAUNCH @ Lunch',
                'career_center_on_events.name': CareerCenters.PEABODY
            },
            {
                'events.id': "83257925",
                'events.name': "Deloitte Virtual Session",
                'career_center_on_events.name': None
            },
            {
                'events.id': "4324725",
                'events.name': "McKinsey Virtual Session",
                'career_center_on_events.name': None
            },
            {
                'events.id': "12980293",
                'events.name': "Google On-Site",
                'career_center_on_events.name': None
            },
        ]
        expected_errors = [
            'Event 526433 (N: How to Find Your First Nursing Job) should have prefix "Nursing:"',
            'Event 328092 (Strategies for Effective Professional Communication webinar) should have prefix "AAP:"',
            'Event 940935 (Homewood: LAUNCH @ Lunch) should have prefix "Peabody:"'
        ]
        self.assertEqual(VerificationResult(self.RULE_NAME, False, expected_errors),
                         jhu_owned_events_are_prefixed_correctly(event_data))
