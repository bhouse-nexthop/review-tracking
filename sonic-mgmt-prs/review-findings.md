# Deep-review findings — sonic-net/sonic-mgmt

**PRs awaiting our action**, sorted by recommendation — each links to its full brief (click → read → back → next). A PR drops off this doc once it's **approved/merged** or **handed back to the author** (changes/info/evidence requested, conflicting, COI-waiting); full state + history live in `actions.jsonl` + git. Recommendations fold in: does the diff match the description, complexity, **author trust** (§8.1), and **whether CI actually runs the test** (a green check on a skipped test proves nothing — see CI column). _Decision support; approval is the human reviewer's call._

**Tally:** Get another opinion: 2 · Hold (your call): 1 · Blocked (COI): 1
_(2026-06-16 — per your go-ahead, **approved + squash-merged six**: #24975, #25000, #24091, #21429, #23542, and #24217 (after neutralizing its `Fixes #24558` so the gating issue stays open). Backport labels flipped for the 202605/202511 requests; #21342 auto-closed as the now-filled test-gap; signoffs preserved, Co-authored-by/Copilot stripped. **Posted formal Request-changes** on #24591 (empty-except swallow) and #17940 (14 items; 3mo stale) → handed back to authors. Two tool/policy bugs fixed this session: (1) `ci_fail_notify` re-notify now keys off the failing-run timestamp, not a wall-clock cooldown (POLICY §3) — 6 stale repeat-nudges suppressed; (2) Rule 6 close-on-merge no longer closes no-keyword "mention" issues — it had wrongly closed #24217's gating issue #24558 + tracking #24215 on merge, both since **reopened**. Off-doc author/reviewer-ball: #24247, #24367, #20456, #24913, #24802, #21144, #24902-followups, #25012 (merged upstream).)_

## Recommendations

| PR | Title | Author / Trust | CI runs test? | ➡ Recommendation |
|----|-------|----------------|---------------|------------------|
| [#24902](#pr-24902) | Handle pytest.fail.Exception in wait_until | wrideout-arista / High | Partial (shared helper) | **Get another opinion** — anders found 4 silent-no-op sites; awaiting @wangxin/@lolyu |
| [#23283](#pr-23283) | Prevent cascading qos_sai failures after fixture error | darius-nexthop / Medium | Partial (off-gate) | **Get another opinion (COI)** — open ZhaohuiS concern; NextHop can't self-approve |
| [#24829](#pr-24829) | Fix: add port name for acl interface parsing | ytzur1 / High | No (alias==name on gate) | **Hold (your call)** — evidence is a pdb dump, no independent approval |
| [#23346](#pr-23346) | SONiC BMC Redfish API and D-Bus test plan | chinmoy-nexthop / Unproven | N-A (doc) | **Blocked (COI)** — NextHop test plan; needs non-NextHop approval |

---

## Briefs

_Ordered by recommendation, same as above._

<a id="pr-24902"></a>

### [PR #24902](https://github.com/sonic-net/sonic-mgmt/pull/24902) — Handle pytest.fail.Exception in wait_until
- **Author / affiliation / trust:** wrideout-arista / Arista / High
- **➡ Recommendation:** **Get another opinion** (in progress) — we posted our blast-radius notes + recruited @wangxin/@lolyu (common-infra maintainers); the author agrees ("as many eyes as possible"). **anders-nexthop ran a repo-wide audit and found 4 call sites that become silent no-ops** — those should land alongside this change. Still awaiting a maintainer sign-off on the semantics; not mergeable until the 4 sites are handled and a maintainer approves.
- **Type:** Bug fix (shared test helper).
- **Complexity:** Medium (by blast radius) — tiny diff but changes `wait_until` behavior **repo-wide** (~1,570 call sites): a `pytest_assert`/`pytest.fail` raised inside a `wait_until` condition (derives from `BaseException`, escapes the current `except Exception`) is now swallowed + retried until timeout instead of failing fast.
- **Description summary:** Makes `wait_until` catch `pytest.fail.Exception` so a transient guard-trip inside a condition retries through instead of fast-failing — the intended reliability fix.
- **Existing reviews/comments:** bhouse-nexthop opinion-request (06-10) recruiting @wangxin/@lolyu + flagging the title typo ("Exeption"). wrideout-arista (author) agreed (06-10). **anders-nexthop audit (06-10 23:07):** of ~1,570 sites, ~22 assert internally; most use the return (`pytest_assert(wait_until(...))`) and are fine (vaguer message + transient-retry = the intended win). **4 return-ignored sites become checks that can never fail:** `gu_utils.py check_table` (GCU ACL mismatch silently ignored), `test_monit_status.py` + `test_frr_bmp_sanity.py check_monit_expected_container_logging` (~180s no-ops), `test_techsupport.py execute_command` (real failure swallowed, then stale `pytest.tar_stdout`).
- **Matches description?:** Yes — one-line `except` change does exactly what's described; the open question is the unscoped blast radius, not correctness.
- **Conflict likelihood:** Low (single shared helper) — but semantic interaction with every `wait_until` caller.
- **Duplication likelihood:** none seen.
- **CI actually runs the test?:** Partial — `wait_until` is exercised everywhere, but the behavior change matters only for the ~22 asserting conditions; the 4 problematic sites aren't all on the PR-gate. CI green does not prove those 4 still fail when they should.
- **Linked issue(s):** none parsed.
- **Reviewer notes:** Not a silent bucket — notes posted, maintainers recruited, author engaged, and anders supplied a concrete call-site audit. Next step belongs to author + maintainers, so it's effectively handed off; kept on-doc only because the responses re-flagged it. **Suggested follow-up to post:** ask wrideout to land the 4 return-ignored conversions (return a bool + assert `wait_until`'s result) alongside this change, and keep the request to @wangxin/@lolyu open for the `wait_until` contract decision. (Also fix the "Exeption" title typo.)

[↑ back to recommendations](#deep-review-findings--sonic-netsonic-mgmt)

<a id="pr-23283"></a>

### [PR #23283](https://github.com/sonic-net/sonic-mgmt/pull/23283) — test_qos_sai: prevent cascading failures after fixture error
- **Author / affiliation / trust:** darius-nexthop / NextHop (OUR company — COI) / Medium
- **➡ Recommendation:** **Get another opinion (COI-blocked)** — defer to the existing MSFT reviewers. Author is NextHop, so this cannot be a plain Approve regardless of code quality; a cross-company approver is required. Independently: GitHub `reviewDecision` is still CHANGES_REQUESTED and ZhaohuiS's design concern is OPEN, so it's not mergeable as-is. Do not approve; let StormLiangMS/ZhaohuiS make the call.
- **Type:** Bug fix (test-infra reliability).
- **Complexity:** Low — 2 files, +46/-0; touches a SHARED fixture file (`tests/qos/conftest.py`) via session-scoped pytest hooks that run for every qos item, guarded by a `TestQosSai` class-name check.
- **Description summary:** When the `testParameter` fixture setup fails, subsequent tests in the same parameter set currently ERROR, inflating failure counts. Adds hooks that record a per-parameter-set setup failure and SKIP later tests in that set, leaving only the seed (`@pytest.mark.fixture_seed testParameter`) to ERROR. Fixes #23282.
- **Existing reviews/comments:** StormLiangMS COMMENTED → **CHANGES_REQUESTED (03-27)** → COMMENTED (04-28); ZhaohuiS COMMENTED + inline (04-28). StormLiangMS's three code items (dict never cleared, fragile `split('-')[0]`, hardcoded `testParameter`) are **addressed**; he left two non-blocking nits and said he'd dismiss the CR but **never did** (GitHub still shows CHANGES_REQUESTED). **ZhaohuiS inline (conftest.py:220) is OPEN/unaddressed** — a design objection.
- **Matches description?:** Yes — implements the described seed-fails / cascade-skips behavior; scoped to `TestQosSai`.
- **Conflict likelihood:** Low — file-isolated vs the other eligible PRs (#24591 touches qos `qos_sai_base.py`, not these files).
- **Duplication likelihood:** none seen.
- **CI actually runs the test?:** Partial / effectively No for validation — the hooks fire only on a *fixture setup failure* (a hardware/image fault that doesn't occur on the VS/KVM gate). CI green = "didn't regress collection", not "exercised the skip path"; author's verification was off-gate.
- **Linked issue(s):** #23282 (issue, OPEN — auto-close on merge via "Fixes #23282").
- **Reviewer notes:** Code clean; StormLiangMS's robustness fixes landed. Substantive open question is ZhaohuiS's: ERROR→SKIP on a known-bad fixture setup risks silently masking real infra/image breakage in nightly (skipped cases ignored). The design keeps the *seed* as ERROR to preserve a signal — partially answers it, but maintainers haven't accepted and the thread is unresolved.
- **Requested changes (to post):** None from us — defer to the open maintainer items:
    - **[ZhaohuiS — OPEN, blocking]** Skip-vs-fail semantics: justify why ERROR-on-seed + SKIP-on-cascade is acceptable for nightly triage (or use a non-skip signal downstream), and get the thread resolved.
    - **[StormLiangMS — administrative]** Stale CHANGES_REQUESTED never dismissed (still the active `reviewDecision`) — needs dismiss/re-review before merge.
    - **[StormLiangMS — nits]** Log cascade-skips at `info` not `warning`; emit the originating param-set key in the `pytest.skip` reason.

[↑ back to recommendations](#deep-review-findings--sonic-netsonic-mgmt)

<a id="pr-24829"></a>

### [PR #24829](https://github.com/sonic-net/sonic-mgmt/pull/24829) — Fix: add port name for acl interface parsing
- **Author / affiliation / trust:** ytzur1 / NVIDIA / High (merged PRs=22, top-company rank #2)
- **➡ Recommendation:** **Hold — your call** — re-eval after our 2026-06-10 evidence-request. The change is additive and safe (a last-resort `elif member in ports` fallback after the existing branches), and ytzur1's response *literally* satisfies what we asked for (`mg_facts['minigraph_acls']` populated on a Mellanox-SN6600_LD-P128C2, where the bug lives). **But** the "evidence" is a pdb/debugger inspection dump, not a clean passing test run, and there is **no independent maintainer approval** — the only review on the PR is our own CHANGES_REQUESTED. Per your policy I'm not approving/merging on our review alone: flagging for your decision — either accept the pdb evidence as sufficient (additive/safe change), or ask ytzur1 for an actual passing run before approving.
- **Type:** Bug fix (ACL interface / minigraph_acls parsing on aliased-port HWSKUs).
- **Complexity:** Low — 1 file, +2/-0; adds a fallback branch to the ACL interface parsing.
- **Description summary:** Adds port-name handling so ACL interface parsing also matches when a member is a port name (not an alias). References #22166.
- **Existing reviews/comments:** bhouse-nexthop CHANGES_REQUESTED (06-10, evidence_request — CI doesn't exercise the new path since the KVM-gate HWSKU has alias==name); ytzur1 posted pdb output (06-14) showing `minigraph_acls` populated (DataAcl: Ethernet0…Ethernet200) on Mellanox-SN6600_LD-P128C2. No other reviewer.
- **Matches description?:** Yes — the 2-line fallback matches the described intent.
- **CI actually runs the test?:** **No** — on the KVM PR-gate the HWSKU has alias==name, so the existing `elif member in port_alias_to_name_map` branch already matches and the new `elif member in ports` fallback is never reached; it only fires on hardware where alias != name (e.g. `etp*` aliases) — exactly the case the bug affects.
- **Linked issue(s):** #22166 (referenced in body).
- **Reviewer notes:** Code is a safe additive fallback (our original assessment stands). The open question is purely evidentiary/process: pdb inspection vs a clean passing run, and no second reviewer — so a merge would rest on our review alone, which is why it's held for your decision. NVIDIA author → no COI gate.

[↑ back to recommendations](#deep-review-findings--sonic-netsonic-mgmt)

<a id="pr-23346"></a>

### [PR #23346](https://github.com/sonic-net/sonic-mgmt/pull/23346) — SONiC BMC Redfish API and D-Bus test plan
- **➡ Recommendation:** Blocked (COI) — NextHop-authored test plan; needs a non-NextHop approval first
- **Author / affiliation:** chinmoy-nexthop (Chinmoy Dey) / NextHop (profile empty; resolved from `-nexthop` suffix)
- **Trust:** Unproven (NextHop)
- **CI runs the test?:** N-A (test-plan doc)
- **Type:** Test plan / design doc (no test code)
- **Complexity:** Low — 1 file, +791/-0, `docs/testplan/redfish/…md`; docs-only, zero blast radius.
- **Description summary:** Plans validation of the SONiC BMC Redfish API (bmcweb + sonic-dbus-bridge) on Aspeed AST2720/AST2700: service-root/chassis/system/firmware inventory, ComputerSystem.Reset, Rack Manager alert/telemetry/event subscription, D-Bus health, graceful degradation, mTLS auth, cross-validated against Redis/busctl/CLI.
- **Existing reviews/comments:** StormLiangMS (DISMISSED) "LGTM, comprehensive"; judyjoseph + shreyansh-nexthop COMMENTED (empty); yxieca AI docs-only note; `/azp run` excluded (docs path not CI-gated).
- **Matches description?:** Partial — doc is solid, but body says "29 test cases / 11 sections" while the content has **34 cases / 12 sections** (mTLS section + TC#30–34 added); headline count stale.
- **Conflict likelihood:** Low — brand-new file, isolated.
- **Duplication likelihood:** none seen — first Redfish/BMC test plan in the repo.
- **Linked issue(s):** none closeable — `Fixes #` blank; referenced sonic-net/SONiC#2043, sonic-redfish#1/#2 are all **PRs** (track-only). Dependent HLDs reportedly not yet merged upstream — confirm before acting.
- **Reviewer notes:** Defer to NextHop on BMC/Aspeed/D-Bus endpoint facts. Reconcile the 29→34 / 11→12 count; the documented `tests/redfish/` tree is a future follow-up.

[↑ back to recommendations](#deep-review-findings--sonic-netsonic-mgmt)
