# Deep-review findings — sonic-net/sonic-mgmt

**PRs awaiting our action**, sorted by recommendation — each links to its full brief (click → read → back → next). A PR drops off this doc once it's **approved/merged** or **handed back to the author** (changes/info/evidence requested, conflicting, COI-waiting); full state + history live in `actions.jsonl` + git. Recommendations fold in: does the diff match the description, complexity, **author trust** (§8.1), and **whether CI actually runs the test** (a green check on a skipped test proves nothing — see CI column). _Decision support; approval is the human reviewer's call._

**Tally:** Approve — ready (pending your go-ahead): 2 · Get another opinion (COI): 1

_(2026-07-10 sweep — first refresh since 06-16, 28 assigned PRs. **Mechanical:** posted 8 `/azp run` (stale CI), CI-fail notify #26068, conflict ping #21144, commit-msg notice #24320, and 2 hand-off ticklers (#24829 evidence, #19020 opinion). **Tool/policy fix:** ticklers no longer re-ping conflicts or CI-failures — that violated Rule 1 ("never auto-re-ping" → escalate) and Rule 5 ("one notify per failing episode"); added push-awareness so a silent code-fix stops a nag rather than getting one. Cut the tickler burst 15→2. **Re-evaluated 8 responded PRs:** #24787 & #24927 evidence satisfied → Approve candidates below; #24320 & #17940 authors addressed our change-requests but items remain → re-requested changes (author-ball); #25093 escalated our open frr-mgmt-framework concern to a formal Request-changes (author-ball); #24247 deferred to @banidoru's open CR; #24403 (CI running) / #24802 (CI failing on author code) / #25123 (opinion pending @saiarcot895) left author-ball. **#24902 merged upstream** (the `wait_until` fix) → dropped. **Escalations (9 long-dead conflicting PRs, author-silent since 06-10, in some cases untouched since mid-2025):** #24685, #21925, #21084, #20331, #19873, #19374, #19067, #18620, #18108 — surfaced to you; recommend closing the stalest. Off-doc author/reviewer-ball: #24247, #24320, #17940, #25093, #24403, #24802, #25123, #23346.)_

## Recommendations

| PR | Title | Author / Trust | CI runs test? | ➡ Recommendation |
|----|-------|----------------|---------------|------------------|
| [#24787](#pr-24787) | [T2] test_sup_fan_recovery after reload + cold reboot | aeedara-nokia / Nokia / Medium | No (T2, skips on VS) — HW pass provided | **Approve — ready** (pending your go-ahead + fresh CI) |
| [#24927](#pr-24927) | Fix test_link_local_ip in dualtor active-active | xixuej / NVIDIA / High | No (dualtor-aa, off-gate) — verified on dualtor | **Approve — ready** (pending your go-ahead + fresh CI) |
| [#23283](#pr-23283) | Prevent cascading qos_sai failures after fixture error | darius-nexthop / NextHop / Medium | Partial (off-gate) | **Get another opinion (COI)** — open ZhaohuiS concern; NextHop can't self-approve |

---

## Briefs

_Ordered by recommendation, same as above._

<a id="pr-24787"></a>

### [PR #24787](https://github.com/sonic-net/sonic-mgmt/pull/24787) — [platform_tests][T2] Add test_sup_fan_recovery.py
- **Author / affiliation / trust:** aeedara-nokia / Nokia / **Medium** (2 merged PRs; top-company rank #8). No COI (non-NextHop).
- **➡ Recommendation:** **Approve — ready.** The one outstanding blocker from our earlier formal Request-changes (a real-hardware pass, since the VS gate can't run T2) is satisfied — the screenshot shows `test_sup_fan_status_after_reload_reboot` **Passed** (not skipped) on a real Nokia 7250 IXR chassis + sup. Additive-only, no shared-infra edits, helpers/signatures all verified present, polling is correct (no dead-sleeps), skips are legitimate applicability guards. **Not acted on — awaiting your explicit go-ahead** (Rule 8), and we just re-triggered CI (stale), so let it come back green first.
- **Type:** New test case (single new file, +226/-0: `tests/platform_tests/test_sup_fan_recovery.py`).
- **Complexity:** Low (additive). Iterates `duthosts.supervisor_nodes`, arms a sup-scoped LogAnalyzer, `config_reload(minigraph, wait=420)` → assert fans OK → `reboot_and_check(COLD)` → assert fans OK → assert no new cores.
- **Existing reviews/comments:** only our CHANGES_REQUESTED (06-10, evidence request). HW-pass ask → **addressed** (screenshot). Transient-parse short-circuit in `_all_fans_ok` → **addressed** (both `duthost.command()` and `verify_show_platform_fan_output()` now wrapped in try/except → retry). No inline threads.
- **Matches description?:** Yes.
- **CI actually runs the test?:** **No** — `impacted-area-kvmtest-t2` passes but the test self-skips on `asic_type=="vs"` (hardware-only). Green check does **not** validate the logic; confidence comes from the Nokia HW run.
- **Vendor scope note:** topology-generic (`t2`), not strictly Nokia-platform-gated, so the vendor-own-hardware exception doesn't *fully* apply — but the additive-only footprint keeps blast radius minimal and the HW evidence covers the gap.
- **Red flags:** none. No dead-sleeps (`wait_until(90,5,0,_all_fans_ok)`; `config_reload(wait=420)`; `reboot_and_check` handles reboot readiness). All referenced helpers verified present. Skips legitimate.
- **Linked issue(s):** none — `Fixes #` placeholder left blank (minor nit).
- **Reviewer notes / do-not-block nits:** (1) empty `Fixes #` link; (2) the fan bug symptom is the *Presence* column but the test asserts on *Status* — author's failing-build repro confirms Status catches it, so empirically fine. Neither warrants holding the PR.

[↑ back to recommendations](#deep-review-findings--sonic-netsonic-mgmt)

<a id="pr-24927"></a>

### [PR #24927](https://github.com/sonic-net/sonic-mgmt/pull/24927) — Fix test_link_local_ip failures in dualtor active-active
- **Author / affiliation / trust:** xixuej / NVIDIA / **High** (32 merged PRs; top-company rank #2). No COI (non-NextHop).
- **➡ Recommendation:** **Approve — ready.** Both concerns from our earlier evidence-request are resolved: (1) the KeyError guard is verified in code, and (2) the author verified `TestLinkLocalIPacket` on a dualtor setup. A Microsoft maintainer (@liat-grozovik) and @nhe-NV are actively driving it to merge. **Not acted on — awaiting your explicit go-ahead** (Rule 8); CI just re-triggered (stale), let it green first.
- **Type:** Bug fix (test correctness for dualtor active-active topology).
- **Complexity:** Low. Switches the fixture to `rand_one_dut_hostname` and derives the downlink router MAC from `VLAN`/`VLAN_MEMBER` config facts.
- **Existing reviews/comments:** our evidence-request (06-10). KeyError concern → **addressed & verified**: `get_downlink_router_mac` uses `config_facts.get('VLAN_MEMBER') or {}`, `config_facts.get('VLAN') or {}`, `vlan_facts.get(vlan_interface) or {}`, and a `return default_router_mac` fallback — a VLAN_MEMBER with no matching VLAN entry can't KeyError. dualtor-aa pass → author-confirmed (verbal; no artifact, but a High-trust NVIDIA author on their own topology).
- **Matches description?:** Yes.
- **CI actually runs the test?:** **No** — dualtor active-active isn't on the standard VS/KVM PR-gate; author verified out-of-band on a dualtor testbed.
- **Red flags:** none found (KeyError guard was the one raised; now clean).
- **Linked issue(s):** none parsed.
- **Reviewer notes:** Strong Approve candidate — concern closed, maintainer-endorsed, High-trust author. Only caveat is the dualtor pass is a verbal confirmation rather than a posted log; acceptable given author trust + own-topology, but worth a glance if you want the artifact before approving.

[↑ back to recommendations](#deep-review-findings--sonic-netsonic-mgmt)

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
