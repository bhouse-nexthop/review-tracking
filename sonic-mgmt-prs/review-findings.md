# Deep-review findings — sonic-net/sonic-mgmt

**PRs awaiting our action**, sorted by recommendation — each links to its full brief (click → read → back → next). A PR drops off this doc once it's **approved/merged** or **handed back to the author** (changes/info/evidence requested, conflicting, COI-waiting); full state + history live in `actions.jsonl` + git. Recommendations fold in: does the diff match the description, complexity, **author trust** (§8.1), and **whether CI actually runs the test** (a green check on a skipped test proves nothing — see CI column). _Decision support; approval is the human reviewer's call._

**Tally:** Blocked (COI): 2  
_(All review-bucket PRs now have our notes posted + are awaiting author/reviewer — see actions.jsonl. Only the 2 COI-blocked NextHop PRs remain for us to act on, by recruiting a cross-company reviewer.)_
_(#24687 merged. Off-doc awaiting author: #24649 (lolyu review), #20001 (staleness), + the earlier change/evidence requests. #18660 closed.)_
_(#24649 → off-doc: unresolved maintainer review (lolyu: drop mocks/use toggle marks/add port stats) + CodeQL uninit-var — awaiting author. #23606 merged; #20001 staleness ask; #18660 closed.)_
_(#23606 merged. #20001 → staleness ask; #18660 closed by author.)_
_(#20001 → asked author to confirm it's not stale (xfail for swss#3498); #18660 closed by author.)_
_(Newly reviewed this sweep; #18660 was closed by its author — superseded by #22982.)_
_(Everything else this cycle is off-doc: 7 merged, 13 change/evidence requests out — all formal blocking Request-changes reviews. See actions.jsonl.)_
_(Off-doc — awaiting author: #24247, #24320, #24845 (changes requested), #24975 (changes requested). Merged this cycle: #23930, #24493, #24545, #24597, #24876, #25134.)_

## Blocked (COI) (2)

| PR | Title | Type/Trust | CI runs test? | Why |
|----|-------|-----------|---------------|-----|
| [#23346](#pr-23346) | SONiC BMC Redfish API and D-Bus test plan | Test plan/doc / Unproven | N-A (test-plan doc) | NextHop-authored test plan; needs a non-NextHop approval first |
| [#25012](#pr-25012) | Fixing PMON status test failures | Bug fix / Medium | No (daemon vs-skip) | NextHop-authored; needs cross-company approval AND a hardware pass |

---

## Briefs

_Ordered by recommendation, same as above._

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

[↑ back to recommendations](#deep-review-findings--sonic-netsonic-mgmt--2026-06-10)

<a id="pr-25012"></a>

### [PR #25012](https://github.com/sonic-net/sonic-mgmt/pull/25012) — Fixing PMON status test failures
- **➡ Recommendation:** Blocked (COI) — NextHop-authored; needs cross-company approval AND a hardware pass
- **Author / affiliation:** caleb-nexthop / NextHop
- **Trust:** Medium (NextHop)
- **CI runs the test?:** No (daemon vs-skip)
- **Type:** Bug fix
- **Complexity:** Medium — 7 files, +35/-55, localized to `tests/platform_tests/daemon/`. New module-scoped `conftest.py` (shared fixtures) consumed by 6 daemon modules.
- **Description summary:** PMON term/kill tests fail under `run_optimal` because `auto_restart=enabled` restarts the container and resets PIDs, breaking `post_pid > pre_pid`. Adds a shared fixture to disable pmon container autorestart (restored on teardown), consolidates per-module `check_daemon_status`, and swaps a `time.sleep(10)` for `wait_until(...)` in test_pcied.
- **Existing reviews/comments:** github-advanced-security (automated, empty body); liamkearney-msft (APPROVED). Author asked if anything blocks merge.
- **Matches description?:** Yes — new conftest with both fixtures, 6 modules drop duplicated fixture, per-module host overrides added, `time.sleep(10)`→`wait_until(120,10,0,...)`. Minor doc/code drift (desc says `wait_until(50,...)`).
- **Conflict likelihood:** Low — file-isolated.
- **Duplication likelihood:** none seen (references #24384 as the wait_until precedent).
- **Reviewer notes:** Clean, well-scoped. Confirm the module-scoped autorestart teardown ordering is fine for modules that previously had no autorestart handling. Note timeout discrepancy (50 vs 120).

[↑ back to recommendations](#deep-review-findings--sonic-netsonic-mgmt--2026-06-10)


