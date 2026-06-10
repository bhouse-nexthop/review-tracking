# review-tracking

Tracking and triage for open-source PRs where a NextHop engineer is a requested
reviewer. The goal: keep review queues moving (unstick merge conflicts and stale
CI, surface failures to authors, deep-review the PRs that are actually ready)
**without** repeating nudges — every action is recorded and gated.

- **[POLICY.md](POLICY.md)** — the canonical, repo-agnostic policy & procedure
  (sweep workflow, Rules 1–5, the action-ledger idempotency model, follow-up
  procedure, comment templates, affiliation resolution).
- **Per-target subdirectories** — one per tracked upstream repo. First target:
  - **[sonic-mgmt-prs/](sonic-mgmt-prs/)** — `sonic-net/sonic-mgmt`, reviewer
    `bhouse-nexthop`.

## Refreshing a tracker

```bash
cd sonic-mgmt-prs
python3 helpers/sweep.py            # dry-run: print the plan, regenerate review-queue.md
python3 helpers/sweep.py --apply    # post comments (rules 1/2/3/5) + update actions.jsonl
```

Deep reviews (Rule 4) are produced separately and recorded with
`helpers/sweep.py --record-review <PR>`. See POLICY.md §5.

This repo contains no secrets; it relies on the local `gh` CLI being
authenticated as the reviewer.
