from datetime import datetime
from typing import List, Union

from src.constants import CareerCenters
from src.insights_fields import EventFields
from src.rule_verification import make_rule
from src.utils import create_or_list_from

#############
# CONSTANTS
#############

UNIVERSITY_WIDE_PREFIX = 'University-Wide:'
CANCELLED_PREFIX = 'CANCELLED:'
TEST_PREFIX = 'Test:'


##########################
# ERROR MESSAGE FUNCTIONS
##########################

def _build_event_prefix_error_message(event: dict, valid_prefixes: List[str]) -> str:
    return (f'Event {event[EventFields.ID]} ({event[EventFields.NAME]}) should have '
            f'prefix {create_or_list_from(valid_prefixes)}')


def _get_event_prefix_error(event: dict) -> Union[dict, None]:
    def _event_is_a_test_event(event_name: str) -> bool:
        return event_name.startswith(TEST_PREFIX)

    def _event_was_intended_to_be_cancelled(event_name: str) -> bool:
        return (
                event_name.startswith(CANCELLED_PREFIX) or
                _event_has_malformed_cancelled_prefix(event_name)
        )

    def _event_has_malformed_cancelled_prefix(event_name: str) -> bool:
        return (
                not event_name.startswith(CANCELLED_PREFIX) and (
                event_name.lower().startswith('cancelled') or
                event_name.lower().startswith('canceled')
        ))

    def _add_cancelled_to_prefixes(prefixes: List[str]) -> List[str]:
        return [f'{CANCELLED_PREFIX} {prefix}' for prefix in prefixes]

    def _get_error_dict(event: dict) -> Union[dict, None]:
        valid_prefixes = _determine_valid_prefixes_for_event(event)
        if _event_has_valid_prefix(event, valid_prefixes):
            return None
        else:
            return {
                'id': event[EventFields.ID],
                'error_msg': _build_event_prefix_error_message(event, valid_prefixes)
            }

    def _determine_valid_prefixes_for_event(event: dict) -> List[str]:
        CAREER_CENTER_PREFIXES = {
            CareerCenters.HOMEWOOD: ['Homewood:'],
            CareerCenters.CAREY: ['Carey:'],
            CareerCenters.SAIS: ['SAIS:', 'SAIS DC:', 'SAIS Europe:', 'HNC:', 'SAIS ALL:'],
            CareerCenters.PDCO: ['PDCO:'],
            CareerCenters.NURSING: ['Nursing:'],
            CareerCenters.BSPH: ['BSPH:'],
            CareerCenters.PEABODY: ['Peabody:'],
            CareerCenters.AAP: ['AAP:']
        }
        valid_prefixes = CAREER_CENTER_PREFIXES[event[EventFields.CAREER_CENTER]]
        if _event_was_intended_to_be_cancelled(event[EventFields.NAME]):
            valid_prefixes = _add_cancelled_to_prefixes(valid_prefixes)
        return valid_prefixes

    def _event_has_valid_prefix(event: dict, valid_prefixes: List[str]) -> bool:
        return any(event[EventFields.NAME].startswith(prefix) for prefix in valid_prefixes)

    if not event[EventFields.CAREER_CENTER]:
        return None
    else:
        cleaned_event_name = _strip_cancelled_prefix_from_event_name(event[EventFields.NAME])
        if _event_is_university_wide(cleaned_event_name) or _event_is_a_test_event(cleaned_event_name):
            return None
        else:
            return _get_error_dict(event)


def _build_invite_only_error_message(event: dict, should_be_invite_only: bool) -> str:
    if should_be_invite_only:
        imperative = 'should'
    else:
        imperative = 'should not'
    return (f'Event {event[EventFields.ID]} ({event[EventFields.NAME]}) {imperative} be invite-only')


def _get_invite_error(event: dict) -> Union[dict, None]:
    def _event_is_upcoming(event: dict) -> bool:
        return datetime.strptime(event[EventFields.START_DATE_TIME], '%Y-%m-%d %H:%M:%S') > datetime.now()

    def _event_is_invite_only(event: dict) -> bool:
        return event[EventFields.IS_INVITE_ONLY] == 'Yes'

    def _get_error_dict(event: dict) -> Union[dict, None]:
        cleaned_event_name = _strip_cancelled_prefix_from_event_name(event[EventFields.NAME])
        if _event_is_upcoming(event):
            if _event_is_university_wide(cleaned_event_name) and _event_is_invite_only(event):
                return _build_invite_only_error_dict(event, should_be_invite_only=False)
            elif not (_event_is_university_wide(cleaned_event_name) or _event_is_invite_only(event)):
                return _build_invite_only_error_dict(event, should_be_invite_only=True)
            else:
                return None
        else:
            return None

    def _build_invite_only_error_dict(event: dict, should_be_invite_only: bool) -> dict:
        return {
            'id': event[EventFields.ID],
            'error_msg': _build_invite_only_error_message(event, should_be_invite_only)
        }

    if not event[EventFields.CAREER_CENTER]:
        return None
    else:
        return _get_error_dict(event)


def _event_has_ad_label(event: dict) -> bool:
    return 'shared: advertisement' in event[EventFields.LABELS_LIST]


def _event_has_wrong_type(event: dict) -> bool:
    return event[EventFields.EVENT_TYPE] != 'Other'


def _build_ad_error_message(event: dict) -> str:
    base_error_str = f'Event {event[EventFields.ID]} ({event[EventFields.NAME]}) should'
    label_error_substr = 'be labeled "shared: advertisement"'
    type_error_substr = 'have event type "Other"'
    if (not _event_has_ad_label(event)) and _event_has_wrong_type(event):
        return f'{base_error_str} {label_error_substr} and {type_error_substr}'
    elif _event_has_wrong_type(event):
        return f'{base_error_str} {type_error_substr}'
    else:
        return f'{base_error_str} {label_error_substr}'


def _get_ad_error(event: dict) -> Union[dict, None]:
    def _event_is_office_hours_ad(event: dict) -> bool:
        return 'office hours' in event[EventFields.NAME].lower()

    def _event_is_homewood(event: dict) -> bool:
        return event[EventFields.CAREER_CENTER] == 'Life Design Lab (Homewood)'

    def _event_is_ad(event: dict) -> bool:
        return _event_is_homewood(event) and _event_is_office_hours_ad(event)

    def _build_error_dict(event: dict) -> dict:
        return {
            'id': event[EventFields.ID],
            'error_msg': _build_ad_error_message(event)
        }

    if _event_is_ad(event) and (not _event_has_ad_label(event) or _event_has_wrong_type(event)):
        return _build_error_dict(event)
    else:
        return None


def _get_virtual_session_error(event: dict) -> Union[dict, None]:
    def is_virtual_session(event: dict) -> bool:
        return event[EventFields.EVENT_TYPE] == 'Virtual Session'

    def is_past_event(event: dict) -> bool:
        return datetime.strptime(event[EventFields.START_DATE_TIME], '%Y-%m-%d %H:%M:%S') < datetime.now()

    def is_external_event(event: dict) -> bool:
        return not event[EventFields.CAREER_CENTER]

    def build_error_msg(event: dict) -> str:
        return f'Event {event[EventFields.ID]} ({event[EventFields.NAME]}) should not have the "Virtual Session" event type'

    if is_past_event(event) and is_virtual_session(event) and not is_external_event(event):
        return {
            'id': event[EventFields.ID],
            'error_msg': build_error_msg(event)
        }
    else:
        return None


###########################
# GENERAL HELPER FUNCTIONS
###########################

def _strip_cancelled_prefix_from_event_name(event_name: str) -> str:
    if event_name.startswith(CANCELLED_PREFIX):
        return event_name[len(CANCELLED_PREFIX):].lstrip()
    else:
        return event_name


def _event_is_university_wide(event_name: str) -> bool:
    return event_name.startswith(UNIVERSITY_WIDE_PREFIX)


############################
# RULES
############################

jhu_owned_events_are_prefixed_correctly = make_rule(
    'Events are prefixed correctly if they are owned by a career center',
    'event_wrong_prefix',
    _get_event_prefix_error
)

events_are_invite_only_iff_not_university_wide = make_rule(
    'Events are invite-only if and only if they are not University-Wide or external',
    'event_invite_only',
    _get_invite_error
)

advertisement_events_are_labeled = make_rule(
    '"Advertisement" events are labeled properly and have event type "Other"',
    'event_advertisements',
    _get_ad_error
)

past_events_do_not_have_virtual_event_type = make_rule(
    'Non-external past events do not have the "Virtual Session" event type',
    'past_event_virtual_session',
    _get_virtual_session_error
)
