## Why

<!-- What concrete failure mode or user need does this change address? -->

## What changed

<!-- Summarize behavior, documentation, examples, and packaging changes. -->

## Evidence

<!-- Paste validation commands and concise results. -->

## Checklist

- [ ] I changed `spec-driven-loop/`, not the generated plugin mirror directly.
- [ ] I ran `pwsh -File scripts/sync-plugin-skill.ps1` when the authoritative skill changed.
- [ ] I ran `python scripts/validate_repo.py` successfully.
- [ ] I updated both Chinese and English public docs when public behavior changed.
- [ ] I preserved the explicit specification approval gate.
- [ ] I preserved main-agent independent acceptance.
- [ ] I removed secrets, personal data, private paths, and proprietary code.
