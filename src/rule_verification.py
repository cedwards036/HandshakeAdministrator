from typing import Callable, List


class VerificationResult:
    """The result of a single rule verification"""

    def __init__(self, rule: str, errors: List[dict] = None):
        if not errors:
            errors = []
        self._data = {
            'rule': rule,
            'errors': errors
        }

    def parse_errors(self, error_parser: callable) -> List[dict]:
        return [error_parser(error) for error in self._data['errors']]

    @property
    def rule(self):
        return self._data['rule']

    @property
    def is_verified(self):
        return not self._data['errors']

    @property
    def errors(self):
        return self._data['errors']

    def add_error(self, error):
        if error is not None:
            self._data['errors'].append(error)

    def __eq__(self, other):
        return self._data == other._data

    def __str__(self):
        return str(self._data)


def make_rule(rule: str, error_func: Callable[[dict], dict]) -> Callable[[List[dict]], VerificationResult]:
    def rule_function(records: List[dict]) -> VerificationResult:
        result = VerificationResult(
            rule=rule,
            errors=[]
        )
        for record in records:
            result.add_error(error_func(record))
        return result

    return rule_function
