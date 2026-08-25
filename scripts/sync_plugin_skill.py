"""Synchronize the authoritative standalone skill into the plugin mirror."""

from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "spec-driven-loop").resolve()
PLUGIN_ROOT = (ROOT / "plugins" / "spec-driven-loop").resolve()
TARGET = (PLUGIN_ROOT / "skills" / "spec-driven-loop").resolve()


def is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def main() -> None:
    if not (SOURCE / "SKILL.md").is_file():
        raise SystemExit(f"Authoritative skill is missing: {SOURCE}")
    if not is_within(TARGET, PLUGIN_ROOT) or TARGET == PLUGIN_ROOT:
        raise SystemExit(f"Refusing unsafe mirror target: {TARGET}")

    if TARGET.exists():
        shutil.rmtree(TARGET)
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SOURCE, TARGET)
    print(f"Synced {SOURCE} -> {TARGET}")


if __name__ == "__main__":
    main()
