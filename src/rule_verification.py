from typing import Callable, List


class VerificationResult:
    """The result of a single rule verification"""

    def __init__(self, rule: str, is_verified: bool, errors: List[str] = None):
        if not errors:
            errors = []
        self._data = {
            'rule': rule,
            'is_verified': is_verified,
            'errors': errors
        }

    def parse_errors(self, error_parser: callable) -> List[dict]:
        return [error_parser(error) for error in self._data['errors']]

    @property
    def rule(self):
        return self._data['rule']

    @property
    def is_verified(self):
        return self._data['is_verified']

    @is_verified.setter
    def is_verified(self, verification_status: bool):
        self._data['is_verified'] = verification_status

    @property
    def errors(self):
        return self._data['errors']

    def add_error(self, error):
        self._data['errors'].append(error)

    def __eq__(self, other):
        return self._data == other._data

    def __str__(self):
        return str(self._data)


def make_rule(rule: str, error_msg_func: Callable[[dict], str]) -> Callable[[List[dict]], VerificationResult]:
    """
    Make a new rule described by the given rule text.

    :param rule: a string describing the rule. For example, "All appointments
                 have an associated type"
    :param error_msg_func: a function that, given a single data record, produces
                           an appropriate error string, if needed. For example,
                           a rule that analyzes a list of event data might use a
                           function that returns "Event [event id] is named
                           incorrectly" if it finds an error, and None otherwise.
    :return: a rule-verifying function that, when given a list of relevant data
             objects, produces a descriptive VerificationResult, including any
             rule-breaking errors found during the verification.
    """

    def rule_function(records: List[dict]) -> VerificationResult:
        result = VerificationResult(
            rule=rule,
            is_verified=False,
            errors=[]
        )
        for record in records:
            error = error_msg_func(record)
            if error is not None:
                result.add_error(error)
        if len(result.errors) == 0:
            result.is_verified = True
        return result

    return rule_function
