#!/usr/bin/env python3
"""Validate portability safeguards and generated mirrors for Stoffel skills."""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import re
import sys

PORTABLE_SKILLS = {
    "stoffel-ai-agent-implementation": (
        "Mandatory portability contract",
        "Project and dependency portability:",
        "Stop and report the unavailable dependency",
    ),
    "stoffel-app-getting-started": (
        "Mandatory portability contract",
        "current crates.io release",
        "do not recommend a local path dependency",
    ),
    "stoffel-full-app-golden-path": (
        "Milestone 0: establish portability",
        "Clean-room completion evidence",
        "cargo metadata --locked --format-version 1",
    ),
    "stoffel-cli-app-workflow": (
        "Audit generated Rust apps",
        "cargo metadata --locked --format-version 1",
        "clean external checkout",
    ),
    "stoffel-rust-app-sdk": (
        "NONPORTABLE framework-development mode",
        "cargo metadata --locked --format-version 1",
        "clean checkout outside the Stoffel framework repository",
    ),
    "stoffel-local-mpc-dev-loop": (
        "public crates.io releases by default",
        "CARGO_MANIFEST_DIR",
        "clone the app into a temporary directory",
    ),
    "stoffel-typed-client-io-bindings": (
        "stoffel-bindgen",
        "CARGO_MANIFEST_DIR",
        "OUT_DIR",
    ),
    "stoffel-app-network-and-offchain-integration": (
        "Portability and provenance preflight",
        "clean external checkout",
        "not clean-room tested",
    ),
    "stoffel-deployment-runbook": (
        "Portability and provenance preflight",
        "clean external app checkout",
        "not clean-room tested",
    ),
    "stoffel-app-troubleshooting": (
        "Portability and provenance diagnosis",
        "cargo metadata --locked --format-version 1",
        "not clean-room tested",
    ),
}

FORBIDDEN_TEXT = (
    "/Users/alice/",
    "prefer the documented source dependency or local path dependency",
    "When developing against a local checkout, make that source-based workflow explicit.",
)

# Placeholder policy text such as /workspace/... remains allowed; concrete paths do not.
CONCRETE_MACHINE_PATHS = (
    re.compile(r"/workspace/[A-Za-z0-9_-]"),
    re.compile(r"/Users/[A-Za-z0-9_-]"),
    re.compile(r"/home/[A-Za-z0-9_-]"),
)

UMBRELLA_MARKERS = (
    "Mandatory portability contract",
    "current crates.io release",
    "full immutable commit SHA",
    "Do not claim completion until portability validation has passed",
)


def load_sync_module(root: Path):
    path = root / "scripts" / "sync_developer_skills.py"
    spec = importlib.util.spec_from_file_location("sync_developer_skills", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    sync = load_sync_module(root)

    umbrella = (root / "skill.md").read_text()
    for marker in UMBRELLA_MARKERS:
        if marker not in umbrella:
            errors.append(f"skill.md missing portability marker: {marker!r}")

    scan_paths = [root / "skill.md", *sorted((root / "developer-skills").glob("*.mdx"))]
    for path in scan_paths:
        text = path.read_text()
        for forbidden in FORBIDDEN_TEXT:
            if forbidden in text:
                errors.append(
                    f"{path.relative_to(root)} contains forbidden portability text: {forbidden!r}"
                )
        for pattern in CONCRETE_MACHINE_PATHS:
            match = pattern.search(text)
            if match:
                errors.append(
                    f"{path.relative_to(root)} contains concrete machine path: {match.group(0)!r}"
                )

    for slug, markers in PORTABLE_SKILLS.items():
        source = root / "developer-skills" / f"{slug}.mdx"
        if not source.is_file():
            errors.append(f"missing source skill: {source.relative_to(root)}")
            continue
        text = source.read_text()
        for marker in markers:
            if marker not in text:
                errors.append(f"{source.relative_to(root)} missing portability marker: {marker!r}")

    for source in sorted((root / "developer-skills").glob("*.mdx")):
        if source.name == "overview.mdx":
            continue
        slug = source.stem
        mirror = root / ".mintlify" / "skills" / slug / "SKILL.md"
        if not mirror.is_file():
            errors.append(f"missing generated mirror: {mirror.relative_to(root)}")
            continue
        fields, body = sync.parse_frontmatter(source)
        expected = sync.render_skill(slug, fields["title"], fields["description"], body)
        if mirror.read_text() != expected:
            errors.append(
                f"{mirror.relative_to(root)} is stale; run python3 scripts/sync_developer_skills.py"
            )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="docs repository root",
    )
    args = parser.parse_args()
    errors = validate(args.root.resolve())
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Validated portability safeguards and mirrors for {len(PORTABLE_SKILLS)} skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
