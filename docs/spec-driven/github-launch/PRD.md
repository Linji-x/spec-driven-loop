# Spec-Driven Loop GitHub Launch Product Requirements

Status: Frozen
Owner: Linji-x
Last updated: 2026-08-25
Approval: Approved by the user on 2026-08-25 via “PLEASE IMPLEMENT THIS PLAN”

## Problem and Context

The repository contains a validated Codex Skill, but its current GitHub presentation is English-only, has no release, no worked example, no visual identity, no community entry points, and no distribution path beyond a short installer prompt. The launch must make the value legible in seconds and provide verifiable installation paths without changing the workflow’s behavior.

## Users and Stakeholders

- Primary: Chinese-speaking Codex users handling medium-to-large software work.
- Secondary: International Codex and agent-skill users.
- Maintainer: `Linji-x`.
- External curators: compatible Codex and agent-skill catalogs.

## Product Goals

- Communicate the differentiator: freeze the specification before code, then let the main agent judge delivery from evidence.
- Make a stable standalone Skill install possible in under 30 seconds.
- Offer a standards-aligned Plugin/Marketplace preview without making it the primary install path.
- Prove the workflow with a complete synthetic worked example.
- Establish a credible open-source release and contribution surface.

## Success Metrics

| Metric | Baseline | Target | Measurement window/source |
| --- | --- | --- | --- |
| GitHub stars | 0 | 100 | Day 30, GitHub repository metadata |
| Unique views | 0 | Track trend | Day 0/3/7/14/30, GitHub traffic API |
| Unique clones | 0 | Track trend | Day 0/3/7/14/30, GitHub traffic API |
| Public release | None | `v1.0.0` live | GitHub Releases |
| External catalog submissions | 0 | 2 valid PRs | GitHub pull requests |

The 100-star target is an operating goal, not a guaranteed implementation outcome or release blocker.

## User Flows

1. A visitor understands the loop and its intended use from the first README viewport.
2. A Codex user copies the stable installer prompt, installs from the `v1.0.0` tag, and invokes `$spec-driven-loop`.
3. A reviewer opens the worked example and inspects the five durable workflow documents and acceptance matrix.
4. A plugin-enabled user adds the repository marketplace and installs the Plugin preview.
5. A contributor uses the issue or PR templates to report a defect or propose an improvement.

## Functional Requirements

| FR ID | Requirement | Priority | Status | Notes |
| --- | --- | --- | --- | --- |
| FR-001 | Publish a Chinese-first README and complete English mirror with a sharp above-the-fold value proposition, installation, usage, scope, workflow, example, FAQ, attribution, contribution, and star CTA. | Must | Frozen | Core positioning is fixed by the approved plan. |
| FR-002 | Provide a stable Skill install from `v1.0.0`, manual installation guidance, explicit invocation guidance, and an accurately caveated Plugin preview. | Must | Frozen | Standalone Skill remains primary. |
| FR-003 | Provide a consistent technical-loop visual system, including README vector art, Skill metadata icons, and a 1280×640 social preview. | Must | Frozen | No generated human imagery. |
| FR-004 | Publish one complete, synthetic Job Dashboard worked example containing all five workflow documents and a visible final acceptance matrix. | Must | Frozen | Derived from isolated forward tests; no personal data. |
| FR-005 | Add validation CI, contribution guidance, issue/PR templates, Discussions, focused repository metadata, and clean merge settings. | Must | Frozen | Issues and Discussions stay enabled; unused Wiki/Projects are disabled. |
| FR-006 | Publish `v1.0.0` with standalone Skill and Plugin archives plus SHA-256 checksums and bilingual release notes. | Must | Frozen | Asset names are contractually fixed. |
| FR-007 | Submit valid catalog PRs to Composio and sickn33, prepare but do not post Chinese campaign copy, and create a Day 0/3/7/14/30 scorecard. | Must | Frozen | VoltAgent submission is deferred until real adoption exists. |

## Business Rules

- Never buy, automate, trade, or spam for stars.
- Do not claim Plugin end-to-end compatibility on surfaces where the command is unavailable.
- Do not weaken or rewrite the Skill’s specification/approval/judgment behavior for marketing.
- External submissions must follow each catalog’s current contribution rules.

## Data Lifecycle

- Repository source, release artifacts, PRs, and Discussions are public.
- Traffic snapshots and campaign drafts remain project-scoped under `<project-workspace>/spec-driven-loop-launch`.
- No secrets, tokens, user data, or private repository information may enter committed files or release archives.

## In Scope

- Repository content, metadata, settings, release, two catalog PRs, and local campaign materials described above.

## Out of Scope

- Paid promotion, fake engagement, posting from the user’s social accounts, a standalone marketing website, or guaranteed star acquisition.

## Non-goals

- Changing the core delivery workflow.
- Supporting every coding agent or claiming compatibility that was not tested.
- Submitting to VoltAgent before its maturity requirement is met.

## Assumptions

| ID | Assumption | Risk | Validation plan | Status |
| --- | --- | --- | --- | --- |
| ASM-001 | The public GitHub repository remains `Linji-x/spec-driven-loop`. | Low | Verify before every remote mutation. | Accepted |
| ASM-002 | `v1.0.0` is the first stable public release. | Low | Confirm no tags/releases exist. | Verified |
| ASM-003 | Plugin CLI availability is staged and may be absent locally. | Medium | Test local CLI; label Plugin route Preview if absent. | Verified absent locally |

## Open Product Decisions

None. The approved launch plan fixed positioning, language, visual direction, distribution shape, version, outreach scope, and 30-day target.

## Decision Log

| Decision ID | Decision | Rationale | Decider/date | Impacted FRs |
| --- | --- | --- | --- | --- |
| DEC-001 | Chinese-first README with English mirror. | Prioritize the target audience without blocking global discovery. | User, 2026-08-25 | FR-001 |
| DEC-002 | Technical loop visual. | Makes the workflow differentiator immediately understandable. | User, 2026-08-25 | FR-003 |
| DEC-003 | Dual Skill + Plugin distribution, Skill primary. | Preserve the proven install path while preparing modern distribution. | User, 2026-08-25 | FR-002, FR-006 |
| DEC-004 | Release as `v1.0.0`. | The workflow and forward tests are already complete. | User, 2026-08-25 | FR-006 |
| DEC-005 | Open valid external catalog PRs directly. | Increase qualified discovery without spam. | User, 2026-08-25 | FR-007 |
