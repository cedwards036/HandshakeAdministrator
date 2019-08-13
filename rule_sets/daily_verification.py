from autohandshake import HandshakeSession, InsightsPage

from src.constants import HANDSHAKE_EMAIL, HANDSHAKE_URL
from src.event_rules import jhu_owned_events_are_prefixed_correctly
from src.verification_report import format_report, generate_report, verify_rules

EVENTS_INSIGHTS_LINK = 'https://app.joinhandshake.com/analytics/explore_embed?insights_page=ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vZXZlbnRzP3FpZD1tSWJjT2t3VjNkN01mVnF3cWpETFo0JmVtYmVkX2RvbWFpbj1odHRwczolMkYlMkZhcHAuam9pbmhhbmRzaGFrZS5jb20mdG9nZ2xlPWZpbA=='

with HandshakeSession(HANDSHAKE_URL, HANDSHAKE_EMAIL) as browser:
    events_insights = InsightsPage(EVENTS_INSIGHTS_LINK, browser)
    events = events_insights.get_data()

if __name__ == '__main__':
    verification_results = verify_rules([
        (jhu_owned_events_are_prefixed_correctly, events)
    ])
    report = generate_report(verification_results)
    print(format_report(report))
