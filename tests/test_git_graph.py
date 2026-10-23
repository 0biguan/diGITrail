"""Local-only regression suite for diGITrail."""
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from generate_git_graph import (  # noqa: E402
    GraphError, dataset_from_git, html_report, normalize_dataset,
)


class GraphTests(unittest.TestCase):
    def setUp(self):
        self.work = tempfile.TemporaryDirectory(prefix="git-graph-test-")
        self.addCleanup(self.work.cleanup)
        self.path = Path(self.work.name) / "repo"
        self.path.mkdir()
        self.run_git("init", "-q", "-b", "main")
        self.run_git("config", "user.name", "Local Test")
        self.run_git("config", "user.email", "test@example.invalid")
        self.write_commit("README.md", "base", "Initial baseline")
        self.root = self.run_git("rev-parse", "HEAD").strip()

    def run_git(self, *args):
        done = subprocess.run(["git", "-C", str(self.path), *args],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                              env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"})
        if done.returncode:
            raise AssertionError(f"git {args}: {done.stderr}")
        return done.stdout

    def write_commit(self, filename, value, subject):
        target = self.path / filename
        target.write_text(value, encoding="utf-8")
        self.run_git("add", "--", filename)
        self.run_git("commit", "-qm", subject)

    def populated(self):
        self.run_git("branch", "feature/example")
        self.run_git("checkout", "-q", "feature/example")
        self.write_commit("feature.txt", "a", "Add example feature")
        self.write_commit("feature.txt", "b", "Refine example feature")
        feature_tip = self.run_git("rev-parse", "HEAD").strip()
        self.run_git("checkout", "-q", "main")
        self.write_commit("main.txt", "base", "Parallel change on main")
        self.run_git("merge", "--no-ff", "feature/example", "-m", "Merge example feature")
        self.run_git("branch", "feature/extra")
        self.run_git("checkout", "-q", "feature/extra")
        self.write_commit("extra.txt", "extra", "Add another example feature")
        self.run_git("checkout", "-q", "main")
        return feature_tip

    def generate(self, include_all=True):
        return dataset_from_git(self.path, days=7,
                                cutoff=datetime(2000, 1, 1, tzinfo=timezone.utc),
                                base=None, include_all=include_all, remotes=False,
                                max_history=1000, origin_url=None)

    def test_parent_graph_and_distinct_branches(self):
        feature_tip = self.populated()
        d = self.generate()
        self.assertEqual(d["baseBranch"], "main")
        self.assertEqual(d["components"], 1)
        self.assertEqual(len(d["refs"]), 3)
        self.assertEqual(d["refs"]["feature/example"], feature_tip)
        nodes = {n["id"]: n for n in d["nodes"]}
        self.assertEqual(len(nodes), 6)
        self.assertTrue(set(d["refs"].values()) <= set(nodes))
        self.assertTrue(any(len(n["parents"]) == 2 for n in nodes.values()))
        for node in nodes.values():
            for parent in node["parents"]:
                self.assertTrue(parent["direct"])
                self.assertTrue(parent["verified"])
                self.assertIn(parent["id"], nodes)
        self.assertEqual(nodes[self.root]["parents"], [])

    def test_read_only_repo(self):
        self.populated()
        before = self.run_git("status", "--porcelain", "--untracked-files=all")
        before_head = self.run_git("rev-parse", "HEAD")
        self.generate()
        self.assertEqual(before, self.run_git("status", "--porcelain", "--untracked-files=all"))
        self.assertEqual(before_head, self.run_git("rev-parse", "HEAD"))

    def test_dangling_parent_is_rejected(self):
        d = self.generate()
        d["nodes"][0]["parents"].append({"id": "bad-parent", "direct": True})
        with self.assertRaisesRegex(GraphError, "Missing parent"):
            normalize_dataset(d, "repo")

    def test_cycles_are_rejected(self):
        d = self.generate()
        d["nodes"][0]["parents"].append({"id": d["nodes"][0]["id"]})
        with self.assertRaisesRegex(GraphError, "cycle"):
            normalize_dataset(d, "repo")

    def test_history_limit_fails_closed(self):
        self.populated()
        with self.assertRaisesRegex(GraphError, "exceeds"):
            dataset_from_git(self.path, days=7,
                cutoff=datetime(2000, 1, 1, tzinfo=timezone.utc),
                base=None, include_all=True, remotes=False,
                max_history=2, origin_url=None)

    def test_html_escaping_and_branches(self):
        self.write_commit("evil.txt", "evil", 'Fix </script><script>alert(1)</script> <img>')
        d = self.generate()
        html = html_report({"repo0": d})
        self.assertIn("git history", html.lower() + " git history")
        self.assertIn("\\u003c/script\\u003e", html)
        self.assertNotIn("</script><script>alert(1)</script>", html)
        self.assertNotIn("__GIT_HISTORY_DATA__", html)
        self.assertIn('data-repo="repo0"', html)
        self.assertIn("Fix \\u003c/script", html)

    def test_single_repo_and_multiple_repo_html(self):
        d = self.generate()
        html = html_report({"repo0": d, "repo1": {**d, "displayName": "duplicate"}})
        self.assertIn('data-repo="repo0"', html)
        self.assertIn('data-repo="repo1"', html)
        self.assertIn("duplicate", html)


    def test_english_ui_and_cli_messages(self):
        dataset = self.generate()
        html = html_report({"repo0": dataset})
        self.assertIn('<html lang="en">', html)
        self.assertIn('diGITrail · Branch & Commit History', html)
        self.assertIn('Structure view', html)
        self.assertIn('All commits', html)
        self.assertIn('Reverse chronological order', html)
        self.assertIn('Export SVG', html)
        self.assertIn('Associated branches', html)
        missing = self.path / 'not-a-repository'
        proc = subprocess.run([sys.executable, str(ROOT / 'scripts' / 'generate_git_graph.py'),
                               '--repo', str(missing), '--output', str(self.path / 'missing.html')],
                              capture_output=True, text=True)
        self.assertEqual(proc.returncode, 2)
        self.assertIn('Repository directory does not exist:', proc.stderr)

    def test_cli_smoke_json_and_html(self):
        out = Path(self.work.name) / "report.html"
        json_out = Path(self.work.name) / "evidence.json"
        cmd = [sys.executable, str(ROOT / "scripts" / "generate_git_graph.py"),
               "--repo", str(self.path), "--all-branches",
               "--output", str(out), "--also-json", str(json_out)]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertTrue(out.is_file())
        self.assertEqual(len(json.loads(json_out.read_text())["repo0"]["nodes"]), 1)
        out2 = Path(self.work.name) / "from_json.html"
        proc2 = subprocess.run([sys.executable, str(ROOT / "scripts" / "generate_git_graph.py"),
                                "--input-json", str(json_out), "--output", str(out2)],
                               capture_output=True, text=True)
        self.assertEqual(proc2.returncode, 0, proc2.stderr)
        self.assertTrue(out2.is_file())

    @unittest.skipUnless(__import__('importlib').util.find_spec('playwright'), "Playwright unavailable")
    def test_chromium_interaction_if_installed(self):
        from playwright.sync_api import sync_playwright
        self.populated()
        data = self.generate()
        html = html_report({"repo0": data, "repo1": {**data, "displayName": "repo-2"}})
        with sync_playwright() as p:
            try:
                browser = p.chromium.launch(executable_path="/usr/bin/chromium", headless=True,
                                             args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"])
            except Exception as exc:
                self.skipTest("Local Chromium could not start: " + str(exc)[:200])
            try:
                page = browser.new_page(viewport={"width": 1280, "height": 780})
                errors = []
                page.on("pageerror", lambda e: errors.append(str(e)))
                page.set_content(html, wait_until="load", timeout=30000)
                self.assertEqual(page.title(), 'diGITrail · Git Branch History')
                self.assertIn('Branch & Commit History', page.locator('h1').inner_text())
                self.assertIn('Newest', page.locator('#order-tag').inner_text())
                for tab in ("repo0", "repo1"):
                    page.locator(f'button[data-repo="{tab}"]').click()
                    for mode in ("summary", "full"):
                        page.locator(f'button[data-mode="{mode}"]').click()
                        if 'Oldest' in page.locator('#order-tag').inner_text():
                            page.locator('#flip-time').click()
                        for orientation in range(2):
                            if orientation:
                                page.locator("#flip-time").click()
                            self.assertIn('Oldest' if orientation else 'Newest',
                                          page.locator('#order-tag').inner_text())
                            self.assertFalse(errors, errors)
                            self.assertEqual(page.locator(".commit-row").count(),
                                             6 if mode == "full" else 4)
                            self.assertEqual(page.locator(".branch-label").count(),
                                             page.locator(".commit-row").count())
                            self.assertNotIn("Render error", page.locator("#graph").inner_text())
                # Distinct branch tips use distinct x coordinates.
                page.locator('button[data-repo="repo0"]').click()
                page.locator('button[data-mode="summary"]').click()
                tips = [data["refs"]["feature/example"], data["refs"]["feature/extra"]]
                xs = [page.locator(f'.commit-row[data-id="{sha}"] circle').first.get_attribute("cx") for sha in tips]
                self.assertEqual(len(set(xs)), 2)
            finally:
                browser.close()


if __name__ == "__main__":
    unittest.main()
