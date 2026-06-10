# Review-tracking policy & procedure

A repeatable, **context-aware** procedure for triaging open PRs where a given
GitHub user is a requested reviewer. It sweeps the review queue, takes the
right action for each PR's state, **records every action it takes**, and uses
that record so it never repeats an action (no duplicate "you have merge
conflicts" pings, no repeated `/azp run`).

This document is the canonical policy. Per-tracked-repo data, generated tables,
and helpers live under that repo's subdirectory (e.g. `sonic-mgmt-prs/`).

---

## 1. Scope

- **Input:** open PRs on a target repo where a configured GitHub login is a
  *requested reviewer* (first tracked target: `sonic-net/sonic-mgmt`,
  reviewer `bhouse-nexthop`).
- **Goal:** keep the queue moving — get stuck PRs unstuck (conflicts, stale
  CI), surface failures to authors, and deep-review the PRs that are actually
  ready, while never spamming authors with repeated identical nudges.
- **Boundaries:** we do **not** approve/merge PRs automatically. Deep-review
  briefs are decision support for the human reviewer. Approvals are human.

---

## 2. Definitions

| Term | Meaning |
|------|---------|
| **Clean** | `mergeable == MERGEABLE` (no merge conflicts with the base branch). |
| **Conflicting** | `mergeable == CONFLICTING`. |
| **Last CI** | The max `completedAt` across the PR's status-check rollup. |
| **Stale CI** | Last CI run is **> 2 weeks** before the sweep date. |
| **Fresh / eligible** | Clean **and** latest CI = PASS **and** last CI within 2 weeks. Only these get deep-reviewed (Rule 4). |
| **Action ledger** | Append-only record of every action we take per PR (see §3). The source of truth for "what have we already done?" |
| **Episode** | A continuous span in one state. A new `/azp run` is allowed only in a *new* CI episode (a fresh run has completed since our last one); a new conflict ping only in a *new* conflict episode. |

---

## 3. The action ledger (context-awareness)

Every action is appended to `<repo>/actions.jsonl`, one JSON object per line:

```json
{"pr": 24416, "action": "conflict_ping", "date": "2026-06-10", "detail": "<comment url>"}
{"pr": 24802, "action": "azp_run",       "date": "2026-06-10", "detail": "<comment url>"}
{"pr": 25012, "action": "deep_review",   "date": "2026-06-10", "detail": "review-findings-2026-06-10.md"}
{"pr": 21144, "action": "ci_fail_notify","date": "2026-06-24", "detail": "<comment url>"}
```

Action types: `conflict_ping`, `azp_run`, `ci_fail_notify`, `deep_review`,
`escalate`, `issue_close`, `misleading_flag`, `commit_msg_notice`, `merge`.

**What gets logged — the principle:** log an action **only if its triggering
condition persists after we act**, so the ledger can stop us repeating it.
Conflicts, stale/failing CI, weak commit messages, and misleading descriptions
all persist until the author (or a merge) resolves them — so those actions are
logged. A **title/description rewrite removes its own trigger** (the title is now
adequate; the next scan won't re-flag it), so it is **not** logged — tracking it
would only add noise. If an author later regresses a title we fixed, the next
scan simply catches it again and we re-fix — no ledger needed.

**Golden rule — check the ledger before acting.** No rule fires for a PR if an
equivalent action already exists for the current episode. This is what stops
repeated pings and repeated `/azp run`. Concretely:

- **`conflict_ping`** — only if the PR is conflicting *and* there is no
  `conflict_ping` since the PR last entered the conflicting state. If it was
  pinged, conflicts persist, and the author has been silent past the
  **escalation window (14 days)**, do **not** re-ping — emit `escalate`
  (surface to the human) instead.
- **`azp_run`** — only if no `azp_run` exists whose date is *after* the current
  Last-CI timestamp. I.e. re-run only once per CI episode: if we already
  triggered a run and a new run has since completed, that episode is closed.
- **`ci_fail_notify`** — only once per failing CI episode (keyed off the
  failing run's `completedAt`); re-notify only when a *newer* failing run
  appears.
- **`deep_review`** — only if the PR has had no `deep_review`, **or** the PR
  head SHA changed since the last review (substantive new commits warrant a
  re-review). Trivial rebases don't.
- **`issue_close`** — only after the PR is merged, only for issues that won't
  auto-close (see Rule 6), and only once per (PR, issue) pair.

---

## 4. Sweep procedure (run each cycle)

1. **Fetch** all requested-reviewer PRs + per-PR CI status, reviews, mergeable,
   changed files, head SHA.
2. **Resolve mergeability.** GitHub computes `mergeable` lazily — the first
   query often returns `UNKNOWN`. Query once to trigger computation, then
   re-poll until every PR resolves to `MERGEABLE`/`CONFLICTING`. (See §7.)
3. **Load the ledger** (`actions.jsonl`).
4. **Classify** each PR and apply the first matching rule below, **gated by the
   ledger** (§3). Append any action taken to the ledger.
4b. **Title/description hygiene (Rule 7):** independently of the rule above,
   check **every** PR's title/description and edit the woefully-inadequate ones.
   This is not gated on CI/merge state.
4c. **Commit-message hygiene (Rule 9):** check **every** PR's commit messages and
   post the one-time policy notice to any with weak/missing-signoff messages, so
   the author can fix it before the PR is merge-ready. Not gated on CI/merge
   state; idempotent via `commit_msg_notice`.
5. **Regenerate** the tracking table and findings (`gen_table.py`).
6. **Report** to the human: new actions taken, escalations, and the current
   eligible-for-review set.

### Decision order per PR

```
if CONFLICTING:                      -> Rule 1 (ping author, once per episode; else escalate)
elif CI == FAIL:
    if we previously azp_run'd this failing episode: -> Rule 5 (notify author of failure)
    else:                            -> Rule 3 (azp_run once)
elif CI == PASS and stale:           -> Rule 2 (azp_run once)
elif CI == PASS and fresh:           -> Rule 4 (deep review, if not already reviewed)
elif CI == PENDING:                  -> no-op (a run is in flight; wait for next sweep)
```

---

## 5. Rules

### Rule 1 — Conflicting → ping the author (once per episode)
- **Trigger:** `CONFLICTING` and no `conflict_ping` in the current conflict
  episode.
- **Action:** comment asking the author to confirm relevance and rebase; record
  `conflict_ping`. Re-running CI is pointless until they rebase, so we do *not*
  `/azp run` a conflicting PR.
- **Template:**
  > Hi @{author}, this PR currently has merge conflicts with the target branch.
  > Could you confirm whether it's still relevant/active? If so, please rebase
  > and resolve the conflicts, and we'll review it. Thanks!
- **No repeats:** if already pinged and still conflicting, stay silent until the
  escalation window (14 days of author silence) elapses, then `escalate` to the
  human — never auto-re-ping.

### Rule 2 — Clean + stale CI → force a fresh run (once per episode)
- **Trigger:** `MERGEABLE`, last CI > 2 weeks old, and no `azp_run` after the
  current Last-CI timestamp.
- **Action:** post `/azp run`; record `azp_run`.

### Rule 3 — Clean + failing CI, not yet retried → force a fresh run
- **Trigger:** `MERGEABLE`, CI = FAIL, no `azp_run` in this failing episode.
- **Action:** post `/azp run` (a stale/old failure may be a flake or already
  fixed upstream; re-running confirms the real state); record `azp_run`. On the
  next sweep this PR resolves to Rule 4 (if it goes green) or Rule 5 (if it
  fails again).

### Rule 4 — Fresh PR → deep review
- **Trigger:** `MERGEABLE`, CI = PASS, fresh (within 2 weeks), and no
  `deep_review` for the current head SHA.
- **Action:** produce a **review brief** (one per PR) and record `deep_review`.
  Present briefs to the human; do not approve.
- **Brief fields:** (1) description summary; (2) existing reviews/comments;
  (3) author affiliation + **trust level** (see §8 / §8.1); (4) type — Bug fix / Feature enhancement /
  New test suite / mix; (5) complexity — Low/Med/High; (6) matches description?
  — Yes/Partial/No + note; (7) conflict likelihood vs other open PRs (name
  overlaps); (8) duplication likelihood (name suspected dup or "none seen");
  (9) **linked issue(s)** and their close-on-merge disposition (see Rule 6);
  (9b) **CI actually exercises the test?** — does the VS/KVM PR-gate CI really
  *run* the added/changed test, or is it **skipped** (hardware-only, `is_vs_device`
  early-skip, platform/ASIC gating, a topology marker the CI doesn't cover such as
  `t2`/dualtor, a `conditional_mark` skip, `skipif`, or manual/allure-only)? Report
  **Yes / No / Partial / N-A (not a test)**. **If No/Partial, that is a red flag:**
  the green check did *not* validate the test logic, so the PR needs deeper manual
  review (read the test as if untested) and the recommendation should lean to
  **Get another opinion** (or request a hardware run / proof of a real pass).
  (10) a one-line reviewer flag; and (11) an **overall recommendation** —
  one of **Approve** / **Request changes** / **Get another opinion** /
  **Reject** — with a short rationale. The recommendation is a *suggestion* for
  the human reviewer (who still makes the call); use **Get another opinion**
  when it turns on domain expertise we lack or touches shared infra broadly,
  and **Reject** only when the change is wrong/harmful or duplicates/forecloses
  a better approach.
- **Conflict/duplication seeding:** compute changed-file overlap across the
  eligible set deterministically; use that to seed fields 7–8, then reason over
  the diffs.
- **Not CI-testable → require hardware-pass evidence, UNLESS it's vendor-scoped
  to the author's own hardware.** When CI does not exercise the change (field 9b
  = No/Partial), the default is to **ask the author for evidence of a passing run
  on real hardware** before we approve/merge — we don't merge an unvalidated test
  on a green check alone.
  - **Vendor-own-hardware exception (no evidence required):** trust a change when
    it is **confined entirely to the author's own vendor hardware** — i.e. **(a)**
    the blast radius touches only that vendor's gear (no shared infra, no other
    vendor's behavior), **(b)** the author is from that vendor (or the vendor
    explicitly requested it), and **(c)** review surfaces no red flags. This
    covers both *adding the vendor's hardware to an existing test's allow-list*
    (e.g. Juniper → TH5 so an existing test runs) **and** *a new/modified test
    scoped only to that vendor's hardware*. We should trust vendors modifying
    things that only affect their own equipment, absent review red flags.
  - **Does NOT qualify:** changes to shared test infra, common libraries, or
    behavior that affects other vendors' platforms — even from a vendor — still
    need a real hardware pass (or another validation path) before merge.
- **Affiliation-aware reviewing:** defer to the author's company on facts about
  that company's **own** hardware/platform/products. Do not raise questions an
  author from that vendor is authoritative on — e.g. don't ask a Juniper
  engineer registering a Juniper hwsku to "confirm the chip generation," or a
  Nokia engineer about Nokia platform specifics. **Still** review framework /
  cross-cutting / shared-infra / correctness concerns regardless of author
  (e.g. a change to `tests/common/*`, a fixture used by everyone, or logic that
  affects other vendors' platforms is fair game no matter who wrote it). The
  test: is the flagged item a fact internal to the author's own product (defer)
  or a shared-infra / cross-vendor / code-correctness concern (review)?

### Rule 5 — Post-`/azp run` follow-up (failure path) → notify the author
- **Trigger:** a PR we previously `/azp run` (Rule 2 or 3) comes back **FAIL**
  on the fresh run, and no `ci_fail_notify` exists for this failing episode.
- **Action:** comment notifying the author that CI failed after a re-run and
  asking them to investigate; record `ci_fail_notify`.
- **Template:**
  > Hi @{author}, we re-triggered CI on this PR and it's still failing. Could
  > you take a look at the latest run and address the failures? Once CI is green
  > we'll proceed with review. Thanks!
- **Success path** (the other outcome of a re-run): if the PR comes back clean +
  passing + fresh, it simply becomes eligible and flows into Rule 4 on the same
  or next sweep — no separate action needed.
- **No repeats:** one notify per failing episode; re-notify only on a *newer*
  failing run.
- **Future enhancement (not yet implemented):** before notifying, pull the
  failing job logs and match against known sonic-mgmt **spurious-failure
  patterns**; if the failure matches a known flake, `/azp run` again (within a
  retry cap) instead of bothering the author, and only notify on a
  non-spurious / persistent failure.

---

### Rule 6 — Issue linkage & manual close on merge
We track every issue a PR references so that, **if/when we approve and merge the
PR, any linked issue that GitHub will not auto-close gets closed manually.**

- **Detection (every sweep):** parse the PR body (and title) for issue
  references — `#N`, `owner/repo#N`, and full `…/issues/N` URLs — and note
  whether each is preceded by a **closing keyword**
  (`close[sd]?`, `fix(es|ed)?`, `resolve[sd]?`).
- **Resolve each reference's type/state via the API** — a bare `#N` is often a
  reference to *another PR* or a "based-on" note, **not** an issue this PR
  fixes. Only `type == issue` references are close candidates; ignore PR refs.
- **Classify each linked issue:**
  | Case | GitHub auto-closes on merge? | Our action on merge |
  |------|------------------------------|---------------------|
  | Same-repo issue **+ closing keyword**, merged to default branch | **Yes** | none (verify it closed) |
  | Same-repo issue, **no closing keyword** | No | **manual close** |
  | **Cross-repo** issue (keyword or not) | **No** (GitHub never auto-closes across repos) | **manual close** |
  | Reference is a PR, or a vague "related to" | n/a | none (track only) |
- **On merge:** for each close candidate, `gh issue close <ref> -c "Resolved by
  <repo>#<pr> (merged)."` and record an `issue_close` ledger entry. Never close
  an issue before the PR is actually merged; never close one GitHub already
  auto-closed.
- **Caveat:** auto-close only fires when the PR merges to the **default branch**.
  A PR merged to a release branch (e.g. `202xxx`) will **not** auto-close even a
  same-repo keyword issue → treat as manual close.

### Rule 7 — PR hygiene: fix woefully-inadequate titles/descriptions
Maintainers (`maintain`/`push` on the repo) **edit** a PR's title and/or
description when it is *woefully inadequate*, so the history is searchable and
future readers can understand what changed.

- **Scope:** applies to **all** assigned PRs regardless of CI/merge state — a
  conflicting or failing PR can still have a useless title. (This is *not*
  gated on Rule 4 eligibility.) Run the title/description check across the whole
  queue each sweep.
- **Trigger (be conservative — don't edit for the sake of editing):** only when
  clearly inadequate, e.g. a non-descriptive title (`Update variables`, `fix`,
  `changes`, a bare filename), an **empty/placeholder PR template** (no summary
  beyond `Fixes # (issue)`, all Approach sections blank), or a description that
  plainly doesn't reflect what the diff does. If the title/description is merely
  terse-but-clear, **leave it**.
- **Misleading ≠ inadequate — flag, do NOT rewrite.** A separate, more serious
  case: the title/description **claims something the diff does not actually do**
  (or contradicts the diff). We must **not** rewrite it — we don't know the real
  intent, and the discrepancy means **we cannot properly review the PR at all**.
  Instead post a comment flagging the specific discrepancy, ask the author to
  clarify/correct intent, record a `misleading_flag`, and treat the PR as **not
  reviewable / blocked** until resolved (it does not merge — see Rule 8). This is
  distinct from "inadequate": inadequate = unclear-but-consistent (we rewrite);
  misleading = actively wrong about what it does (we block and ask). The Rule 4
  "Matches description? = No" finding feeds directly into this.
- **How to edit (inadequate case only):**
  - Keep it **as short as possible** while accurately reflecting what the PR
    does — someone may reference it later. No padding.
  - **Follow the repo PR template** (Description/Summary, Type of change, Back
    port, Approach). Preserve the author's correct selections (e.g. an already-
    checked "Type of change"); fill only what's missing.
  - **Never fabricate** verification/test claims on the author's behalf — if how
    they tested is unknown, say so factually (e.g. "config-only change", "test
    plan only — no code"). Base the summary on the actual diff.
  - Leave an HTML-comment audit note in the body recording that a maintainer
    edited it and the original title.
- **Permission fallback:** editing title/body needs `maintain`/`push`. If we
  only have `triage`, do **not** edit — instead post a comment *suggesting* a
  better title/description and asking the author to apply it.
- **Author notice (required with every edit):** post one comment telling the
  author we updated the title/description, **with specifics** — which template
  sections were empty, or that the title was non-descriptive — and ask them to
  do better next time. **Tone: firm but professional**, never hostile or
  demeaning; these are public, attributed to us, and aimed at fellow OSS
  contributors. Community standing matters more than venting.
- **Idempotency:** **not logged** — the rewrite makes the title adequate, so the
  next scan won't re-flag it (see §3 "what gets logged"). The PR's own new
  title/body + the audit HTML-comment + the public author notice are the durable
  record; a ledger entry would just be noise. If the author regresses it, the
  next scan re-catches it.

### Rule 8 — Merge & squash procedure
Once a PR is genuinely ready, the agent may perform the merge (after human
approval — see preconditions), applying these rules.

- **Preconditions (ALL required before the agent merges):**
  1. **Human approval** — `reviewDecision == APPROVED` from a human maintainer
     (not a bot, not us auto-approving). Approval is still a human decision.
  2. CI green (latest = PASS), `mergeable == MERGEABLE`, not a draft.
  3. **No open `misleading_flag`** and no unresolved blocking review on the PR
     (a misleading/unclear description means it isn't reviewable → don't merge).
  4. **Cross-company gate (conflict of interest):** if the PR **author is from
     our own company (NextHop)**, the approvals must include **at least one
     approval from a different company**. We **never** merge a NextHop-authored
     PR on NextHop-only approvals. Resolve affiliation per §8; NextHop = profile
     company "NextHop", a `-nexthop` login, or an `@nexthop.ai` email.
  5. Linked issues noted for close-on-merge (Rule 6).
  The agent never merges on a third-party approval alone without these met; when
  in doubt, leave it for the human.
- **Finding a cross-company reviewer (for our own PRs).** When a NextHop-authored
  PR lacks a non-NextHop approval, don't just wait — proactively line up a
  suitable external reviewer: someone who has **previously contributed to / has
  approval rights in the same area** (the files/paths this PR touches). Request
  their review (add them as a reviewer or tag them in a comment), or surface the
  candidates to the human. `sweep.py --suggest-reviewers <PR>` lists candidates
  (recent non-NextHop contributors to the touched paths, with a best-effort
  write-access check). This keeps our own PRs honest and unblocks them legitimately.
- **Method — squash by default.** Use squash-merge for essentially everything.
  - **Exception → rebase-and-merge:** only when the PR is **large (>1000 lines
    total)** **and** its commits are **individually, independently auditable**
    (each a coherent, separately-reviewable change). Then rebase-and-merge to
    preserve those commits on a linear history. If it's big but the commits are
    messy/WIP, still squash. When unsure, squash.
- **Squash commit message:**
  - **Prefer the author's commit message.** If the PR's commit message is
    reasonable, use it (subject from the PR title or the commit headline; body
    from the author's commit body). Only rewrite it if it's inadequate
    (Rule 9) — keep it short and accurate, never fabricate.
  - **`Signed-off-by` is required (DCO-gated repo).** Ensure the message ends
    with `Signed-off-by: <Author Name> <author git-commit email>` taken from the
    PR commit author metadata (fall back to the GitHub display name only if the
    commit email is a `users.noreply` address). If the author's signoff is
    already present, keep it; don't duplicate.
  - **NEVER add a `Co-authored-by` line.** Strip any that GitHub would auto-add.
  - Do not invent test/verification claims.
- **Rebase case:** each preserved commit keeps its own message + signoff; we
  don't rewrite individual commit messages (if one is inadequate, that's a
  Rule 9 comment, not a block).
- **Approval summary comment (required whenever we approve).** When we approve a
  PR, post a short comment recording **how we reached that conclusion**, so the
  rationale is on the public record and others can see what our approval did (and
  didn't) rest on. Include:
  1. **PR type** — bug fix / feature / new test / test improvement / backport / doc.
  2. **Did CI actually run the test and pass?** — the crucial item. If **yes**,
     say so and name the job/topology (e.g. "exercised on the t1-lag-vpp PR-gate
     job"). If CI does **not** exercise the test (Rule 4 field 9b — hardware-only,
     skipped topology, etc.), **say that explicitly** and state how we gained
     confidence instead (depth of code review, the author's hardware run, etc.).
  3. A one-line rationale (e.g. "simple None-guard bug fix", "adds isolated new
     test coverage") and any caveats.
  Keep it brief. This is what makes an approval auditable and stops a misleading
  green check from being mistaken for validation. (The summary lives on the PR;
  GitHub records the approval — no ledger entry needed.)
- **On merge:** run the close-on-merge step (Rule 6) for linked issues and
  record a `merge` ledger entry (detail = method + resulting commit/PR).
- **Tooling:** `sweep.py --merge <PR>` is dry-run by default (prints method +
  the exact squash message it would use); `--apply` executes after re-checking
  every precondition.

### Rule 9 — Commit-message hygiene
Commit messages matter as much as the PR description — at squash time the commit
message is what we *prefer* for the permanent record, so encourage good ones.

- **When evaluated — at SWEEP time, not at merge.** The commit-message check and
  the author notice run as part of each sweep (sweep step 4c), the same way the
  title/description check does. The point is to tell the author **early** so they
  can fix it themselves (a quick amend/rebase) long before the PR is ready to
  merge — not to surprise them at merge time. Merge (Rule 8) never posts a commit
  notice; if a message is still inadequate at merge, we silently rewrite the
  squash message instead.
- **Sweep check:** each PR's commit message(s) for: (a) a reasonable, descriptive
  message (not `wip`, `fix`, `address comments`, `.`), and (b) a
  `Signed-off-by: Full Name <email>` trailer (DCO requires it anyway).
- **Inadequate (vague but not wrong) → comment, don't block.** Post a
  firm-professional comment stating the policy: squashable, reasonable commit
  messages with a `Signed-off-by` line, and **no `Co-authored-by`**. Do **not**
  hold the PR waiting for the author to amend — we can approve/merge and, if the
  message is inadequate, **rewrite the squash message at merge** (Rule 8),
  preferring the author's wording and adding their `Signed-off-by`.
- **Misleading (claims what the change doesn't do) → flag + block.** Same as the
  misleading case in Rule 7: record a `misleading_flag`, ask for clarification,
  and do not merge until resolved.
- Record a `commit_msg_notice` when we leave a policy comment (idempotent: once
  per PR unless the messages regress).

## 6. State transitions (lifecycle of one PR)

```
                         ┌─────────────┐
                         │ CONFLICTING │──ping(once)──▶ wait │ silent 14d ▶ ESCALATE
                         └─────────────┘
   (author rebases) ───────────▼
                         ┌─────────────┐  stale/old-fail   ┌──────────┐
                         │   CLEAN     │───── /azp run ────▶│ PENDING  │
                         └─────────────┘    (once/episode) └────┬─────┘
                              ▲                                  │
                   green again│                    ┌─────────────┴─────────────┐
                              │                    ▼                           ▼
                         ┌─────────┐          CI PASS+fresh                 CI FAIL
                         │ELIGIBLE │◀───────────────                   notify author (once)
                         └────┬────┘                                        │
                              │ deep review (once/SHA)                      ▼
                              ▼                                        wait for author
                         REVIEW BRIEF ──▶ human triage / approval
```

Idempotency is enforced at every arrow by the ledger (§3).

---

## 7. Mergeability caveat
GitHub computes `mergeable` lazily — the first API query usually returns
`UNKNOWN`. Trigger computation with one pass of queries, then re-poll until
every PR resolves to `MERGEABLE`/`CONFLICTING`. Never act on `UNKNOWN`.

## 8. Author-affiliation resolution
Resolve in this order; mark **"unknown"** (never guess) if none apply:
1. **SII author→org map** (authoritative, community-maintained):
   `sonic-net/sonic-tsc` → `sii_author_map/author.csv` (`login,name,org`; `null`
   = unknown). Cached locally at `data/author_org_map.csv`; refresh with
   `gh api repos/sonic-net/sonic-tsc/contents/sii_author_map/author.csv --jq .content | base64 -d > data/author_org_map.csv`.
2. GitHub profile `company` field.
3. Verified public email domain.
4. Login-suffix convention: `-nexthop`→NextHop, `-arista`→Arista,
   `-cisco`→Cisco, `-nv`/`-nvidia`→NVIDIA, `-ms`/`-msft`/`-microsoft`→Microsoft,
   `-nokia`→Nokia, `[Marvell]`/`-marvell`→Marvell, etc.
5. Org membership.

The map doesn't cover everyone (e.g. NextHop authors and some newer logins are
absent) — those still fall through to the profile/suffix heuristics.

## 8.1 Author trust (review-scrutiny weighting)
A per-author trust level that modulates **how much scrutiny** a PR gets — it is an
input to the recommendation, never an override of a hard gate.

- **Five levels:** **Expert · High · Medium · Low · Unproven.**
- **Primary signal — merged-PR history in the repo** (`sweep.py --trust <login>`
  counts the author's merged PRs):
  - **Expert** ≥ 50 · **High** ≥ 25 · **Medium** ≥ 8 · **Low** ≥ 1 · **Unproven** 0.
  - History is primary on purpose: a prolific contributor with an unresolved
    company (e.g. 55 merged PRs, affiliation "unknown") is still Expert, and a
    first-PR author **is Unproven even at a top company**.
- **Secondary signal — top-20 contributor company** (one-level bump, **capped at
  High**): if the author's affiliation is in the **top 20** orgs of
  `sii_org_predict.csv` (`data/sii_org_predict.csv`, **excluding "Others"**), bump
  one level — Low→Medium, Medium→High. **Expert is individual-only and is NEVER
  granted by company** — the bump tops out at High; reaching Expert requires the
  ≥50-merged history on its own. **Unproven is never bumped.** (So 31 merged at a
  top company = High, not Expert; 53 merged anywhere = Expert.)
- **How it's used:**
  - **Expert / High trust** → lighter touch; on low-risk or vendor-own-hardware
    changes with no red flags, comfortable to approve.
  - **Unproven / Low** → more scrutiny; read the diff carefully, and for changes
    CI doesn't validate, lean toward requiring a hardware pass / second opinion
    even for smaller diffs.
- **Never overrides hard gates.** Trust does NOT waive: CI-coverage for shared
  infra (a high-trust author's non-CI-validated *shared* change still needs a real
  hardware pass), the cross-company COI gate, a `misleading_flag`, or DCO. It only
  shifts how skeptically we read things that are otherwise in-bounds.

## 9. The `/azp run` command
Plain **`/azp run`** queues a *new* run of **all** repo pipelines (new run
number, picks up current YAML/config) — a full re-run. This is what we want.
The GitHub "Re-run failed checks" UI button only retries failed checks against
the *old* run and is **not** equivalent. `/azp run` is also the repo convention
(`mssonicbld` posts it). It is permission-gated (Azure DevOps) and its response
only renders if the repo uses the Azure Pipelines GitHub App — if a comment has
no effect, the commenter may lack trigger rights.

## 10. Artifacts & helpers (per tracked repo)
- `review-queue.md` — generated tracking table (status + follow-up column).
- `review-findings-<date>.md` — deep-review briefs for that sweep.
- `actions.jsonl` — the append-only action ledger (§3).
- `helpers/` — the sweep scripts and table generator.
- `data/` — raw JSON/TSV snapshots from the last sweep (for reproducibility;
  may be gitignored if noisy).

## 11. Change log
- **2026-06-10** — initial policy. Rules 1–4 established during the first
  sonic-mgmt sweep; Rule 5 (post-`/azp run` follow-up) and the action-ledger
  idempotency model added the same day. Rule 6 (issue linkage & manual
  close-on-merge, incl. cross-repo / missing-keyword detection) added the same
  day. Rule 7 (fix woefully-inadequate PR titles/descriptions + firm-professional
  author notice; applies to the whole queue, not just review-ready PRs) added the
  same day. Rule 8 (squash-by-default merge, rebase exception for large auditable
  PRs, prefer author commit message, author Signed-off-by, never Co-authored-by,
  agent merges after human approval) and Rule 9 (commit-message hygiene) added the
  same day, plus the misleading-vs-inadequate distinction (misleading title /
  description / commit message → flag & block, never silently rewrite). Added the
  Rule 4 **CI-coverage** check (does the VS PR-gate actually run the test, or is it
  skipped → green check ≠ validated → deeper review), the **not-CI-testable →
  require hardware-pass evidence** rule with the **vendor-own-hardware exception**,
  and the **approval summary comment** (Rule 8: record type + whether CI ran/passed
  the test + rationale on every approval). Also: DCO-based signoff detection,
  Rule 5 re-notify cooldown. Added the SII author→org map as affiliation source #1
  (§8), and the **author-trust metric** (§8.1: 5 levels Expert/High/Medium/Low/
  Unproven; primary = merged-PR history, secondary = top-20-company bump capped at
  High; Expert is individual-only).
