# diGITrail

**Interactive Git history visualizer for AI agents and the command line.**

Turn a Git repository into a single, portable HTML report. Explore branch forks, merges and commit ancestry in a GitKraken-style graph, with search, branch highlighting and SVG export. Runs locally with Python's standard library; the report works offline in your browser.

[Download ZIP](https://github.com/0biguan/diGITrail/archive/refs/heads/main.zip) · [Try the demo](#try-the-demo) · [Quick start](#quick-start) · [Use as an agent skill](#use-as-an-agent-skill)

![diGITrail Structure view: a fictional sample app with six coloured branches, three merges, commit messages, branch labels and dates](docs/images/digitrail-preview.png)

*Actual graph output from the bundled renderer. This entirely fictional sample contains 23 commits, 6 branches and 3 merges. Structure view compresses it into 11 visible nodes. All names, identifiers, messages, dates and parent relationships were created for this example.*

## Why diGITrail?

- **Real Git ancestry:** connections follow ordered commit parents, preserving actual forks and merges.
- **Readable branch history:** the primary branch stays in the first lane and every visible node has a full branch label.
- **Two levels of detail:** Structure view compresses linear chains; All commits shows every commit.
- **Interactive exploration:** reverse chronology, search commits, highlight a branch, zoom and inspect commit details.
- **Portable output:** share one self-contained HTML file or export the graph as SVG.
- **Read-only and local:** the generator reads Git without changing your repository or starting CI. Reports need no server, CDN or third-party Python packages.
- **CLI or agent skill:** run the generator directly or let a skills-compatible assistant use the bundled instructions. Multiple repositories can share one report.

## Try the demo

1. [Download the repository ZIP](https://github.com/0biguan/diGITrail/archive/refs/heads/main.zip) and extract it.
2. Open **`examples/demo.html`** in a modern browser. The prebuilt demo requires no Python installation.
3. Switch between **Structure view** and **All commits**, reverse the order, search for `keyboard`, click a commit or select **Export SVG**.

The demo includes the complete interface and its controls. Its [fictional source data](examples/demo.json) and [regeneration instructions](examples/README.md) are included. The README image shows the graph area; a [vector version](docs/images/digitrail-preview.svg) is also available.

## Quick start

**Requirements:** Python 3.9+ and Git, on Windows, Linux or macOS. The generator uses only the Python standard library. A modern browser opens the resulting report.

Download and extract the ZIP, or clone the project:

```bash
git clone https://github.com/0biguan/diGITrail.git
cd diGITrail
```

Generate a report for a local repository:

```bash
python3 scripts/generate_git_graph.py --repo /path/to/repository --days 7 --output git-history.html
```

Windows PowerShell:

```powershell
py scripts/generate_git_graph.py --repo 'C:\path\to\repository' --days 7 --output git-history.html
```

Open `git-history.html` in your browser. For a first run with the included example data:

```bash
python3 scripts/generate_git_graph.py --input-json examples/demo.json --output git-history.html
```

Useful options:

| Goal | Option |
| --- | --- |
| Include inactive branches | `--all-branches` |
| Select a different primary branch | `--base master` |
| Include remote refs already stored locally | `--remotes` |
| Save validated source data alongside the report | `--also-json git-history.json` |
| Use a reproducible reference date | `--as-of 2000-01-08` |
| Combine repositories | Repeat `--repo` for each repository |

Run `python3 scripts/generate_git_graph.py --help` for all options. Use `py` instead of `python3` with the Windows Python launcher.

## Use as an agent skill

The internal skill name is **`digitrail`**. Keep [`SKILL.md`](SKILL.md), `scripts/`, `assets/` and `references/` together in the skill folder used by your assistant, following that environment's installation instructions. Downloading the repository alone does not install a skill in an account.

Example requests:

> Use diGITrail to visualize the branches and merges in this repository from the last seven days.

> Generate an offline Git history report for these two local repositories, with main in the first lane.

The assistant needs access to Python and a local Git checkout, or complete, verified commit data from a connector. The [connector JSON format](references/data-format.md) documents the alternative input path.

## How history is interpreted

The default seven-day window selects branch heads with recent **commit activity**. Complete reachable ancestry is retained to show where those branches forked, even when it extends beyond the window. Git does not normally record reliable branch creation dates.

- Branch labels on shared commits are inferred visual associations. A commit may belong to the ancestry of several branches.
- Graph edges use commit parent relationships. Pull request targets alone do not establish ancestry.
- The default exploration limit is 30,000 commits. Generation stops if that limit is exceeded; adjust `--max-history` when appropriate.
- Missing parents in a shallow clone are reported as incomplete history. Repositories can also legitimately contain multiple unrelated roots.
- Reports embed commit messages, branch names and repository metadata. Review generated reports before sharing them publicly.

## Project structure

| Path | Purpose |
| --- | --- |
| [`SKILL.md`](SKILL.md) | Agent instructions and accuracy requirements |
| [`scripts/generate_git_graph.py`](scripts/generate_git_graph.py) | Standalone Python CLI |
| [`assets/template.html`](assets/template.html) | Self-contained report interface |
| [`examples/`](examples/) | Fictional demo, editable JSON and reproduction guide |
| [`docs/images/`](docs/images/) | Public preview image and vector export |
| [`references/data-format.md`](references/data-format.md) | Connector input schema |
| [`tests/`](tests/) | Local Git ancestry and optional browser regression tests |
| [`.github/ISSUE_TEMPLATE/`](.github/ISSUE_TEMPLATE/) | Bug reports and feature suggestions |

## Contributing

Bug reports, documentation improvements and reproducible examples are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for the development workflow and privacy guidelines for examples.

```bash
python3 -m unittest discover -s tests -v
```

The optional browser test uses a locally installed Chromium browser through Playwright. The generator does not require either package. No hosted CI is needed to run the tests.

## License and commercial permissions

**diGITrail is source-available under the PolyForm Noncommercial License 1.0.0.**
Personal and other uses permitted by the license are free. Commercial use is **not granted** by this license and requires separate written permission from the copyright holder. See [`LICENSE`](LICENSE) for the full binding terms. To enquire about a commercial license, contact the project owner through GitHub.

This is a noncommercial software license, **not an OSI-approved open-source license**.

Required Notice: Copyright 2026 0biguan (https://github.com/0biguan/diGITrail)
