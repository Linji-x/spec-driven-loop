# Spec-Driven Loop GitHub Launch Delivery Loop

Current state: validating
Current loop: LOOP-001
Frozen specification: `PRD.md`, `TECH_DESIGN.md`, `ACCEPTANCE.md` (Approved/Frozen, 2026-08-25)
Current objective: Validate the completed launch package and submit the self-review PR.
Blocking issue: None
Next action: Commit and push `docs/launch-v1`, open the self-review PR, and inspect CI.
Last updated: 2026-08-25

## Current Loop — LOOP-001

- Objective: Deliver FR-001 through FR-007 and collect evidence for AC-001 through AC-007.
- Related FRs/ACs: FR-001–FR-007; AC-001–AC-008.
- Agent assignments: Main agent executes TASK-001 through TASK-005 serially; no subagents authorized.
- Dependencies: Frozen approved plan; clean source repository; GitHub admin access.
- Outputs: Chinese and English READMEs; workflow SVG, Skill icon, 1280×640 social preview; anonymized Job Dashboard example; community templates; Preview Plugin and repository Marketplace; mirror, validation, CI, and release scripts; bilingual release notes.
- Files changed: README/docs/examples/community files; `spec-driven-loop/agents/openai.yaml` and brand assets; generated Plugin/Marketplace; `scripts/**`; `.github/workflows/validate.yml`; frozen launch documents.
- Commands/checks executed: OpenAI `quick_validate.py` on canonical and mirror Skills; official local `validate_plugin.py`; repository link/asset/example/mirror validation; deterministic archive build; ZIP integrity and SHA-256 validation; social image visual inspection.
- Results: Both Skills report `Skill is valid!`; official Plugin validator passes; repository validation passes with and without release packages; PNG dimensions are 1280×640 and 512×512; canonical instruction body and references are unchanged.
- Evidence: Validator exit codes 0; `dist/SHA256SUMS.txt`; archive member inspection; `git diff -- spec-driven-loop/SKILL.md spec-driven-loop/references` empty; rendered social preview.
- Main-agent judgment: Pending
- Failure conditions observed: Local `main` was not the remote history; avoided by branching directly from `origin/main` without rewriting local history.
- Rework requirements: Removed two machine-local paths detected by repository validation; rerun passed.
- Unresolved risks: Plugin CLI is unavailable locally; end-to-end Plugin installation may remain a documented Preview caveat.
- Next state: validating
- Next action: Commit, push, open the PR, and await CI evidence.

## Prior Loops

None.
