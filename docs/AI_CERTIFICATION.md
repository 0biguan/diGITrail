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

## Manual acceptance tests still required

- Upload the candidate ZIP to an eligible ChatGPT workspace and verify that
  ChatGPT installs and invokes digitrail and delivers the real HTML.
- In a clean ChatGPT conversation with no prior diGITrail files, provide only
  the two GitHub URLs and the time window. Verify that actual SKILL.md, code,
  and template were read and used, and that the generated HTML opens.
- Repeat on each supported plan/surface; record any required GitHub connector,
  code-execution access, network restrictions, and failures.
- Compare the output with the pinned CLI report, including parent edges,
  branch names, both views, time order and SVG export. Browser interaction
  is not yet automatically certified by this workflow.

## Promotion gate

Keep the draft PR unmerged until the hosted CI passes, code changes are
reviewed and the remaining manual capability tests are labelled accurately.
No undocumented assertion of universal ChatGPT compatibility.
