#!/usr/bin/env python3
"""diGITrail: create a self-contained, interactive GitKraken-like commit graph.

Read-only Git access, Python 3.9+ standard library. The renderer is bundled
with the skill and does not load remote scripts, images or fonts.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from collections import deque
from typing import Any
from urllib.parse import urlsplit, urlunsplit

SKILL_DIR = Path(__file__).resolve().parents[1]
TEMPLATE = SKILL_DIR / "assets" / "template.html"
SHA_RE = re.compile(r"^[0-9a-f]{40,64}$")


class GraphError(Exception):
    pass


def git(repo: Path, *args: str) -> str:
    env = os.environ.copy()
    env["GIT_OPTIONAL_LOCKS"] = "0"
    env["GIT_TERMINAL_PROMPT"] = "0"
    cmd = ["git", "-C", str(repo), *args]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          env=env, check=False)
    if proc.returncode:
        raise GraphError(f"Git could not complete {' '.join(args[:2])}: "
                         f"{proc.stderr.decode('utf-8', 'replace').strip()}")
    return proc.stdout.decode("utf-8", "replace")



def safe_origin_url(url: str | None) -> str:
    """Keep only HTTPS/HTTP repository origins without embedded credentials."""
    if not url:
        return ""
    raw = url.strip()
    ssh = re.fullmatch(r"git@([^:/]+):([^\s]+)", raw)
    if ssh:
        raw = f"https://{ssh.group(1)}/{ssh.group(2)}"
    if raw.startswith("ssh://git@"):
        raw = "https://" + raw.removeprefix("ssh://git@")
    parsed = urlsplit(raw)
    if parsed.scheme not in {"https", "http"} or not parsed.hostname:
        return ""
    path = parsed.path.rstrip("/")
    if path.endswith(".git"):
        path = path[:-4]
    # Omit user:password@, access tokens, queries, fragments and anchors.
    host = parsed.hostname
    if parsed.port:
        host += f":{parsed.port}"
    return urlunsplit((parsed.scheme, host, path, "", ""))


def repo_origin_url(repo: Path) -> str:
    try:
        raw = git(repo, "remote", "get-url", "origin").strip()
    except GraphError:
        return ""
    return safe_origin_url(raw)

def read_refs(repo: Path, include_remotes: bool) -> dict[str, str]:
    namespaces = ["refs/heads"] + (["refs/remotes"] if include_remotes else [])
    output = git(repo, "for-each-ref", "--format=%(refname)%09%(objectname)", *namespaces)
    refs: dict[str, str] = {}
    for line in output.splitlines():
        fields = line.split("\t", 1)
        if len(fields) != 2:
            continue
        refname, sha = fields
        if refname.endswith("/HEAD") or not SHA_RE.fullmatch(sha):
            continue
        if refname.startswith("refs/heads/"):
            short = refname.removeprefix("refs/heads/")
        elif refname.startswith("refs/remotes/"):
            short = refname.removeprefix("refs/remotes/")
        else:
            continue
        refs[short] = sha
    return refs


def find_base_branch(repo: Path, refs: dict[str, str], user_base: str | None) -> str:
    if user_base:
        if user_base not in refs:
            raise GraphError(f"Primary branch '{user_base}' was not found: {list(refs)}")
        return user_base
    for name in ("main", "master", "trunk", "develop", "origin/main", "origin/master"):
        if name in refs:
            return name
    try:
        current = git(repo, "symbolic-ref", "--quiet", "--short", "HEAD").strip()
        if current in refs:
            return current
    except GraphError:
        pass
    if not refs:
        raise GraphError("No local Git branches are available")
    return sorted(refs)[0]


def read_commits(repo: Path, max_history: int) -> dict[str, dict[str, Any]]:
    # Use a NUL-terminated record for commit headers. The one-line subject is
    # free of LF. No shell, checkout, fetch, pull, refresh or write operations.
    output = git(repo, "log", "--all", "--date-order", "-z",
                 f"--max-count={max_history+1}",
                 "--format=%H%x1f%P%x1f%ct%x1f%s")
    commits: dict[str, dict[str, Any]] = {}
    for entry in output.split("\x00"):
        entry = entry.strip("\r\n")
        if not entry:
            continue
        fields = entry.split("\x1f", 3)
        if len(fields) != 4 or not SHA_RE.fullmatch(fields[0]):
            raise GraphError("Git history returned an unexpected record")
        sha, parent_str, timestamp, subject = fields
        moment = dt.datetime.fromtimestamp(int(timestamp), dt.timezone.utc)
        commits[sha] = {
            "id": sha,
            "msg": subject.strip(),
            "date": moment.strftime("%Y-%m-%d"),
            "clock": moment.strftime("%H:%M"),
            "timestamp": int(timestamp),
            "parent_ids": parent_str.split() if parent_str else [],
        }
    if len(commits) > max_history:
        raise GraphError(
            f"The repository exceeds {max_history:,} commits in the scanned history. "
            "Increase --max-history (if memory permits) or narrow the branch selection. "
            "An incomplete graph with fabricated origins will not be generated."
        )
    return commits


def reachable(selected_refs: dict[str, str], commits: dict[str, dict[str, Any]]) -> set[str]:
    queue = deque(selected_refs.values())
    selected: set[str] = set()
    while queue:
        sha = queue.popleft()
        if sha in selected:
            continue
        if sha not in commits:
            raise GraphError(f"Commit not found in history: {sha}. Is this a shallow clone?")
        selected.add(sha)
        queue.extend(commits[sha]["parent_ids"])
    return selected


def normalize_dataset(data: dict[str, Any], label: str) -> dict[str, Any]:
    """Validate connected Git graph and normalise input from Git or connector."""
    if not isinstance(data, dict):
        raise GraphError("The dataset must be a JSON object")
    raw = data.get("nodes")
    refs = data.get("refs")
    if not isinstance(raw, list) or not raw or not isinstance(refs, dict) or not refs:
        raise GraphError("Non-empty nodes and branch refs are required")
    base = data.get("baseBranch") or ("main" if "main" in refs else next(iter(refs)))
    if base not in refs:
        raise GraphError(f"Primary branch not found: {base}")
    id_map = {}
    for node in raw:
        if not isinstance(node, dict) or not isinstance(node.get("id"), str):
            raise GraphError("Invalid node")
        sha = node["id"]
        if sha in id_map:
            raise GraphError(f"Duplicate commit {sha}")
        id_map[sha] = node
        if not isinstance(node.get("parents", []), list):
            raise GraphError(f"Invalid parent list for {sha}")
        date = node.get("date")
        if date and (not isinstance(date, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date)):
            raise GraphError(f"Invalid date for {sha}")
    for name, sha in refs.items():
        if not isinstance(name, str) or not isinstance(sha, str) or sha not in id_map:
            raise GraphError(f"Reference '{name}' has no corresponding node: {sha}")
    for sha, node in id_map.items():
        for parent in node.get("parents", []):
            pid = parent.get("id") if isinstance(parent, dict) else parent
            if pid not in id_map:
                raise GraphError(f"Missing parent {pid} of commit {sha}. "
                                 "Provide the complete history or explicitly mark a known boundary.")
    # Kahn cycle validation. Iterative so long linear histories cannot overflow.
    degree = {sha: len(node.get("parents", [])) for sha, node in id_map.items()}
    children: dict[str, list[str]] = {sha: [] for sha in id_map}
    for sha, node in id_map.items():
        for parent in node.get("parents", []):
            pid = parent.get("id") if isinstance(parent, dict) else parent
            children[pid].append(sha)
    pending = deque(sha for sha, count in degree.items() if count == 0)
    visited = 0
    while pending:
        current = pending.popleft()
        visited += 1
        for child in children[current]:
            degree[child] -= 1
            if degree[child] == 0:
                pending.append(child)
    if visited != len(id_map):
        raise GraphError("A cycle was detected in the commit history")
    graph: dict[str, set[str]] = {sha: set() for sha in id_map}
    for sha, node in id_map.items():
        for p in node.get("parents", []):
            pid = p["id"] if isinstance(p, dict) else p
            graph[sha].add(pid)
            graph[pid].add(sha)
    # A disconnected graph is allowed only if history is genuinely unrelated.
    remaining = set(graph)
    components = 0
    while remaining:
        components += 1
        start = remaining.pop()
        waiting = [start]
        while waiting:
            for neighbor in graph[waiting.pop()]:
                if neighbor in remaining:
                    remaining.remove(neighbor)
                    waiting.append(neighbor)
    clean_nodes = []
    for item in raw:
        node = dict(item)
        node["parents"] = [
            ({"id": p, "direct": True, "verified": True} if isinstance(p, str)
             else {"direct": True, "verified": True, **p})
            for p in item.get("parents", [])
        ]
        clean_nodes.append(node)
    normalized = dict(data)
    normalized.update(displayName=label, baseBranch=base,
                      components=components, nodes=clean_nodes, refs=refs,
                      originUrl=safe_origin_url(data.get("originUrl")))
    return normalized


def dataset_from_git(repo: Path, days: int, cutoff: dt.datetime,
                     base: str | None, include_all: bool,
                     remotes: bool, max_history: int,
                     origin_url: str | None) -> dict[str, Any]:
    if not repo.is_dir():
        raise GraphError(f"Repository directory does not exist: {repo}")
    git(repo, "rev-parse", "--is-inside-work-tree")
    refs = read_refs(repo, include_remotes=remotes)
    main = find_base_branch(repo, refs, base)
    commits = read_commits(repo, max_history=max_history)
    active = {name: sha for name, sha in refs.items()
              if sha in commits and (include_all or commits[sha]["timestamp"] >= int(cutoff.timestamp()) or name == main)}
    if not active:
        active = {main: refs[main]}
    ids = reachable(active, commits)
    # Reachable ancestry is complete, rather than inventing truncated parents.
    nodes = []
    for sha in ids:
        c = commits[sha]
        nodes.append({
            "id": sha,
            "msg": c["msg"],
            "date": c["date"],
            "clock": c["clock"],
            "parents": [{"id": p, "direct": True, "verified": True} for p in c["parent_ids"]],
        })
    nodes.sort(key=lambda item: (item["date"], item["clock"], item["id"]), reverse=True)
    label = repo.resolve().name
    data = {"repo": label, "displayName": label,
            "originUrl": safe_origin_url(origin_url) if origin_url is not None else repo_origin_url(repo),
            "baseBranch": main,
            "nodes": nodes, "refs": active, "days": days,
            "cutoffUtc": cutoff.isoformat(),
            "scope": "Branches with recent commits; complete ancestry retained to show their origins"}
    return normalize_dataset(data, label)


def html_report(datasets: dict[str, dict[str, Any]]) -> str:
    if not TEMPLATE.is_file():
        raise GraphError(f"HTML template not found: {TEMPLATE}")
    template = TEMPLATE.read_text(encoding="utf-8")
    payload = json.dumps(datasets, ensure_ascii=False, separators=(",", ":"))
    # Prevent an untrusted Git commit subject from closing the script element.
    payload = payload.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    payload = payload.replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    first = next(iter(datasets))
    tabs = "".join(
        '<button data-repo="' + html_escape(key) + '"' + (' class="chosen"' if key == first else '') + '>' +
        html_escape(datasets[key]["displayName"]) + '</button>'
        for key in datasets
    )
    result = template.replace("__GIT_HISTORY_DATA__", payload)
    result = result.replace("__GIT_HISTORY_TABS__", tabs)
    if "__GIT_HISTORY_DATA__" in result or "__GIT_HISTORY_TABS__" in result:
        raise GraphError("The template contains unreplaced placeholders")
    return result


def html_escape(text: str) -> str:
    return (str(text).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--repo", action="append", type=Path, metavar="GIT_PATH",
                       help="Local repository (repeatable; never modifies Git)")
    group.add_argument("--input-json", type=Path,
                       help="Normalized commit and branch-ref JSON obtained from a connector")
    parser.add_argument("--output", type=Path, required=True, help="Output path for the standalone HTML report")
    parser.add_argument("--days", type=int, default=7, help="Days of branch activity to include (default: 7)")
    parser.add_argument("--as-of", help="Reference UTC date in YYYY-MM-DD format (reproducible)")
    parser.add_argument("--base", help="Primary branch (main, master, etc.)")
    parser.add_argument("--all-branches", action="store_true",
                        help="Include all branches, including inactive ones")
    parser.add_argument("--remotes", action="store_true",
                        help="Include remote refs already available locally (never fetches)")
    parser.add_argument("--max-history", type=int, default=30000,
                        help="Maximum commits scanned per repository; fail if exceeded")
    parser.add_argument("--origin-url", help="HTTPS repository URL for commit hyperlinks")
    parser.add_argument("--also-json", type=Path, help="Also save validated JSON for later reuse")
    args = parser.parse_args(argv)
    if args.days < 1 or args.max_history < 1:
        parser.error("--days and --max-history must be greater than zero")
    now = (dt.datetime.fromisoformat(args.as_of).replace(tzinfo=dt.timezone.utc)
           if args.as_of else dt.datetime.now(dt.timezone.utc))
    cutoff = now - dt.timedelta(days=args.days)
    try:
        if args.input_json:
            raw = json.loads(args.input_json.read_text(encoding="utf-8"))
            if "nodes" in raw and "refs" in raw:
                raw = {"repo0": raw}
            if not isinstance(raw, dict) or not raw:
                raise GraphError("The input JSON must contain one or more datasets")
            datasets = {key: normalize_dataset(value, value.get("displayName") or str(key))
                        for key, value in raw.items()}
        else:
            if args.origin_url is not None and len(args.repo) != 1:
                raise GraphError("--origin-url is supported with exactly one --repo. For multiple repositories, "
                                 "use their existing local Git origins or --input-json.")
            datasets = {}
            for index, repo in enumerate(args.repo):
                data = dataset_from_git(repo, days=args.days, cutoff=cutoff, base=args.base,
                                        include_all=args.all_branches, remotes=args.remotes,
                                        max_history=args.max_history, origin_url=args.origin_url)
                datasets[f"repo{index}"] = data
        report = html_report(datasets)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")
        if args.also_json:
            args.also_json.parent.mkdir(parents=True, exist_ok=True)
            args.also_json.write_text(json.dumps(datasets, ensure_ascii=False, indent=2), encoding="utf-8")
        for key, data in datasets.items():
            print(f"{data['displayName']}: {len(data['nodes'])} commits, "
                  f"{len(data['refs'])} branches, {data['components']} component(s), "
                  f"primary={data['baseBranch']}")
        print(f"HTML generated: {args.output}")
        return 0
    except (GraphError, OSError, ValueError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
