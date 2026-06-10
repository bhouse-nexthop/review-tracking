# Deep-review findings — sonic-net/sonic-mgmt

**PRs awaiting our action**, sorted by recommendation — each links to its full brief (click → read → back → next). A PR drops off this doc once it's **approved/merged** or **handed back to the author** (changes/info/evidence requested, conflicting, COI-waiting); full state + history live in `actions.jsonl` + git. Recommendations fold in: does the diff match the description, complexity, **author trust** (§8.1), and **whether CI actually runs the test** (a green check on a skipped test proves nothing — see CI column). _Decision support; approval is the human reviewer's call._

**Tally:** Request changes: 3 · Needs hardware-pass evidence: 10 · Get another opinion: 5 · Blocked (COI): 2  
_(6 approved & merged-track this cycle: #23930, #24493, #24545, #24597, #24876, #25134 — now off-doc; #24975 awaiting author.)_

## Request changes (3)

| PR | Title | Type/Trust | CI runs test? | Why |
|----|-------|-----------|---------------|-----|
| [#24247](#pr-24247) | [SNAPPI][AI] Finding the minimum frame size wi… | New test suite / Medium | No (snappi/nut) | resolve global test_results xdist hazard + double-start, then snappi pass |
| [#24320](#pr-24320) | changes for port speed test enhancement | Mix (refactor+fix) / High | No (t2/lrh/urh) | Partial match + scope creep; abdosi says approach may be superseded |
| [#24845](#pr-24845) | ARS test script | New test suite / Medium | No (marvell-teralynx) | fix live CodeQL regex + acl.json action/value mismatch, then marvell HW pass |

## Needs hardware-pass evidence (10)

| PR | Title | Type/Trust | CI runs test? | Why |
|----|-------|-----------|---------------|-----|
| [#18701](#pr-18701) | Fix missing PSU fans in test_psu_fan.py port t… | Backport (bugfix) / Low | No (api not in gate) | PSU api not in gate; faithful backport of merged #17641 (lower risk) |
| [#24437](#pr-24437) | save pfcwd_timer_accuracy test result to file | Feature (diag) / Medium | Partial (vs early-return) | shared pfcwd test; changed save-path unreached on vs |
| [#24787](#pr-24787) | [platform_tests][T2] Add test_sup_fan_recovery… | New test suite / Medium | No (t2 chassis) | new T2 chassis test; hardware-only; no human review yet |
| [#24829](#pr-24829) | Fix: add port name for acl interface parsing | Bug fix / High | No (fix branch not hit on vs) | shared minigraph lib; new ACL branch only hit on hardware |
| [#24884](#pr-24884) | [bgp scale] Reduce DUT-side observer load duri… | Test improvement / Expert | No (isolated-scale topo) | isolated-scale topology; not run on the gate |
| [#24927](#pr-24927) | Fix test_link_local_ip failures in dualtor act… | Bug fix / High | Partial (not dualtor-aa) | dualtor-active-active path not exercised by the gate |
| [#24930](#pr-24930) | [vxlan] Improve vnet bgp subintf cleanup diagn… | Test improvement / Expert | No (physical/cisco-8000) | cisco-8000 hardware; author affiliation unknown (no vendor-trust) |
| [#25000](#pr-25000) | Fix test_srv6_vlan_forwarding when no ipv6 mgm… | Bug fix / High | No (mellanox/broadcom only) | touches mellanox AND broadcom (cross-vendor); not CI-run |
| [#25040](#pr-25040) | [bgp/agg] Make BGP aggregate-address tests sol… | Bug fix (flake) / Medium | No (m1 topo, not in gate) | m1 topology not in gate; shared bgp aggregate suite |
| [#25094](#pr-25094) | Add disable_memory_utilization option for fwut… | Test improvement / Medium | Partial (firmware skipped) | firmware tests skip on vs; request a hardware run |

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

<a id="pr-24247"></a>

### [PR #24247](https://github.com/sonic-net/sonic-mgmt/pull/24247) — [SNAPPI][AI] Finding the minimum frame size with no packet loss
- **➡ Recommendation:** Request changes — resolve global test_results xdist hazard + double-start, then snappi pass
- **Author / affiliation:** vikumarks (Vinod Kumar) / Keysight Technologies (Snappi/Ixia TG vendor)
- **Trust:** Medium (Keysight)
- **CI runs the test?:** No (snappi/nut)
- **Type:** New test suite — new `tests/snappi_tests/dataplane/test_min_frame_size.py` + additive `boundary_check` helper in `dataplane/files/helper.py`
- **Complexity:** Medium — 2 files, +242/-0; one net-new, one additive helper (shared by the dataplane snappi suite). Runs only on `topology("nut")` with an Ixia/IxNetwork backend.
- **Description summary:** Binary-searches 64-byte-aligned frame sizes (64..9100) at 100% line rate to find the smallest size with zero loss, for IPv4/IPv6 and RFC2889 on/off; sanity-checks the max frame first, then leftmost-True binary search, recording to a DataFrame + GaugeMetric.
- **Existing reviews/comments:** banidoru (AI reviewer, 3 iterations) — early CHANGES_REQUESTED, latest COMMENTED ("most concerns addressed, ~5 minor open"). yxieca non-blocking AI note. No human approval (REVIEW_REQUIRED, mergeStateStatus BLOCKED).
- **Matches description?:** Yes — implements the binary-search min-frame flow. (Body summary line says "maximum traffic rate" but the implementation/title target minimum frame size.)
- **Conflict likelihood:** Low — new file isolated; helper.py change is a single appended function.
- **Duplication likelihood:** none seen.
- **Linked issue(s):** none — `Fixes #` placeholder blank.
- **Reviewer notes:** Two real, still-open items in head: (1) module-level `global test_results` DataFrame mutated across parametrized runs → xdist/parallel contamination risk; (2) possible double traffic start (`start_stop(start,…)` then `boundary_check` calls `StartStatelessTrafficBlocking()` with no intervening stop). Uses private RestPy (`snappi_api._ixnetwork`) — Ixia-only by design (defer to Keysight), but breaks the vendor-neutral SNAPPI abstraction.
- **Requested changes (to post):**
  1. **`global test_results` DataFrame** — it's module-level and mutated across parametrized runs, so under xdist/`-n` (or repeated params) results contaminate each other. Scope it to a fixture / per-test return instead of a module global.
  2. **Double traffic start** — `start_stop(start, traffic)` runs, then the first `boundary_check` calls `StartStatelessTrafficBlocking()` with no intervening stop. Stop before re-starting (or start traffic once).
  3. **Description nit** — the Summary says "maximum traffic rate" but the test finds the *minimum frame size*; please correct it.
  - Also: the PR-gate doesn't run this (snappi/`nut`), so please attach a passing snappi/Ixia run before merge. We defer to Keysight on the Ixia-private RestPy usage.

[↑ back to recommendations](#deep-review-findings--sonic-netsonic-mgmt--2026-06-10)

<a id="pr-24320"></a>

### [PR #24320](https://github.com/sonic-net/sonic-mgmt/pull/24320) — changes for port speed test enhancement
- **➡ Recommendation:** Request changes — Partial match + scope creep; abdosi says approach may be superseded
- **Author / affiliation:** rawal01 / Nokia
- **Trust:** High (Nokia)
- **CI runs the test?:** No (t2/lrh/urh)
- **Type:** Mix — test refactor + several incidental bug fixes
- **Complexity:** Medium-High — single file, +257/-111, near-total rewrite of fixture/DUT-selection logic + multi-ASIC plumbing; confined to one test.
- **Description summary:** Enhances `test_port_speed_change` to cover both downgrade and upgrade (was one direction) via parametrization, reworks DUT/port selection, decouples traffic-source DUT from the test DUT, adds multi-ASIC namespace context.
- **Existing reviews/comments:** yejianquan (COMMENTED, non-blocking) credited real bug fixes and asked for test results + inline comments. anamehra asked about testbed setup. abdosi: master approach will move to no-patch-cleanup; 202405 needs a separate testcase.
- **Matches description?:** **Partial** — parametrization/bidirectional coverage + DUT-selection rework match intent, but the diff also contains undisclosed changes (ACL enumeration from config_facts, `/localhost/` patch removal, wholesale PORT object replace, BUFFER_QUEUE cleanup, new split-patch `No.1b` flow). Real fixes but scope creep vs the description.
- **Conflict likelihood:** Low — file-isolated.
- **Duplication likelihood:** none seen.
- **Reviewer notes:** abdosi flagged the master approach is still evolving → may be partially superseded; confirm direction. Wholesale PORT replace + split-patch ordering are the riskiest changes; requested test results not yet posted.
- **Requested changes (to post):**
  1. **Scope vs. description** — the diff goes well beyond "add parametrization": it also changes ACL enumeration (config_facts-driven), removes the `/localhost/` patch ops, does a wholesale PORT-object replace, adds BUFFER_QUEUE cleanup, and a new split-patch `No.1b` remove flow. Please either narrow the PR to the described change or update the description to cover everything — and split the unrelated fixes into their own PR(s) if practical.
  2. **Confirm direction** — abdosi notes the master approach is moving away from remove-op patch cleanup and that 202405 needs a separate testcase; please confirm this isn't superseded before we invest further review.
  3. **Test results** — post the run results yejianquan asked for and address the inline comments.
  - Also: the PR-gate doesn't run this (`topology t2/lrh/urh`), so a t2 hardware pass is needed to validate the rewrite.

[↑ back to recommendations](#deep-review-findings--sonic-netsonic-mgmt--2026-06-10)

<a id="pr-24845"></a>

### [PR #24845](https://github.com/sonic-net/sonic-mgmt/pull/24845) — ARS test script
- **➡ Recommendation:** Request changes — fix live CodeQL regex + acl.json action/value mismatch, then marvell HW pass
- **Author / affiliation:** apannerselva / Marvell Technology
- **Trust:** Medium (Marvell)
- **CI runs the test?:** No (marvell-teralynx)
- **Type:** New test suite
- **Complexity:** Medium — 7 files, +797/-1; new `tests/ecmp/ars/` package + ptf script; only shared touch is an additive block in `tests_mark_conditions.yaml`.
- **Description summary:** New ARS (Adaptive Routing and Switching) suite implementing the ARS HLD test plan (SONiC#1958): per-packet/per-flowlet load balancing across NHG selector modes, an ACL "disable ARS" action, non-ARS behavior, and a stress test, with a new ptf dataplane test. T0-only, gated to Marvell-teralynx.
- **Existing reviews/comments:** github-advanced-security[bot] raised many CodeQL findings (unused imports, two "unmatchable caret/dollar" regex warnings). radha-danda triggered `/azpw run`; author pinged reviewers. No human approval.
- **Matches description?:** Yes — the 10 parametrized cases + marvell-teralynx gating match. Caveats: diff appears out of sync with some CodeQL-flagged symbols (post-scan cleanup), but unmatchable-regex findings still apply; `acl.json` defines action `DISABLE_ARS_FORWARDING` then sets it to `"DROP"` — looks semantically off.
- **Conflict likelihood:** Low — additive overlap with #24545 only (different region of the yaml).
- **Duplication likelihood:** none seen.
- **Reviewer notes:** Needs a human pass: fix the live CodeQL regex warnings, confirm the `acl.json` action/value mismatch, verify unused-import findings actually resolved. Heavy `time.sleep` + full `config_reload` per case → slow/flaky-prone.
- **Requested changes (to post):**
  1. **CodeQL — unmatchable regex** — the anchored patterns in `verify_bgp_ecmp` / `has_ecmp_routes` have internal `^`/`$`, so they can never match; please fix them.
  2. **Unused imports** — the diff looks out of sync with the CodeQL scan; confirm the flagged unused imports are actually removed.
  3. **`acl.json` action/value mismatch** — it defines action `DISABLE_ARS_FORWARDING` but the rule sets it to `"DROP"`; please reconcile.
  4. **Dead sleeps** — heavy `time.sleep` + a full `config_reload` per case is slow and flake-prone; gate on readiness (`wait_until`) where a signal exists rather than fixed sleeps.
  - Also: the PR-gate doesn't run this (gated to marvell-teralynx), so a marvell-teralynx hardware pass is needed.

[↑ back to recommendations](#deep-review-findings--sonic-netsonic-mgmt--2026-06-10)

<a id="pr-18701"></a>

### [PR #18701](https://github.com/sonic-net/sonic-mgmt/pull/18701) — Fix missing PSU fans in test_psu_fan.py port to 202411
- **➡ Recommendation:** Needs hardware-pass evidence — PSU api not in gate; faithful backport of merged #17641 (lower risk)
- **Author / affiliation:** eyakubch / **unknown** (empty profile company, no org suffix)
- **Trust:** Low (unknown)
- **CI runs the test?:** No (api not in gate)
- **Type:** Backport (bug fix) — clean 202411 backport of merged master PR #17641
- **Complexity:** Low — 3 files, +48/-17, all under `tests/platform_tests/api/`.
- **Description summary:** Fixes `test_psu_fans.py` failures on devices with absent/skipped PSUs by extracting `skip_absent_psu` to a module-level `conftest.py` function and wiring it into `TestPsuFans` (mirroring `test_psu.py`); populates `self.psu_skip_list` in setup.
- **Existing reviews/comments:** yxieca (Microsoft) AI note "no issues found" but **DISMISSED**; BuildBot added 202311/202405/202505 backport labels.
- **Matches description?:** Yes — exactly the helper extraction + skip-guard insertion, consistent with `test_psu.py`.
- **Conflict likelihood:** Low — targets release branch `202411`, isolated to PSU API tests; sibling backports go to other branches.
- **Duplication likelihood:** none — legitimate backport of #17641, not a dup.
- **Linked issue(s):** none closeable — references master PR #17641 (a PR); `Fixes #` blank.
- **Reviewer notes:** Faithful to master; minor PEP8 nit (blank lines before the new module-level function) and conftest-as-importable-module pattern (matches master). PSU hardware isn't author-specific.
- **Suggested recommendation:** Approve — low-risk faithful backport of an already-merged fix, isolated to a release branch.

[↑ back to recommendations](#deep-review-findings--sonic-netsonic-mgmt--2026-06-10)

<a id="pr-24437"></a>

### [PR #24437](https://github.com/sonic-net/sonic-mgmt/pull/24437) — save pfcwd_timer_accuracy test result to file
- **➡ Recommendation:** Needs hardware-pass evidence — shared pfcwd test; changed save-path unreached on vs
- **Author / affiliation:** wenjwang-nv / NVIDIA
- **Trust:** Medium (NVIDIA)
- **CI runs the test?:** Partial (vs early-return)
- **Type:** Feature enhancement (test instrumentation / diagnostics)
- **Complexity:** Low — +56/-1 across 2 files; opt-in CLI flag + fixture + helper; conftest touch is purely additive.
- **Description summary:** Adds an opt-in `--save-timer-results` option that writes pfcwd timer-accuracy metrics to a JSON file under `/tmp` for trend analysis. Default off, existing behavior unchanged.
- **Existing reviews/comments:** nhe-NV reviewed then APPROVED. No unresolved concerns.
- **Matches description?:** Yes — exactly the described option/fixture/writer. No scope creep.
- **Conflict likelihood:** Low — file-isolated.
- **Duplication likelihood:** none seen.
- **Reviewer notes:** Minor non-blocking: hardcoded `/tmp` path; `test_func_name` param is always the literal test name (redundant). Already approved by an NVIDIA reviewer.
- **Suggested recommendation:** Approve — clean opt-in instrumentation, already approved by nhe-NV

[↑ back to recommendations](#deep-review-findings--sonic-netsonic-mgmt--2026-06-10)

<a id="pr-24787"></a>

### [PR #24787](https://github.com/sonic-net/sonic-mgmt/pull/24787) — [platform_tests][T2] Add test_sup_fan_recovery.py
- **➡ Recommendation:** Needs hardware-pass evidence — new T2 chassis test; hardware-only; no human review yet
- **Author / affiliation:** aeedara-nokia / Nokia
- **Trust:** Medium (Nokia)
- **CI runs the test?:** No (t2 chassis)
- **Type:** New test suite (single new T2 chassis regression test)
- **Complexity:** Low–Medium — one new self-contained file (+196/-0); no shared-lib edits. Medium-ish because it does a destructive minigraph override-reload + cold reboot.
- **Description summary:** Adds `test_sup_fan_status_after_reload_reboot` iterating supervisor nodes: snapshots `/var/core`, arms a LogAnalyzer for the thermalctld bug signature, minigraph override-reload, asserts fans OK, cold-reboots, re-asserts, checks no new cores. Targets a thermalctld/psu regression where fans returned `Not present`.
- **Existing reviews/comments:** None substantive — only EasyCLA. No human review.
- **Matches description?:** Yes — every described step implemented; VS skip + missing-minigraph skip are disclosed extras.
- **Conflict likelihood:** Low — file-isolated.
- **Duplication likelihood:** none seen.
- **Reviewer notes:** (1) `_all_fans_ok` calls `verify_show_platform_fan_output` which asserts internally — if it asserts on malformed output, `wait_until` may not retry cleanly. (2) Destructive (override-reload + cold reboot of a chassis sup), recovery leans on `reboot_and_check`; no `Fixes #` link.
- **Suggested recommendation:** Get another opinion — new destructive T2 chassis test with no human review yet — wants a platform/T2 SME; add a Fixes link

[↑ back to recommendations](#deep-review-findings--sonic-netsonic-mgmt--2026-06-10)

<a id="pr-24829"></a>

### [PR #24829](https://github.com/sonic-net/sonic-mgmt/pull/24829) — Fix: add port name for acl interface parsing
- **➡ Recommendation:** Needs hardware-pass evidence — shared minigraph lib; new ACL branch only hit on hardware
- **Author / affiliation:** ytzur1 / NVIDIA
- **Trust:** High (NVIDIA)
- **CI runs the test?:** No (fix branch not hit on vs)
- **Type:** Bug fix
- **Complexity:** Low — 2 added lines in `ansible/library/minigraph_facts.py` (a widely-used shared Ansible fact lib, so non-trivial blast radius despite the tiny change).
- **Description summary:** PR #22166 made `minigraph_dpg.j2` put interface names (not aliases) in ACL `AttachTo` on non-multi-ASIC setups; the parser only matched aliases → empty `acl_intfs`/`minigraph_acls` → KeyError on `mg_facts["minigraph_acls"]["DataAcl"]`. Adds an `elif member in ports` fallback.
- **Existing reviews/comments:** None (REVIEW_REQUIRED).
- **Matches description?:** Yes — exactly the described fallback after the alias branch.
- **Conflict likelihood:** Low — file-isolated.
- **Duplication likelihood:** none seen.
- **Reviewer notes:** Additive (can't regress existing matches). Confirm `ports` is in scope/populated at that point; change is unconditional (not ASIC-mode gated) — likely fine as a last-resort fallback. No test added (author validated via internal regression).
- **Suggested recommendation:** Approve — minimal additive last-resort fallback; low regression risk (a test would be nice-to-have)

[↑ back to recommendations](#deep-review-findings--sonic-netsonic-mgmt--2026-06-10)

<a id="pr-24884"></a>

### [PR #24884](https://github.com/sonic-net/sonic-mgmt/pull/24884) — [bgp scale] Reduce DUT-side observer load during route convergence tests
- **➡ Recommendation:** Needs hardware-pass evidence — isolated-scale topology; not run on the gate
- **Author / affiliation:** yutongzhang-microsoft / Microsoft
- **Trust:** Expert (Microsoft)
- **CI runs the test?:** No (isolated-scale topo)
- **Type:** Test improvement (measurement-fidelity tuning)
- **Complexity:** Low — single test file, +82/-4; no shared-lib touch, but an autouse fixture mutates live DUT state (stops `openbmpd`, disables redis RDB) so teardown/restore matters.
- **Description summary:** Profiling showed ~35% of DUT OnCPU during `test_sessions_flapping[500]` came from `openbmpd` + `redis-check-rdb` — observer noise inflating convergence numbers. Adds a fixture to stop openbmpd + disable redis saves (restored after), raises poll interval 1s→5s, caps sairedis-log reads at last 100MB, memoizes `_get_backplane_ports`.
- **Existing reviews/comments:** None.
- **Matches description?:** Yes — all four changes faithful, with save/restore guards (`module_ignore_errors=True`).
- **Conflict likelihood:** Low — file-isolated (sibling #25040 touches different bgp files).
- **Duplication likelihood:** none seen.
- **Reviewer notes:** (1) Redis `save` restore relies on `config get save` formatting; if it differs or has <2 lines, the original is silently left disabled. (2) 1s→5s coarsens convergence resolution 5× for *all* callers, not just the [500] case — confirm acceptable for sub-5s measurements.
- **Suggested recommendation:** Get another opinion — the 1s→5s poll change coarsens convergence resolution for ALL callers — wants a scale-test owner's eye

[↑ back to recommendations](#deep-review-findings--sonic-netsonic-mgmt--2026-06-10)

<a id="pr-24927"></a>

### [PR #24927](https://github.com/sonic-net/sonic-mgmt/pull/24927) — Fix test_link_local_ip failures in dualtor active-active topology
- **➡ Recommendation:** Needs hardware-pass evidence — dualtor-active-active path not exercised by the gate
- **Author / affiliation:** xixuej / NVIDIA (nvidia-sonic)
- **Trust:** High (NVIDIA)
- **CI runs the test?:** Partial (not dualtor-aa)
- **Type:** Bug fix
- **Complexity:** Low — single test file, +25/-11; no shared-lib touch.
- **Description summary:** Fixes `test_link_local_ip` failures on dualtor active-active after `SAI_NOT_DROP_SIP_DIP_LINK_LOCAL=1` was added. (1) Downlink ingress used global router MAC instead of shared VLAN MAC (dropped) → new `get_downlink_router_mac()` from config_facts; (2) adds the `dualtor_active_active_setup_standby_on_random_unselected_tor` marker and switches DUT-selection fixture to `rand_one_dut_hostname`.
- **Existing reviews/comments:** nhe-NV — APPROVED; yyynini — APPROVED ("lgtm").
- **Matches description?:** Yes — per-direction `router_mac` plumbed through; marker + fixture swap present.
- **Conflict likelihood:** Low — file-isolated.
- **Duplication likelihood:** none seen.
- **Reviewer notes:** (1) Fixture swap changes DUT-enumeration semantics for *all* topologies (test is `topology('any')`); sanity-check non-dualtor coverage. (2) `get_downlink_router_mac` indexes `config_facts['VLAN'][vlan_interface]` unguarded — KeyError possible in an unlikely config state. Double-approved.
- **Suggested recommendation:** Approve — faithful dualtor-aa fix, double-approved; note the all-topology fixture swap

[↑ back to recommendations](#deep-review-findings--sonic-netsonic-mgmt--2026-06-10)

<a id="pr-24930"></a>

### [PR #24930](https://github.com/sonic-net/sonic-mgmt/pull/24930) — [vxlan] Improve vnet bgp subintf cleanup diagnostics
- **➡ Recommendation:** Needs hardware-pass evidence — cisco-8000 hardware; author affiliation unknown (no vendor-trust)
- **Author / affiliation:** yyynini / **unknown** (profile name "Yawen"; no company/email; appears as approver on NVIDIA PRs #24927/#24876 → possible NVIDIA association, unconfirmed)
- **Trust:** Expert (unknown)
- **CI runs the test?:** No (physical/cisco-8000)
- **Type:** Test improvement (diagnostics + cleanup hardening)
- **Complexity:** Low — single test file, +78/-37; no shared-lib touch.
- **Description summary:** Adds bounded DUT-state diagnostic logging when the WL→T1 VXLAN encap verification fails, and refactors `cleanup()` into independent named phases so one failing phase doesn't abort the rest. Explicitly does not change dataplane expectations/timeout/topology/skip.
- **Existing reviews/comments:** None.
- **Matches description?:** Yes — `dump_encap_failure_diagnostics()` wraps verify in try/except, dumps the listed commands, re-raises; `cleanup()` split into `cleanup_step`-wrapped phases. Minor reasonable extras: backup-existence guard before `mv`, `mv -f`, `continue_on_fail`/`module_ignore_errors` on ptf shell cmds, `rm -f /tmp/{file}` on ptfhost.
- **Conflict likelihood:** Low — file-isolated.
- **Duplication likelihood:** none seen.
- **Reviewer notes:** (1) New `remove_temp_files` prefixes `/tmp/` to entries that may be full local paths — could target wrong path on PTF host; confirm what `temp_files` holds. (2) `cleanup_step` swallows per-phase exceptions by design (reduces signal if cleanup silently breaks).
- **Suggested recommendation:** Approve — behavior-preserving diagnostics/cleanup hardening; only confirm the temp-file path assumption

[↑ back to recommendations](#deep-review-findings--sonic-netsonic-mgmt--2026-06-10)

<a id="pr-25000"></a>

### [PR #25000](https://github.com/sonic-net/sonic-mgmt/pull/25000) — Fix test_srv6_vlan_forwarding when no ipv6 mgmt for ptf docker
- **➡ Recommendation:** Needs hardware-pass evidence — touches mellanox AND broadcom (cross-vendor); not CI-run
- **Author / affiliation:** ytzur1 / NVIDIA
- **Trust:** High (NVIDIA)
- **CI runs the test?:** No (mellanox/broadcom only)
- **Type:** Bug fix
- **Complexity:** Low — single test file, +6/-4, same fallback in three spots.
- **Description summary:** When the PTF docker has no IPv6 mgmt address, `ptfhost.mgmt_ipv6` is falsy and the test builds packets with an invalid source IP. Adds `ptf_mgmt_ipv6 = ptfhost.mgmt_ipv6 if ptfhost.mgmt_ipv6 else "1000::1"` used as `ipv6_src` in both packet builders. Targets 202605.
- **Existing reviews/comments:** None.
- **Matches description?:** Yes. Scope note: description says the same applies to `test_srv6_dataplane.py`, which is not included here.
- **Conflict likelihood:** Low — file-isolated.
- **Duplication likelihood:** none seen.
- **Reviewer notes:** (1) Confirm hardcoded `"1000::1"` is a valid non-conflicting source for the dataplane assertions. (2) Consider shipping the `test_srv6_dataplane.py` fix together per the author's own description.
- **Suggested recommendation:** Approve — correct fallback; optionally fold in the sibling test_srv6_dataplane.py fix the author mentions

[↑ back to recommendations](#deep-review-findings--sonic-netsonic-mgmt--2026-06-10)

<a id="pr-25040"></a>

### [PR #25040](https://github.com/sonic-net/sonic-mgmt/pull/25040) — [bgp/agg] Make BGP aggregate-address tests solid against per-DUT flakiness
- **➡ Recommendation:** Needs hardware-pass evidence — m1 topology not in gate; shared bgp aggregate suite
- **Author / affiliation:** nanali-msft / Microsoft
- **Trust:** Medium (Microsoft)
- **CI runs the test?:** No (m1 topo, not in gate)
- **Type:** Bug fix (test-reliability)
- **Complexity:** Medium — 4 files, +111/-32, confined to the bgp aggregate suite (1 shared helper module + 3 test modules).
- **Description summary:** Hardens the suite against per-DUT flakiness: makes route verification origin-aware (filter M2 paths by the DUT's own ASN), forces a deterministic disabled→enabled BBR transition instead of trusting ambient state, and exempts the stress module from the memory-utilization monitor.
- **Existing reviews/comments:** shixizhang — APPROVED.
- **Matches description?:** Yes — `expected_asn` plumbed through with EOS/FRR token matching; BBR forced-transition with try/finally restore; `disable_memory_utilization` mark; baseline `safe_remove_aggregate` + expected-absent precheck.
- **Conflict likelihood:** Low — files isolated to bgp aggregate suite.
- **Duplication likelihood:** none seen (#25094 uses the same `disable_memory_utilization` marker on a different file — same pattern, not a dup).
- **Reviewer notes:** Verify `get_bbr_default_state` and `safe_remove_aggregate` already exist in the helper module (used but not defined in this diff) or imports break.
- **Suggested recommendation:** Approve — faithful flakiness hardening, approved; just verify the two helpers pre-exist

[↑ back to recommendations](#deep-review-findings--sonic-netsonic-mgmt--2026-06-10)

<a id="pr-25094"></a>

### [PR #25094](https://github.com/sonic-net/sonic-mgmt/pull/25094) — Add disable_memory_utilization option for fwutil test cases
- **➡ Recommendation:** Needs hardware-pass evidence — firmware tests skip on vs; request a hardware run
- **Author / affiliation:** zypgithub / **unknown** (profile company empty; display name "Yanpeng Zhang")
- **Trust:** Medium (unknown)
- **CI runs the test?:** Partial (firmware skipped)
- **Type:** Test improvement (test-infra marker)
- **Complexity:** Low — 1 file, +2/-1, a single `pytestmark` entry.
- **Description summary:** fwutil tests reboot the DUT, making the before/after memory-utilization plugin produce false failures. Adds `pytest.mark.disable_memory_utilization` to the module's `pytestmark`.
- **Existing reviews/comments:** nhe-NV — APPROVED.
- **Matches description?:** Yes — marker is a real recognized hook; no scope creep.
- **Conflict likelihood:** Low — file-isolated.
- **Duplication likelihood:** none seen (marker reused widely, distinct files).
- **Reviewer notes:** Clean, idiomatic, consistent with other modules using the marker. One maintainer approval. Nothing needing attention.
- **Suggested recommendation:** Approve — clean idiomatic marker, approved by nhe-NV

[↑ back to recommendations](#deep-review-findings--sonic-netsonic-mgmt--2026-06-10)

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
- **Suggested recommendation:** Get another opinion — doc-only/low-risk, but a Microsoft maintainer should decide whether a plan with no test code and untested boundaries clears the "[Test gap]" bar; currently has no valid approval.

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
- **Suggested recommendation:** Get another opinion — defer to r12f/Keysight; confirm the requested dedup-refactor + HLD event naming actually landed ("Still waiting for updates") before approval.

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
- **Suggested recommendation:** Get another opinion — sound and isolated, but should land with r12f's sign-off given the deferred skeleton dedup + stale docstring + lingering unused import.

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
- **Suggested recommendation:** Get another opinion — one-line fix but changes shared wait_until semantics repo-wide; have a common-infra maintainer confirm

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
- **Suggested recommendation:** Get another opinion — intentional syslog-sampling sensitivity trade-off weakens the test's core purpose — needs a maintainer sign-off; also a hardcoded platform string

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
- **Suggested recommendation:** Approve (minor nit) — docs-only, isolated, sound; fix the count mismatch and confirm dependent-HLD status. (Repo convention: maintainers don't formally approve docs-only PRs.)

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
- **Suggested recommendation:** Approve — clean, well-scoped consolidation, approved by liamkearney-msft

[↑ back to recommendations](#deep-review-findings--sonic-netsonic-mgmt--2026-06-10)

