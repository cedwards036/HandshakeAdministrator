from typing import List

from autohandshake import (HandshakeBrowser, MajorSettingsPage, AccessRequestPage,
                           RequestStatus, LabelSettingsPage, AppointmentTypesListPage,
                           StaffPage, InsightsPage, FileType)

from src.utils import to_csv, get_datestamped_filename, \
    create_filepath_in_download_dir, config, read_and_delete_json

DESTINATION_FILEPATH = r'S:\Reporting & Data\One-Off Reports\rejected_students.csv'


def download_rejected_student_requests(browser: HandshakeBrowser) -> str:
    output_filepath = _create_csv_filepath('rejected_students')
    request_page = AccessRequestPage(browser)
    rejects = request_page.get_request_data(RequestStatus.REJECTED)
    to_csv(rejects, output_filepath)
    return output_filepath


def download_pending_student_requests(browser: HandshakeBrowser) -> str:
    output_filepath = _create_csv_filepath('pending_students')
    request_page = AccessRequestPage(browser)
    pending = request_page.get_request_data(RequestStatus.WAITING)
    to_csv(pending, output_filepath)
    return output_filepath


def download_label_settings_data(browser: HandshakeBrowser) -> tuple:
    def _write_simple_file(label_data: List[dict]):
        csv_rows = [_get_simple_row(row) for row in label_data]
        filepath = _create_csv_filepath('simple_label_settings')
        to_csv(csv_rows, filepath)
        return filepath

    def _write_detailed_file(label_data: List[dict]):
        csv_rows = []
        for row in label_data:
            csv_rows = _add_complex_row_to_list(row, csv_rows)
        filepath = _create_csv_filepath('detailed_label_settings')
        to_csv(csv_rows, filepath)
        return filepath

    def _get_simple_row(row: dict) -> dict:
        return {
            'label_name': row['label_name'],
            'usage_count': sum(row['usage_counts'].values()),
            'used_for': row['used_for'],
            'created_by_first_name': row['created_by_first_name'],
            'created_by_last_name': row['created_by_last_name'],
            'label_type': row['label_type']
        }

    def _add_complex_row_to_list(row: dict, output_data: List[dict]) -> List[dict]:
        for used_for_type, count in row['usage_counts'].items():
            output_data.append({
                'label_name': row['label_name'],
                'usage_count': count,
                'used_for': used_for_type,
                'created_by_first_name': row['created_by_first_name'],
                'created_by_last_name': row['created_by_last_name'],
                'label_type': row['label_type']
            })
        return output_data

    label_page = LabelSettingsPage(browser)
    label_data = label_page.get_label_data()
    return (_write_simple_file(label_data), _write_detailed_file(label_data))


def download_major_mapping(browser: HandshakeBrowser) -> str:
    def _restructure_major_mapping_data(mapping_data: List[dict]) -> List[dict]:
        mapping_rows = []
        for mapping in mapping_data:
            for group in mapping['groups']:
                mapping_rows.append({'major': mapping['major'],
                                     'group': group})
        return mapping_rows

    output_filepath = _create_csv_filepath('major_mapping')
    major_page = MajorSettingsPage(browser)
    mappings = major_page.get_major_mapping()
    to_csv(_restructure_major_mapping_data(mappings), output_filepath)
    return output_filepath


def download_appointment_type_settings(browser: HandshakeBrowser) -> str:
    output_filepath = _create_csv_filepath('appt_type_settings')
    types_page = AppointmentTypesListPage(browser)
    type_settings = types_page.get_type_settings()
    to_csv(type_settings, output_filepath)
    return output_filepath


def download_staff(browser: HandshakeBrowser) -> str:
    def _get_staff_insights_data(browser: HandshakeBrowser):
        STAFF_INSIGHTS_URL = 'https://app.joinhandshake.com/analytics/explore_embed?insights_page=ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vY2FyZWVyX3NlcnZpY2Vfc3RhZmZzP3FpZD1Bc2lZUEJpWVlaczNUYTVRMGdmODNsJmVtYmVkX2RvbWFpbj1odHRwczolMkYlMkZhcHAuam9pbmhhbmRzaGFrZS5jb20mdG9nZ2xlPWZpbA=='
        insights_page = InsightsPage(STAFF_INSIGHTS_URL, browser)
        filepath = insights_page.download_file(config['download_dir'], file_type=FileType.JSON)
        return read_and_delete_json(filepath)

    output_filepath = _create_csv_filepath('handshake_staff')
    staff_page = StaffPage(browser)
    staff_names = staff_page.get_staff_names()
    insights_data = _get_staff_insights_data(browser)
    to_csv(merge_staff_data(staff_names, insights_data), output_filepath)
    return output_filepath


def merge_staff_data(names: List[str], insights_data: List[dict]):
    def _full_name(insights_row: dict):
        return f"{insights_row['Career Service Staffs First Name'].strip()} {insights_row['Career Service Staffs Last Name'].strip()}"

    names_set = set(names)
    return [row for row in insights_data if _full_name(row) in names_set]


def _create_csv_filepath(filename: str):
    return create_filepath_in_download_dir(f'{get_datestamped_filename(filename)}.csv')
