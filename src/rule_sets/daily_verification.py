import os
from datetime import datetime
from typing import List

from autohandshake import HandshakeBrowser, InsightsPage, FileType

from src.rule_verification import VerificationResult
from src.rules.appointment_rules import (
    past_appointments_have_finalized_status,
    all_appointments_have_a_type
)
from src.rules.event_rules import (
    jhu_owned_events_are_prefixed_correctly,
    events_are_invite_only_iff_not_university_wide,
    advertisement_events_are_labeled
)
from src.utils import (write_to_file, BrowsingSession, create_filepath_in_download_dir,
                       get_datestamped_filename, read_and_delete_json, config)
from src.verification_report import verify_rules, create_error_csv, VerificationReport

EVENTS_INSIGHTS_LINK = 'https://app.joinhandshake.com/analytics/explore_embed?insights_page=ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vZXZlbnRzP3FpZD0wbU9oNkdmYklkRlN6enYweHpiempFJmVtYmVkX2RvbWFpbj1odHRwczolMkYlMkZhcHAuam9pbmhhbmRzaGFrZS5jb20mdG9nZ2xlPWZpbA=='
APPTS_INSIGHTS_LINK = 'https://app.joinhandshake.com/analytics/explore_embed?insights_page=ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vYXBwb2ludG1lbnRzP3FpZD0xYTJpcktJSlFhR0loNTl5eVJHTkhnJmVtYmVkX2RvbWFpbj1odHRwczolMkYlMkZhcHAuam9pbmhhbmRzaGFrZS5jb20mdG9nZ2xlPWZpbA=='

REPORT_FILEPATH = create_filepath_in_download_dir(f'{get_datestamped_filename("daily_rule_verification_results")}.txt')
APPT_STATUS_CSV_FILEPATH = create_filepath_in_download_dir(f'{get_datestamped_filename("appt_status_errors")}.csv')
OUTPUT_DIR = create_filepath_in_download_dir(f'{get_datestamped_filename("daily_rule_verification_results")}')


def daily_verification(browser: HandshakeBrowser) -> str:
    events = _get_event_data(browser)
    appts = _get_appointment_data(browser)
    results = verify_rules([
        (jhu_owned_events_are_prefixed_correctly, events),
        (events_are_invite_only_iff_not_university_wide, events),
        (advertisement_events_are_labeled, events),
        (all_appointments_have_a_type, appts),
        (past_appointments_have_finalized_status, appts)
    ])
    os.mkdir(OUTPUT_DIR)
    _write_error_csvs(results, OUTPUT_DIR)
    _write_summary_text_report(VerificationReport(results), os.path.join(OUTPUT_DIR, 'all_errors.txt'))
    return OUTPUT_DIR


def _get_event_data(browser: HandshakeBrowser) -> List[dict]:
    events_insights = InsightsPage(EVENTS_INSIGHTS_LINK, browser)
    events_insights.set_date_range_filter('Events', 'Start Date Date', datetime(2019, 7, 1).date(),
                                          datetime(2020, 7, 1).date())
    filepath = events_insights.download_file(config['download_dir'], file_type=FileType.JSON)
    return read_and_delete_json(filepath)


def _get_appointment_data(browser: HandshakeBrowser) -> List[dict]:
    appts_insights = InsightsPage(APPTS_INSIGHTS_LINK, browser)
    filepath = appts_insights.download_file(config['download_dir'], file_type=FileType.JSON)
    return read_and_delete_json(filepath)


def _write_summary_text_report(report: VerificationReport, filepath: str):
    write_to_file(str(report), filepath)


def _write_error_csvs(verification_results: List[VerificationResult], output_dir: str):
    for result in verification_results:
        if not result.is_verified:
            create_error_csv(result, output_dir)


if __name__ == '__main__':
    with BrowsingSession(chromedriver_path='../chromedriver.exe') as browser:
        daily_verification(browser)
