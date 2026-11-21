# diGITrail

**Interactive Git history graphs for AI agents and the command line.**

diGITrail turns real Git commit ancestry into a **single, self-contained HTML report**. Explore forks, merges, branch names and Git tags with two detail levels, chronology reversal, search, branch highlighting, zoom, commit details and SVG export. The original Python generator and HTML template are shared by all three ways of using diGITrail.

![Current diGITrail interface showing the fictional demo's commits, branches, golden Git tags and All/Branches/Tags controls](docs/images/digitrail-preview.png)

*Real output from the bundled renderer using the [fully fictional demo dataset](examples/demo.json): 23 commits, 6 branch references, 3 merge commits and 6 tags. The sample does not contain anyone's repository history. [Open the interactive demo](https://0biguan.github.io/diGITrail/) *(Ctrl+click to open in a new tab)* · [View the vector export](docs/images/digitrail-preview.svg).*

## Choose how to use diGITrail

| | **1. AI zero-install** | **2. Installed AI skill** | **3. Local Python CLI** |
| --- | --- | --- | --- |
| **Best for** | Asking an assistant to generate a report once, from GitHub URLs | Reusing diGITrail frequently without sharing its source URL each time | Running the generator yourself or scripting it |
| **Setup on your computer** | None | Upload a skill ZIP to an eligible assistant environment | Download/clone diGITrail; have Git and Python 3.9+ |
| **Who executes the generator?** | A capable AI cloud computer | The assistant's eligible execution environment | Your own computer |
| **What must be accessible?** | Original source, full Git history, Python and Git | Installed skill files, full Git history, Python and Git | A local Git checkout or validated JSON input |
| **Confirmed here** | **ChatGPT Work** | **Installed skill in ChatGPT Work** | **GitHub-hosted CLI regression tests** |

**Important compatibility boundary:** the two AI workflows were demonstrated in **ChatGPT Work**, not universally across ChatGPT. A standard Chat session could not access the installed skill, and a separate zero-install standard-Chat attempt could not transfer GitHub files into its Python environment. Other AI assistants (including Claude) **have not been tested**; they might work if they provide equivalent file, Git and code-execution access. See [certification and test limitations](docs/AI_CERTIFICATION.md).

Jump to the method you want:

1. [AI zero-install: use a GitHub URL in ChatGPT Work](#1-ai-zero-install--chatgpt-work)
2. [Installed AI skill: upload once and reuse](#2-installed-ai-skill)
3. [Local Python CLI: run diGITrail yourself](#3-local-python-cli)

## 1. AI zero-install — ChatGPT Work

Use this option if you want to **provide a source URL and a target GitHub repository and receive the original HTML without installing diGITrail**. No code or skill is installed on your own computer.

### Requirements

- A **ChatGPT Work** session (or another assistant with equivalent capabilities) that can use a **network-enabled cloud computer/terminal**.
- Permission to read the source and the Git repository being analysed; a public repository is easiest. Private repositories require separately authorised access. Never paste GitHub tokens into prompts.
- A cloud environment able to run **Git** and **Python 3.9+**, obtain full commit ancestry and branch references, and execute diGITrail's actual Python generator and HTML template.
- A browser to open the downloaded HTML. The report itself does not need internet access.

Opening a normal ChatGPT conversation and simply pasting the URL **does not** automatically install or make the skill available. Availability of Work/cloud-computer capabilities depends on account and workspace permissions.

### Steps

1. Open a **new ChatGPT Work conversation**.
2. Supply the diGITrail **source branch URL**, the target repository URL and the date range using the prompt below.
3. Request an actual **downloadable HTML**. The assistant should use a full-history, read-only (towards GitHub) cloud checkout and the original renderer, not Mermaid or a reimplementation.
4. Open the HTML in a browser. Check **Structure view**, **All commits**, the **All / Branches / Tags** label filter and **Export SVG**.

### Copy-and-paste example

> Use the **original diGITrail** from:
>
> https://github.com/0biguan/diGITrail/tree/main
>
> Generate a standalone interactive HTML report for:
>
> https://github.com/0biguan/diGITrail-sample
>
> Show branch activity **from 1 October 2026 (00:00 UTC) through the time of this request**, including all remote branches and lightweight and annotated tags on their commit ancestry. Preserve verified earlier ancestors required to show genuine forks and merges.
>
> Read `SKILL.md` in the selected source branch. Obtain the reviewed source and a **full-history** Git checkout in temporary cloud directories; use the **original** `scripts/generate_git_graph.py` and `assets/template.html`. Calculate the appropriate `--days` and `--as-of` arguments because the CLI does not currently have a `--since` option; use `--all-branches --remotes` to include inactive remote branches. Return the actual self-contained HTML file.
>
> Do not install software on my computer, push or change either repository, create tags, trigger GitHub Actions or substitute Mermaid or another graph renderer. If the environment cannot execute the original code or read complete Git data, explain the limitation without inventing a report.

The date is deliberately **fixed at 1 October 2026**, rather than “the last seven days”. It selects activity, **not branch-creation dates**; earlier ancestral commits can still appear. A cloud clone only creates temporary **cloud-local** files and does not modify GitHub.

**Validation:** zero-install was demonstrated in ChatGPT Work with the earlier tag-free interface; the updated tag-enabled CLI and browser behaviour have passed GitHub-hosted tests. The updated AI prompt remains subject to Work's actual permissions. [Detailed AI notes](docs/AI_USAGE.md).

## 2. Installed AI skill

Use this option when an eligible assistant can **install diGITrail's packaged skill once** and reuse it by name. You still need Git access to the **target** repository, but you do not need to supply the diGITrail **source URL** in every prompt.

### Requirements

- A ChatGPT account/workspace that offers **personal skill uploads** and makes those skills available in the execution mode you use. The user-tested combination was **an installed diGITrail skill in ChatGPT Work**. It was **not visible** to that user's ordinary Chat session.
- Git and Python 3.9+ in the skill execution environment, or compatible verified Git input. Installation itself does not grant GitHub access or code execution.
- The packaged skill ZIP, which contains the original `SKILL.md`, Python generator, HTML template, schema reference and noncommercial licence.

### Obtain the skill ZIP

**No development setup:** download [`digitrail-skill.zip` from the latest stable GitHub Release](https://github.com/0biguan/diGITrail/releases/latest/download/digitrail-skill.zip). The ZIP is attached automatically by `.github/workflows/release-skill.yml` when a stable release is published. **Before the first release**, build it from the repository as shown below. GitHub Actions test artifacts are temporary, not the official distribution.

**Alternatively**, in a downloaded diGITrail source checkout (Python 3.9+):

```bash
python3 scripts/package_skill.py --output dist/digitrail-skill.zip
```

### Install and try it

1. Where supported in ChatGPT, navigate to **Plugins → Skills → Create → Upload from your computer**. The wording or availability may vary by account/workspace.
2. Upload **`digitrail-skill.zip`**. Follow the platform's security-review prompts; an upload can be refused.
3. Confirm the installed skill is named **`digitrail`**. Start a **new Work session** in which the skill is accessible.
4. Ask for the report without supplying the diGITrail **source** URL:

> Use my **installed diGITrail skill** to generate a downloadable, standalone interactive HTML history for **https://github.com/0biguan/diGITrail-sample**.
>
> Include all remote branches and relevant Git tags, and show activity **from 1 October 2026 (00:00 UTC) through the time of this request**, retaining complete earlier ancestry. Use only the **original Python generator and HTML template from the installed skill**; do not download diGITrail's source again or recreate the graph. Do not modify GitHub or run workflows. If the installed skill is unavailable, tell me what is missing.

Verify the same UI controls as in option 1. The previous installed-skill Work trial generated an authentic report, while a standard-Chat trial could not find the installed files. **Skill visibility is environment-specific**, not a guarantee attached to the account.

## 3. Local Python CLI

Use this option for direct control, offline generation from a repository already on your machine, reproducible inputs, or automation. It does **not** require ChatGPT.

### Requirements and installation

- Windows, macOS or Linux with **Python 3.9+** and **Git**.
- A local Git checkout with **complete history** (not a shallow checkout), or a valid connector JSON file.
- **No external Python packages** for the generator; Chromium/Playwright are only for optional browser tests and screenshots.

Download the [stable source ZIP from `main`](https://github.com/0biguan/diGITrail/archive/refs/heads/main.zip) or clone the repository:

```bash
git clone https://github.com/0biguan/diGITrail.git
cd diGITrail
```

### Generate a report

```bash
python3 scripts/generate_git_graph.py \
  --repo /path/to/your/repository \
  --all-branches --remotes \
  --output git-history.html \
  --also-json git-history.json
```

On Windows PowerShell, use the launcher `py` instead of `python3`:

```powershell
py scripts/generate_git_graph.py --repo 'C:\path\to\repository' --all-branches --remotes --output 'git-history.html'
```

Open `git-history.html` in a modern browser. It is self-contained and works offline. This command reads the checkout without creating commits, branches, tags, or running GitHub workflows.

| CLI option | What it does |
| --- | --- |
| `--days 7` | Include branches with recent commit activity (default seven days) |
| `--as-of YYYY-MM-DD` | Fix the reference date for reproducible results |
| `--all-branches` | Include inactive branches, too |
| `--remotes` | Include locally present remote-tracking references; **does not fetch** |
| `--base master` | Select another primary branch |
| `--max-history 30000` | Set the history limit; fail rather than truncate silently |
| `--also-json history.json` | Export the validated graph source |
| `--input-json history.json` | Generate HTML from verified JSON instead of local Git |
| Repeat `--repo` | Display multiple repositories in one report |

To regenerate the completely fictional demo without touching a real repository:

```bash
python3 scripts/generate_git_graph.py --input-json examples/demo.json --output demo.html
```

Read [the connector input schema](references/data-format.md) or run `python3 scripts/generate_git_graph.py --help` for the complete CLI.

## Interactive demo and visual features

[**Open the live, interactive demo**](https://0biguan.github.io/diGITrail/) *(Ctrl+click to open in a new tab)*. GitHub Pages serves the interactive application in your browser with JavaScript enabled; no download or installation is required. Alternatively, download the source and open `examples/demo.html` locally. After publication the demo is deployed from `main` through `.github/workflows/deploy-demo-pages.yml`.

It uses fixed, **entirely fictional** commits from January 2000; six fictional tags illustrate lightweight, annotated and shared-commit tags. Try the **All / Branches / Tags** visibility filter, **Structure / All commits**, time reversal, searching for `keyboard` or `v1.0.0`, selecting a commit, and **Export SVG**.

- **Actual ancestry:** edges come from ordered Git commit parents, never merely PR metadata.
- **Structure view:** keeps branch tips, forks, merges, roots **and tagged commits** visible while collapsing other linear segments.
- **Associated references:** branch labels keep their branch colours; **tags appear in gold**. The summary separates branch and tag counts.
- **Tag types:** lightweight tags identify a commit directly; annotated tags can also provide a tagger, date and message. Both are resolved to the actual commit, with annotation details in the inspector.
- **Read-only output:** the HTML needs no CDN, external JavaScript, fonts or live server.
- **SVG export:** exports the graph with its currently displayed reference labels.

[Demo data](examples/demo.json) · [How to regenerate the demo and previews](examples/README.md) · [SVG preview](docs/images/digitrail-preview.svg).

## Accuracy, security and limits

Git does **not** reliably record a branch's creation time. A time window refers to **commit activity**; older ancestors remain available to explain forks. Shared commits can be visually associated with multiple branches. For annotated tags, the generator resolves the tag object to its target commit; only tags on commits retained by the selected ancestry appear.

The generator refuses incomplete parents or cycles in connector JSON; shallow checkouts can have incomplete ancestry. Large histories may reach the configured safety limit. Check outputs before sharing: commit messages and branch names from **your** repository are embedded in the HTML.

The AI methods depend on each assistant's actual access to repositories, skill files and code execution; do not assume all assistants or account plans behave the same way. **Other AI assistants, including Claude, are untested here—not known to be incompatible.** See [test evidence and scope](docs/AI_CERTIFICATION.md).

## Project layout and contributing

| Path | Purpose |
| --- | --- |
| [`SKILL.md`](SKILL.md) | Instructions used by AI agents |
| [`scripts/generate_git_graph.py`](scripts/generate_git_graph.py) | Single production renderer, used by all three modes |
| [`scripts/package_skill.py`](scripts/package_skill.py) | Deterministic installable skill ZIP builder |
| [`assets/template.html`](assets/template.html) | Self-contained interactive HTML interface |
| [`examples/`](examples/) | Fictional demo data, rendered HTML and regeneration guide |
| [`docs/images/`](docs/images/) | Generated image and SVG previews |
| [`references/data-format.md`](references/data-format.md) | Verified connector JSON and tags schema |
| [`tests/`](tests/) | Git ancestry, tags, safety and Chromium regression tests |
| [`docs/AI_CERTIFICATION.md`](docs/AI_CERTIFICATION.md) | Tested capabilities and limitations |

Contributions, issues and documentation improvements are welcome; see [CONTRIBUTING.md](CONTRIBUTING.md). Run the tests with:

```bash
python3 -m unittest discover -s tests -v
```

## Releases and downloads

The [Releases page](https://github.com/0biguan/diGITrail/releases) provides versioned distributions. For each published stable `vMAJOR.MINOR.PATCH` release, GitHub Actions checks the release tag belongs to `main`, runs package tests and attaches `digitrail-skill.zip`. GitHub also supplies source archives for each tag. The skill contains the same original renderer, HTML template and licence as the repository. See [CI validation](https://github.com/0biguan/diGITrail/actions/workflows/ai-distribution-validation.yml) for test evidence; AI environment support varies.

## Licence and commercial permissions

diGITrail is **source-available under the PolyForm Noncommercial License 1.0.0**, not an OSI-approved open-source licence. Uses permitted by that licence are allowed; commercial use is **not granted** and requires separate written permission from the copyright holder. Read [`LICENSE`](LICENSE) for the binding terms.

Required Notice: Copyright 2026 0biguan (https://github.com/0biguan/diGITrail)
