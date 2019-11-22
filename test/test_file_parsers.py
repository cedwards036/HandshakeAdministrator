import unittest

from src.job_label_parser import parse_job_file


class TestJobFileParser(unittest.TestCase):
    TEST_FILEPATH = 'test_job_file.csv'

    def test_parser(self):
        expected = [
            {
                'job_id': '105127',
                'job_url': 'https://jhu.joinhandshake.com/jobs/105127',
                'qualification_labels': ['qual label 1', 'qual label 3']
            },
            {
                'job_id': '200919',
                'job_url': 'https://jhu.joinhandshake.com/jobs/200919',
                'qualification_labels': ['qual label 1', 'qual label 2']
            },
            {
                'job_id': '201957',
                'job_url': 'https://jhu.joinhandshake.com/jobs/201957',
                'qualification_labels': ['qual label 4']
            }
        ]
        self.assertEqual(expected, parse_job_file(self.TEST_FILEPATH))
