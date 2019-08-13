from typing import List


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


def generate_report(rule_results: List[VerificationResult]) -> dict:
    """
    Given a list of rule verification results, create a summary report.

    :param rule_results: a list of rule result dicts
    :return: a report summarizing the rule results
    """
    report = {
        'verified': [],
        'broken': {}
    }
    for rule_result in rule_results:
        if rule_result.is_verified:
            report['verified'].append(rule_result.rule)
        else:
            report['broken'][rule_result.rule] = rule_result.errors
    return report


def format_report(report: dict) -> str:
    """Given a rule result report object, create a printable report"""
    result = '================== Verification Report ===================\n'
    if report['verified']:
        result += '\nRules verified:\n\n'
        for verified_rule in report['verified']:
            result += f'    {verified_rule}\n'
    if report['broken']:
        result += '\nRules broken:\n\n'
        for broken_rule, errors in report['broken'].items():
            result += f'    {broken_rule}\n'
            for error in errors:
                result += f'        {error}\n'
    result += f'\n================== {len(report["verified"])} verified, {len(report["broken"])} broken =================='
    return result


def verify_rules(rules: List[tuple] = None) -> List[dict]:
    """Given a list of rules to check and their associated data, verify the rules.

    :param rules: a list of tuples of the form: (verification_func, data)
    :returns: a list of rule result dicts, one for each rule that was tested
    """
    if not rules:
        return []
    results = []
    for rule in rules:
        results.append(rule[0](rule[1]))
    return results
