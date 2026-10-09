"""Behavioral regression checks for the offline acceptance boundary."""

import copy
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

import run_demo


class AcceptanceFixtureTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="java-acceptance-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.verifier = run_demo.Verifier()
        self.candidate = run_demo.copy_candidate(self.verifier, self.root / "candidate")
        self.source = self.candidate / "src/AuthService.java"

    def correct_patch(self):
        self.source.write_bytes((run_demo.HERE / "solution/AuthService.java").read_bytes())

    def assert_boundary_rejected_before_execution(self):
        with patch("run_demo.run_process", side_effect=AssertionError("must not execute")):
            result = self.verifier.verify(self.candidate, completion_claim="Everything passed.")
        self.assertEqual("REJECT", result["verdict"])
        self.assertEqual("source_boundary_violation", result["reason"])

    def test_completion_claim_does_not_repair_the_baseline_defect(self):
        result = self.verifier.verify(self.candidate, completion_claim="Done; tested successfully.")
        self.assertEqual("REJECT", result["verdict"])
        self.assertEqual("acceptance_failed", result["reason"])
        self.assertFalse(result["receipt"]["completion_claim_authoritative"])
        self.assertNotEqual(0, result["receipt"]["execution"]["exit_code"])
        self.assertIn("missing_suffix", result["receipt"]["execution"]["stderr"])

    def test_wrong_patch_fails_real_external_assertions(self):
        self.source.write_text(
            "public class AuthService { public static boolean authenticateToken(String token) { "
            "return token != null && token.length() > 4; } }", encoding="utf-8")
        result = self.verifier.verify(self.candidate)
        self.assertEqual("REJECT", result["verdict"])
        self.assertIn("wrong_prefix", result["receipt"]["execution"]["stderr"])

    def test_exit_zero_with_wrong_output_is_rejected(self):
        self.source.write_text(
            'public class AuthService { static { System.out.println("I passed"); System.exit(0); } '
            'public static boolean authenticateToken(String token) { return false; } }', encoding="utf-8")
        result = self.verifier.verify(self.candidate)
        self.assertEqual(0, result["receipt"]["execution"]["exit_code"])
        self.assertEqual("REJECT", result["verdict"])
        self.assertEqual("acceptance_output_mismatch", result["reason"])

    def test_canned_exact_case_markers_cannot_spoof_fresh_completion(self):
        markers = " ".join(f'System.out.println("CASE {case} PASS");'
                           for case in self.verifier.contract["expected_test_cases"])
        self.source.write_text("public class AuthService { static { " + markers
                               + " System.exit(0); } public static boolean authenticateToken(String token) { return false; } }",
                               encoding="utf-8")
        result = self.verifier.verify(self.candidate, completion_claim="All nine cases passed.")
        self.assertEqual(0, result["receipt"]["execution"]["exit_code"])
        self.assertEqual(self.verifier.contract["expected_test_cases"],
                         result["receipt"]["passed_test_cases"])
        self.assertEqual("REJECT", result["verdict"])
        self.assertEqual("acceptance_output_mismatch", result["reason"])
        self.assertNotIn("COMPLETE ", result["receipt"]["execution"]["stdout"])
        self.assertEqual(64, len(result["receipt"]["completion_marker_sha256"]))

    def test_forged_candidate_tests_are_rejected_before_execution(self):
        (self.candidate / "AuthServiceAcceptance.java").write_text(
            'public class AuthServiceAcceptance { public static void main(String[] a) {} }', encoding="utf-8")
        self.assert_boundary_rejected_before_execution()

    def test_missing_companion_file_is_rejected_before_execution(self):
        (self.candidate / "src/TokenClient.java").unlink()
        self.assert_boundary_rejected_before_execution()

    def test_unexpected_file_is_rejected_before_execution(self):
        (self.candidate / "hidden-config.txt").write_text("skip-tests=true", encoding="utf-8")
        self.assert_boundary_rejected_before_execution()

    def test_empty_unexpected_directory_is_rejected_before_execution(self):
        (self.candidate / "tests").mkdir()
        self.assert_boundary_rejected_before_execution()

    def test_companion_file_edit_is_rejected_before_execution(self):
        (self.candidate / "src/TokenClient.java").write_text(
            "public class TokenClient { public static boolean canSignIn(String token) { return true; } }",
            encoding="utf-8")
        self.assert_boundary_rejected_before_execution()

    def test_symlink_escape_is_rejected_before_execution(self):
        outside = self.root / "outside.java"
        outside.write_bytes((run_demo.HERE / "solution/AuthService.java").read_bytes())
        self.source.unlink()
        try:
            self.source.symlink_to(outside)
        except OSError as error:
            self.skipTest(f"platform does not permit creating symlinks: {error}")
        self.assert_boundary_rejected_before_execution()

    def test_compile_failure_cannot_be_accepted(self):
        self.source.write_text("public class AuthService { syntax error }", encoding="utf-8")
        result = self.verifier.verify(self.candidate)
        self.assertEqual("compiler_failed", result["reason"])
        self.assertEqual("REJECT", result["verdict"])
        self.assertNotEqual(0, result["receipt"]["compile"]["exit_code"])
        self.assertIsNone(result["receipt"]["execution"])

    def test_correct_patch_passes_every_frozen_case_and_revalidates(self):
        self.correct_patch()
        result = self.verifier.verify(self.candidate, completion_claim="I might still be wrong.")
        self.assertEqual("ACCEPT", result["verdict"])
        receipt = result["receipt"]
        self.assertEqual(0, receipt["compile"]["exit_code"])
        self.assertEqual(0, receipt["execution"]["exit_code"])
        self.assertEqual(self.verifier.contract["expected_test_cases"], receipt["passed_test_cases"])
        self.assertEqual({"AC-001", "AC-002", "AC-003", "AC-004"},
                         {item["id"] for item in receipt["acceptance_criteria"]})
        self.assertEqual("ACCEPT", self.verifier.revalidate(self.candidate, receipt)["verdict"])

    def test_source_change_invalidates_previously_successful_evidence(self):
        self.correct_patch()
        accepted = self.verifier.verify(self.candidate)
        self.assertEqual("ACCEPT", accepted["verdict"])
        self.source.write_bytes(self.verifier.fixture_root.joinpath("src/AuthService.java").read_bytes())
        result = self.verifier.revalidate(self.candidate, accepted["receipt"])
        self.assertEqual("REJECT", result["verdict"])
        self.assertEqual("stale_evidence", result["reason"])

    def test_forged_receipt_cannot_bind_different_source(self):
        self.correct_patch()
        accepted = self.verifier.verify(self.candidate)
        forged = copy.deepcopy(accepted["receipt"])
        forged["candidate_manifest_sha256"] = "0" * 64
        body = {key: value for key, value in forged.items() if key not in {"receipt_sha256", "signature"}}
        forged["receipt_sha256"] = run_demo.sha256(run_demo.canonical_json(body))
        result = self.verifier.revalidate(self.candidate, forged)
        self.assertEqual("REJECT", result["verdict"])
        self.assertEqual("invalid_receipt", result["reason"])

    def test_receipt_from_different_verifier_instance_requires_fresh_execution(self):
        self.correct_patch()
        accepted = self.verifier.verify(self.candidate)
        other = run_demo.Verifier()
        self.assertEqual("invalid_receipt", other.revalidate(self.candidate, accepted["receipt"])["reason"])

    def test_changed_frozen_test_invalidates_the_successful_receipt(self):
        copied_example = self.root / "example"
        shutil.copytree(run_demo.HERE, copied_example)
        verifier = run_demo.Verifier(copied_example)
        self.correct_patch()
        accepted = verifier.verify(self.candidate)
        self.assertEqual("ACCEPT", accepted["verdict"])
        verifier.frozen_test_path.write_text("// tampered external test", encoding="utf-8")
        result = verifier.revalidate(self.candidate, accepted["receipt"])
        self.assertEqual("REJECT", result["verdict"])
        self.assertEqual("stale_evidence", result["reason"])

    def test_changed_contract_invalidates_the_successful_receipt(self):
        copied_example = self.root / "example"
        shutil.copytree(run_demo.HERE, copied_example)
        verifier = run_demo.Verifier(copied_example)
        self.correct_patch()
        accepted = verifier.verify(self.candidate)
        self.assertEqual("ACCEPT", accepted["verdict"])
        contract = json.loads(verifier.contract_path.read_text(encoding="utf-8"))
        contract["task"] = "A different task."
        verifier.contract_path.write_text(json.dumps(contract), encoding="utf-8")
        self.assertEqual("stale_evidence", verifier.revalidate(self.candidate, accepted["receipt"])["reason"])

    def test_hanging_candidate_hits_actual_process_timeout(self):
        copied_example = self.root / "example"
        shutil.copytree(run_demo.HERE, copied_example)
        contract_path = copied_example / "contract.json"
        contract = json.loads(contract_path.read_text(encoding="utf-8"))
        contract["run_timeout_seconds"] = 0.5
        contract_path.write_text(json.dumps(contract), encoding="utf-8")
        verifier = run_demo.Verifier(copied_example)
        self.source.write_text("public class AuthService { public static boolean authenticateToken(String token) { while (true) {} } }", encoding="utf-8")
        result = verifier.verify(self.candidate)
        self.assertEqual("REJECT", result["verdict"])
        self.assertEqual("execution_timeout", result["reason"])
        self.assertTrue(result["receipt"]["execution"]["timed_out"])
        self.assertIsNone(result["receipt"]["execution"]["exit_code"])


if __name__ == "__main__":
    unittest.main()
