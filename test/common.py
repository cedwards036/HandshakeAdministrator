import unittest
from typing import List

from src.rule_verification import VerificationResult


def assertContainsErrorIDs(test_class: unittest.TestCase, ids: List[str], verification_result: VerificationResult):
    for id in ids:
        test_class.assertTrue(any(error['id'] == id for error in verification_result.errors))


def assertIsVerified(test_class: unittest.TestCase, verification_result: VerificationResult):
    test_class.assertTrue(verification_result.is_verified)
