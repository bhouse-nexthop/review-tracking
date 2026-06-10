# sonic-mgmt-prs

Review tracking for **`sonic-net/sonic-mgmt`**, reviewer **`bhouse-nexthop`**.
Governed by [../POLICY.md](../POLICY.md).

## Files

| File | What it is |
|------|------------|
| `review-queue.md` | Generated tracking table: per-PR CI status, last CI, merge state, next action, last logged action. |
| `review-findings-<date>.md` | Deep-review briefs (Rule 4) for that sweep — description summary, existing reviews, author affiliation, type, complexity, matches-description?, conflict & duplication likelihood, reviewer flags. |
| `actions.jsonl` | Append-only **action ledger** — every conflict ping, `/azp run`, CI-failure notify, and deep review we've done, with dates. This is what makes the sweep idempotent (no repeated pings/runs). |
| `helpers/sweep.py` | The sweep tool (fetch → classify → ledger-gated plan → dry-run/apply → render table). |
| `helpers/review_prompt.md` | The per-PR deep-review prompt template used to drive Rule 4 reviews. |
| `data/` | Raw JSON/TSV snapshots from the last sweep (provenance/debug). |
| `data/author_org_map.csv` | Cached SII author→org map (`sonic-net/sonic-tsc`), authoritative source for affiliation. Refresh: `gh api repos/sonic-net/sonic-tsc/contents/sii_author_map/author.csv --jq .content \| base64 -d > data/author_org_map.csv` |

## First sweep — 2026-06-10

Of 61 open requested-reviewer PRs:
- **15 conflicting** → conflict-ping sent (Rule 1).
- **25 clean + stale/failing CI** → `/azp run` posted (Rules 2/3).
- **21 fresh (clean + passing + recent)** → deep-reviewed (Rule 4) →
  `review-findings-2026-06-10.md`.

See the ledger (`actions.jsonl`) for the authoritative per-PR action history.
