# Java acceptance example: technical design

Status: Example frozen input, version 1  
Behavior owner: [PRD.md](PRD.md)  
Executable boundary: [contract.json](contract.json)

## Interface and ownership

```java
public static boolean authenticateToken(String token)
```

The implementation candidate is `fixture/candidate/src/AuthService.java`. `fixture/candidate/src/TokenClient.java` is a frozen companion source; `fixture/tests/AuthServiceAcceptance.java` contains independently owned checks. The candidate may change only `AuthService.java`. The complete candidate manifest and allowed write path are declared in `contract.json`; deleting or adding candidate files cannot silently escape that manifest.

The checks compile alongside the candidate. They exercise the behavior in [ACCEPTANCE.md](ACCEPTANCE.md) and return process results that the verifier can inspect. Java dependencies are limited to the JDK.

The harness also emits a fresh per-run completion marker after its assertions. Exit 0 plus canned static PASS lines is insufficient. This marker validates the replay output protocol; code running in the same JVM can inspect its environment, so this mechanism does not provide security against arbitrary hostile Java.

## Verification and evidence

`run_demo.py` builds each predefined candidate in a temporary workspace, checks the file boundary and frozen inputs, invokes `javac`, and runs the frozen Java checks when compilation succeeds. Failures produce `REJECT`; only the compliant candidate produces `ACCEPT`.

A receipt binds the candidate file manifest and hashes to the current contract, frozen tests, and verifier and records compiler/runtime exit codes and check results. Before using a previous receipt, recompute its bindings. A green result from different source is stale evidence. An instance-specific HMAC also rejects modified receipts; reuse is limited to the issuing `Verifier` instance. A saved report cannot authorize acceptance in a new session, which must rerun verification.

Hash binding detects a mismatch; it does not protect against an attacker who can rewrite the verifier or its trusted inputs. The verifier, frozen contract/tests, and local toolchain are trusted inputs in this demonstration. This runner is not an OS sandbox for arbitrary hostile Java code.

## Replay and output

The scenarios, expected verdicts, and next actions are listed in [README.md](README.md). They are synthetic replay inputs, not model-generated attempts. The result schema has `schema_version: 1`, `evaluation_kind: deterministic_verifier_replay`, a `scenarios` array, and `all_expected_verdicts_matched`.

By default, output is printed and temporary workspaces are cleaned. `--output PATH` preserves one JSON report. No receipt from this example should be copied into another project as proof of acceptance.
