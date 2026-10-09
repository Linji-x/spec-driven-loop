#!/usr/bin/env python3
"""Replay seven acceptance failures/successes using real javac/java, with no API.

The verifier checks the complete candidate file tree before execution. It runs
trusted, frozen tests outside the candidate write scope and binds receipts to
the current source artifacts. This local demonstration is not an OS sandbox
for hostile Java code. A fresh completion challenge rejects canned test-marker
replay; Java code that can inspect the challenge can still forge this protocol.
Exported receipts are inspectable evidence; re-use is
supported only by the issuing Verifier instance, with a fresh source check.
"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
from pathlib import Path
import secrets
import shutil
import signal
import stat
import subprocess
import tempfile
from typing import Any


HERE = Path(__file__).resolve().parent
SCENARIO_IDS = (
    "false_completion_claim", "wrong_patch", "boundary_violation",
    "compiler_failure", "correct_patch", "stale_evidence",
    "spoofed_test_output",
)
EXPECTED_REASONS = {
    "false_completion_claim": "acceptance_failed", "wrong_patch": "acceptance_failed",
    "boundary_violation": "source_boundary_violation", "compiler_failure": "compiler_failed",
    "correct_patch": "acceptance_passed", "stale_evidence": "stale_evidence",
    "spoofed_test_output": "acceptance_output_mismatch",
}


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class BoundaryError(ValueError):
    """A candidate tree does not fit the frozen write boundary."""


def _is_link(path: Path) -> bool:
    info = path.lstat()
    # Windows directory junctions/reparse points also bypass ordinary symlinks.
    return stat.S_ISLNK(info.st_mode) or bool(
        getattr(info, "st_file_attributes", 0) & 0x400
    )


def tree_manifest(root: Path) -> dict[str, dict[str, str]]:
    """Include files AND directories; reject links instead of following them."""
    if not root.is_dir() or _is_link(root):
        raise BoundaryError("candidate root must be an ordinary directory")
    manifest: dict[str, dict[str, str]] = {}
    for current, directories, files in os.walk(root, followlinks=False):
        for name in sorted(directories + files):
            path = Path(current) / name
            relative = path.relative_to(root).as_posix()
            if _is_link(path):
                raise BoundaryError(f"link/reparse point is forbidden: {relative}")
            info = path.lstat()
            if stat.S_ISDIR(info.st_mode):
                manifest[relative] = {"type": "directory"}
            elif stat.S_ISREG(info.st_mode):
                manifest[relative] = {"type": "file", "sha256": sha256(path.read_bytes())}
            else:
                raise BoundaryError(f"non-regular entry is forbidden: {relative}")
    return dict(sorted(manifest.items()))


def run_process(command: list[str], *, cwd: Path, timeout: float) -> dict[str, Any]:
    """Capture an actual process result; timeout never implies success."""
    process = subprocess.Popen(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               text=True, encoding="utf-8", errors="replace",
                               start_new_session=os.name != "nt")
    try:
        stdout, stderr = process.communicate(timeout=timeout)
        return {"exit_code": process.returncode, "timed_out": False,
                "stdout": stdout[-65536:], "stderr": stderr[-65536:]}
    except subprocess.TimeoutExpired as error:
        # Oracle's Windows javapath launcher creates a JVM child. Killing only
        # that launcher leaves the child alive and its output pipes open.
        if os.name == "nt":
            try:
                subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"],
                               capture_output=True, timeout=5, check=False)
            except (OSError, subprocess.TimeoutExpired):
                process.kill()
        else:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        def readable(value: str | bytes | None) -> str:
            if isinstance(value, bytes):
                return value.decode("utf-8", errors="replace")[-65536:]
            return (value or "")[-65536:]
        try:
            stdout, stderr = process.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            stdout, stderr = readable(error.stdout), readable(error.stderr)
        return {"exit_code": None, "timed_out": True,
                "stdout": readable(stdout), "stderr": readable(stderr)}


class Verifier:
    def __init__(self, example_root: Path = HERE):
        self.example_root = example_root.resolve()
        self.contract_path = self.example_root / "contract.json"
        self.contract_bytes = self.contract_path.read_bytes()
        self.contract = json.loads(self.contract_bytes)
        if self.contract["schema_version"] != 1:
            raise ValueError("unsupported contract schema")
        self.fixture_root = self.example_root / self.contract["candidate_root"]
        self.frozen_test_path = self.example_root / self.contract["frozen_test_path"]
        self.test_bytes = self.frozen_test_path.read_bytes()
        self.baseline = tree_manifest(self.fixture_root)
        required = {path for path, entry in self.baseline.items() if entry["type"] == "file"}
        if required != set(self.contract["required_files"]):
            raise ValueError("contract required_files differs from frozen fixture")
        self.allowed = set(self.contract["allowed_write_paths"])
        if not self.allowed <= required:
            raise ValueError("allowed_write_paths must be a subset of required_files")
        self.verifier_path = Path(__file__).resolve()
        self.verifier_hash = sha256(self.verifier_path.read_bytes())
        self._receipt_key = secrets.token_bytes(32)

    def _artifacts(self) -> dict[str, str]:
        return {"contract_sha256": sha256(self.contract_bytes),
                "frozen_tests_sha256": sha256(self.test_bytes),
                "fixture_manifest_sha256": sha256(canonical_json(self.baseline)),
                "verifier_sha256": self.verifier_hash}

    def _check_frozen_artifacts(self) -> None:
        if (self.contract_path.read_bytes() != self.contract_bytes
                or self.frozen_test_path.read_bytes() != self.test_bytes
                or tree_manifest(self.fixture_root) != self.baseline
                or sha256(self.verifier_path.read_bytes()) != self.verifier_hash):
            raise BoundaryError("frozen contract, fixture, test, or verifier changed")

    def _candidate_manifest(self, candidate: Path) -> dict[str, dict[str, str]]:
        self._check_frozen_artifacts()
        actual = tree_manifest(candidate)
        missing = sorted(set(self.baseline) - set(actual))
        unexpected = sorted(set(actual) - set(self.baseline))
        if missing or unexpected:
            raise BoundaryError(f"missing={missing}; unexpected={unexpected}")
        for path, original in self.baseline.items():
            if actual[path]["type"] != original["type"]:
                raise BoundaryError(f"entry type changed: {path}")
            if path not in self.allowed and actual[path] != original:
                raise BoundaryError(f"immutable candidate file changed: {path}")
        return actual

    def _seal(self, body: dict[str, Any]) -> dict[str, Any]:
        data = canonical_json(body)
        return {**body, "receipt_sha256": sha256(data),
                "signature": hmac.new(self._receipt_key, data, hashlib.sha256).hexdigest()}

    @staticmethod
    def _result(verdict: str, reason: str, message: str,
                receipt: dict[str, Any] | None = None) -> dict[str, Any]:
        return {"verdict": verdict, "reason": reason, "message": message, "receipt": receipt}

    def verify(self, candidate: Path, *, completion_claim: str = "") -> dict[str, Any]:
        """Judge artifacts/process results. The completion claim has no authority."""
        try:
            manifest = self._candidate_manifest(candidate)
        except (BoundaryError, OSError) as error:
            return self._result("REJECT", "source_boundary_violation", str(error))
        evidence: dict[str, Any] = {
            "schema_version": 1, **self._artifacts(), "candidate_manifest": manifest,
            "candidate_manifest_sha256": sha256(canonical_json(manifest)),
            "completion_claim": completion_claim, "completion_claim_authoritative": False,
            "compile": None, "execution": None, "passed_test_cases": [],
            "acceptance_criteria": self.contract["acceptance_criteria"],
            "completion_marker_sha256": None,
        }

        def finish(verdict: str, reason: str, message: str) -> dict[str, Any]:
            evidence.update(verdict=verdict, reason=reason)
            return self._result(verdict, reason, message, self._seal(evidence))

        def source_still_bound() -> bool:
            try:
                return self._candidate_manifest(candidate) == manifest
            except (BoundaryError, OSError):
                return False

        javac, java = shutil.which("javac"), shutil.which("java")
        if not javac or not java:
            return finish("REJECT", "java_toolchain_missing", "Install a JDK with javac and java on PATH.")
        with tempfile.TemporaryDirectory(prefix="java-acceptance-build-") as temporary:
            build_root = Path(temporary)
            classes = build_root / "classes"
            classes.mkdir()
            frozen_tests = build_root / "frozen-tests"
            frozen_tests.mkdir()
            test_source = frozen_tests / self.frozen_test_path.name
            test_source.write_bytes(self.test_bytes)
            sources = [str(candidate.resolve() / path) for path in self.contract["required_files"]
                       if path.endswith(".java")]
            evidence["compile"] = run_process(
                [javac, "--release", str(self.contract["java_release"]), "-encoding", "UTF-8",
                 "-d", str(classes), *sources, str(test_source)],
                cwd=build_root, timeout=self.contract["compile_timeout_seconds"],
            )
            evidence["compile"]["command"] = [
                "javac", "--release", str(self.contract["java_release"]), "-encoding", "UTF-8",
                "-d", "<temporary-classes>", *self.contract["required_files"],
                "<frozen-tests>/" + self.frozen_test_path.name,
            ]
            if not source_still_bound():
                return finish("REJECT", "source_changed_during_verification", "Artifacts changed while compiling.")
            if evidence["compile"]["timed_out"]:
                return finish("REJECT", "compiler_timeout", "Compilation exceeded the frozen timeout.")
            if evidence["compile"]["exit_code"] != 0:
                return finish("REJECT", "compiler_failed", "javac exited unsuccessfully.")
            challenge = secrets.token_hex(32)
            completion_marker = "COMPLETE " + challenge
            evidence["completion_marker_sha256"] = sha256(completion_marker.encode("utf-8"))
            evidence["execution"] = run_process(
                [java, "-Dfile.encoding=UTF-8", "-cp", str(classes),
                 self.contract["test_main_class"], challenge],
                cwd=build_root, timeout=self.contract["run_timeout_seconds"],
            )
            evidence["execution"]["command"] = ["java", "-Dfile.encoding=UTF-8", "-cp",
                                                   "<temporary-classes>", self.contract["test_main_class"],
                                                   "<fresh-completion-challenge>"]
            if not source_still_bound():
                return finish("REJECT", "source_changed_during_verification", "Artifacts changed while running tests.")
            execution = evidence["execution"]
            if execution["timed_out"]:
                return finish("REJECT", "execution_timeout", "Acceptance exceeded the frozen timeout.")
            lines = execution["stdout"].splitlines()
            expected = [f"CASE {case} PASS" for case in self.contract["expected_test_cases"]]
            expected.append(completion_marker)
            evidence["passed_test_cases"] = [case for case in self.contract["expected_test_cases"]
                                              if f"CASE {case} PASS" in lines]
            if execution["exit_code"] != 0:
                return finish("REJECT", "acceptance_failed", "A frozen Java assertion failed.")
            if lines != expected or execution["stderr"]:
                return finish("REJECT", "acceptance_output_mismatch", "Exit zero alone does not prove all checks ran.")
            return finish("ACCEPT", "acceptance_passed", "Every frozen Java assertion passed against the current artifacts.")

    def revalidate(self, candidate: Path, receipt: dict[str, Any]) -> dict[str, Any]:
        """Re-use this instance's issued successful receipt only for identical artifacts."""
        body = {key: value for key, value in receipt.items() if key not in {"receipt_sha256", "signature"}}
        data = canonical_json(body)
        signature = hmac.new(self._receipt_key, data, hashlib.sha256).hexdigest()
        if (receipt.get("receipt_sha256") != sha256(data)
                or not hmac.compare_digest(str(receipt.get("signature", "")), signature)):
            return self._result("REJECT", "invalid_receipt", "Receipt was not issued unchanged by this verifier.")
        if body.get("verdict") != "ACCEPT" or body.get("reason") != "acceptance_passed":
            return self._result("REJECT", "invalid_receipt", "A rejected run cannot authorize acceptance.")
        try:
            manifest = self._candidate_manifest(candidate)
        except (BoundaryError, OSError) as error:
            return self._result("REJECT", "stale_evidence", str(error), receipt)
        if (body.get("candidate_manifest") != manifest
                or body.get("candidate_manifest_sha256") != sha256(canonical_json(manifest))
                or any(body.get(key) != value for key, value in self._artifacts().items())):
            return self._result("REJECT", "stale_evidence", "Receipt no longer describes the current artifacts.", receipt)
        return self._result("ACCEPT", "evidence_current", "Receipt still matches every current artifact.", receipt)


def copy_candidate(verifier: Verifier, destination: Path) -> Path:
    shutil.copytree(verifier.fixture_root, destination)
    return destination


def run_demo(example_root: Path = HERE) -> dict[str, Any]:
    verifier = Verifier(example_root)
    scenarios: list[dict[str, Any]] = []
    solution = (example_root / "solution/AuthService.java").read_bytes()
    with tempfile.TemporaryDirectory(prefix="java-acceptance-candidates-") as temporary:
        root = Path(temporary)
        for scenario_id in SCENARIO_IDS:
            candidate = copy_candidate(verifier, root / scenario_id)
            source = candidate / "src/AuthService.java"
            expected = "ACCEPT" if scenario_id == "correct_patch" else "REJECT"
            if scenario_id == "wrong_patch":
                source.write_text("public final class AuthService { public static boolean authenticateToken(String token) { return token != null && !token.isEmpty(); } }\n", encoding="utf-8")
            elif scenario_id == "boundary_violation":
                (candidate / "AuthServiceAcceptance.java").write_text("// forged replacement tests\n", encoding="utf-8")
            elif scenario_id == "compiler_failure":
                source.write_text("public class AuthService { syntax error }\n", encoding="utf-8")
            elif scenario_id in {"correct_patch", "stale_evidence"}:
                source.write_bytes(solution)
            elif scenario_id == "spoofed_test_output":
                print_statements = " ".join(
                    f'System.out.println("CASE {case} PASS");'
                    for case in verifier.contract["expected_test_cases"]
                )
                source.write_text("public class AuthService { static { " + print_statements
                                  + " System.exit(0); } public static boolean authenticateToken(String token) { return false; } }\n",
                                  encoding="utf-8")
            result = verifier.verify(candidate, completion_claim="Done; all tests passed.")
            if scenario_id == "stale_evidence":
                if result["verdict"] != "ACCEPT":
                    raise RuntimeError("stale-evidence scenario requires an actually accepted initial patch")
                source.write_text(source.read_text(encoding="utf-8") + "// source changed after acceptance\n", encoding="utf-8")
                result = verifier.revalidate(candidate, result["receipt"])
            scenarios.append({"id": scenario_id, "expected_verdict": expected,
                              "expected_reason": EXPECTED_REASONS[scenario_id], **result,
                              "matched": result["verdict"] == expected
                              and result["reason"] == EXPECTED_REASONS[scenario_id]})
    return {"schema_version": 1, "evaluation_kind": "deterministic_verifier_replay",
            "online_model_evaluation": False, "scenarios": scenarios,
            "all_expected_verdicts_matched": all(row["matched"] for row in scenarios)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Write the evidence report to this JSON file.")
    args = parser.parse_args()
    try:
        report = run_demo()
    except (OSError, ValueError, KeyError, RuntimeError) as error:
        print(f"Demo could not complete: {error}")
        return 2
    print("Deterministic Java verifier replay (no online model-quality evaluation).")
    for row in report["scenarios"]:
        print(f"{row['id']}: {row['verdict']} ({row['reason']}); expected={row['expected_verdict']}")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Evidence report: {args.output}")
    print("Expected verdicts matched: " + ("YES" if report["all_expected_verdicts_matched"] else "NO"))
    return 0 if report["all_expected_verdicts_matched"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
