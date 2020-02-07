import os
from typing import List

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
                self._broken[rule_result.rule] = [error['error_msg'] for error in rule_result.errors]

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


def create_error_csv(verification_result: VerificationResult, dir_path: str) -> str:
    """
    Given a rule to verify and some data to verify against, create a CSV file
    detailing any rule-breaking records.

    :param verification_func: the rule verification function
    :param data: data to use in verifying the rule
    :param filepath: the filepath where the CSV should be written
    :return: the resulting filepath of the new CSV
    """
    filepath = os.path.join(dir_path, f'{verification_result.rule_abbrev}.csv')
    to_csv(verification_result.errors, filepath)
    return filepath


def verify_rules(rules: List[tuple] = None) -> List[VerificationResult]:
    """Given a list of rules to check and their associated data, verify the rules.

    :param rules: a list of tuples of the form: (verification_func, data)
    :returns: a list of rule verification results, one for each rule that was tested
    """
    if rules is not None:
        return [rule[0](rule[1]) for rule in rules]
    else:
        return []
