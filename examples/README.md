# Fictional diGITrail demo

Open `demo.html` in a modern browser to explore the complete diGITrail interface offline. The prebuilt file needs no Python installation.

The sample represents a fictional application with **23 commits, 6 branch references and 3 merges**. All identifiers, names, messages, dates and parent relationships were created specifically for this fixture. No real repository was used to populate it. Dates are fixed in January 2000, and `originUrl` is empty so the demo contains no live repository links.

## Files

| File | Purpose |
| --- | --- |
| [`demo.json`](demo.json) | Complete, editable fictional commit graph |
| [`demo.html`](demo.html) | Generated interactive report |
| [`../docs/images/digitrail-preview.svg`](../docs/images/digitrail-preview.svg) | Structure-view graph exported with the interface's own SVG export code |
| [`../docs/images/digitrail-preview.png`](../docs/images/digitrail-preview.png) | Rasterized copy of that vector export for the main README |

The identifiers are deterministic example hashes. The fixture's parent links describe its invented graph; its `verified` flags indicate internally specified fixture edges.

## Regenerate the HTML

From the repository root:

```bash
python3 scripts/generate_git_graph.py --input-json examples/demo.json --output examples/demo.html
```

Use `py` instead of `python3` with the Windows Python launcher.

To update the preview, open the regenerated demo, select **Structure view**, keep **Newest first** and choose **Export SVG**. Save the export as `docs/images/digitrail-preview.svg`. The README PNG is a 1860-pixel-wide rasterization of that graph. Its 11 visible nodes preserve the three merges and branch forks while compressing 12 linear commits.

## Explore the interface

- Switch to **All commits** to see all 23 fixture nodes.
- Reverse chronological order while retaining the same parent relationships.
- Search for `keyboard` and highlight `fix/keyboard-nav`.
- Click a commit to inspect its identifier, date, associated branch and parents.
- Export the current graph as a self-contained SVG.

Keep any replacement public demo equally fictional and self-contained. Review JSON, HTML, vector exports and images together before publishing them.
