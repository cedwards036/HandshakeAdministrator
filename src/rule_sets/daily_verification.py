from datetime import datetime

from autohandshake import InsightsPage

from src.rules.appointment_rules import past_appointments_have_finalized_status
from src.rules.event_rules import (
    jhu_owned_events_are_prefixed_correctly,
    events_are_invite_only_iff_not_university_wide
)
from src.utils import print_and_write_to_file, BrowsingSession
from src.verification_report import run_rule_verifications, VerificationReport

EVENTS_INSIGHTS_LINK = 'https://app.joinhandshake.com/analytics/explore_embed?insights_page=ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vZXZlbnRzP3FpZD00VW8yOTJMbFhLWEw4ZUs0SnZqSXdOJmVtYmVkX2RvbWFpbj1odHRwczolMkYlMkZhcHAuam9pbmhhbmRzaGFrZS5jb20mdG9nZ2xlPWZpbA=='
APPTS_INSIGHTS_LINK = 'https://app.joinhandshake.com/analytics/explore_embed?insights_page=ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vYXBwb2ludG1lbnRzP3FpZD1UbFFzVVVtRWpTRUNQNldBMVQzTk1zJmVtYmVkX2RvbWFpbj1odHRwczolMkYlMkZhcHAuam9pbmhhbmRzaGFrZS5jb20mdG9nZ2xlPWZpbA=='

REPORT_FILEPATH = 'C:\\Users\\cedwar42\\Downloads\\daily_rule_verification_results.txt'


def handle_daily_rule_report(report: VerificationReport):
    print_and_write_to_file(str(report), REPORT_FILEPATH)


with BrowsingSession() as browser:
    events_insights = InsightsPage(EVENTS_INSIGHTS_LINK, browser)
    events_insights.set_date_range_filter('Events', 'Start Date Date', datetime(2019, 7, 1).date(),
                                          datetime(2020, 7, 1).date())
    events = events_insights.get_data()

    appts_insights = InsightsPage(APPTS_INSIGHTS_LINK, browser)
    appts = appts_insights.get_data()

if __name__ == '__main__':
    run_rule_verifications([
        (jhu_owned_events_are_prefixed_correctly, events),
        (events_are_invite_only_iff_not_university_wide, events),
        (past_appointments_have_finalized_status, appts)
    ], handle_daily_rule_report)
