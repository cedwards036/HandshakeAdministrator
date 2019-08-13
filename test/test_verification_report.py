import unittest
from src.verification_report import generate_report, format_report


class TestVerificationReport(unittest.TestCase):

    def test_report_with_no_results(self):
        self.assertEqual({
            'verified': [],
            'broken': {}
        }, generate_report([]))

    def test_report_with_one_verified_result(self):
        self.assertEqual({
            'verified': ['All dogs should be cute'],
            'broken': {}
        }, generate_report([{'is_verified': True, 'rule': 'All dogs should be cute'}]))

    def test_report_with_verified_and_unverified_results(self):
        self.assertEqual({
            'verified': ['All dogs should be cute'],
            'broken': {'All numbers should be even': ['3 is not even', '5 is not even']}
        }, generate_report([{'is_verified': True, 'rule': 'All dogs should be cute'},
                            {'is_verified': False, 'rule': 'All numbers should be even',
                             'errors': ['3 is not even', '5 is not even']}]))

    def test_format_report_with_no_results(self):
        test_report = {
            'verified': [],
            'broken': []
        }
        expected = ('================== Verification Report ===================\n'
                    '\n'
                    '================== 0 verified, 0 broken ==================')
        self.assertEqual(expected, format_report(test_report))

    def test_format_report_with_one_verified(self):
        test_report = {
            'verified': ['All dogs should be cute'],
            'broken': []
        }
        expected = ('================== Verification Report ===================\n'
                    '\n'
                    'Rules verified:\n'
                    '\n'
                    '    All dogs should be cute\n'
                    '\n'
                    '================== 1 verified, 0 broken ==================')
        self.assertEqual(expected, format_report(test_report))

    def test_format_report_with_one_broken(self):
        test_report = {
            'verified': [],
            'broken': {'All numbers should be even': ['3 is not even', '5 is not even']}
        }
        expected = ('================== Verification Report ===================\n'
                    '\n'
                    'Rules broken:\n'
                    '\n'
                    '    All numbers should be even\n'
                    '        3 is not even\n'
                    '        5 is not even\n'
                    '\n'
                    '================== 0 verified, 1 broken ==================')
        self.assertEqual(expected, format_report(test_report))

    def test_format_report_with_mutliple_of_each(self):
        test_report = {
            'verified': ['All dogs should be good', 'All cats should be ok I guess'],
            'broken': {
                'All numbers should be even': [
                    '3 is not even',
                    '5 is not even'],
                'People should eat no more than four hot dogs at a time': [
                    'Jimmy ate five hot dogs',
                    'Sarah ate thirty hot dogs',
                    'Scout ate two hundred hot dogs'
                ]}
        }
        expected = ('================== Verification Report ===================\n'
                    '\n'
                    'Rules verified:\n'
                    '\n'
                    '    All dogs should be good\n'
                    '    All cats should be ok I guess\n'
                    '\n'
                    'Rules broken:\n'
                    '\n'
                    '    All numbers should be even\n'
                    '        3 is not even\n'
                    '        5 is not even\n'
                    '    People should eat no more than four hot dogs at a time\n'
                    '        Jimmy ate five hot dogs\n'
                    '        Sarah ate thirty hot dogs\n'
                    '        Scout ate two hundred hot dogs\n'
                    '\n'
                    '================== 2 verified, 2 broken ==================')
        self.assertEqual(expected, format_report(test_report))
