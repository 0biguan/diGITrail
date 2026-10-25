"""Regression tests for the separately packaged AI skill."""
from __future__ import annotations

import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from package_skill import FILES, build_skill_zip  # noqa: E402


class SkillPackageTests(unittest.TestCase):
    def test_zip_contains_exact_required_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "digitrail-skill.zip"
            build_skill_zip(path)
            with ZipFile(path) as archive:
                expected = {"digitrail/" + file for file in FILES}
                self.assertEqual(set(archive.namelist()), expected)
                self.assertEqual(archive.testzip(), None)
                for relative in FILES:
                    self.assertEqual(
                        archive.read("digitrail/" + relative),
                        (ROOT / relative).read_bytes(),
                    )
                skill = archive.read("digitrail/SKILL.md").decode("utf-8")
                self.assertTrue(skill.startswith("---\nname: digitrail\n"))
                self.assertIn("scripts/generate_git_graph.py", skill)

    def test_build_is_reproducible(self):
        with tempfile.TemporaryDirectory() as tmp:
            first, second = (Path(tmp) / name for name in ("first.zip", "second.zip"))
            build_skill_zip(first)
            build_skill_zip(second)
            self.assertEqual(hashlib.sha256(first.read_bytes()).digest(),
                             hashlib.sha256(second.read_bytes()).digest())

    def test_packaged_renderer_parses(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "out.zip"
            build_skill_zip(path)
            with ZipFile(path) as archive:
                content = archive.read("digitrail/scripts/generate_git_graph.py")
                compile(content, "generate_git_graph.py", "exec")

    def test_cli_build(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "candidate.zip"
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts/package_skill.py"),
                 "--output", str(path)],
                capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(path.is_file())


if __name__ == "__main__":
    unittest.main()
