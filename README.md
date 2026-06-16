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
python3 helpers/sweep.py            # dry-run: print the plan (no writes)
python3 helpers/sweep.py --apply    # post comments (rules 1/2/3/5) + update actions.jsonl
```

**Files:** `review-findings.md` is the single human doc — a minimal, recommendation-sorted
list of PRs **awaiting our action** (a PR drops off once it's approved/merged or handed back
to the author). `actions.jsonl` is the machine system of record (full state + history). There
is no `review-queue.md`.

Deep reviews (Rule 4) are produced separately — start from a pre-filled brief
skeleton (`helpers/sweep.py --scaffold-review <PR>`, or `--scaffold-eligible` for
the whole eligible set), fill the judgment fields, then record with
`helpers/sweep.py --record-review <PR>`. See POLICY.md §5.

**Always commit *and* push.** Every cycle, commit any changes to `actions.jsonl`,
`review-findings.md`, `helpers/`, `data/`, or the docs and push them — the ledger
is the system of record and must be durable, never left in a dirty working tree
(POLICY.md §4.7).

Other modes:
```bash
python3 helpers/sweep.py --issues            # linked-issue / close-on-merge report (Rule 6)
python3 helpers/sweep.py --commits           # commit-message hygiene report (Rule 9)
python3 helpers/sweep.py --suggest-reviewers <PR>  # cross-company reviewer candidates for a NextHop PR (Rule 8)
python3 helpers/sweep.py --merge <PR>        # dry-run squash/rebase plan + message (Rule 8)
python3 helpers/sweep.py --merge <PR> --apply     # approve+merge — ONLY after a human explicitly tells you to approve this PR (Rule 8); the agent never self-approves
python3 helpers/sweep.py --close-issues <PR> --apply  # manual issue close after merge (Rule 6)
```

This repo contains no secrets; it relies on the local `gh` CLI being
authenticated as the reviewer.
