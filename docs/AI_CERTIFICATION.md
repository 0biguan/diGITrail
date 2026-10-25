# AI distribution certification log

## Protected baseline

- Source repository: 0biguan/diGITrail
- Stable main commit recorded before experiment:
  ab5cec73c2b5a7a7264d382d6f53959aeaa58445
- Baseline Git tree:
  1f480e54f2c9a283baa34868a8552de20b9eb78e
- Experimental branch: feature/ai-distribution, created from that commit.
- Synthetic fixture repository: 0biguan/diGITrail-sample
- Fixture snapshot selected for hosted CI:
  d0cc925e28b46345ffcff12fda61e273a232cde0

The experiment must never update stable main, rewrite the fixture's history,
push tags, or launch mutating GitHub workflows.

## Confirmed by read-only GitHub API inspection (2026-10-25)

- 29 branch references, 26 distinct branch-head SHAs, eight published tag refs.
- main reachable history (at the time of inspection): 61 commits; 13 merge
  commits, including one three-parent octopus merge; one authentic root; all
  parent SHAs represented in the returned history.
- Six representative branch walks also reached roots without missing parents.
- The original renderer uses Python standard-library modules, a local HTML
  template and Git or validated connector JSON.
- The current renderer has no tag rendering; the fixture's SCENARIOS.md
  still described its tags as unpublished at the time of inspection.

API inspection is not a substitute for executing the original renderer.

## Automatic acceptance tests (GitHub-hosted runners)

The single pull-request workflow in this experiment:

1. Executes existing renderer regression tests and the new packaging tests.
2. Retrieves the pinned synthetic fixture without changing its history.
3. Runs the synthetic topology verifier.
4. Executes the original renderer with a fixed date and all branches.
5. Asserts expected Git ancestry completeness and standalone HTML markers.
6. Builds a deterministic skill candidate ZIP and uploads temporary artefacts.

A successful CI run certifies the tested CLI/package *within the hosted
environment*. It does not establish ChatGPT skill installation or generic
zero-install use.

## First independent zero-install result (2026-10-25)

**FAIL in ordinary ChatGPT chat**, from the user's clean-session report:

- The assistant could consult SKILL.md on feature/ai-distribution.
- Its Python 3.13.5 and Git 2.47.3 were present, but
  `curl` could not resolve `raw.githubusercontent.com` (DNS error 6).
- It could not transfer the original renderer/template and complete verified
  Git DAG into the Python execution environment.
- No original interactive HTML was produced.
- This does **not** demonstrate failure of the renderer or CLI.
- A recommendation to manually upload ZIP files would not meet the user's
  zero-install acceptance condition.

**Follow-up Work result (2026-10-25): user-reported SUCCESS.** The user
confirmed that the fresh ChatGPT Work experiment using the experimental
branch prompt worked. This is evidence that the Work zero-install path is
feasible in that user's environment, but the HTML file, executed commands,
and Git relationship fidelity have not been independently inspected in
this conversation. Do not classify it as broadly certified or assume that
ordinary ChatGPT now works. Additional acceptance: examine the real HTML
and repeat the same prompt in a second fresh Work session.

## Independent audit of the actual Work HTML (2026-10-25)

The user supplied the produced `diGITrail-sample-7days.html` for direct inspection.

**Result: PASS for inspected output and interactive functionality.**

- File size: 58,135 bytes; SHA-256:
  `fc550f0848201c53c38dcad4fdc2ed8620b34544714ae1b4e38547c13bcc3834`.
- After replacing the generated JSON payload and repo tab with their two
  source placeholders, the submitted HTML matches the branch's original
  `assets/template.html` **exactly** (31,267 characters). This verifies
  reuse of the exact shipped renderer interface rather than Mermaid or an
  independently recreated template.
- Embedded graph: 102 unique commits, 115 parent references with no
  missing targets, one root, 13 merges (including one three-parent octopus).
- All 29 GitHub remote branch heads matched their published commit SHA.
  The report has 30 branch refs because it additionally contains a local
  `main` alongside `origin/main` at the same SHA; 26 unique heads.
- Automated Chromium audit of the actual file: **19/19 checks passed**,
  **zero JavaScript page errors**. Verified Structure mode (49 displayed
  nodes), All commits (102), all branch labels, chronology reversal,
  SHA search, branch highlighting, zoom, commit details, correct GitHub links,
  and an actual SVG export download.
- Output contains inline CSS/JavaScript/payload without external scripts or
  CDN assets; works as a standalone browser document.
- The file's embedded cutoff is
  `2026-10-18T11:48:20.652115+00:00`, corresponding to the requested
  seven-day window at report creation.

**Scope of certification:** The user-reported fresh ChatGPT Work zero-install
trial produced a technically valid diGITrail report using the exact shipped
HTML template and matching GitHub refs. The original Work terminal/command
history was not supplied, so invocation of the Python script cannot be
independently attested from command logs. One successful Work run does not
prove compatibility with ordinary ChatGPT or all Work configurations.

**Minor observations:** The two refs `main` and `origin/main` refer to
the same commit, so the UI shows 30 references for 29 remote branches.
Tags are not displayed by the current renderer even when they exist on
GitHub. These do not invalidate the tested branch/commit graph.

## Installed ChatGPT skill: uploaded output audit (2026-10-25)

**Result: successful user-reported installed-skill run; inspected HTML PASS.**
The user reported installing the packaged diGITrail skill into ChatGPT and
receiving `diGITrail-sample-history.html`, produced for
`0biguan/diGITrail-sample` from 2026-10-01 00:00 UTC through
2026-10-25 16:48 UTC. The assistant in that run reported using the
skill's original Python generator/template, 29 remote branches and 102
commits; its Chromium testing was blocked in that environment.

The supplied HTML was independently audited:

- Output size: **58,206 bytes**; SHA-256:
  `ef8964916bc1b5516ac56da644c21ac2bfe5231e736800b8b175aa9b2ec43a89`.
- After replacing only the embedded JSON payload and generated repository
  tab with the source placeholders, the HTML **exactly matches**
  `assets/template.html` from the experimental source branch.
- Embedded records: **102 unique commits**, **115 verified ordered parent
  relations**, **no missing parent nodes**, **one true root**, **13 merge
  commits**, including an **octopus merge with three parents**.
- **29 remote branch references** (26 distinct heads) were present and
  all match the corresponding GitHub published branch SHA. The selected
  primary branch is `origin/main`. Unlike the earlier Work report, the
  installed-skill output does not duplicate it as a separate local `main`.
- The embedded commit IDs, messages, dates and ordered parents match those
  in the earlier successful zero-install Work report exactly. Its remote
  branch name-to-SHA mapping is also identical.
- **26/26 automated Chromium interaction checks passed** during an
  independent audit, with no page JavaScript errors. Tests covered Structure
  (49 nodes), All commits (102), actual SVG generation/export, chronological
  reversal, filters/search, lane positioning, branch labels, highlighting,
  zoom, details and working GitHub commit links.
- The audit loaded the report's unmodified HTML content into Chromium using
  the browser automation API; direct `file://` navigation was blocked by
  the audit sandbox's administrative policy. This does **not** affect the
  JavaScript interaction and SVG-export results.
- Self-contained CSS, JavaScript and graph JSON; no CDN assets/scripts.

**Provenance limit:** the HTML is verified as genuine diGITrail output and
the user confirms the installed-skill workflow. We have **not** inspected
that ChatGPT run's terminal logs, so the exact execution mechanism cannot
be independently established from the HTML alone. Do not claim that
installation or code execution will work for every ChatGPT plan or workspace.

## Manual acceptance tests still required

- User-reported installed ChatGPT skill test succeeded; independently audited
  HTML matches original template and GitHub ancestry. Review terminal logs
  if exact script invocation needs attestation; repeat on other supported
  plans/workspaces before claiming broad compatibility.
- ChatGPT Work zero-install output has already been independently audited.
  Additional clean Work runs would assess reproducibility.
- A separate ordinary ChatGPT chat failed because the Python environment
  could not download the source. Do not describe ordinary-chat zero-install
  as supported without a new successful test.
- Repeat on each supported plan/surface; record any required GitHub connector,
  code-execution access, network restrictions, and failures.
- CLI, Work and installed-skill reports have verified ancestry and template
  consistency; further plan/surface checks remain outside this test scope.

## Promotion gate

Keep the draft PR unmerged until the hosted CI passes, code changes are
reviewed and the remaining manual capability tests are labelled accurately.
No undocumented assertion of universal ChatGPT compatibility.
