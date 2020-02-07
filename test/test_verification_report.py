import unittest

from src.rule_verification import VerificationResult
from src.verification_report import VerificationReport, _verify_rules


class TestVerificationResult(unittest.TestCase):

    def test_cannot_add_a_null_error(self):
        result = VerificationResult('All dogs should be cute')
        result.add_error(None)
        self.assertEqual([], result.errors)
        self.assertTrue(result.is_verified)

    def test_adding_error_sets_is_verified_to_false(self):
        result = VerificationResult('All dogs should be cute')
        result.add_error({'error_msg': 'this one dog is not cute'})
        self.assertFalse(result.is_verified)


class TestVerificationReport(unittest.TestCase):

    def test_report_with_no_results(self):
        self.assertEqual({
            'verified': [],
            'broken': {}
        }, VerificationReport([]).as_dict())

    def test_report_with_one_verified_result(self):
        self.assertEqual({
            'verified': ['All dogs should be cute'],
            'broken': {}
        }, VerificationReport([VerificationResult('All dogs should be cute')]).as_dict())

    def test_report_with_verified_and_unverified_results(self):
        self.assertEqual({
            'verified': ['All dogs should be cute'],
            'broken': {'All numbers should be even': ['3 is not even', '5 is not even']}
        }, VerificationReport([VerificationResult('All dogs should be cute'),
                               VerificationResult('All numbers should be even',
                                                  [{'error_msg': '3 is not even'}, {'error_msg': '5 is not even'}])]).as_dict())

    def test_verification_report_equality(self):
        no_results = VerificationReport([])
        one_result = VerificationReport([VerificationResult('All dogs should be cute')])
        three_results = VerificationReport([
            VerificationResult('All dogs should be good'),
            VerificationResult('All cats should be ok I guess'),
            VerificationResult('All numbers should be even', [
                {'error_msg': '3 is not even'},
                {'error_msg': '5 is not even'}
            ])])

        self.assertEqual(VerificationReport([]), no_results)
        self.assertEqual(VerificationReport([VerificationResult('All dogs should be cute')]),
                         one_result)
        self.assertNotEqual(VerificationReport([VerificationResult('All cats should be cute')]), one_result)
        self.assertEqual(VerificationReport([
            VerificationResult('All dogs should be good'),
            VerificationResult('All cats should be ok I guess'),
            VerificationResult('All numbers should be even', [
                {'error_msg': '3 is not even'},
                {'error_msg': '5 is not even'}
            ])]), three_results)

    def test_report_str_with_no_results(self):
        test_report = VerificationReport([])
        expected = ('================== Verification Report ===================\n'
                    '\n'
                    '================== 0 verified, 0 broken ==================')
        self.assertEqual(expected, str(test_report))

    def test_report_str_with_one_verified(self):
        test_report = VerificationReport([VerificationResult('All dogs should be cute')])
        expected = ('================== Verification Report ===================\n'
                    '\n'
                    'Rules verified:\n'
                    '\n'
                    '    All dogs should be cute\n'
                    '\n'
                    '================== 1 verified, 0 broken ==================')
        self.assertEqual(expected, str(test_report))

    def test_report_str_with_one_broken(self):
        test_report = VerificationReport(
            [VerificationResult('All numbers should be even', [{'error_msg': '3 is not even'}, {'error_msg': '5 is not even'}])])
        expected = ('================== Verification Report ===================\n'
                    '\n'
                    'Rules broken:\n'
                    '\n'
                    '    All numbers should be even\n'
                    '        3 is not even\n'
                    '        5 is not even\n'
                    '\n'
                    '================== 0 verified, 1 broken ==================')
        self.assertEqual(expected, str(test_report))

    def test_report_str_with_mutliple_of_each(self):
        test_report = VerificationReport([
            VerificationResult('All dogs should be good'),
            VerificationResult('All cats should be ok I guess'),
            VerificationResult('All numbers should be even', [
                {'error_msg': '3 is not even'},
                {'error_msg': '5 is not even'}
            ]),
            VerificationResult('People should eat no more than four hot dogs at a time', [
                {'error_msg': 'Jimmy ate five hot dogs'},
                {'error_msg': 'Sarah ate thirty hot dogs'},
                {'error_msg': 'Scout ate two hundred hot dogs'}
            ])
        ])
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
        self.assertEqual(expected, str(test_report))


class TestVerifyRules(unittest.TestCase):

    def test_verify_no_rules(self):
        self.assertEqual([], _verify_rules())
        self.assertEqual([], _verify_rules([]))

    def test_verify_one_rule(self):
        self.assertEqual([{'field1': 193, 'field2': 4}], _verify_rules([
            (lambda x: {'field1': x['f1'], 'field2': x['f2']}, {'f1': 193, 'f2': 4})
        ]))

    def test_verify_multiple_rules(self):
        data1 = None

        def func1(data):
            return VerificationResult('The sky should be blue')

        data2 = [2, 4, 5, 6, 7, 8, 10]

        def func2(data):
            result = VerificationResult('All numbers should be even')
            for n in data:
                if n % 2 != 0:
                    result.add_error({'error_msg': f'{n} is odd'})
            return result

        expected = [
            VerificationResult('The sky should be blue'),
            VerificationResult('All numbers should be even',
                               [{'error_msg': '5 is odd'},
                                {'error_msg': '7 is odd'}])
        ]

        self.assertEqual(expected, _verify_rules([
            (func1, data1),
            (func2, data2)
        ]))
