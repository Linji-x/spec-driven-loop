# Java acceptance: reproducible verifier replay

[中文 README](../../README.md) · [English README](../../README.en.md)

This example runs a real Java compiler and frozen acceptance checks against seven predefined candidates. It demonstrates why a completion claim, forged tests or output, or an old green report cannot replace independent acceptance.

It is an **offline, deterministic verifier replay**, not a live multi-agent run or a model success-rate benchmark. The candidates and their expected verdicts are authored fixtures. No model, API key, package download, or network access is needed after Python and a JDK are installed.

## Run

Requirements: Python 3.10+, JDK 17+, and `java` and `javac` on `PATH`. Run from the repository root:

```text
python examples/java-acceptance/run_demo.py
```

The default run prints its result and cleans up temporary candidate and build directories. To retain the JSON evidence report in the ignored `.tmp/` directory:

```text
python examples/java-acceptance/run_demo.py --output .tmp/java-acceptance-report.json
```

Check the verifier itself with:

```text
python -m unittest discover -s examples/java-acceptance -p test_run_demo.py -v
```

The demo exits successfully when every fixture produces its expected verdict. `all_expected_verdicts_matched` means the replay behaves as designed; it does **not** mean all candidates were accepted. The inputs and expected verdicts are fixed; receipt signatures and runtime diagnostics may vary between runs. If a prerequisite is missing or a verdict differs, resolve that failure before relying on the example.

## Contract and scenarios

`AuthService.authenticateToken(String token)` returns `true` only for a string beginning with the exact prefix `usr-` followed by at least one character. It returns `false` for `null`, the empty string, a wrong prefix, and bare `usr-`. This is a minimal string-validation contract, not production authentication.

| Scenario ID | Expected verdict | What it demonstrates | Next action after the verdict |
| --- | --- | --- | --- |
| `false_completion_claim` | REJECT | A claim of completion cannot make the original failing candidate pass. | Implement the missing behavior and rerun independent checks. |
| `wrong_patch` | REJECT | A plausible patch still fails a frozen boundary case. | Correct the failed AC without changing its contract. |
| `boundary_violation` | REJECT | A candidate attempts to bypass acceptance by changing frozen inputs. | Restore those inputs and keep edits within the allowed source file. |
| `compiler_failure` | REJECT | Source that cannot compile has no valid runtime evidence. | Fix compilation and rerun the gate. |
| `spoofed_test_output` | REJECT | Printing the expected static PASS lines and exiting 0 omits the harness's fresh completion marker. | Remove the bypass and rerun the frozen harness. |
| `correct_patch` | ACCEPT | A candidate satisfies the frozen checks with current evidence. | Inspect the receipt and retain it with the delivery record. |
| `stale_evidence` | REJECT | A receipt from an earlier candidate does not prove the current candidate. | Regenerate evidence for the current source and frozen inputs. |

These next actions explain the workflow; the demo does not implement an autonomous rework state machine.

## Inspectable inputs and records

| File | Responsibility |
| --- | --- |
| [PRD.md](PRD.md) | Example behavior and scope |
| [TECH_DESIGN.md](TECH_DESIGN.md) | Java interface, write boundary, and evidence binding |
| [ACCEPTANCE.md](ACCEPTANCE.md) | Stable AC IDs and pass conditions |
| [AGENT_PLAN.md](AGENT_PLAN.md) | Illustrative implementation and judge responsibilities |
| [LOOP.md](LOOP.md) | Replay verification record and remaining limits |
| [contract.json](contract.json) | Machine-readable file manifest and write boundary |
| [AuthService.java](fixture/candidate/src/AuthService.java) | Initial candidate; the only allowed implementation write |
| [TokenClient.java](fixture/candidate/src/TokenClient.java) | Frozen companion source |
| [AuthServiceAcceptance.java](fixture/tests/AuthServiceAcceptance.java) | Frozen checks executed by the verifier |
| [Correct patch](solution/AuthService.java) | Predefined passing candidate |

The report identifies `evaluation_kind: deterministic_verifier_replay` and records scenario verdicts, hashes, command exit codes, and individual check results. Its receipts bind evidence to the current candidate manifest, contract, frozen tests, and verifier. Inspect those fields instead of accepting the scenario label or completion text alone.

Receipt reuse is supported only within the issuing `Verifier` instance. The saved JSON is an inspectable report, not trusted cross-session resume evidence; start a new session by rerunning verification.

This example verifies one small contract under a trusted local verifier and toolchain. The per-run completion marker checks the replay output protocol and rejects the canned spoof; it does not make the JVM a sandbox or prevent code that can inspect or control its execution environment from forging output. The example does not establish general code correctness or prompt-injection resistance.
