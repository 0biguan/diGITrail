---
name: digitrail
description: diGITrail creates self-contained, interactive, GitKraken-style commit-history graphs using the real parent relationships from a read-only local Git repository or verified GitHub commit data. Use for requests to visualize Git branches, forks, merges, or commit ancestry. It keeps the primary branch in the first column, labels every visible commit, preserves branch separation and real ancestry, supports compact/full views, chronological reversal, searching, and SVG export.
---

# diGITrail

Generate an interactive, standalone **HTML graph of Git commits and their actual parent relationships**, similar to GitKraken. Prefer a local Git checkout and use Git **read-only**. Never create branches, commits, tags, merges, CI runs, deployments, or other side effects to build the chart.

## When to use

Use diGITrail when the user asks for a GitKraken-like history graph, branch visualization, a Git branch tree, where branches fork or merge, or the interactive ancestry of commits. These triggers apply in any language.

**Always use Git ancestry, not pull request metadata, for graph connections.** A pull request's base branch is not evidence of where its source branch forked. Git normally does **not** record when a branch was created: a request for “branches created in the last seven days” usually requires clarification or should be presented as **branches active in that period**, unless creation evidence exists.

## Procedure

1. Identify the repository and time window. Default to the last seven days of branch activity if not specified. Reuse the repository already established in the conversation. Ask only if it is genuinely unknown and cannot be found. Include multiple repositories with repeated `--repo` flags when appropriate.
2. Prefer the supplied or locally available Git checkout. Run `scripts/generate_git_graph.py` without altering the repository. Do **not** run `git clone`, `git fetch`, `git pull`, `git checkout`, hosted runners, or GitHub Actions just to generate a graph. Obtain the user's permission before performing any new network operation not already authorized by their request.
3. Produce a standalone HTML file with the interactive graph and controls. Optionally produce a validated JSON evidence file with `--also-json`.
4. Validate the commit/parent structure. When a graphical browser is available, exercise both chronological directions and both **Structure** and **All commits** views for each repository.
5. Link to the verified HTML output file and explain the selected period, branch and commit counts, and any incomplete history or other limitations. Never claim that branch creation dates were verified merely because heads have recent commits.

## Commands

Linux/macOS:

```bash
python3 scripts/generate_git_graph.py \
  --repo /path/to/repository \
  --days 7 \
  --output /mnt/data/git-history.html \
  --also-json /mnt/data/git-history.json
```

Windows PowerShell:

```powershell
py scripts/generate_git_graph.py --repo 'C:\path\to\repository' --days 7 --output 'C:\Temp\git-history.html'
```

Multiple repositories:

```bash
python3 scripts/generate_git_graph.py \
  --repo /path/to/repo-a \
  --repo /path/to/repo-b \
  --output /mnt/data/multi-repo-git-history.html
```

Additional options: `--base master` to select a primary branch other than `main`; `--all-branches` to include inactive branches; `--remotes` to include **already available local** remote refs (never fetches); `--as-of 2000-01-08` to reproduce a UTC cutoff; `--max-history 30000` to cap the complete ancestry; and `--origin-url https://github.com/example/sample-repository` for commit hyperlinks.

If the graph is too large, narrow the branches or period **without inventing endpoints or parent relationships**. The generator fails instead of silently truncating history when it exceeds its configured limit. A shallow repository with missing parents must be reported as incomplete; it must not be presented as having genuine roots where history is missing. Do not assume unrelated Git histories have a shared ancestor.

## GitHub connector or other verified commit data

When a local checkout is unavailable and the user has granted access to a GitHub connector, read each relevant commit's **SHA, ordered parent SHAs, committer timestamp, and subject**, plus the branch-head refs. Retrieve ancestors until every referenced parent is included, or explicitly mark genuine known history boundaries. If required parents cannot be verified, state that full origin verification was not possible.

Normalize the data to the schema in `references/data-format.md`, save it as JSON, and generate the HTML:

```bash
python3 scripts/generate_git_graph.py \
  --input-json /mnt/data/commits.json \
  --output /mnt/data/git-history.html
```

Each commit can be reachable from more than one branch. The branch name shown for an intermediate node is a **visual association inferred from actual ancestry and nearby references**, not proof of exclusive branch ownership. Never fabricate branch labels or SHA relationships to make the graph look tidier.

## Visualization requirements

- The primary branch (`main`, `master`, or `--base`) stays in **column one**, following its first-parent history.
- Show the **newest commits at the top** by default, with a button to reverse the order.
- Show a **full branch label on every visible node**. Avoid truncation or ellipses in branch labels.
- Keep distinct branches on separate lanes until their **real common ancestor**. Do not merge branches visually just because they can reuse an SVG column.
- The default **Structure** view retains branch references, merges, divergence points, and true roots, compressing linear chains into `+N` counts. **All commits** displays each commit separately.
- Keep the header compact and the graph responsive. Provide commit/branch search, branch highlighting, zoom, a details panel, and SVG export.
- Ship one self-contained HTML file with inline CSS, JavaScript, and data; require no CDN, network fonts, remote images, or live server.
- Use actual parent SHAs, not pull request base/head metadata, for graph edges.
- If a history ends because of a verified scope boundary, label it explicitly. Do not show an unverified endpoint as a Git root.
- If a repository genuinely contains multiple unrelated histories, show and explain the separate components.

## Verification

Run the bundled local tests whenever this skill changes:

```bash
python3 -m unittest discover -s tests -v
```

Tests create temporary local Git histories; the optional browser test uses Playwright and locally installed Chromium. They do **not** use hosted CI or remote runners.


## License

PolyForm Noncommercial License 1.0.0. Commercial use requires separate written permission. See the `LICENSE` file distributed with this skill.

Required Notice: Copyright 2026 0biguan (https://github.com/0biguan/diGITrail)
