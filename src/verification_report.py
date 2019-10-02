from typing import List, Callable

from src.rule_verification import VerificationResult
from src.utils import to_csv


class VerificationReport:
    """A report detailing the results of multiple rule verifications"""

    def __init__(self, verification_results: List[VerificationResult]):
        self._verified = []
        self._broken = {}
        for rule_result in verification_results:
            if rule_result.is_verified:
                self._verified.append(rule_result.rule)
            else:
                self._broken[rule_result.rule] = rule_result.errors

    @property
    def verified(self):
        return list(self._verified)

    @property
    def broken(self):
        return {rule: [rule_breaker for rule_breaker in rule_breakers]
                for rule, rule_breakers in self._broken.items()}

    def has_verified(self):
        """Return whether the report contains any verified rules"""
        return len(self._verified) > 0

    def has_broken(self):
        """Return whether the report contains any broken rules"""
        return len(self._broken) > 0

    def as_dict(self):
        """Return the report as a dictionary"""
        return {
            'verified': self.verified,
            'broken': self.broken
        }

    def __eq__(self, other):
        return self.as_dict() == other.as_dict()

    def __str__(self):
        result = '================== Verification Report ===================\n'
        if self.has_verified():
            result += '\nRules verified:\n\n'
            for verified_rule in self.verified:
                result += f'    {verified_rule}\n'
        if self.has_broken():
            result += '\nRules broken:\n\n'
            for broken_rule, errors in self.broken.items():
                result += f'    {broken_rule}\n'
                for error in errors:
                    result += f'        {error}\n'
        result += f'\n================== {len(self.verified)} verified, {len(self.broken)} broken =================='
        return result


def run_rule_verifications(rules: List[tuple] = None, callback: Callable = print):
    """
    Given a list of rules to check and their associated data, verify the rules and output a report.

    :param rules: a list of tuples of the form: (verification_func, data)
    :param callback: a function to which to pass the generated report. For example,
                     pass "print" to print the report to the console, or pass a
                     function that writes the report to a file on disk.
    """
    verification_results = _verify_rules(rules)
    report = VerificationReport(verification_results)
    callback(report)


def create_error_csv(verification_func: callable, data: List[dict],
                     error_parser: callable, filepath: str) -> str:
    """
    Given a rule to verify and some data to verify against, create a CSV file
    detailing any rule-breaking records.

    :param verification_func: the rule verification function
    :param data: data to use in verifying the rule
    :param filepath: the filepath where the CSV should be written
    :return: the resulting filepath of the new CSV
    """
    verification_result = verification_func(data)
    csv_data = verification_result.parse_errors(error_parser)
    to_csv(csv_data, filepath)
    return filepath


def _verify_rules(rules: List[tuple] = None) -> List[VerificationResult]:
    """Given a list of rules to check and their associated data, verify the rules.

    :param rules: a list of tuples of the form: (verification_func, data)
    :returns: a list of rule verification results, one for each rule that was tested
    """
    if not rules:
        return []
    results = []
    for rule in rules:
        results.append(rule[0](rule[1]))
    return results
