#!/usr/bin/env python3
"""Build a small, reproducible diGITrail agent-skill ZIP (stdlib only).

This packages existing production files without changing the renderer.
The output is a distribution candidate, not evidence of acceptance by ChatGPT.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]
FILES = (
    "SKILL.md",
    "LICENSE",
    "scripts/generate_git_graph.py",
    "assets/template.html",
    "references/data-format.md",
)
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)


def build_skill_zip(output: Path) -> None:
    sources = []
    for relative in FILES:
        source = ROOT / relative
        if not source.is_file() or source.is_symlink():
            raise ValueError(f"Missing or unsafe skill file: {relative}")
        sources.append((relative, source.read_bytes()))

    skill_header = sources[0][1].decode("utf-8")
    if not skill_header.startswith("---\n") or "\nname: digitrail\n" not in skill_header:
        raise ValueError("SKILL.md is missing valid digitrail frontmatter")

    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, "w") as archive:
        for relative, data in sources:
            info = ZipInfo("digitrail/" + relative, ZIP_TIMESTAMP)
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, data)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("dist/digitrail-skill.zip"))
    args = parser.parse_args()
    build_skill_zip(args.output)
    print(f"Skill candidate created: {args.output}")


if __name__ == "__main__":
    main()
