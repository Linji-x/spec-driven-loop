# Spec-Driven Loop GitHub Launch Acceptance Contract

Status: Frozen
Based on PRD/Tech Design: 2026-08-25
Approval: Approved by the user on 2026-08-25

## Scope Boundaries

### In Scope

FR-001 through FR-007 and their repository, release, GitHub configuration, local campaign, and catalog-submission outputs.

### Out of Scope

Paid promotion, fake engagement, posting through the user’s social accounts, and guaranteed star acquisition.

### Non-goals

Changing Skill behavior, claiming untested agent compatibility, or bypassing external catalog rules.

### Deferred

VoltAgent submission until credible community usage exists; Day 3/7/14/30 metric collection occurs after launch.

### Assumptions

The approved repository, version, installation commands, visual direction, and outreach targets remain unchanged.

### Release Blockers

AC-001 through AC-007 are blocking. AC-008 is a non-blocking operating metric.

### Definition of Done

The launch PR is merged with green checks; GitHub metadata and community settings are updated; `v1.0.0` and three verified assets are public; a tag-based isolated Skill install succeeds; two rule-compliant catalog PRs are opened or a rule-based documented deferral replaces an invalid submission; the local launch kit and Day 0 scorecard exist; the final acceptance matrix is recorded in `LOOP.md`.

## Acceptance Criteria

### AC-001 — README communicates and converts
- Related FRs: FR-001, FR-002
- Blocking: Yes
- Scenario: A new visitor opens the repository.
- Preconditions: GitHub renders the default README.
- Action/event: Inspect the first viewport and navigate all primary sections.
- Expected result: Chinese-first page, English switch, technical value proposition, real badges, stable install prompt, invocation example, scope, workflow, outputs, worked example, FAQ, contribution, attribution, license, and non-manipulative Star CTA are present.
- Required evidence: Rendered README inspection and automated relative-link check.

### AC-002 — Standalone Skill remains valid and installable
- Related FRs: FR-002, FR-003
- Blocking: Yes
- Scenario: A user installs the tagged standalone Skill.
- Preconditions: Public `v1.0.0` tag exists.
- Action/event: Run the bundled `install-skill-from-github.py` into an isolated destination and validate the result.
- Expected result: Installation succeeds, the expected files and branding metadata exist, `quick_validate.py` passes, and explicit invocation remains required.
- Required evidence: Installer output, installed tree, validation output, and `openai.yaml` inspection.

### AC-003 — Plugin and Marketplace are structurally valid
- Related FRs: FR-002, FR-006
- Blocking: Yes
- Scenario: The repository Plugin distribution is inspected and packaged.
- Preconditions: Canonical Skill is synchronized into the Plugin.
- Action/event: Compare mirrors and run Plugin validation.
- Expected result: All canonical Skill files match byte-for-byte; valid `plugin.json` and marketplace metadata exist; Plugin is version `1.0.0`; no unsupported components or TODO placeholders exist.
- Required evidence: Hash comparison, JSON inspection, `validate_plugin.py` output, archive file list.

### AC-004 — Visual assets are correct and usable
- Related FRs: FR-003
- Blocking: Yes
- Scenario: GitHub and Codex render the branding assets.
- Preconditions: Vector and PNG assets are generated.
- Action/event: Inspect source and rendered images.
- Expected result: Workflow order is correct; images are legible in light/dark contexts; Skill icon paths resolve; social preview is exactly 1280×640 and is uploaded to repository settings.
- Required evidence: Image dimensions, file-path checks, rendered preview inspection, GitHub settings confirmation.

### AC-005 — Example, community files, and CI are complete
- Related FRs: FR-004, FR-005
- Blocking: Yes
- Scenario: A reviewer explores the repository or opens a contribution.
- Preconditions: Launch branch content is complete.
- Action/event: Inspect the worked example, templates, and CI run.
- Expected result: All five example documents and an acceptance matrix exist; Bug/Feature and PR templates are usable; CI validates Skill, Plugin, mirrors, paths, images, packages, and checksums; all checks pass.
- Required evidence: File list, content inspection, CI run URL and conclusion.

### AC-006 — GitHub release and settings are live
- Related FRs: FR-005, FR-006
- Blocking: Yes
- Scenario: A public user visits the merged repository.
- Preconditions: Launch PR checks pass.
- Action/event: Inspect repository metadata, settings, tag, and release.
- Expected result: Description/topics are updated; Issues and Discussions are enabled; Wiki/Projects are disabled; merge settings favor squash and branch cleanup; `v1.0.0` points to the merged commit and exposes all three named assets with bilingual notes.
- Required evidence: GitHub API snapshots, tag/release URL, asset list, and checksum verification.

### AC-007 — Ethical launch distribution is ready
- Related FRs: FR-007
- Blocking: Yes
- Scenario: Launch outreach is prepared and executed.
- Preconditions: `v1.0.0` is public.
- Action/event: Submit to compatible catalogs and build the local campaign package.
- Expected result: Composio and sickn33 PRs follow current rules and link/source the release; VoltAgent is deferred; local GitHub Discussion/V2EX/掘金/知乎/X copy and scorecard exist; no external social post is made.
- Required evidence: PR URLs or documented rule-based deferral, local file list, Day 0 snapshot.

### AC-008 — Thirty-day growth target
- Related FRs: FR-007
- Blocking: No
- Scenario: The campaign runs for 30 days.
- Preconditions: Launch completes.
- Action/event: Record scheduled metric snapshots.
- Expected result: Progress toward 100 stars is measurable without manipulative promotion.
- Required evidence: Day 3/7/14/30 scorecard entries.

## Coverage Map

| FR ID | AC IDs | Coverage notes |
| --- | --- | --- |
| FR-001 | AC-001 | README and language parity |
| FR-002 | AC-001, AC-002, AC-003 | Installation and distribution |
| FR-003 | AC-002, AC-004 | Skill/UI branding and social preview |
| FR-004 | AC-005 | Complete worked example |
| FR-005 | AC-005, AC-006 | Community, CI, and repository settings |
| FR-006 | AC-003, AC-005, AC-006 | Plugin and release assets |
| FR-007 | AC-007, AC-008 | Ethical distribution and measurement |
