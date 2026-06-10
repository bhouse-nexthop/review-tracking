# Deep-review findings — sonic-net/sonic-mgmt

**PRs awaiting our action**, sorted by recommendation — each links to its full brief (click → read → back → next). A PR drops off this doc once it's **approved/merged** or **handed back to the author** (changes/info/evidence requested, conflicting, COI-waiting); full state + history live in `actions.jsonl` + git. Recommendations fold in: does the diff match the description, complexity, **author trust** (§8.1), and **whether CI actually runs the test** (a green check on a skipped test proves nothing — see CI column). _Decision support; approval is the human reviewer's call._

**Tally:** Approve: 2 · Get another opinion: 5 · Blocked (COI): 2  
_(#23606 merged. #20001 → staleness ask; #18660 closed by author.)_
_(#20001 → asked author to confirm it's not stale (xfail for swss#3498); #18660 closed by author.)_
_(Newly reviewed this sweep; #18660 was closed by its author — superseded by #22982.)_
_(Everything else this cycle is off-doc: 7 merged, 13 change/evidence requests out — all formal blocking Request-changes reviews. See actions.jsonl.)_
_(Off-doc — awaiting author: #24247, #24320, #24845 (changes requested), #24975 (changes requested). Merged this cycle: #23930, #24493, #24545, #24597, #24876, #25134.)_

## Approve (2)

| PR | Title | Type/Trust | CI runs test? | Why |
|----|-------|-----------|---------------|-----|
| [#24649](#pr-24649) | [dualtor] Add tunnel-termination drop test on standby ToR | New test suite / Expert | No (dualtor not in gate) | author linked real HW runs (Cisco 8101 + Arista) → evidence met; closes #21092 |
| [#24687](#pr-24687) | pfcwd: ignore benign cisco-8000 SAI/orchagent errors | Bug fix (loganalyzer) / Expert | Partial (cisco-8000 branch not on vs) | additive asic-gated ignore-list, idiomatic, low risk |

## Get another opinion (5)

| PR | Title | Type/Trust | CI runs test? | Why |
|----|-------|-----------|---------------|-----|
| [#19020](#pr-19020) | [Test gap] Test plan to verify vxlan tunnel na… | Test plan/doc / Expert | N-A (test-plan doc) | test-plan doc under-delivers vs its own objectives |
| [#21658](#pr-21658) | [AI - Snappi] BGP convergence testcase for sin… | New test (snappi) / Expert | No (snappi/nut) | snappi (not CI-run) + r12f review comments open |
| [#21660](#pr-21660) | [AI - Snappi] BGP convergence testcase for Dev… | New test (snappi) / Expert | No (snappi/nut) | snappi (not CI-run) + r12f skeleton-dedup request open |
| [#24902](#pr-24902) | Handle pytest.fail.Exeption in wait_until | Bug fix / High | Partial (lib runs; new branch not asserted) | one-line change to shared wait_until; repo-wide behavioral effect |
| [#25123](#pr-25123) | [TH6] test_po_cleanup fix for large number of … | Bug fix / Expert | Partial (>64-LAG branch unreachable on vs) | intentional syslog-sampling sensitivity needs maintainer sign-off; Nokia-HW path |

## Blocked (COI) (2)

| PR | Title | Type/Trust | CI runs test? | Why |
|----|-------|-----------|---------------|-----|
| [#23346](#pr-23346) | SONiC BMC Redfish API and D-Bus test plan | Test plan/doc / Unproven | N-A (test-plan doc) | NextHop-authored test plan; needs a non-NextHop approval first |
| [#25012](#pr-25012) | Fixing PMON status test failures | Bug fix / Medium | No (daemon vs-skip) | NextHop-authored; needs cross-company approval AND a hardware pass |

---

## Briefs

_Ordered by recommendation, same as above._

<a id="pr-19020"></a>

### [PR #19020](https://github.com/sonic-net/sonic-mgmt/pull/19020) — [Test gap] Test plan to verify vxlan tunnel name length
- **➡ Recommendation:** Get another opinion — test-plan doc under-delivers vs its own objectives
- **Author / affiliation:** wsycqyz (ShiyanWangMS) / Microsoft *(low confidence — profile empty, no `-ms` suffix; inferred from display name)*
- **Trust:** Expert (Microsoft)
- **CI runs the test?:** N-A (test-plan doc)
- **Type:** Test plan / design doc (no test code)
- **Complexity:** Low — 1 file, +84/-0, `docs/testplan/Vxlan-tunnel-name-length-test-plan.md`.
- **Description summary:** Plans verification that VXLAN tunnel interface names longer than the historical 15-char limit can be created/listed/deleted; backs sonic-buildimage #20108 (YANG name-length validation). Two cases: create a long-named tunnel via `config load`, delete via redis-cli, confirm via `show vxlan tunnel`.
- **Existing reviews/comments:** yxieca (Microsoft) AI note "no issues found" but **DISMISSED** (not an approval); `/azp run` excluded (docs path).
- **Matches description?:** Partial — PR body template is essentially empty; the doc delivers a thin but coherent plan.
- **Conflict likelihood:** Low — brand-new file.
- **Duplication likelihood:** none seen.
- **Linked issue(s):** sonic-buildimage#20108 is a **PR** (cross-repo, closed) — track-only; `Fixes #` blank.
- **Reviewer notes:** Under-delivers vs its own objectives — TC1 lists 16/32/63-char objectives but exercises only one ~30-char name (no boundary cases); TC2 deletes via raw `redis-cli del` (bypasses config tooling); markdown code-fence glitch; empty PR template. Defer to Microsoft on intent.

[↑ back to recommendations](#deep-review-findings--sonic-netsonic-mgmt--2026-06-10)

<a id="pr-21658"></a>

### [PR #21658](https://github.com/sonic-net/sonic-mgmt/pull/21658) — [AI - Snappi] BGP convergence testcase for single session flap Down (Case 1)
- **➡ Recommendation:** Get another opinion — snappi (not CI-run) + r12f review comments open
- **Author / affiliation:** selldinesh (Dinesh Kumar Sellappan) / Keysight Technologies
- **Trust:** Expert (Keysight)
- **CI runs the test?:** No (snappi/nut)
- **Type:** New test suite (Snappi dataplane BGP convergence test)
- **Complexity:** Low–Medium — single new file `test_bgp_single_port_down.py`, +272/-0; shared logic in the merged `helper.py`.
- **Description summary:** Measures BGP convergence (packet-loss duration) for a single-session flap over two `event_type`s (`t0_port_shutdown`, `route_withdrawal`) across frame sizes 64–8192 (IPv6); records a convergence-time gauge.
- **Existing reviews/comments:** r12f (Microsoft) — 5 actionable inline comments (rename event types to HLD, lift common code, rename `subnet_type`→`ip_version`, add scale/prefix params, adjust frame sizes); author replied "fixed" to 4; r12f "Still waiting for updates." yxieca DISMISSED.
- **Matches description?:** Yes — Case 1 single-session flap as described.
- **Conflict likelihood:** Low — brand-new file.
- **Duplication likelihood:** none — confirmed **sibling** of #21660 (clean series), not a dup.
- **Linked issue(s):** none — `Fixes #` blank; dependency #21565 already merged.
- **Reviewer notes:** r12f's dedup-refactor of the two event branches is still largely unmet (substantial duplicated setup/teardown); test only parametrizes IPv6 (IPv4 ranges are dead config); hardcoded `/home/admin/ai_acl.json` + `chmod 666`. Defer to Keysight on the TG harness.

[↑ back to recommendations](#deep-review-findings--sonic-netsonic-mgmt--2026-06-10)

<a id="pr-21660"></a>

### [PR #21660](https://github.com/sonic-net/sonic-mgmt/pull/21660) — [AI - Snappi] BGP convergence testcase for Device Unisolation (Case 3)
- **➡ Recommendation:** Get another opinion — snappi (not CI-run) + r12f skeleton-dedup request open
- **Author / affiliation:** selldinesh (Dinesh Kumar Sellappan) / Keysight Technologies
- **Trust:** Expert (Keysight)
- **CI runs the test?:** No (snappi/nut)
- **Type:** New test suite (Snappi dataplane BGP-convergence case)
- **Complexity:** Low–Medium — single new file `test_bgp_device_unisolation.py`, +221/-0; relies on the already-merged shared `helper.py` (#21204).
- **Description summary:** Snappi BGP dataplane-convergence test over three "device unisolation" recovery events (`config_reload`, `all_ports_startup`, `bgp_container_restart`), parametrized by IP version / frame rate / frame size; reports convergence time as a Gauge metric.
- **Existing reviews/comments:** r12f (Microsoft) — multiple inline comments (no approve): reuse one skeleton across cases 1/2/3, drop an unneeded param, select the t1 device from topo/tbinfo not a hostname substring; author marked some fixed, deferred skeleton reuse. advanced-security flagged unused imports. yxieca DISMISSED ×2.
- **Matches description?:** Yes — implements the three events. Minor: docstring/body is stale copy-paste from Case 1 ("fec errors").
- **Conflict likelihood:** Low — single new file.
- **Duplication likelihood:** none — confirmed **sibling** of #21658 (different file, shared helper), not a dup; r12f's skeleton-dedup request is the legit overlap, deferred.
- **Linked issue(s):** none — `Fixes #` blank; #21204 (dep, merged) and #21658 (sibling) are PRs.
- **Reviewer notes:** Fix stale docstring; verify the `configure_acl_for_route_withdrawl` unused import was actually removed; t1 selection still uses `'t1' in hostname` substring (fragile). Defer to Keysight on harness style; skeleton dedup is the only real maintainability lever.

[↑ back to recommendations](#deep-review-findings--sonic-netsonic-mgmt--2026-06-10)

<a id="pr-24902"></a>

### [PR #24902](https://github.com/sonic-net/sonic-mgmt/pull/24902) — Handle pytest.fail.Exeption in wait_until
- **➡ Recommendation:** Get another opinion — one-line change to shared wait_until; repo-wide behavioral effect
- **Author / affiliation:** wrideout-arista / Arista
- **Trust:** High (Arista)
- **CI runs the test?:** Partial (lib runs; new branch not asserted)
- **Type:** Bug fix
- **Complexity:** Low — one-line change (+1/-1) in shared `tests/common/utilities.py`; narrow change but broad blast radius (`wait_until` is used everywhere).
- **Description summary:** `wait_until` catches `Exception`, but `pytest.fail()` raises `pytest.fail.Exception` (a `BaseException` subclass) which escapes the handler → immediate failure instead of retry. Adds `pytest.fail.Exception` to the `except` tuple. Fixes #24726.
- **Existing reviews/comments:** No formal reviews; author pinged wangxin/lolyu/yutongzhang-microsoft.
- **Matches description?:** Yes — exactly the widened `except`; rationale technically accurate (`pytest` already imported).
- **Conflict likelihood:** Low — file-isolated.
- **Duplication likelihood:** none seen.
- **Reviewer notes:** Behavioral nuance: a `pytest_assert`/`pytest.fail` inside a condition is now swallowed and retried to timeout — intended, but any call site relying on fast-fail changes behavior. Title typo ("Exeption").

[↑ back to recommendations](#deep-review-findings--sonic-netsonic-mgmt--2026-06-10)

<a id="pr-25123"></a>

### [PR #25123](https://github.com/sonic-net/sonic-mgmt/pull/25123) — [TH6] test_po_cleanup fix for large number of lags(100s)
- **➡ Recommendation:** Get another opinion — intentional syslog-sampling sensitivity needs maintainer sign-off; Nokia-HW path
- **Author / affiliation:** sanjair-git / Nokia
- **Trust:** Expert (Nokia)
- **CI runs the test?:** Partial (>64-LAG branch unreachable on vs)
- **Type:** Bug fix (labeled "Test case improvement")
- **Complexity:** Medium — single file, +79/-5; adds branching LAG-count logic, syslog sampling heuristics, and a custom BGP-wait path; confined to one test.
- **Description summary:** On TH6/large topologies with 100+ port channels, `test_po_cleanup_after_reload` fails falsely because (1) LogAnalyzer needs a per-LAG SIGTERM line for every LAG and rsyslog drops lines under CPU stress, and (2) the built-in BGP wait is unrealistic while CPUs are pegged. Keeps strict per-LAG matching at ≤64 LAGs; for >64, uses a broad SIGTERM regex + a stratified mandatory sample, then drops stress load before asserting BGP convergence.
- **Existing reviews/comments:** None.
- **Matches description?:** Yes — `LAG_LOG_STRICT_PER_PC_MAX=64` threshold, `stratified_lag_samples_for_syslog`, broad SIGTERM pattern, `wait_for_bgp=False` + `killall yes` + explicit wait.
- **Conflict likelihood:** Low — file-isolated.
- **Duplication likelihood:** none seen.
- **Reviewer notes:** (1) Author acknowledges a single broken LAG can slip through if not in the sample and its syslog line is dropped — an intentional sensitivity trade-off a maintainer should sign off (the test's purpose is catching missing-SIGTERM regressions). (2) `bgp_wait_seconds_after_config_reload` hardcodes platform `x86_64-nokia_ixr7220_h6_128-r0` and duplicates `config_reload`'s timeout math (will silently drift). No linked issue; `64` is a magic number with no >64-path test evidence shown.

[↑ back to recommendations](#deep-review-findings--sonic-netsonic-mgmt--2026-06-10)

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


<a id="pr-24649"></a>

### [PR #24649](https://github.com/sonic-net/sonic-mgmt/pull/24649) — [dualtor] Add test for tunnel termination drop on standby ToR
- **➡ Recommendation:** Approve — clean self-contained new dualtor test; all imported helpers/fixtures verified present; call signatures match the established `test_ipinip.py` patterns; closes the #21092 test gap. CI doesn't run it, but the author provided real hardware runs.
- **Author / affiliation / trust:** yyynini (Yawen) / Microsoft (yawenni@microsoft.com) / Expert (55 merged)
- **CI runs the test?:** No — not listed in `pr_test_scripts.yaml`, so the KVM gate doesn't run it; `topology('dualtor')` + `enable_active_active`. **Hardware evidence provided:** author linked ElasticTest runs on Cisco 8101 and Arista (libra/gemini) in the PR body → evidence bar met.
- **Type:** New test case (dualtor IPinIP tunnel-termination drop)
- **Complexity:** Med — packet construction + 3-way topology branching + negative assertions (`verify_no_packet` + `tunnel_traffic_monitor(existing=False)`).
- **Description summary:** Adds `test_tunnel_term_drop_standby`: a standby ToR receives an IPinIP packet and the test asserts it's dropped (neither decapsulated to the server nor re-encapsulated to T1), for both active-standby and active-active cable types.
- **Existing reviews/comments:** github-advanced-security (no findings); lolyu COMMENTED (non-blocking); yxieca AI note (its concerns are already satisfied in-code).
- **Matches description?:** Yes.
- **Conflict likelihood:** Low — single new file.
- **Duplication likelihood:** none — reuses but doesn't duplicate `test_ipinip.py`; this is the dedicated drop/loop-prevention case.
- **Linked issue(s):** `Fixes #21092` (open test-gap, same-repo + keyword) → **auto-closes on merge to default branch**.
- **Reviewer notes:** Verified all five imported helpers exist at head SHA and the fixture call signature matches. Optional non-blocking: add the file to `pr_test_scripts.yaml` so it runs in the gated dualtor pipeline rather than only manual ElasticTest.

[↑ back to recommendations](#deep-review-findings--sonic-netsonic-mgmt--2026-06-10)

<a id="pr-24687"></a>

### [PR #24687](https://github.com/sonic-net/sonic-mgmt/pull/24687) — pfcwd: ignore benign cisco-8000 SAI/orchagent errors during teardown of test_pfcwd_cli
- **➡ Recommendation:** Approve — narrow, asic-gated loganalyzer ignore-list extension following the existing vs/KVM pattern in the same fixture; additive-only, zero behavior change on other platforms.
- **Author / affiliation / trust:** wsycqyz (ShiyanWangMS) / Microsoft / Expert (100+ merged)
- **CI runs the test?:** Partial — `test_pfcwd_cli.py` is in the gate so the fixture loads/parses, but the new `Cisco8000IgnoreRegex` branch is guarded by `asic_type == 'cisco-8000'`, which never matches on the vs gate — so the ignore behavior itself is hardware-only and not validated; green CI only confirms the existing path is unbroken.
- **Type:** Bug fix (test reliability / loganalyzer false-positive suppression)
- **Complexity:** Low — 1 file, +16/-0: a regex list + one conditional `extend`.
- **Description summary:** On cisco-8000, `test_pfcwd_show_stat` passes but flags ERROR at teardown from a burst of benign syncd/orchagent ERR lines during LAG-member QoS rebind. Suppresses only those signatures, only on cisco-8000, mirroring the existing vs/KVM ignore pattern; root-cause orchagent fix tracked separately.
- **Existing reviews/comments:** No human reviews; bot/automation only.
- **Matches description?:** Yes — exactly the six regexes + cisco-8000-gated `extend`.
- **Conflict likelihood:** Low — single fixture in one file.
- **Duplication likelihood:** none seen.
- **Linked issue(s):** none (`Fixes #` blank; a nightly testplan ID referenced, no GitHub issue).
- **Reviewer notes:** Verified the asic-gated `ignore_regex.extend` pattern is idiomatic (matches existing vs/KVM/Tacacs blocks in this fixture). Minor: a couple of the regexes are somewhat generic, so they'd suppress those syncd lines for any test using this fixture on cisco-8000 — acceptable given the cisco-8000 + single-file scope.

[↑ back to recommendations](#deep-review-findings--sonic-netsonic-mgmt--2026-06-10)
