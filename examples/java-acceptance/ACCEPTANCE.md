# Java acceptance example: frozen acceptance contract

Status: Example frozen input, version 1  
Based on: [PRD.md](PRD.md) and [TECH_DESIGN.md](TECH_DESIGN.md)  
Blocking criteria: AC-001 through AC-004

## AC-001 — Accept a valid token

- Related requirement: FR-001.
- Action: Invoke `AuthService.authenticateToken` with the exact prefix `usr-` and a nonempty suffix.
- Pass condition: Return `true` for the valid cases in the frozen checks.
- Evidence: Current verifier receipt with the corresponding Java check results.

## AC-002 — Reject invalid tokens

- Related requirement: FR-002.
- Action: Invoke the method with `null`, an empty string, a wrong prefix, and bare `usr-`.
- Pass condition: Return `false` for every invalid case, without an unhandled exception.
- Evidence: Current verifier receipt with the corresponding Java check results.

## AC-003 — Compile and run unchanged acceptance checks

- Related requirement: FR-003.
- Action: Independently compile the candidate with the frozen Java checks and run those checks.
- Pass condition: Frozen tests are unchanged, compilation exits 0, execution exits 0, all required check results pass, and the harness emits the fresh per-run completion marker. Static PASS text alone is insufficient.
- Evidence: Frozen-test hashes, executed commands, compiler/runtime exit codes, and individual check results. A completion claim alone supplies none of these.

## AC-004 — Enforce scope and current evidence

- Related requirement: FR-004.
- Action: Compare the complete candidate manifest to the write boundary and recompute source, contract, test, and verifier bindings before accepting a receipt.
- Pass condition: Only the allowed implementation file changes; frozen inputs match; the receipt belongs to the current candidate and trusted inputs.
- Evidence: File manifest, hashes, boundary verdict, and receipt freshness result. Reused receipts must be issued unchanged by the same `Verifier` instance; exported reports require fresh verification in a new session.

## Verdict and next action

Accept a candidate only when all blocking criteria pass with current evidence. A failure or an unexecuted check cannot be recorded as a pass. A gate may stop early after a blocking failure; inspect the receipt to determine which checks actually ran.

Use the scenario-specific next actions in [README.md](README.md): correct implementation defects, restore frozen inputs, or regenerate stale evidence. If the desired product behavior changes, update the real project's specification and approval record instead of weakening checks to make a candidate pass.

The replay itself has a separate health condition: every predefined scenario matches its expected verdict. Six intended rejections and one intended acceptance can therefore produce a successful demo run.
