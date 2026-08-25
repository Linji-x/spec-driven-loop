# Spec-Driven Loop

[简体中文](README.md) · [English](README.en.md)

![Spec-Driven Loop: Inspect, Grill, Freeze, Agents, Judge, Loop](docs/assets/workflow.svg)

[![Release](https://img.shields.io/github/v/release/Linji-x/spec-driven-loop?display_name=tag&sort=semver)](https://github.com/Linji-x/spec-driven-loop/releases/latest)
[![CI](https://github.com/Linji-x/spec-driven-loop/actions/workflows/validate.yml/badge.svg)](https://github.com/Linji-x/spec-driven-loop/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/github/license/Linji-x/spec-driven-loop)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/Linji-x/spec-driven-loop?style=flat)](https://github.com/Linji-x/spec-driven-loop/stargazers)
[![Last commit](https://img.shields.io/github/last-commit/Linji-x/spec-driven-loop)](https://github.com/Linji-x/spec-driven-loop/commits/main)

**Freeze the specification before parallel development. Let the main agent judge delivery from evidence.**

Spec-Driven Loop is a development skill for Codex. It turns an uncertain, medium-to-large software request into an approvable PRD, technical design, and acceptance contract; coordinates implementation; and makes the main agent independently verify the result. If the chat stops, `LOOP.md` preserves the evidence, judgment, and next action.

## Install in 30 seconds

Invoke the built-in Skill Installer in Codex:

```text
$skill-installer Install https://github.com/Linji-x/spec-driven-loop/tree/v1.0.0/spec-driven-loop
```

Then call the skill explicitly:

```text
$spec-driven-loop Build a Job Dashboard with filters, pagination, and role-based access
```

Codex usually detects a newly installed skill automatically. Restart only if `$spec-driven-loop` does not appear. See the official [OpenAI Skills documentation](https://developers.openai.com/codex/skills) for current installation and discovery behavior.

## The problem it solves

Many AI coding failures are specification failures: product choices get guessed, shared interfaces change during parallel work, and an agent's “done” report is mistaken for acceptance.

Spec-Driven Loop gives each fact one durable owner:

| Artifact | Authoritative responsibility |
| --- | --- |
| `PRD.md` | Problem, users, product behavior, and business rules |
| `TECH_DESIGN.md` | Architecture, interfaces, data, security, and operations |
| `ACCEPTANCE.md` | Observable pass/fail proof for every frozen requirement |
| `AGENT_PLAN.md` | Dependencies, file ownership, task contracts, and validation |
| `LOOP.md` | Current state, evidence, main-agent judgment, rework, and next action |

## The loop

```text
Inspect ──► Grill ──► Freeze ──► Agents ──► Judge
   ▲                                               │
   └──────────────── Loop / Rework ◄───────────────┘
```

1. **Inspect** the repository, architecture, interfaces, tests, and conventions before asking questions.
2. **Grill** only consequential product or technical decisions, one small frontier at a time.
3. **Freeze** the PRD, technical design, and acceptance contract; production code waits for explicit approval.
4. **Agents** implement against frozen shared interfaces with dependency-aware, non-overlapping file ownership.
5. **Judge** means the main agent inspects the diff, runs validation, and maps evidence to every acceptance criterion.
6. **Loop** sends code defects to focused rework and requirement changes back through specification approval.

No subagents? The main agent can execute the same `AGENT_PLAN.md` serially without lowering the acceptance bar.

## When to use it

Use it for:

- new products, cross-module features, or substantial refactors;
- work that needs a PRD, technical design, acceptance criteria, and a recoverable execution record;
- multi-agent delivery, shared interfaces, migrations, permissions, or high rework risk;
- teams that want evidence-backed acceptance instead of self-reported completion.

Skip it for:

- tiny bug fixes, single-file edits, explanations, or review-only work;
- pure research, disposable scripts, or simple tasks with an already complete specification;
- requests where the goal is code generation without agreeing on scope or acceptance.

## Usage

### Start from an uncertain request

```text
$spec-driven-loop Add team invitations, role permissions, and member audit logs to the existing SaaS product
```

The skill inspects the system, drafts the specification, and asks only the decisions you actually own. Implementation starts after you explicitly approve the frozen specification and acceptance contract.

### Resume existing work

```text
$spec-driven-loop Read docs/spec-driven/team-invites/, verify the approved specs, and resume from LOOP.md
```

If the documents remain valid, the skill resumes planning or execution instead of reopening settled questions.

### Request strict acceptance

```text
$spec-driven-loop Independently judge this delivery. Report every AC, its evidence, result, and gap; do not accept agent self-reporting.
```

## Worked example: Job Dashboard

The [anonymized synthetic case study](examples/job-dashboard/README.md) shows a Job Dashboard moving from a frozen request to final acceptance. It includes the complete [PRD](examples/job-dashboard/PRD.md), [technical design](examples/job-dashboard/TECH_DESIGN.md), [acceptance contract](examples/job-dashboard/ACCEPTANCE.md), [agent plan](examples/job-dashboard/AGENT_PLAN.md), [execution loop](examples/job-dashboard/LOOP.md), and final evidence matrix.

It is derived from a completed forward test and contains no real customer, account, or private source code.

## Other installation options

### Manual

Copy `spec-driven-loop/` into the official user-level skill directory:

```text
$HOME/.agents/skills/spec-driven-loop
```

The repository's `spec-driven-loop/` directory is always the authoritative, independently installable skill.

### Plugin (Preview)

Codex versions that support Plugin Marketplace can add this repository:

```text
codex plugin marketplace add Linji-x/spec-driven-loop --ref v1.0.0
```

Then install **Spec-Driven Loop** from the desktop **Plugins Directory**. The maintainer's current local CLI does not yet expose `codex plugin`, so this route is labeled **Preview**. It is not the primary installation method, and we do not claim end-to-end verification across all environments. The package follows the official [OpenAI Plugin packaging documentation](https://developers.openai.com/plugins/build/plugins).

The plugin skill is generated from the authoritative standalone directory, and CI rejects drift.

## Upgrade and uninstall

- Upgrade by rerunning the stable install command or replacing the directory with the archive from the [latest release](https://github.com/Linji-x/spec-driven-loop/releases/latest).
- Keep `tree/v1.0.0` in the URL for a pinned installation; change the tag explicitly when upgrading.
- Uninstall by removing `$HOME/.agents/skills/spec-driven-loop`. Plugin users can uninstall from the Plugins Directory.

## FAQ

<details>
<summary><strong>Does every project need multiple agents?</strong></summary>

No. Agent coordination is an execution option, not a dependency. A single main agent can execute the plan serially while preserving specification approval, file ownership, and independent acceptance.
</details>

<details>
<summary><strong>Why not let the agent code immediately?</strong></summary>

For medium-to-large work, expensive mistakes usually come from boundaries and interfaces rather than typing speed. Frozen specs give implementation and acceptance one stable target. Small changes should skip this skill.
</details>

<details>
<summary><strong>Does the “Grill” stage require another skill?</strong></summary>

No. The questioning method is inspired by Matt Pocock's MIT-licensed `grill-me` / `grilling` decision-tree and frontier approach, but this skill is self-contained.
</details>

<details>
<summary><strong>How do I resume after interruption?</strong></summary>

Invoke the skill again and point it to the relevant `LOOP.md`. The durable documents preserve the frozen state, evidence, judgment, unresolved risks, and next action.
</details>

<details>
<summary><strong>Why does it not trigger implicitly?</strong></summary>

It contains an explicit approval gate and is intentionally unsuitable for small tasks. Invoke it with `$spec-driven-loop ...`.
</details>

## Contributing

Bug reports, workflow improvements, and real case studies are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting a change. If you modify the authoritative skill, run the sync and validation commands so the plugin mirror remains identical.

Use [Discussions](https://github.com/Linji-x/spec-driven-loop/discussions) for Q&A, ideas, and show-and-tell examples.

## Roadmap

- Collect more reproducible, anonymized delivery cases.
- Improve the decision frontier and evidence templates from community feedback.
- Complete end-to-end installation checks in more Plugin Marketplace environments.
- Aim for 100 stars in the first 30 days. This is a transparent growth goal, not a promised outcome.

## License and credits

[MIT License](LICENSE). The requirements-clarification approach is inspired by Matt Pocock's MIT-licensed `grill-me` / `grilling` work and redesigned here around specification freezing, agent coordination, and independent acceptance.

If this loop saves you from one expensive rework cycle, consider leaving a ⭐. A real use case or thoughtful issue is even more valuable.
