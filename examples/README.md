# Fictional diGITrail demonstration

The demo is **real output from the original renderer**, driven by deliberately fictional Git data. It does not expose any user's repository, project history, identifiers or personal data.

## What is in the demo?

- **23 commits**, **6 branch references** and **3 merges** with internally consistent, invented parent relationships.
- **6 fictional tags**, including lightweight and annotated examples, two tags pointing to the same commit and a tagged commit that would otherwise be collapsed in Structure view.
- Fixed dates in **January 2000**. The `originUrl` is blank, so there are no outgoing links to a real repository.
- The B + D interface: gold tag pills alongside branch labels, separate counts and an **All / Branches / Tags** filter.
- Neither obsolete top-right badge (**Newest at top** / **Read-only**) is shown; the chronology toggle remains.

| File | Role |
| --- | --- |
| [`demo.json`](demo.json) | Editable, fictional source graph and tag metadata |
| [`demo.html`](demo.html) | Complete self-contained interactive report |
| [`../docs/images/digitrail-preview.png`](../docs/images/digitrail-preview.png) | Actual browser screenshot of the current demo including the toolbar and tags |
| [`../docs/images/digitrail-preview.svg`](../docs/images/digitrail-preview.svg) | Export from the current demo using diGITrail's own SVG button |

## Open and explore

Open the [**live interactive demo**](https://0biguan.github.io/diGITrail/) hosted by GitHub Pages. It loads `index.html` as a real webpage, unlike GitHub's source-code viewer for `demo.html`. You can also download `demo.html` from this repository and open it directly in a modern browser; no server, Git or Python is needed to **view** it.

**Repository owner setup:** Enable `Settings → Pages → Build and deployment → Source: GitHub Actions` once, if it is not already enabled. The `.github/workflows/deploy-demo-pages.yml` workflow deploys the verified fictional demo only from `main`. Until GitHub Pages is enabled and a deployment succeeds, the public link may return 404.

Try **Structure view** and **All commits**; switch the **All / Branches / Tags** filter; search for `v1.0.0`, `docs-preview` or `keyboard`; reverse the chronology; open a tagged commit's details to view its type/annotation; export SVG.

## Regenerate the HTML yourself

From the repository root, with Python 3.9+:

```bash
python3 scripts/generate_git_graph.py --input-json examples/demo.json --output examples/demo.html
```

The documentation's PNG and SVG are **generated outputs**, not manually drawn approximations. Maintainers can manually run the GitHub-hosted **Refresh fictional demo previews** workflow on `main` after changing the demo data or template. It uses the original generator, loads the result in Chromium, verifies the tags, captures the interface and exports SVG using the built-in control. It commits generated changes only when explicitly triggered; ordinary pushes do not start an asset-writing workflow. The Pages workflow can be re-run manually after an asset refresh.

Keep the demo fictional and ensure `demo.json`, `demo.html`, preview PNG and SVG remain synchronised whenever the renderer or the fixture changes.
