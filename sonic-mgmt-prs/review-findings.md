# Deep-review findings — sonic-net/sonic-mgmt

**PRs awaiting our action**, sorted by recommendation — each links to its full brief (click → read → back → next). A PR drops off this doc once it's **approved/merged** or **handed back to the author** (changes/info/evidence requested, conflicting, COI-waiting); full state + history live in `actions.jsonl` + git. Recommendations fold in: does the diff match the description, complexity, **author trust** (§8.1), and **whether CI actually runs the test** (a green check on a skipped test proves nothing — see CI column). _Decision support; approval is the human reviewer's call._

**Tally:** Get another opinion (COI): 1 · _(no open Approve candidates — #24787 & #24927 approved 2026-07-23)_

_(2026-07-23 sweep — 26 assigned PRs, first refresh since 07-10. **Approved #24247** (Keysight, no COI, your go-ahead): the ball had come back to us — @banidoru's blocking CR was dismissed by maintainer @r12f (banidoru now COMMENTED), leaving **our own** 06-10 Request-changes as the sole block while @r12f + @thisptr-sh pinged us to re-check. Re-review at 98282b7 confirmed all three of our 06-10 asks resolved (local `test_results` + `nonlocal` → no xdist contamination; double traffic-start removed; description corrected to "minimum frame size"), plus teardown, index-based binary search w/ max-frame sanity check, and `boundary_check` extracted to `helper.py`; author's posted snappi run on `vms-snappi-sonic` converges (128B loss → 192B no-loss). @thisptr-sh had already approved. Posted APPROVE → reviewDecision now APPROVED; dropped from this doc. Non-blocking nit left for a follow-up: non-RFC2889 `[False-*]` variant shows loss in the shared log. **Mechanical:** Rule-5 CI-fail notices on #20841 (@rbpittman) and #17940 (@Pterosaur) — both still failing after our 07-10 `/azp run`, new episodes. **Not acted:** the sweep's `azp_run` on #24247 was a stale-CI misfire (CI is green) — suppressed. The 9 dead-conflicting escalations (#24685/#21925/#21084/#20331/#19873/#19374/#19067/#18620/#18108) are unchanged from 07-10 and still recommend closing the stalest. **Approved #24787 & #24927** (your go-ahead): #24787 re-verified unchanged since our 07-10 deep review at f92d5a3 (Nokia HW pass, additive-only, CI green, we were the only reviewer); #24927 re-verified at 0769d3c (moved past our SHA — delta is master-merge drift + a hardening of the exact KeyError guard we'd flagged; @nhe-NV approved on NVIDIA's dualtor topology, CI green). Both reviewDecision now APPROVED → dropped from this doc.)_

_(2026-07-10 sweep — first refresh since 06-16, 28 assigned PRs. **Mechanical:** posted 8 `/azp run` (stale CI), CI-fail notify #26068, conflict ping #21144, commit-msg notice #24320, and 2 hand-off ticklers (#24829 evidence, #19020 opinion). **Tool/policy fix:** ticklers no longer re-ping conflicts or CI-failures — that violated Rule 1 ("never auto-re-ping" → escalate) and Rule 5 ("one notify per failing episode"); added push-awareness so a silent code-fix stops a nag rather than getting one. Cut the tickler burst 15→2. **Re-evaluated 8 responded PRs:** #24787 & #24927 evidence satisfied → Approve candidates below; #24320 & #17940 authors addressed our change-requests but items remain → re-requested changes (author-ball); #25093 escalated our open frr-mgmt-framework concern to a formal Request-changes (author-ball); #24247 deferred to @banidoru's open CR; #24403 (CI running) / #24802 (CI failing on author code) / #25123 (opinion pending @saiarcot895) left author-ball. **#24902 merged upstream** (the `wait_until` fix) → dropped. **Escalations (9 long-dead conflicting PRs, author-silent since 06-10, in some cases untouched since mid-2025):** #24685, #21925, #21084, #20331, #19873, #19374, #19067, #18620, #18108 — surfaced to you; recommend closing the stalest. Off-doc author/reviewer-ball: #24247, #24320, #17940, #25093, #24403, #24802, #25123, #23346.)_

## Recommendations

| PR | Title | Author / Trust | CI runs test? | ➡ Recommendation |
|----|-------|----------------|---------------|------------------|
| [#23283](#pr-23283) | Prevent cascading qos_sai failures after fixture error | darius-nexthop / NextHop / Medium | Partial (off-gate) | **Get another opinion (COI)** — open ZhaohuiS concern; NextHop can't self-approve |

---

## Briefs

_Ordered by recommendation, same as above._

_(#24787 and #24927 were approved 2026-07-23 and dropped from this doc — see the sweep note above and `actions.jsonl` for their approval records.)_

<a id="pr-23283"></a>

### [PR #23283](https://github.com/sonic-net/sonic-mgmt/pull/23283) — test_qos_sai: prevent cascading failures after fixture error
- **Author / affiliation / trust:** darius-nexthop / NextHop (OUR company — COI) / Medium
- **➡ Recommendation:** **Get another opinion (COI-blocked)** — defer to the existing MSFT reviewers. Author is NextHop, so this cannot be a plain Approve regardless of code quality; a cross-company approver is required. Independently: GitHub `reviewDecision` is still CHANGES_REQUESTED and ZhaohuiS's design concern is OPEN, so it's not mergeable as-is. Unchanged since our last review (last activity yxieca non-blocking note 05-24).
- **Type:** Bug fix (test-infra reliability).
- **Complexity:** Low — 2 files, +46/-0; touches a SHARED fixture file (`tests/qos/conftest.py`) via session-scoped pytest hooks, guarded by a `TestQosSai` class-name check.
- **Description summary:** When the `testParameter` fixture setup fails, subsequent tests in the same parameter set currently ERROR. Adds hooks that record a per-parameter-set setup failure and SKIP later tests, leaving only the seed to ERROR. Fixes #23282.
- **Existing reviews/comments:** StormLiangMS's three code items addressed; he said he'd dismiss his CR but never did (GitHub still shows CHANGES_REQUESTED). **ZhaohuiS inline (conftest.py:220) is OPEN** — a design objection.
- **CI actually runs the test?:** Partial / effectively No — hooks fire only on a fixture setup failure (a hardware/image fault that doesn't occur on the VS/KVM gate).
- **Linked issue(s):** #23282 (issue, OPEN — auto-close on merge via "Fixes #23282").
- **Requested changes (to post):** None from us — defer to the open maintainer items:
    - **[ZhaohuiS — OPEN, blocking]** Skip-vs-fail semantics: justify why ERROR-on-seed + SKIP-on-cascade is acceptable for nightly triage (or use a non-skip signal downstream), and get the thread resolved.
    - **[StormLiangMS — administrative]** Stale CHANGES_REQUESTED never dismissed (still the active `reviewDecision`) — needs dismiss/re-review before merge.
    - **[StormLiangMS — nits]** Log cascade-skips at `info` not `warning`; emit the originating param-set key in the `pytest.skip` reason.

[↑ back to recommendations](#deep-review-findings--sonic-netsonic-mgmt)
