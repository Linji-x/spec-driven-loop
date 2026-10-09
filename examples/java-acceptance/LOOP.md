# Java acceptance example: replay record

Current state: Replay verified  
Record ID: LOOP-001  
Verification date: 2026-10-09  
Contract: Example frozen input, version 1  
Approval provenance: No historical user approval asserted  
Next action: Rerun in the reader's environment and inspect that run's evidence report

## LOOP-001 scope

This record covers validation of the checked-in deterministic replay. It is not a transcript of agents implementing a product. The seven candidates are predefined fixtures, and their intended outcomes are listed in [README.md](README.md).

## Verification commands

From the repository root:

```text
python examples/java-acceptance/run_demo.py --output .tmp/java-acceptance-report.json
python -m unittest discover -s examples/java-acceptance -p test_run_demo.py -v
```

Observed environment: Windows, Python 3.11.9, JDK 21.0.8 compiling with `--release 17`.

- Demo exit code: 0. All seven expected verdicts matched; `all_expected_verdicts_matched` was `true`.
- Verifier regression exit code: 0. `Ran 18 tests` / `OK (skipped=1)`: 17 passed and the symlink-creation check was skipped because Windows did not grant that privilege.
- Evidence report: `.tmp/java-acceptance-report.json`, retained from the final independent verification. It is local evidence and is not checked in as a transferable acceptance receipt.

| Scenario ID | Observed verdict | Observed reason |
| --- | --- | --- |
| `false_completion_claim` | REJECT | `acceptance_failed` |
| `wrong_patch` | REJECT | `acceptance_failed` |
| `boundary_violation` | REJECT | `source_boundary_violation` |
| `compiler_failure` | REJECT | `compiler_failed` |
| `correct_patch` | ACCEPT | `acceptance_passed` |
| `stale_evidence` | REJECT | `stale_evidence` |
| `spoofed_test_output` | REJECT | `acceptance_output_mismatch` |

For `correct_patch`, the receipt recorded compiler and execution exit codes of 0, all nine frozen Java cases, the harness completion marker, and source/contract/test/verifier bindings. The canned-output scenario exited 0 but lacked the fresh completion marker, so it was rejected. The regression checks also confirmed that a changed source invalidates earlier evidence and a different verifier instance cannot reuse the receipt.

This records one local fixture verification. It is not a CI result, a production acceptance decision, or a model-success measurement.

## Remaining limits

- This validates the fixture and its verifier, not a model's coding ability or live multi-agent coordination.
- The Java method checks a string shape; it is not a production authentication implementation.
- The contract, verifier, and local toolchain are trusted. Hashes alone do not secure an attacker-controlled verifier.
- A fresh harness marker rejects the canned-output fixture; it is a replay protocol check, not protection against arbitrary hostile Java.
- A receipt must be regenerated after changing the candidate or trusted acceptance inputs.
- Symlink rejection still needs execution in an environment that permits creating symlinks; the local skipped check is not a pass.
