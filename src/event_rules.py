from typing import List

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

UNIVERSITY_WIDE_PREFIX = 'University-Wide:'
CANCELLED_PREFIX = 'CANCELLED:'


def jhu_owned_events_are_prefixed_correctly(events: List[dict]) -> VerificationResult:
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
    if not event['career_center_on_events.name']:
        return None
    else:
        cleaned_event_name = _get_cleaned_event_name(event['events.name'])
        if _event_is_university_wide(cleaned_event_name):
            return None
        else:
            valid_prefixes = CAREER_CENTER_PREFIXES[event['career_center_on_events.name']]
            for prefix in valid_prefixes:
                if cleaned_event_name.startswith(prefix):
                    return None
            if event['events.name'].startswith(CANCELLED_PREFIX):
                valid_prefixes = _add_cancelled_to_prefixes(valid_prefixes)
            return _build_event_prefix_error_str(event, valid_prefixes)


def _get_cleaned_event_name(event_name: str) -> str:
    if event_name.startswith(CANCELLED_PREFIX):
        return event_name[len(CANCELLED_PREFIX):].lstrip()
    else:
        return event_name


def _event_is_university_wide(event_name: str) -> bool:
    return event_name.startswith(UNIVERSITY_WIDE_PREFIX)


def _add_cancelled_to_prefixes(prefixes: List[str]) -> List[str]:
    return [f'{CANCELLED_PREFIX} {prefix}' for prefix in prefixes]


def _build_event_prefix_error_str(event: dict, valid_prefixes: List[str]) -> str:
    return (f'Event {event["events.id"]} ({event["events.name"]}) should have '
            f'prefix {create_or_list_from(valid_prefixes)}')


def events_are_invite_only_iff_not_university_wide(events: List[dict]) -> VerificationResult:
    """
    Rule: Events should be marked invite-only if and only if they are not
    University-Wide or external
    """
    result = VerificationResult(
        rule='Events are invite-only if and only if they are not University-Wide or external',
        is_verified=False,
        errors=[]
    )
    for event in events:
        error = _get_invite_error(event)
        if error:
            result.add_error(error)
    if len(result.errors) == 0:
        result.is_verified = True
    return result


def _get_invite_error(event: dict):
    if not event['career_center_on_events.name']:
        return None
    else:
        cleaned_event_name = _get_cleaned_event_name(event['events.name'])
        if _event_is_university_wide(cleaned_event_name) and _event_is_invite_only(event):
            return _build_invite_only_error_string(event, should_be_invite_only=False)
        elif not (_event_is_university_wide(cleaned_event_name) or _event_is_invite_only(event)):
            return _build_invite_only_error_string(event, should_be_invite_only=True)
        else:
            return None


def _event_is_invite_only(event: dict) -> bool:
    return event['events.invite_only'] == 'Yes'


def _build_invite_only_error_string(event: dict, should_be_invite_only: bool) -> str:
    if should_be_invite_only:
        imperative = 'should'
    else:
        imperative = 'should not'
    return (f'Event {event["events.id"]} ({event["events.name"]}) {imperative} be invite-only')
