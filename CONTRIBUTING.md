# Contributing to diGITrail

Please use the repository's issue forms for reproducible bugs and feature suggestions. Small, focused pull requests make changes easier to review.

## Local development

Use Python 3.9+ and Git. The generator has no third-party Python dependencies.

```bash
python3 -m unittest discover -s tests -v
python3 scripts/generate_git_graph.py --input-json examples/demo.json --output git-history.html
```

Open `git-history.html` in a modern browser. When changing the renderer, check Structure view, All commits, both chronological directions, branch highlighting, search, commit details and SVG export. The optional browser test requires Playwright and a locally installed Chromium. Run tests locally; a hosted CI workflow is not required.

## Accuracy and scope

- Preserve ordered Git parents, true divergence points, merge points and complete reachable ancestry.
- Keep the primary branch in the first lane and full branch labels on visible nodes.
- Keep Git access read-only and generated reports self-contained and usable offline.
- Clearly describe incomplete history, inferred branch associations and other limits.
- Update the relevant documentation and add a focused regression test for behavioral changes.

## Safe public examples

Use the fictional fixture in [`examples/demo.json`](examples/demo.json) or another deliberately invented history. Review reports and screenshots for private repository names, commit messages, authors, paths, tokens and embedded origin URLs before attaching them to an issue or pull request.

The public demo, source JSON and preview image should describe the same example. Regeneration instructions are in [`examples/README.md`](examples/README.md).

## License


diGITrail is distributed under the PolyForm Noncommercial License 1.0.0. Review [`LICENSE`](LICENSE) before using or contributing to the project. The README explains how to request commercial permission.
