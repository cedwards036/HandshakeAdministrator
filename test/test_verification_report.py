import unittest

from src.verification_report import (VerificationResult, generate_report,
                                     format_report, verify_rules)


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
        }, generate_report([VerificationResult('All dogs should be cute', True)]))

    def test_report_with_verified_and_unverified_results(self):
        self.assertEqual({
            'verified': ['All dogs should be cute'],
            'broken': {'All numbers should be even': ['3 is not even', '5 is not even']}
        }, generate_report([VerificationResult('All dogs should be cute', True),
                            VerificationResult('All numbers should be even', False,
                                               ['3 is not even', '5 is not even'])]))

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


class TestVerifyRules(unittest.TestCase):

    def test_verify_no_rules(self):
        self.assertEqual([], verify_rules())
        self.assertEqual([], verify_rules([]))

    def test_verify_one_rule(self):
        self.assertEqual([{'field1': 193, 'field2': 4}], verify_rules([
            (lambda x: {'field1': x['f1'], 'field2': x['f2']}, {'f1': 193, 'f2': 4})
        ]))

    def test_verify_multiple_rules(self):
        data1 = None

        def func1(data):
            return VerificationResult('The sky should be blue', True)

        data2 = [2, 4, 5, 6, 7, 8, 10]

        def func2(data):
            result = VerificationResult('All numbers should be even', True)
            for n in data:
                if n % 2 != 0:
                    result.add_error(f'{n} is odd')
                    result.is_verified = False
            return result

        expected = [
            VerificationResult('The sky should be blue', True),
            VerificationResult('All numbers should be even', False,
                               ['5 is odd', '7 is odd'])
        ]

        self.assertEqual(expected, verify_rules([
            (func1, data1),
            (func2, data2)
        ]))
