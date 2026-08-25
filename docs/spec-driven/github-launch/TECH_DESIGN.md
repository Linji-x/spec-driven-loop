# Spec-Driven Loop GitHub Launch Technical Design

Status: Frozen
Based on PRD: 2026-08-25
Owner: Main agent
Approval: Approved by the user on 2026-08-25

## Current System State

- Public repository: `Linji-x/spec-driven-loop`, default branch `main`.
- Canonical Skill: `spec-driven-loop/` with `SKILL.md`, `agents/openai.yaml`, and two references.
- Repository root contains only the Skill, README, and MIT license.
- Baseline: 0 stars, 0 views, 0 clones, no releases, Discussions disabled, Wiki/Projects enabled.
- Local `codex` build does not expose `codex plugin`; Plugin installation must be labeled Preview.

## Overall Approach

Implement on `docs/launch-v1` from `origin/main`, commit and push, open a self-review PR, require green checks, squash-merge, then tag and release the merged commit. Keep the standalone Skill authoritative. Generate the Plugin mirror deterministically and fail CI on drift.

## Modules and Responsibilities

| Module | Responsibility | Related FRs | Owned contracts |
| --- | --- | --- | --- |
| README and brand assets | Positioning, installation, usage, diagrams, language parity | FR-001, FR-003 | Stable install/invocation copy |
| Canonical Skill metadata | Installed appearance without behavior changes | FR-002, FR-003 | `allow_implicit_invocation: false` |
| Plugin and Marketplace | Preview packaging and discoverability | FR-002, FR-006 | Plugin name/version/path/policy |
| Example | Evidence that the workflow produces durable, reviewable artifacts | FR-004 | Five document names and stable IDs |
| Validation and release scripts | Mirror, validation, packaging, checksums | FR-005, FR-006 | Archive names and contents |
| GitHub configuration | Metadata, community surfaces, PR merge/release | FR-005, FR-006 | `main`, `v1.0.0` |
| Outreach workspace | Campaign copy, scorecard, catalog forks/PRs | FR-007 | No social posting authority |

## Interface Contracts

- Stable Skill install prompt: `$skill-installer Install https://github.com/Linji-x/spec-driven-loop/tree/v1.0.0/spec-driven-loop`.
- Latest-development install prompt may use `main`, but it is secondary.
- Manual user scope documented as `$HOME/.agents/skills/spec-driven-loop`, with a note that the bundled installer may use the installation’s configured Codex home.
- Invocation: `$spec-driven-loop <medium-to-large software request>`.
- Plugin ID and outer folder: `spec-driven-loop`.
- Repository marketplace entry: `./plugins/spec-driven-loop`, `AVAILABLE`, `ON_INSTALL`, category `Developer Tools`.
- Release assets: `spec-driven-loop-skill-v1.0.0.zip`, `spec-driven-loop-plugin-v1.0.0.zip`, `SHA256SUMS.txt`.

## Data Model and Migration

No runtime data model or migration. Repository structure expands with docs, examples, assets, Plugin/Marketplace files, validation scripts, and GitHub templates.

## State Transitions

`origin/main → docs/launch-v1 → PR checks green → squash merge → v1.0.0 tag/release → catalog PRs → Day 0 scorecard`.

## Concurrency, Consistency, and Idempotency

- Work is serialized by the main agent; no subagents are authorized.
- `scripts/sync-plugin-skill.ps1` replaces the Plugin mirror from the canonical Skill and is safe to rerun.
- `scripts/build-release.ps1` recreates a clean output directory and deterministic archive names.
- Validation compares file paths and SHA-256 hashes between canonical and Plugin copies.

## Authentication, Authorization, Privacy, and Security

- Use the existing authenticated GitHub account only for repositories in the approved plan.
- Never print credentials or place them in files.
- Release archives are assembled from allowlisted directories and inspected before upload.
- Synthetic examples are scrubbed of machine-specific commands, private paths, and personal data.

## Failures, Retry, Recovery, and Degradation

- CI failure: do not merge or release; append evidence to `LOOP.md` and repair only failed ACs.
- Plugin CLI absent: retain the Preview label and validate structure without claiming installation success.
- Social preview API unavailable: upload through the authenticated GitHub web settings surface.
- Catalog rule mismatch: do not force submission; report and defer that catalog.
- External PR validation failure: keep the PR open only if bounded repair is possible; otherwise close with an honest explanation.

## Performance and Capacity

README assets should remain lightweight; PNG social preview is exactly 1280×640. CI targets a small repository and should complete in a few minutes.

## Observability: Logs, Metrics, and Alerts

- GitHub Actions logs are the release gate.
- Local launch scorecard records Day 0/3/7/14/30 stars, views, clones, referrers, PR status, and feedback.
- No recurring automation is created without a separate user request.

## Compatibility

- Standalone Skill: ChatGPT desktop/Codex surfaces that support local skills and the bundled Skill Installer.
- Plugin: only plugin-enabled Codex/ChatGPT surfaces; explicitly Preview until end-to-end tested.
- Markdown and SVG must render on GitHub in light and dark themes.

## Release and Rollback

- Release from the squash-merged `main` commit.
- If release assets are wrong, replace them only after rebuilding and revalidating; do not silently retag a different commit.
- Repository content rollback uses a normal revert PR, never history rewriting.

## Test Boundaries

- Skill validation with Codex `quick_validate.py`.
- Plugin validation with `plugin-creator/scripts/validate_plugin.py`.
- Exact mirror comparison, Markdown link/path checks, JSON/YAML parse, PNG dimensions, archive allowlist, and SHA-256 verification.
- Public tag install into an isolated destination with `skill-installer`.
- GitHub remote inspection after merge/release.

## Alternatives Considered

- Plugin-only distribution: rejected because the local Plugin CLI is unavailable and the current Skill path already works.
- Custom Plugin path without mirror: rejected because the current validator requires `skills/`.
- Symlinked mirror: rejected for GitHub archive and Windows portability.
- AI-generated hero illustration: rejected in favor of a deterministic technical diagram.

## Blocked Technical Issues

None. Plugin end-to-end installation is non-blocking when the current surface lacks the command, provided the Preview caveat remains.

## Technical Decision Log

| Decision ID | Decision | Alternatives | Rationale | Related FRs |
| --- | --- | --- | --- | --- |
| TDEC-001 | Keep a canonical Skill and generated Plugin mirror. | Move, symlink, custom path | Preserves existing URL and passes Plugin schema. | FR-002, FR-006 |
| TDEC-002 | Generate vector artwork deterministically and render PNG. | Image generation | Ensures text accuracy, reproducibility, and brand consistency. | FR-003 |
| TDEC-003 | Pin release installation to `v1.0.0`. | `main` only | Gives users a stable, immutable install source. | FR-002, FR-006 |
