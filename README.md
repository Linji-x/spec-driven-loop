# Spec-Driven Loop

`spec-driven-loop` is an explicit-invocation Codex skill for medium-to-large software work. It turns uncertain requests into an approved product specification, technical design, acceptance contract, coordinated multi-agent implementation, and evidence-backed main-agent judgment.

## What it enforces

- Inspect the existing system before asking the user questions.
- Treat discoverable facts as the agent's responsibility and consequential decisions as the user's.
- Draft and progressively grill `PRD.md` and `TECH_DESIGN.md` with a dependency-tree frontier.
- Keep uncertainty visible as `TBD`, `ASSUMPTION`, or `BLOCKED`.
- Freeze stable `FR-*` requirements and `AC-*` acceptance criteria.
- Require explicit user approval before production code is written.
- Assign exact, non-overlapping file ownership and freeze shared contracts before parallel work.
- Treat subagent reports as evidence, never as project acceptance.
- Maintain a recoverable, append-only `LOOP.md`.
- Require the main agent to inspect actual changes, run system-level checks, and judge every blocking acceptance criterion.
- Stop automatic rework after the same acceptance criterion fails three consecutive loops.

## Workflow

1. Inspect repository rules, architecture, interfaces, data, tests, and deployment.
2. Draft and grill the product requirements.
3. Draft and grill the technical design.
4. Freeze the acceptance contract and request implementation approval.
5. Create the agent plan and recoverable delivery loop.
6. Execute independently verifiable slices with bounded ownership.
7. Integrate and judge the implementation against observable evidence.
8. Deliver the acceptance matrix, evidence, caveats, and remaining risks.

## Install

Ask Codex to install the skill from the skill folder in this repository:

```text
$skill-installer Install https://github.com/Linji-x/spec-driven-loop/tree/main/spec-driven-loop
```

For a manual installation, copy the `spec-driven-loop/` directory into the user skills directory configured by your Codex installation.

## Use

The skill is explicit-only. Invoke it with `$spec-driven-loop`:

```text
$spec-driven-loop Design and implement resumable batch uploads for the existing RAG service.
```

The skill will stop for product or technical decisions when necessary and will not modify production code until the specification is explicitly approved.

## Skill contents

```text
spec-driven-loop/
├── SKILL.md
├── agents/
│   └── openai.yaml
└── references/
    ├── document-templates.md
    └── agent-and-judge-contracts.md
```

## Validation

The skill is validated with Codex's `skill-creator` `quick_validate.py` and has been forward-tested in isolated repositories for:

- an ambiguous Spring Boot RAG batch-upload request, where it inspected the system, drafted the PRD, exposed a decision frontier, and refused premature coding;
- a frozen multi-agent feature, where it froze shared contracts, delegated non-overlapping work, independently ran the full acceptance gate, and recorded an `ACCEPTED` loop.

## Attribution

The requirements-grilling stage is informed by Matt Pocock's MIT-licensed `grill-me` / `grilling` decision-tree and frontier method. The skill is self-contained and does not require either project at runtime.

## License

MIT — see [LICENSE](LICENSE).
