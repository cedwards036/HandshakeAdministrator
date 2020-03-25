import unittest

from src.data_download_functions import merge_staff_data


class TestStaffDataMerge(unittest.TestCase):

    def test(self):
        names = ['John Smith', 'Elle Gonzales - (Finance)']
        insights_data = [
            {
                'Career Service Staffs First Name': 'John',
                'Career Service Staffs Last Name': 'Smith',
                'field': 'value'
            },
            {
                'Career Service Staffs First Name': ' Elle ',
                'Career Service Staffs Last Name': ' Gonzales - (Finance) ',
                'field': 'other value'
            },
            {
                'Career Service Staffs First Name': 'Archived',
                'Career Service Staffs Last Name': 'Staff',
                'field': 'a third value'
            }
        ]
        expected = [
            {
                'Career Service Staffs First Name': 'John',
                'Career Service Staffs Last Name': 'Smith',
                'field': 'value'
            },
            {
                'Career Service Staffs First Name': ' Elle ',
                'Career Service Staffs Last Name': ' Gonzales - (Finance) ',
                'field': 'other value'
            },
        ]
        self.assertEqual(expected, merge_staff_data(names, insights_data))
