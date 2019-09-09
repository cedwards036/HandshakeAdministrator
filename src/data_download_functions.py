from typing import List

from autohandshake import (HandshakeBrowser, MajorSettingsPage, AccessRequestPage,
                           RequestStatus, LabelSettingsPage, AppointmentTypesListPage)

from src.utils import to_csv, get_datestamped_filename, create_filepath_in_download_dir

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


def _create_csv_filepath(filename: str):
    return create_filepath_in_download_dir(f'{get_datestamped_filename(filename)}.csv')
