# Spec-Driven Loop GitHub Launch Agent Plan

Status: Frozen
Specification approval reference: `PRD.md`, `TECH_DESIGN.md`, and `ACCEPTANCE.md`, approved 2026-08-25
Shared contracts frozen at: `origin/main` commit `675e22b9c9b993a250678bbced24f3e3a40545ec`
Plan owner: Main agent

No subagents are assigned. The main agent executes the tasks serially because the user did not authorize delegation and several release files share version and branding contracts.

## Frozen Shared Contracts

| Contract/type/schema | Location | Owner | Change approval rule |
| --- | --- | --- | --- |
| Canonical Skill behavior | `spec-driven-loop/SKILL.md` and references | Main agent | Marketing work must not change behavior. |
| Explicit invocation policy | `spec-driven-loop/agents/openai.yaml` | Main agent | Must remain `false` for implicit invocation. |
| Plugin identity and version | `plugins/spec-driven-loop/.codex-plugin/plugin.json` | Main agent | Name `spec-driven-loop`, version `1.0.0`. |
| Release asset names | Release scripts and Acceptance AC-006 | Main agent | Must match the three frozen filenames. |
| Stable installation URL | README language variants | Main agent | Must use the `v1.0.0/spec-driven-loop` tree URL. |

## Dependency Graph

`TASK-001 → TASK-002 → TASK-003 → TASK-004 → TASK-005`.

## Ownership Map

| Task ID | Allowed paths | Forbidden paths | Overlap check |
| --- | --- | --- | --- |
| TASK-001 | `docs/spec-driven/github-launch/**` | Existing Skill behavior | Specification only |
| TASK-002 | README variants, `docs/assets/**`, `examples/**`, `CONTRIBUTING.md`, `.github/**`, Skill metadata/assets | Skill instruction body and references | Branding/docs stage |
| TASK-003 | `plugins/**`, `.agents/plugins/**`, `scripts/**`, validation workflow | GitHub remote settings and external repos | Packaging stage |
| TASK-004 | Git branch/PR, repository settings, tag/release | External catalogs | Remote launch stage |
| TASK-005 | `<project-workspace>/spec-driven-loop-launch/**` and approved catalog forks | Source repository after release except bounded fixes | Outreach stage |

## Tasks

### TASK-001 — Freeze durable launch documents
- Objective: Record approved product, technical, acceptance, execution, and recovery contracts.
- Related FRs: FR-001 through FR-007
- Related ACs: AC-001 through AC-008
- Inputs: Approved implementation plan and inspected repository/GitHub state.
- Dependencies: None.
- Allowed files/directories: `docs/spec-driven/github-launch/**`.
- Forbidden files/directories: All other paths.
- Required outputs: Five durable documents.
- Required checks: Cross-reference IDs and approval state.
- Required evidence: Git diff and document inspection.
- Stop and report when: The approved plan is ambiguous or conflicts with repository facts.

### TASK-002 — Build public documentation, visuals, example, and community surface
- Objective: Implement FR-001, FR-003, FR-004, and repository-file portions of FR-005.
- Related FRs: FR-001, FR-003, FR-004, FR-005
- Related ACs: AC-001, AC-004, AC-005
- Inputs: Frozen launch documents and synthetic forward-test artifacts.
- Dependencies: TASK-001.
- Allowed files/directories: README variants, `docs/assets/**`, `examples/**`, `CONTRIBUTING.md`, `.github/**`, `spec-driven-loop/agents/openai.yaml`, `spec-driven-loop/assets/**`.
- Forbidden files/directories: `spec-driven-loop/SKILL.md`, `spec-driven-loop/references/**`, Plugin/package paths.
- Required outputs: Bilingual READMEs, brand system, full example, contribution and issue/PR templates.
- Required checks: Relative links, visual rendering, PNG dimensions, core Skill diff restriction.
- Required evidence: File list, image previews, check output.
- Stop and report when: Branding requires a behavior change or example data is not synthetic.

### TASK-003 — Build Plugin, Marketplace, validation, and release packaging
- Objective: Implement FR-002, validation portions of FR-005, and release artifacts for FR-006.
- Related FRs: FR-002, FR-005, FR-006
- Related ACs: AC-002, AC-003, AC-005
- Inputs: Canonical Skill and frozen version/asset contracts.
- Dependencies: TASK-002.
- Allowed files/directories: `plugins/**`, `.agents/plugins/**`, `scripts/**`, validation workflow.
- Forbidden files/directories: Canonical Skill body/references, README content except bounded command corrections.
- Required outputs: Scaffolded Plugin, repo marketplace, deterministic sync/validate/build scripts, CI workflow.
- Required checks: `quick_validate.py`, `validate_plugin.py`, mirror comparison, packaging/checksum verification.
- Required evidence: Command outputs and archive listings.
- Stop and report when: Plugin schema requires changing the canonical Skill or unsupported manifest fields.

### TASK-004 — Integrate, self-review, publish, and configure GitHub
- Objective: Merge a green PR and publish the verified `v1.0.0` release.
- Related FRs: FR-005, FR-006
- Related ACs: AC-001 through AC-006
- Inputs: TASK-002/003 outputs and validation evidence.
- Dependencies: TASK-003.
- Allowed files/directories: `docs/spec-driven/github-launch/LOOP.md` plus approved Git/GitHub state.
- Forbidden files/directories: Unrelated repositories.
- Required outputs: Commit, PR, self-review, squash merge, settings, tag, release, social preview.
- Required checks: CI green, merged SHA inspection, release asset checksum download/verify.
- Required evidence: PR/check/release URLs and GitHub API snapshots.
- Stop and report when: Any blocking AC lacks evidence or the target commit changes unexpectedly.

### TASK-005 — Submit catalogs and prepare campaign workspace
- Objective: Implement FR-007 without spam or unauthorized social posting.
- Related FRs: FR-007
- Related ACs: AC-007, AC-008
- Inputs: Public release URL, current catalog contribution rules, Day 0 traffic baseline.
- Dependencies: TASK-004.
- Allowed files/directories: Stable project workspace and approved catalog forks.
- Forbidden files/directories: Social accounts, VoltAgent submission, unrelated repositories.
- Required outputs: Two valid PRs or documented rule-based deferral, campaign copy, scorecard.
- Required checks: Catalog-specific validation and final link inspection.
- Required evidence: PR URLs, local file list, scorecard snapshot.
- Stop and report when: A catalog rejects new submissions by policy or requires authority beyond a normal PR.

## Integration Order

Execute TASK-001 through TASK-005 serially. Any bounded repair appends a new delivery loop and targets only failed ACs.

## Main-Agent Validation Plan

- Inspect the complete diff and ensure the core Skill instruction body and references are unchanged.
- Run local validation and public tag installation independently.
- Inspect GitHub Actions rather than trusting local-only results.
- Verify every blocking AC with direct evidence and record the final matrix in `LOOP.md`.
