#!/usr/bin/env python3
"""Regression tests for the skill portability validator."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load_validator():
    path = ROOT / "scripts" / "validate_skill_portability.py"
    spec = importlib.util.spec_from_file_location("validate_skill_portability", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


VALIDATOR = load_validator()


class SkillPortabilityValidationTests(unittest.TestCase):
    def make_fixture(self, parent: Path) -> Path:
        fixture = parent / "docs"
        fixture.mkdir()
        shutil.copy2(ROOT / "skill.md", fixture / "skill.md")
        shutil.copytree(ROOT / "developer-skills", fixture / "developer-skills")
        shutil.copytree(ROOT / ".mintlify" / "skills", fixture / ".mintlify" / "skills")
        (fixture / "scripts").mkdir()
        shutil.copy2(
            ROOT / "scripts" / "sync_developer_skills.py",
            fixture / "scripts" / "sync_developer_skills.py",
        )
        return fixture

    def test_current_skills_pass(self) -> None:
        self.assertEqual(VALIDATOR.validate(ROOT), [])

    def test_rejects_container_local_framework_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = self.make_fixture(Path(directory))
            source = fixture / "developer-skills" / "stoffel-app-getting-started.mdx"
            source.write_text(source.read_text() + "\n`/workspace/acme/framework`\n")
            errors = VALIDATOR.validate(fixture)
            self.assertTrue(any("concrete machine path" in error for error in errors), errors)

    def test_rejects_windows_user_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = self.make_fixture(Path(directory))
            source = fixture / "developer-skills" / "stoffel-app-getting-started.mdx"
            source.write_text(source.read_text() + "\n`C:\\Users\\alice\\stoffel`\n")
            errors = VALIDATOR.validate(fixture)
            self.assertTrue(any("concrete machine path" in error for error in errors), errors)

    def test_rejects_stale_generated_mirror(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = self.make_fixture(Path(directory))
            mirror = (
                fixture
                / ".mintlify"
                / "skills"
                / "stoffel-rust-app-sdk"
                / "SKILL.md"
            )
            mirror.write_text(mirror.read_text() + "\n<!-- stale -->\n")
            errors = VALIDATOR.validate(fixture)
            self.assertTrue(any("is stale" in error for error in errors), errors)

    def test_rejects_stale_mirror_outside_portability_marker_set(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = self.make_fixture(Path(directory))
            mirror = (
                fixture
                / ".mintlify"
                / "skills"
                / "stoffel-lang-app-programming"
                / "SKILL.md"
            )
            mirror.write_text(mirror.read_text() + "\n<!-- stale -->\n")
            errors = VALIDATOR.validate(fixture)
            self.assertTrue(any("stoffel-lang-app-programming" in error for error in errors), errors)

    def test_rejects_removed_clean_room_gate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = self.make_fixture(Path(directory))
            source = fixture / "developer-skills" / "stoffel-deployment-runbook.mdx"
            source.write_text(source.read_text().replace("clean external app checkout", "external app checkout", 1))
            errors = VALIDATOR.validate(fixture)
            self.assertTrue(any("clean external app checkout" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
