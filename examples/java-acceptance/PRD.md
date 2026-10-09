# Java acceptance example: product contract

Status: Example frozen input, version 1  
Provenance: Authored demonstration fixture; no historical user approval is asserted

## Goal

Make independent acceptance reproducible: compile and run frozen Java checks, reject failing or out-of-scope candidates, and reject evidence that belongs to an earlier candidate.

## Requirements

| FR ID | Required behavior |
| --- | --- |
| FR-001 | `AuthService.authenticateToken(String token)` accepts the exact prefix `usr-` with a nonempty suffix. |
| FR-002 | The method rejects `null`, an empty string, a wrong prefix, and bare `usr-`. |
| FR-003 | Acceptance uses frozen checks and real compiler/runtime exit codes; completion text is only a claim. |
| FR-004 | Candidate changes stay within the declared source boundary, and evidence is bound to current source, contract, and tests. |
| FR-005 | Seven predefined scenarios replay without models, credentials, downloaded Java dependencies, or network calls. |

The suffix rule means at least one character, with no additional trimming, identity lookup, or credential verification requirement. Expanding that rule would change this example contract.

## Scope and success

In scope: a minimal Java method, a Python verifier, frozen Java checks, evidence receipts, and deterministic failure scenarios.

Production authentication, live agent orchestration, provider selection, and model-quality measurement are outside this example. Success means each scenario produces its expected verdict and the correct patch meets [AC-001 through AC-004](ACCEPTANCE.md). It does not mean every candidate passes.

For a real project, product approval and its provenance belong to that project's current specifications. This fixture is not evidence that anyone approved a production change.
