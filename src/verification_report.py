from typing import List, Callable

from src.rule_verification import VerificationResult


def run_rule_verifications(rules: List[tuple] = None, callback: Callable = print):
    """
    Given a list of rules to check and their associated data, verify the rules and output a report.

    :param rules: a list of tuples of the form: (verification_func, data)
    :param callback: a function to which to pass the generated report. For example,
                     pass "print" to print the report to the console, or pass a
                     function that writes the report to a file on disk.
    """
    verification_results = _verify_rules(rules)
    report = _generate_report(verification_results)
    callback(_format_report(report))


def _verify_rules(rules: List[tuple] = None) -> List[VerificationResult]:
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


def _generate_report(rule_results: List[VerificationResult]) -> dict:
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


def _format_report(report: dict) -> str:
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
