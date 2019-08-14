from autohandshake import HandshakeSession, InsightsPage

from src.constants import HANDSHAKE_EMAIL, HANDSHAKE_URL
from src.event_rules import jhu_owned_events_are_prefixed_correctly
from src.utils import print_and_write_to_file
from src.verification_report import run_rule_verifications

EVENTS_INSIGHTS_LINK = 'https://app.joinhandshake.com/analytics/explore_embed?insights_page=ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vZXZlbnRzP3FpZD1tSWJjT2t3VjNkN01mVnF3cWpETFo0JmVtYmVkX2RvbWFpbj1odHRwczolMkYlMkZhcHAuam9pbmhhbmRzaGFrZS5jb20mdG9nZ2xlPWZpbA=='
REPORT_FILEPATH = 'C:\\Users\\cedwar42\\Downloads\\event_rule_verification_results.txt'


def handle_event_rule_report(report_text: str):
    print_and_write_to_file(report_text, REPORT_FILEPATH)

with HandshakeSession(HANDSHAKE_URL, HANDSHAKE_EMAIL) as browser:
    events_insights = InsightsPage(EVENTS_INSIGHTS_LINK, browser)
    events = events_insights.get_data()

if __name__ == '__main__':
    run_rule_verifications([
        (jhu_owned_events_are_prefixed_correctly, events)
    ], handle_event_rule_report)
