# Connector JSON input format

The CLI accepts one dataset or a JSON object of datasets. Each dataset uses the following schema:

```json
{
  "displayName": "sample-repository",
  "baseBranch": "main",
  "originUrl": "https://github.com/example/sample-repository",
  "refs": {
    "main": "full-commit-sha-A",
    "feature/task": "full-commit-sha-B"
  },
  "nodes": [
    {
      "id": "full-commit-sha-A",
      "date": "2000-01-01",
      "clock": "10:25",
      "msg": "Merge feature/task",
      "parents": [
        {"id": "parent-1-sha", "direct": true, "verified": true},
        {"id": "parent-2-sha", "direct": true, "verified": true}
      ]
    }
  ]
}
```

* Placeholder IDs above are explanatory only, not a valid complete input. Real input **must include all parent nodes**, down to root or an explicitly documented history boundary. The validator refuses references to missing parents.
* Parent order matters. The **first parent** represents the primary continuation for a merge commit.
* Use committer dates in UTC (`YYYY-MM-DD` and `HH:MM`) where possible. Avoid guessing missing timestamps.
* SHA values should preferably be the full SHA returned by Git. They must be unique and consistent across nodes and refs.
* `refs` represents the selected branch heads. `baseBranch` must match one of its keys.
* A commit can be reachable from multiple branch heads; a branch label is a UI interpretation, not an exclusive property of the commit.
* Do not substitute GitHub pull-request base/head branch names for actual SHA parent links.
* `originUrl` must be a trusted http(s) repository URL for clickable commit links; leave empty for local-only histories.

For multiple datasets, use:

```json
{
  "repo0": {"displayName": "repo A", "refs": {}, "nodes": []},
  "repo1": {"displayName": "repo B", "refs": {}, "nodes": []}
}
```

The inner `{}` and `[]` are placeholders; populate each with valid data as in the full example.
