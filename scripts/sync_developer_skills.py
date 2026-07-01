#!/usr/bin/env python3
"""Mirror visible developer skill pages into Mintlify SKILL.md files.

Run from the docs repo root after editing files under developer-skills/.
The script keeps the human-readable MDX pages as the source of truth and writes
machine-discoverable skill files under .mintlify/skills/<slug>/SKILL.md.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "developer-skills"
SKILL_DIR = ROOT / ".mintlify" / "skills"

COMPATIBILITY = (
    "Requires access to the current Stoffel CLI/SDK docs and app-facing "
    "Stoffel tooling. Rust stable and Cargo are required for CLI and Rust SDK workflows."
)


def parse_frontmatter(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text()
    if not text.startswith("---\n"):
        raise ValueError(f"{path} does not start with YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError(f"{path} has unterminated YAML frontmatter")

    frontmatter = text[4:end]
    body = text[end + len("\n---\n") :].lstrip("\n")
    fields: dict[str, str] = {}
    for line in frontmatter.splitlines():
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"')
    for required in ("title", "description"):
        if not fields.get(required):
            raise ValueError(f"{path} missing required frontmatter field: {required}")
    return fields, body


def render_skill(slug: str, title: str, description: str, body: str) -> str:
    return f"""---
name: {slug}
description: {description}
license: MIT
compatibility: {COMPATIBILITY}
metadata:
  author: Stoffel Labs
  version: "1.0"
  docs-page: /developer-skills/{slug}
  source: Stoffel App Developer Skills
---

# {title}

{body}"""


def main() -> None:
    written = 0
    for mdx in sorted(SOURCE_DIR.glob("*.mdx")):
        if mdx.name == "overview.mdx":
            continue
        slug = mdx.stem
        fields, body = parse_frontmatter(mdx)
        out_dir = SKILL_DIR / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / "SKILL.md"
        out_path.write_text(render_skill(slug, fields["title"], fields["description"], body))
        written += 1
    print(f"Wrote {written} skill file(s) under {SKILL_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
