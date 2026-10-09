"""Validate repository invariants, public links, examples, assets, and packages."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
import sys
import zipfile
from pathlib import Path
from urllib.parse import unquote

from validate_plugin import validate as validate_plugin


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "spec-driven-loop"
MIRROR = ROOT / "plugins" / "spec-driven-loop" / "skills" / "spec-driven-loop"
PLUGIN = ROOT / "plugins" / "spec-driven-loop"
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
LOCAL_PATH_RE = re.compile(r"\b[A-Za-z]:[\\/](?:Users|computer)[\\/]", re.IGNORECASE)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def tree(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): digest(path)
        for path in sorted(root.rglob("*"))
        if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc"
    }


def check_mirror(errors: list[str]) -> None:
    source_tree = tree(SOURCE)
    mirror_tree = tree(MIRROR)
    if source_tree != mirror_tree:
        source_only = sorted(source_tree.keys() - mirror_tree.keys())
        mirror_only = sorted(mirror_tree.keys() - source_tree.keys())
        changed = sorted(key for key in source_tree.keys() & mirror_tree.keys() if source_tree[key] != mirror_tree[key])
        errors.append(f"plugin skill mirror drift: source-only={source_only}, mirror-only={mirror_only}, changed={changed}")


def check_markdown_links(errors: list[str]) -> None:
    for markdown in sorted(ROOT.rglob("*.md")):
        if any(part in {".git", ".venv", "dist"} for part in markdown.parts):
            continue
        text = markdown.read_text(encoding="utf-8")
        if LOCAL_PATH_RE.search(text) or "fixture user" in text.lower():
            errors.append(f"private or fixture path leaked into {markdown.relative_to(ROOT)}")
        for match in LINK_RE.finditer(text):
            raw = match.group(1).strip()
            if raw.startswith("<") and raw.endswith(">"):
                raw = raw[1:-1]
            target = raw.split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:", "codex://")):
                continue
            target = unquote(target).split(" ", 1)[0]
            resolved = (markdown.parent / target).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(f"link escapes repository in {markdown.relative_to(ROOT)}: {raw}")
                continue
            if not resolved.exists():
                errors.append(f"broken local link in {markdown.relative_to(ROOT)}: {raw}")


def png_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()[:24]
    if len(data) != 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG")
    return struct.unpack(">II", data[16:24])


def check_assets(errors: list[str]) -> None:
    expected = {
        ROOT / "docs" / "assets" / "social-preview.png": (1280, 640),
        SOURCE / "assets" / "icon-512.png": (512, 512),
    }
    for path, dimensions in expected.items():
        try:
            actual = png_dimensions(path)
        except (OSError, ValueError) as exc:
            errors.append(f"invalid PNG {path.relative_to(ROOT)}: {exc}")
            continue
        if actual != dimensions:
            errors.append(f"wrong dimensions for {path.relative_to(ROOT)}: {actual}, expected {dimensions}")
    for path in (ROOT / "docs" / "assets" / "workflow.svg", SOURCE / "assets" / "icon.svg"):
        if not path.is_file() or "<svg" not in path.read_text(encoding="utf-8"):
            errors.append(f"missing or invalid SVG: {path.relative_to(ROOT)}")


def check_required_files(errors: list[str]) -> None:
    required = [
        ROOT / "README.md",
        ROOT / "README.en.md",
        ROOT / "CONTRIBUTING.md",
        ROOT / ".github" / "ISSUE_TEMPLATE" / "bug_report.yml",
        ROOT / ".github" / "ISSUE_TEMPLATE" / "feature_request.yml",
        ROOT / ".github" / "PULL_REQUEST_TEMPLATE.md",
        ROOT / ".agents" / "plugins" / "marketplace.json",
        PLUGIN / ".codex-plugin" / "plugin.json",
        ROOT / "docs" / "release" / "v1.0.0.md",
    ]
    required.extend(ROOT / "examples" / "job-dashboard" / name for name in ("README.md", "PRD.md", "TECH_DESIGN.md", "ACCEPTANCE.md", "AGENT_PLAN.md", "LOOP.md"))
    required.extend(
        ROOT / "examples" / "java-acceptance" / name
        for name in (
            "README.md", "PRD.md", "TECH_DESIGN.md", "ACCEPTANCE.md",
            "AGENT_PLAN.md", "LOOP.md", "contract.json", "run_demo.py", "test_run_demo.py",
        )
    )
    for path in required:
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(f"required file missing or empty: {path.relative_to(ROOT)}")

    skill_text = (SOURCE / "SKILL.md").read_text(encoding="utf-8")
    if not skill_text.startswith("---\n") and not skill_text.startswith("---\r\n"):
        errors.append("authoritative SKILL.md is missing YAML frontmatter")
    if "name: spec-driven-loop" not in skill_text or "description:" not in skill_text:
        errors.append("authoritative SKILL.md is missing required metadata")

    marketplace = json.loads((ROOT / ".agents" / "plugins" / "marketplace.json").read_text(encoding="utf-8"))
    entry = marketplace.get("plugins", [{}])[0]
    if entry.get("source", {}).get("path") != "./plugins/spec-driven-loop":
        errors.append("marketplace source path must be ./plugins/spec-driven-loop")
    if entry.get("policy") != {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}:
        errors.append("marketplace policy must be AVAILABLE / ON_INSTALL")


def check_dist(errors: list[str]) -> None:
    dist = ROOT / "dist"
    expected_archives = {
        "spec-driven-loop-skill-v1.0.0.zip": "spec-driven-loop/SKILL.md",
        "spec-driven-loop-plugin-v1.0.0.zip": "spec-driven-loop/.codex-plugin/plugin.json",
    }
    for name, member in expected_archives.items():
        archive = dist / name
        if not archive.is_file():
            errors.append(f"missing release archive: dist/{name}")
            continue
        try:
            with zipfile.ZipFile(archive) as payload:
                bad = payload.testzip()
                names = payload.namelist()
                if bad:
                    errors.append(f"corrupt archive member in {name}: {bad}")
                if member not in names:
                    errors.append(f"archive {name} missing {member}")
        except zipfile.BadZipFile:
            errors.append(f"invalid zip archive: {name}")

    sums = dist / "SHA256SUMS.txt"
    if not sums.is_file():
        errors.append("missing dist/SHA256SUMS.txt")
        return
    parsed: dict[str, str] = {}
    for line in sums.read_text(encoding="utf-8").splitlines():
        pieces = line.split("  ", 1)
        if len(pieces) == 2:
            parsed[pieces[1]] = pieces[0]
    for name in expected_archives:
        archive = dist / name
        if archive.is_file() and parsed.get(name) != digest(archive):
            errors.append(f"checksum mismatch: {name}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dist", action="store_true", help="also validate release packages")
    args = parser.parse_args()
    errors: list[str] = []
    check_required_files(errors)
    check_mirror(errors)
    check_markdown_links(errors)
    check_assets(errors)
    errors.extend(f"plugin: {error}" for error in validate_plugin(PLUGIN))
    if args.dist:
        check_dist(errors)
    if errors:
        print("Repository validation failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print("Repository validation passed" + (" (including release packages)" if args.dist else ""))


if __name__ == "__main__":
    main()
