from typing import List

def generate_report(rule_results: List[dict]) -> dict:
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
        if rule_result['is_verified']:
            report['verified'].append(rule_result['rule'])
        else:
            report['broken'][rule_result['rule']] = rule_result['errors']
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
