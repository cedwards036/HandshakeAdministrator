from src.constants import CareerCenters
from src.utils import create_or_list_from
from src.verification_report import VerificationResult

CAREER_CENTER_PREFIXES = {
    CareerCenters.HOMEWOOD: ['Homewood:'],
    CareerCenters.CAREY: ['Carey:'],
    CareerCenters.SAIS: ['SAIS DC:', 'SAIS Europe:', 'HNC:'],
    CareerCenters.PDCO: ['PDCO:'],
    CareerCenters.NURSING: ['Nursing:'],
    CareerCenters.BSPH: ['BSPH:'],
    CareerCenters.PEABODY: ['Peabody:'],
    CareerCenters.AAP: ['AAP:']
}


def jhu_owned_events_are_prefixed_correctly(events: list) -> VerificationResult:
    """Rule: all events that are controlled by a JHU career center must have the correct prefix in their name"""
    result = VerificationResult(
        rule='Events are prefixed correctly if they are owned by a career center',
        is_verified=False,
        errors=[]
    )
    for event in events:
        error = _get_event_prefix_error(event)
        if error:
            result.add_error(error)
    if len(result.errors) == 0:
        result.is_verified = True
    return result


def _get_event_prefix_error(event: dict):
    if not event['career_center_on_events.name'] or event['events.name'].startswith('University-Wide'):
        return None
    desired_prefixes = CAREER_CENTER_PREFIXES[event['career_center_on_events.name']]
    for prefix in desired_prefixes:
        if event['events.name'].startswith(prefix):
            return None
    return _build_event_prefix_error_str(event)


def _build_event_prefix_error_str(event: dict) -> str:
    desired_prefixes = CAREER_CENTER_PREFIXES[event["career_center_on_events.name"]]
    return (f'Event {event["events.id"]} ({event["events.name"]}) should have '
            f'prefix {create_or_list_from(desired_prefixes)}')
