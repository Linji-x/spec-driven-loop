"""Self-contained CI validation for the repository's Codex plugin manifest."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")
IDENTIFIER = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
COLOR = re.compile(r"^#[0-9A-Fa-f]{6}$")


def require_string(payload: dict, key: str, errors: list[str], prefix: str = "") -> str | None:
    value = payload.get(key)
    label = f"{prefix}.{key}" if prefix else key
    if not isinstance(value, str) or not value.strip():
        errors.append(f"`{label}` must be a non-empty string")
        return None
    return value


def validate(plugin_root: Path) -> list[str]:
    errors: list[str] = []
    manifest_path = plugin_root / ".codex-plugin" / "plugin.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return ["missing `.codex-plugin/plugin.json`"]
    except json.JSONDecodeError as exc:
        return [f"invalid plugin JSON: {exc}"]

    name = require_string(manifest, "name", errors)
    version = require_string(manifest, "version", errors)
    require_string(manifest, "description", errors)
    if name and not IDENTIFIER.fullmatch(name):
        errors.append("`name` must be a lowercase kebab-case identifier")
    if version and not SEMVER.fullmatch(version):
        errors.append("`version` must be strict semantic versioning")

    author = manifest.get("author")
    if not isinstance(author, dict):
        errors.append("`author` must be an object")
    else:
        require_string(author, "name", errors, "author")

    skills = require_string(manifest, "skills", errors)
    if skills:
        skill_root = (plugin_root / skills).resolve()
        try:
            skill_root.relative_to(plugin_root.resolve())
        except ValueError:
            errors.append("`skills` must resolve inside the plugin root")
        if not skill_root.is_dir() or not any(skill_root.glob("*/SKILL.md")):
            errors.append("`skills` must contain at least one skill directory")

    interface = manifest.get("interface")
    if not isinstance(interface, dict):
        errors.append("`interface` must be an object")
    else:
        for key in ("displayName", "shortDescription", "longDescription", "developerName", "category", "defaultPrompt"):
            require_string(interface, key, errors, "interface")
        capabilities = interface.get("capabilities")
        if not isinstance(capabilities, list) or not capabilities or not all(isinstance(item, str) and item.strip() for item in capabilities):
            errors.append("`interface.capabilities` must be a non-empty string array")
        color = interface.get("brandColor")
        if color is not None and (not isinstance(color, str) or not COLOR.fullmatch(color)):
            errors.append("`interface.brandColor` must use #RRGGBB")
        for key in ("composerIcon", "logo", "logoDark"):
            value = interface.get(key)
            if value is None:
                continue
            if not isinstance(value, str) or not value.strip():
                errors.append(f"`interface.{key}` must be a non-empty path")
                continue
            target = (plugin_root / value).resolve()
            try:
                target.relative_to(plugin_root.resolve())
            except ValueError:
                errors.append(f"`interface.{key}` must stay inside the plugin root")
                continue
            if not target.is_file():
                errors.append(f"`interface.{key}` does not exist: {value}")

    serialized = json.dumps(manifest)
    if "[TODO:" in serialized:
        errors.append("manifest contains an unresolved TODO placeholder")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("plugin_path")
    args = parser.parse_args()
    root = Path(args.plugin_path).resolve()
    errors = validate(root)
    if errors:
        print("Plugin validation failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print(f"Plugin validation passed: {root}")


if __name__ == "__main__":
    main()
