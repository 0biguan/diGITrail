# diGITrail for AI: three usage modes (experimental)

This document applies to the isolated AI-distribution experiment. The original
command-line renderer remains unchanged.

## 1. Zero-installation AI (ChatGPT Work: successful user trial)

Provide the diGITrail source URL and a target repository URL:

> Read the real diGITrail SKILL.md and renderer at
> https://github.com/0biguan/diGITrail/tree/feature/ai-distribution
> and generate its original self-contained HTML graph for
> https://github.com/0biguan/diGITrail-sample with activity from
> 1 October 2026 (00:00 UTC) through the time of this request.
> Use real Git parent relationships. Do not substitute another graph renderer.
> Do not make any changes to either GitHub repository.

This is a **request**, not an installation mechanism. A ChatGPT environment must
be able to read the project files, access complete Git ancestry and run Python.
If any capability is absent, the assistant must say so and must not fabricate a
diGITrail report. Standard Python sandboxes may have no direct network access:
obtain source and Git data with permitted tools first, then pass local files to
the renderer. Never download and execute remote code without reviewing the
source and using a trusted, pinned commit.

Read SKILL.md and references/data-format.md before using the connector path.
For each branch HEAD, obtain commit IDs, ordered parent IDs, UTC timestamps and
subjects, recursively tracing all parents. Build validated JSON and execute:

    python3 scripts/generate_git_graph.py --input-json /tmp/commits.json --output /tmp/git-history.html

Deliver the actual generated HTML file. GitHub pull-request base metadata does
not establish ancestry. Missing parents cannot be invented or omitted silently.

**Not certified:** a fresh, ordinary ChatGPT session accepting a bare GitHub
URL and automatically completing all steps, or compatibility with every plan.

### Best next test: ChatGPT Work with a network-enabled cloud computer

A fresh, ordinary ChatGPT chat has already failed this experiment
(2026-10-25): it could read SKILL.md but its Python shell could not resolve
raw.githubusercontent.com, and it could not place complete source and Git
ancestry into that Python environment. This is an **environment/transport**
failure, not a renderer regression. Downloading ZIPs manually defeats the
zero-install goal.

A different test surface is **ChatGPT Work**. Work may provide a cloud
computer, browser, terminal and network access, depending on plan and
workspace controls. The user installs nothing on their own computer.

In a new **Work** conversation, ask:

> Use the original diGITrail from
> https://github.com/0biguan/diGITrail/tree/feature/ai-distribution
> to generate the standalone interactive HTML history for
> https://github.com/0biguan/diGITrail-sample with activity from
> 1 October 2026 (00:00 UTC) through the time of this request.
> Preserve complete verified ancestry to show genuine branch origins.
> Choose the corresponding --as-of and --days cutoff (there is no
> native --since flag). Read SKILL.md from that exact source branch first. If Work has network-enabled
> shell access, retrieve the verified project code and a **full-history** clone
> of the sample into isolated temporary cloud directories. Execute the
> original scripts/generate_git_graph.py with --remotes, and deliver the actual
> generated HTML. Do not modify either GitHub repository, write remote refs,
> launch Actions workflows, or substitute Mermaid. If cloud networking or
> code execution is blocked, report the limitation precisely.

The initial clone is read-only **with respect to GitHub**, but creates
temporary files in the cloud computer, which is allowed in this mode.
Avoid shallow sample checkouts. The output HTML belongs in a separate
temporary results directory. Inspect the downloaded code before running it;
pin a trusted commit when reproducibility matters.

**Test outcome (2026-10-25):** A clean ChatGPT Work session successfully
produced a standalone HTML report. The actual uploaded HTML was inspected:
its generated structure matches the original `assets/template.html` exactly;
all 29 published GitHub branch heads match; 102 commits and complete parent
links are present; 19/19 Chromium UI checks passed with no JavaScript errors.
See `docs/AI_CERTIFICATION.md` for the audit evidence and scope.
The original Work terminal log has not been examined, and the standard
ChatGPT chat attempt failed due to environment networking restrictions.
Work availability and cloud permissions vary; do not claim universal support.

Official references:
- https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex
- https://help.openai.com/en/articles/20001280-using-cloud-browser-in-chatgpt

## 2. Installed skill (successful user trial; account-dependent)

Generate the ZIP from the repository without modifying production code:

    python3 scripts/package_skill.py --output dist/digitrail-skill.zip

This creates digitrail/SKILL.md plus the renderer, template, reference schema
and licence. In ChatGPT accounts eligible for personal skills, navigate to
Plugins > Skills > Create > Upload from your computer and upload the candidate.
ChatGPT performs its own scan and may accept, flag, or reject the package.
Installation does not grant GitHub access or a Python runtime.

Example after successful installation:

> Use diGITrail to generate the HTML commit graph for
> 0biguan/diGITrail-sample covering activity from 1 October 2026
> through the time of this request, with full branch ancestry.

The ZIP structure and embedded code are tested automatically. **Observed
test (2026-10-25):** a user installed the package into ChatGPT and
generated an HTML report using the installed skill. The actual output was
independently audited: it exactly matched the original shipped template,
contained the same 102 authentic commits and 29 GitHub branch refs as the
successful Work report, and passed **26/26 Chromium UI checks**, including
SVG export. The originating ChatGPT terminal log was not inspected and
availability varies by account. See `docs/AI_CERTIFICATION.md`.

Official reference: https://help.openai.com/en/articles/20001066-skills-in-chatgpt

**Ordinary Chat limitation (2026-10-25):** The same user tested an installed
skill in a regular Chat conversation; that environment could not find the
`digitrail` skill, `generate_git_graph.py` or its files, even though Git
was installed. No report was produced. This is a failure of skill visibility
in that tested session, **not** a failure of the original renderer and not
evidence that installation was lost. For now, the installed-skill workflow is
verified in **ChatGPT Work**, not in ordinary Chat. Account and session
permissions may vary.

## 3. Local command line (existing stable path)

Python 3.9+ and Git:

    python3 scripts/generate_git_graph.py --repo /path/to/repository --days 7 --output git-history.html

The CLI is independent of ChatGPT. No local Python packages beyond the standard
library are needed for its renderer.

## Guarantees and limits

- All three modes should use the **same** scripts/generate_git_graph.py.
- The original HTML must keep Structure/All commits, time reversal, search,
  branch highlighting and SVG export.
- The generator now reads lightweight and annotated Git tags and includes
  validated tag metadata in the JSON input format. Their commits appear in
  Structure view, gold pills share the Associated references column, and
  the summary shows separate branch/tag counts with All/Branches/Tags
  label filters. Tags are scoped to the selected branch ancestry.
- The source-backed GitHub sample provides eight published tag fixtures for
  the regression workflow. This new feature is certified only once the
  corresponding GitHub-hosted tag tests pass.
- Use a synthetic test repository and test without writing any Git refs.
- Do not promise universal zero-install compatibility before fresh-session
  tests establish the specific supported ChatGPT surfaces.
- Do not merge this experiment into main until regression results are reviewed.
