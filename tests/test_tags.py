"""Regression tests for Git tag extraction, filtering, and UI presentation."""
from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from generate_git_graph import GraphError, dataset_from_git, html_report, normalize_dataset  # noqa: E402


class TagTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="digitrail-tags-")
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name) / "repo"
        self.repo.mkdir()
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.name", "Tag Test")
        self.git("config", "user.email", "tag-test@example.invalid")
        self.write_commit("start.txt", "root", "Initial commit")
        self.root = self.git("rev-parse", "HEAD").strip()
        self.git("checkout", "-qb", "feature/example")
        self.write_commit("feature.txt", "1", "First feature")
        self.middle = self.git("rev-parse", "HEAD").strip()
        self.write_commit("feature.txt", "2", "Second feature")
        self.git("checkout", "-q", "main")
        self.write_commit("main.txt", "main", "Main update")
        self.git("merge", "--no-ff", "feature/example", "-m", "Merge feature")
        self.head = self.git("rev-parse", "HEAD").strip()

        self.git("tag", "v0.1.0", self.root)
        self.git("tag", "middle-light", self.middle)
        self.git("tag", "middle-alias", self.middle)
        self.git("tag", "-a", "v1.0.0", "-m", "First stable release", self.head)

    def git(self, *args):
        p = subprocess.run(["git", "-C", str(self.repo), *args],
                           capture_output=True, text=True,
                           env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"})
        if p.returncode:
            raise AssertionError(f"Git {args}: {p.stderr}")
        return p.stdout

    def write_commit(self, name, content, subject):
        (self.repo / name).write_text(content, encoding="utf-8")
        self.git("add", "--", name)
        self.git("commit", "-qm", subject)

    def data(self):
        return dataset_from_git(
            self.repo, days=30, cutoff=datetime(2000, 1, 1, tzinfo=timezone.utc),
            base="main", include_all=True, remotes=False, max_history=100,
            origin_url="https://github.com/0biguan/diGITrail-sample",
        )

    def test_tag_types_targets_metadata_and_shared_commit(self):
        tags = self.data()["tags"]
        self.assertEqual(set(tags), {"v0.1.0", "v1.0.0", "middle-light", "middle-alias"})
        self.assertEqual(tags["v0.1.0"]["type"], "lightweight")
        self.assertEqual(tags["v0.1.0"]["commit"], self.root)
        self.assertEqual(tags["middle-light"]["commit"], self.middle)
        self.assertEqual(tags["middle-alias"]["commit"], self.middle)
        stable = tags["v1.0.0"]
        self.assertEqual(stable["type"], "annotated")
        self.assertEqual(stable["commit"], self.head)
        self.assertEqual(stable["tagger"], "Tag Test")
        self.assertEqual(stable["message"], "First stable release")
        self.assertTrue(stable["date"])
        d = self.data()
        self.assertEqual(normalize_dataset(d, "repo")["tags"], tags)
        self.assertEqual(len(d["nodes"]), 5)

    def test_tag_validation_and_optional_schema(self):
        d = self.data()
        for broken in (
            {"missing": {"commit": "a" * 40, "type": "lightweight"}},
            {"wrong": {"commit": self.head, "type": "branch"}},
            {"wrong": {"commit": self.head, "type": "annotated", "message": 100}},
        ):
            with self.assertRaises(GraphError):
                normalize_dataset({**d, "tags": broken}, "repo")
        no_tags = normalize_dataset({**d, "tags": {}}, "repo")
        self.assertEqual(no_tags["tags"], {})
        old_format = dict(d)
        del old_format["tags"]
        self.assertEqual(normalize_dataset(old_format, "repo")["tags"], {})

    def test_escaped_tag_metadata_and_report(self):
        d = self.data()
        d["tags"]["evil"] = {"type": "annotated", "commit": self.head,
                             "message": "</script><script>alert('oops')</script>"}
        html = html_report({"repo0": normalize_dataset(d, "repo")})
        self.assertIn(r"\u003c/script\u003e", html)
        self.assertNotIn("</script><script>alert('oops')</script>", html)
        self.assertIn("ASSOCIATED REFERENCES", html)
        self.assertIn('data-ref-visibility="tags"', html)
        self.assertNotIn('id="order-tag"', html)
        self.assertNotIn('>Read-only</span>', html)

    def test_cli_html_and_json_roundtrip(self):
        out = Path(self.tmp.name) / "report.html"
        evidence = Path(self.tmp.name) / "evidence.json"
        p = subprocess.run([sys.executable, str(ROOT / "scripts/generate_git_graph.py"),
                            "--repo", str(self.repo), "--all-branches",
                            "--also-json", str(evidence), "--output", str(out)],
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("4 tags", p.stdout)
        d = json.loads(evidence.read_text())["repo0"]
        self.assertEqual(len(d["tags"]), 4)
        other = Path(self.tmp.name) / "from_json.html"
        again = subprocess.run([sys.executable, str(ROOT / "scripts/generate_git_graph.py"),
                                "--input-json", str(evidence), "--output", str(other)],
                               capture_output=True, text=True)
        self.assertEqual(again.returncode, 0, again.stderr)
        self.assertIn("middle-alias", other.read_text())

    @unittest.skipUnless(__import__("importlib").util.find_spec("playwright"), "Playwright unavailable")
    def test_browser_tags_structure_filters_details_and_svg(self):
        from playwright.sync_api import sync_playwright

        html = html_report({"repo0": self.data()})
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True,
                                        args=["--no-sandbox", "--disable-dev-shm-usage"])
            try:
                page = browser.new_page(viewport={"width": 1280, "height": 780},
                                        accept_downloads=True)
                errors = []
                page.on("pageerror", lambda ex: errors.append(str(ex)))
                page.set_content(html)
                self.assertEqual(page.locator("#counttags").inner_text(), "4")
                self.assertEqual(page.locator("#countrefs").inner_text(), "2")
                self.assertEqual(page.locator("#order-tag").count(), 0)
                self.assertEqual(page.get_by_text("Read-only", exact=True).count(), 0)
                self.assertEqual(page.locator(".commit-row").count(), 4)
                self.assertEqual(page.locator(".ref-tag").count(), 4)
                self.assertEqual(page.locator(f'.commit-row[data-id="{self.middle}"] .ref-tag').count(), 2)
                self.assertEqual(page.locator(f'.commit-row[data-id="{self.root}"]').count(), 1)

                page.locator('[data-ref-visibility="branches"]').click()
                self.assertEqual(page.locator(".ref-tag").count(), 0)
                self.assertEqual(page.locator(".commit-row").count(), 4)
                page.locator('[data-ref-visibility="tags"]').click()
                self.assertEqual(page.locator(".branch-label").count(), 0)
                self.assertEqual(page.locator(".ref-tag").count(), 4)
                page.locator(f'.commit-row[data-id="{self.middle}"]').click()
                self.assertIn("middle-alias", page.locator("#detail-tags").inner_text())
                page.locator(f'.commit-row[data-id="{self.head}"]').click()
                self.assertIn("First stable release", page.locator("#detail-tags").inner_text())
                page.locator('[data-ref-visibility="all"]').click()
                page.locator('[data-mode="full"]').click()
                self.assertEqual(page.locator(".commit-row").count(), 5)
                page.locator("#flip-time").click()
                self.assertIn("Oldest", page.locator("#order-description").inner_text())
                page.locator("#find").fill("middle-light")
                self.assertIn("1 matches", page.locator("#found").inner_text())
                with page.expect_download() as download_info:
                    page.locator("#download-svg").click()
                download = download_info.value
                self.assertTrue(download.suggested_filename.endswith(".svg"))
                saved = Path(self.tmp.name) / "export.svg"
                download.save_as(str(saved))
                export = saved.read_text()
                self.assertIn("middle-alias", export)
                self.assertIn("tag-label", export)
                self.assertFalse(errors, errors)
            finally:
                browser.close()


if __name__ == "__main__":
    unittest.main()
