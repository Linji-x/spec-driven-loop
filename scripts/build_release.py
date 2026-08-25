"""Build deterministic v1.0.0 Skill and Plugin release archives."""

from __future__ import annotations

import hashlib
import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIST = (ROOT / "dist").resolve()
VERSION = "1.0.0"


def sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def add_tree(archive: zipfile.ZipFile, source: Path, root_name: str) -> None:
    for path in sorted(source.rglob("*")):
        if not path.is_file() or "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        relative = path.relative_to(source).as_posix()
        info = zipfile.ZipInfo(f"{root_name}/{relative}", date_time=(2020, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        archive.writestr(info, path.read_bytes())


def build(name: str, source: Path) -> Path:
    target = DIST / name
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        add_tree(archive, source, "spec-driven-loop")
    return target


def main() -> None:
    if DIST.parent != ROOT.resolve() or DIST.name != "dist":
        raise SystemExit(f"Refusing unsafe dist path: {DIST}")
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()

    skill = build(f"spec-driven-loop-skill-v{VERSION}.zip", ROOT / "spec-driven-loop")
    plugin = build(f"spec-driven-loop-plugin-v{VERSION}.zip", ROOT / "plugins" / "spec-driven-loop")
    sums = DIST / "SHA256SUMS.txt"
    sums.write_text(
        "\n".join(f"{sha256(path)}  {path.name}" for path in (skill, plugin)) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"Built {skill.name}, {plugin.name}, and {sums.name}")


if __name__ == "__main__":
    main()
