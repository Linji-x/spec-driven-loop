# Java acceptance example: responsibility plan

Status: Illustrative plan for the example frozen contract  
Execution mode: Deterministic replay of predefined candidates; no live agents are launched

## Inputs and roles

| Task ID | Responsibility | Allowed writes | Read-only inputs |
| --- | --- | --- | --- |
| TASK-001 | Implement FR-001 and FR-002 against the frozen Java interface. | Candidate `src/AuthService.java` only | Companion source, contract, acceptance checks |
| TASK-002 | Independently inspect scope, compile/run checks, and judge AC-001 through AC-004. | A new evidence report | Current candidate, contract, acceptance checks |
| TASK-003 | Record failed ACs, evidence, and the next action. | The delivery's loop record | Verifier receipt and specifications |

The path boundary is relative to the copied candidate workspace and declared in [contract.json](contract.json). These roles explain how to adapt the example to a real delivery. The demo replays authored files instead of assigning these tasks to models.

## Dependencies and completion

TASK-002 requires the current TASK-001 candidate. TASK-003 requires the independent receipt. Verification is repeated after any candidate change; an earlier receipt cannot stand in for the new result.

An implementation report may include changed files, checks, and limitations, but its completion claim does not decide acceptance. The judge checks frozen-input integrity, the complete source manifest, compile/runtime results, and evidence freshness.

For failures, use the next action attached to the scenario in [README.md](README.md). The example has no automatic retry budget or autonomous rework controller; a successful replay proves only that these verifier scenarios behave as expected.
