# sonic-mgmt-prs

Review tracking for **`sonic-net/sonic-mgmt`**, reviewer **`bhouse-nexthop`**.
Governed by [../POLICY.md](../POLICY.md).

## Files

| File | What it is |
|------|------------|
| `review-findings.md` | **The single human doc** — minimal, recommendation-sorted list of PRs **awaiting our action**, each linking to its full brief. A PR drops off once approved/merged or handed back to the author (changes/info/evidence requested, conflicting, COI-waiting). Undated; regenerated recurringly. |
| `actions.jsonl` | **Machine system of record** — append-only ledger of every action + timestamp, awaiting-other state, and author responses. Powers idempotency and what `review-findings.md` shows/removes. The complete per-PR state. |
| `helpers/sweep.py` | The sweep tool (fetch → classify → ledger-gated plan → dry-run/apply). Maintains the ledger; does **not** write a human table. Deep-review scaffolds: `--scaffold-review <PR>` / `--scaffold-eligible`. |
| `helpers/review_prompt.md` | The per-PR deep-review prompt template (Rule 4). |
| `data/author_org_map.csv` | Cached SII author→org map (`sonic-net/sonic-tsc`). Refresh: `gh api repos/sonic-net/sonic-tsc/contents/sii_author_map/author.csv --jq .content \| base64 -d > data/author_org_map.csv` |
| `data/sii_org_predict.csv` | Cached org contribution scores (for the trust company-bump, >1500). |
| `data/org_normalization.json` | Editable affiliation canonicalization: legal suffixes, aliases, email domains. |

## First sweep — 2026-06-10

Of 61 open requested-reviewer PRs: 15 conflicting → conflict-ping (Rule 1); 25 clean +
stale/failing CI → `/azp run` (Rules 2/3); 21 fresh → deep-reviewed (Rule 4), plus 6 more
that went green after the `/azp run`. See `actions.jsonl` for the authoritative history.
