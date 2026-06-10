# Deep-review findings — sonic-net/sonic-mgmt — 2026-06-10

Deep review (Rule 4) of the **21 eligible PRs** (no merge conflicts, CI passing,
last CI run within 2 weeks) where `bhouse-nexthop` is a requested reviewer.
These briefs are decision support for the human reviewer — no approvals implied.

## Triage summary

| PR | Type | Cmplx | Matches desc? | Existing approvals | Conflict | Dup | Suggested rec | Headline flag for reviewer |
|----|------|-------|---------------|--------------------|----------|-----|---------------|----------------------------|
| [#23930](https://github.com/sonic-net/sonic-mgmt/pull/23930) | Feature (hwsku reg) | Low | Yes | none | Low | none | Approve | Vendor hwsku from the vendor (defer on chip classification); vmittal-msft asked for descriptive title + master PR |
| [#24320](https://github.com/sonic-net/sonic-mgmt/pull/24320) | Mix (refactor+fixes) | Med-High | **Partial** | none (commented) | Low | none | Req changes / 2nd opinion | Scope creep beyond description; abdosi says approach may be superseded; risky wholesale PORT replace |
| [#24437](https://github.com/sonic-net/sonic-mgmt/pull/24437) | Feature (diag) | Low | Yes | nhe-NV | Low | none | Approve | Clean |
| [#24493](https://github.com/sonic-net/sonic-mgmt/pull/24493) | Bug fix | Low | Yes | nhe-NV | Low | none | Approve | Clean; confirm auth coverage preserved elsewhere |
| [#24545](https://github.com/sonic-net/sonic-mgmt/pull/24545) | Bug fix | Med | Yes | StormLiangMS, ZhaohuiS | **Med** (24845 shared yaml) | none | Approve | VS recovery timing assumption; post-recovery interface assertion removed |
| [#24597](https://github.com/sonic-net/sonic-mgmt/pull/24597) | Bug fix | Med | Yes | nhe-NV | Low | none | Approve | Confirm `sonic_deploy_202505.j2` template name + IPv6 asic set |
| [#24787](https://github.com/sonic-net/sonic-mgmt/pull/24787) | New test suite | Low-Med | Yes | none | Low | none | 2nd opinion | Destructive (reload+cold reboot); no `Fixes #` link; no human review yet |
| [#24829](https://github.com/sonic-net/sonic-mgmt/pull/24829) | Bug fix | Low | Yes | none | Low | none | Approve | No test added; confirm `ports` scope + ASIC-mode coverage |
| [#24845](https://github.com/sonic-net/sonic-mgmt/pull/24845) | New test suite | Med | Yes | none | Low (24545) | none | Req changes | Live CodeQL regex warnings; `acl.json` action/value mismatch; slow/flaky-prone |
| [#24876](https://github.com/sonic-net/sonic-mgmt/pull/24876) | Bug fix (flake) | Low | Yes | ZhaohuiS, prhoskot | Low | none | Approve | Comment/code mismatch on stability gate (cosmetic) |
| [#24884](https://github.com/sonic-net/sonic-mgmt/pull/24884) | Test improvement | Low | Yes | none | Low | none | 2nd opinion | Redis `save` restore edge case; 1s→5s poll coarsens convergence resolution globally |
| [#24902](https://github.com/sonic-net/sonic-mgmt/pull/24902) | Bug fix | Low | Yes | none | Low | none | 2nd opinion | Changes shared `wait_until` semantics (fast-fail → retry); title typo |
| [#24927](https://github.com/sonic-net/sonic-mgmt/pull/24927) | Bug fix | Low | Yes | nhe-NV, yyynini | Low | none | Approve | Fixture swap changes DUT-enumeration for all topologies; unguarded VLAN index |
| [#24930](https://github.com/sonic-net/sonic-mgmt/pull/24930) | Test improvement | Low | Yes | none | Low | none | Approve | Author affiliation **unknown**; `/tmp/{file}` path assumption in cleanup |
| [#24975](https://github.com/sonic-net/sonic-mgmt/pull/24975) | Bug fix | Low | Yes | nhe-NV | Low | none | Approve | Fixed 3s pause is a timing band-aid (vs readiness wait); low risk |
| [#25000](https://github.com/sonic-net/sonic-mgmt/pull/25000) | Bug fix | Low | Yes | none | Low | none | Approve | Sibling `test_srv6_dataplane.py` arguably needs same fix, not included |
| [#25012](https://github.com/sonic-net/sonic-mgmt/pull/25012) | Bug fix | Med | Yes | liamkearney-msft | Low | none | Approve | Clean; minor wait_until timeout doc/code drift (50 vs 120) |
| [#25040](https://github.com/sonic-net/sonic-mgmt/pull/25040) | Bug fix (flake) | Med | Yes | shixizhang | Low | none (25094 same marker, diff file) | Approve | Confirm `get_bbr_default_state`/`safe_remove_aggregate` pre-exist |
| [#25094](https://github.com/sonic-net/sonic-mgmt/pull/25094) | Test improvement | Low | Yes | nhe-NV | Low | none | Approve | Author affiliation **unknown**; clean idiomatic change |
| [#25123](https://github.com/sonic-net/sonic-mgmt/pull/25123) | Bug fix | Med | Yes | none | Low | none | 2nd opinion | Intentional syslog-sampling sensitivity trade-off (sign-off needed); hardcoded platform string |
| [#25134](https://github.com/sonic-net/sonic-mgmt/pull/25134) | Bug fix (enable) | Low | Yes | none | Low | none | Approve | Re-enables a previously-skipped test — flake risk in gating |

**Patterns:** 20/21 match their description (only #24320 is Partial — scope
creep). Only one file-overlap pair in the set: **#24545 ↔ #24845** (both touch
`tests_mark_conditions.yaml`, in different regions → trivial textual merge at
worst). No duplicates detected. Closest-to-merge (approved + clean + green):
#24437, #24493, #24545, #24597, #24876, #24927, #24975, #25012, #25040, #25094.

---

## Linked issues & close-on-merge (Rule 6)

Issue references found in the eligible PRs, with API-resolved type/state and the
close disposition. GitHub only auto-closes **same-repo issues with a closing
keyword** merged to the default branch; everything else needs a **manual close**
when we merge.

| PR | Reference | Type | Keyword? | Disposition on merge |
|----|-----------|------|----------|----------------------|
| [#24902](https://github.com/sonic-net/sonic-mgmt/pull/24902) | sonic-net/sonic-mgmt#24726 | issue (open) | `Fixes` ✓ | **Auto-closes** (GitHub handles) |
| [#25134](https://github.com/sonic-net/sonic-mgmt/pull/25134) | sonic-net/sonic-buildimage#25768 | issue (open) | `Fixes` ✓ | **MANUAL** — cross-repo, won't auto-close |
| [#25012](https://github.com/sonic-net/sonic-mgmt/pull/25012) | sonic-net/sonic-mgmt#25013 | issue (open) | none | **MANUAL** — no closing keyword |
| [#24320](https://github.com/sonic-net/sonic-mgmt/pull/24320) | sonic-net/sonic-mgmt#23585 | issue (open) | none | **MANUAL** — no keyword (verify it actually fixes it) |
| [#24545](https://github.com/sonic-net/sonic-mgmt/pull/24545) | sonic-net/sonic-mgmt#21889 | **PR** (closed) | none | track-only (not an issue) |
| [#24829](https://github.com/sonic-net/sonic-mgmt/pull/24829) | sonic-net/sonic-mgmt#22166 | **PR** (closed) | none | track-only (not an issue) |
| [#24845](https://github.com/sonic-net/sonic-mgmt/pull/24845) | sonic-net/sonic#1958 | **PR** (closed, HLD) | none | track-only (not an issue) |

The other 14 eligible PRs reference no issue. **Action when we eventually merge:**
manually close #25768 (on sonic-buildimage), #25013, and #23585 (if #24320 is
merged as its fix) — `sweep.py --close-issues <PR> --apply` does this and logs
an `issue_close` ledger entry. #24902's issue will close itself.

---

## Briefs

### [PR #23930](https://github.com/sonic-net/sonic-mgmt/pull/23930) — Update variables
- **Author / affiliation:** SaiYasaswiniP / Juniper Networks
- **Type:** Feature enhancement (testbed/framework — new hwsku registration)
- **Complexity:** Low — single file, +2/-2, appends one hwsku string to two existing lists in `ansible/group_vars/sonic/variables`. Shared variables file but purely additive.
- **Description summary:** Adds the Juniper Broadcom-based hwsku `Juniper-QFX5241-64-OD` to the testbed's Broadcom hwsku registries so the platform is recognized. Title/description are minimal.
- **Existing reviews/comments:** No formal reviews. EasyCLA signed. yxieca asked about a pre-test failure (author: unrelated pytest_cache permission error). vmittal-msft asked the author to add a master PR and make the title/description more descriptive — not yet addressed.
- **Matches description?:** Yes — adds the hwsku to `broadcom_hwskus` and `broadcom_th5_hwskus`. No scope creep.
- **Conflict likelihood:** Low — file-isolated.
- **Duplication likelihood:** none seen.
- **Reviewer notes:** Additive and self-consistent; the author is from Juniper registering a Juniper hwsku, so the chip-generation classification is theirs to make — defer to them on it. The only open items are process: vmittal-msft asked for a descriptive title and a companion master PR.
- **Suggested recommendation:** Approve — additive vendor hwsku from the vendor; only the title/master-PR process items remain

### [PR #24320](https://github.com/sonic-net/sonic-mgmt/pull/24320) — changes for port speed test enhancement
- **Author / affiliation:** rawal01 / Nokia
- **Type:** Mix — test refactor + several incidental bug fixes
- **Complexity:** Medium-High — single file, +257/-111, near-total rewrite of fixture/DUT-selection logic + multi-ASIC plumbing; confined to one test.
- **Description summary:** Enhances `test_port_speed_change` to cover both downgrade and upgrade (was one direction) via parametrization, reworks DUT/port selection, decouples traffic-source DUT from the test DUT, adds multi-ASIC namespace context.
- **Existing reviews/comments:** yejianquan (COMMENTED, non-blocking) credited real bug fixes and asked for test results + inline comments. anamehra asked about testbed setup. abdosi: master approach will move to no-patch-cleanup; 202405 needs a separate testcase.
- **Matches description?:** **Partial** — parametrization/bidirectional coverage + DUT-selection rework match intent, but the diff also contains undisclosed changes (ACL enumeration from config_facts, `/localhost/` patch removal, wholesale PORT object replace, BUFFER_QUEUE cleanup, new split-patch `No.1b` flow). Real fixes but scope creep vs the description.
- **Conflict likelihood:** Low — file-isolated.
- **Duplication likelihood:** none seen.
- **Reviewer notes:** abdosi flagged the master approach is still evolving → may be partially superseded; confirm direction. Wholesale PORT replace + split-patch ordering are the riskiest changes; requested test results not yet posted.
- **Suggested recommendation:** Request changes / get another opinion — Partial match + undisclosed scope creep; abdosi indicates the approach may be superseded — split it and confirm direction

### [PR #24437](https://github.com/sonic-net/sonic-mgmt/pull/24437) — save pfcwd_timer_accuracy test result to file
- **Author / affiliation:** wenjwang-nv / NVIDIA
- **Type:** Feature enhancement (test instrumentation / diagnostics)
- **Complexity:** Low — +56/-1 across 2 files; opt-in CLI flag + fixture + helper; conftest touch is purely additive.
- **Description summary:** Adds an opt-in `--save-timer-results` option that writes pfcwd timer-accuracy metrics to a JSON file under `/tmp` for trend analysis. Default off, existing behavior unchanged.
- **Existing reviews/comments:** nhe-NV reviewed then APPROVED. No unresolved concerns.
- **Matches description?:** Yes — exactly the described option/fixture/writer. No scope creep.
- **Conflict likelihood:** Low — file-isolated.
- **Duplication likelihood:** none seen.
- **Reviewer notes:** Minor non-blocking: hardcoded `/tmp` path; `test_func_name` param is always the literal test name (redundant). Already approved by an NVIDIA reviewer.
- **Suggested recommendation:** Approve — clean opt-in instrumentation, already approved by nhe-NV

### [PR #24493](https://github.com/sonic-net/sonic-mgmt/pull/24493) — Update the gNMI setup without authentication for liquid cooling case
- **Author / affiliation:** JibinBao / NVIDIA
- **Type:** Bug fix
- **Complexity:** Low — single helper file, +2/-10, narrow blast radius.
- **Description summary:** Simplifies liquid-cooling gNMI setup by skipping gNMI auth: adds `-n` (no-auth) to the `py_gnmicli.py` subscribe call and removes client-cert/`client_auth true` setup, so the test only verifies events are received. Claims auth coverage remains via other suites.
- **Existing reviews/comments:** nhe-NV — APPROVED (no comment).
- **Matches description?:** Yes — adds `-n`, deletes cert HSETs + `client_auth true`, updates docstring; coherent with no-auth.
- **Conflict likelihood:** Low — file-isolated.
- **Duplication likelihood:** none seen.
- **Reviewer notes:** Clean. Human may confirm the claim that auth coverage is preserved in `test_gnmi.py` (not verifiable from this diff).
- **Suggested recommendation:** Approve — narrow, coherent no-auth change, approved by nhe-NV

### [PR #24545](https://github.com/sonic-net/sonic-mgmt/pull/24545) — Fix test_monitoring_critical_processes timeout by killing database container last
- **Author / affiliation:** xwjiang-ms / Microsoft
- **Type:** Bug fix
- **Complexity:** Medium — 2 files, +164/-45; logic rewrite of one test + recovery fixture; touches shared `tests_mark_conditions.yaml` (one stanza deleted).
- **Description summary:** PR #21889 added `database` to the critical-process kill list; alphabetical iteration kills it early, redis death hangs subsequent SSH → external timeout (0 passes in 365 days). Fix splits into two phases (kill non-database first with loganalyzer verify, then database last, skip syslog verify, let recovery fixture reboot) and removes the obsolete xfail/skip YAML entry.
- **Existing reviews/comments:** StormLiangMS (approved after 5 substantive + 4 nits addressed); ZhaohuiS (positive); lipxu raised per-ASIC `database0/1` containers (now handled via `re.fullmatch(r"database(\d+)?")`); author self-flagged a multi-ASIC VS SysRq timing race; yxieca AI note on skip/xfail logic.
- **Matches description?:** Yes — two-phase kill + YAML removal + database-last recovery. Undisclosed-but-reasonable extras: KVM→`is_vs_device` broadening, multi/single-ASIC SysRq handling, new `database_config.json`-wait + `config_reload` recovery.
- **Conflict likelihood:** Med — shares `tests_mark_conditions.yaml` with #24845 in non-overlapping regions → textual rebase at worst, no semantic conflict.
- **Duplication likelihood:** none seen.
- **Reviewer notes:** (1) Multi-ASIC VS recovery hinges on a fixed `MULTI_ASIC_VS_REBOOT_DELAY_SEC=15` pre-scheduled SysRq — confirm robust on slow/loaded VS. (2) Recovery now waits for `database_config.json` + `config_reload(wait_for_bgp=True)` instead of verifying interfaces up — a real reduction in post-recovery assertion; conscious sign-off.
- **Suggested recommendation:** Approve — fixes a 365-day-dead test; substantive feedback addressed and two approvals — note the VS timing assumption

### [PR #24597](https://github.com/sonic-net/sonic-mgmt/pull/24597) — Update the fanout switch deploy step due to lack of /etc/sysctl.conf
- **Author / affiliation:** echuawu / NVIDIA (Nvidia Networking)
- **Type:** Bug fix
- **Complexity:** Medium — 2 files, +215/-1, mostly a new 204-line task file copied from the 202505 flow; touches the shared `fanout` role dispatcher.
- **Description summary:** SONiC 202511 images no longer ship `/etc/sysctl.conf` (IPv6-disable config moved to `/usr/lib/sysctl.d/90-sonic.conf`), so the existing IPv6 step fails during fanout deploy. Adds `fanout_sonic_202511.yml` targeting the new path and wires it via a `'202511' in build_version` branch.
- **Existing reviews/comments:** nhe-NV — APPROVED. yxieca non-blocking AI note (false-positive skip/disable trigger).
- **Matches description?:** Yes — sysctl path fix present. Undisclosed-but-required extra: dispatcher guard tightened `'2025'`→`'202505'` so 202511 doesn't also match 202505.
- **Conflict likelihood:** Low — file-isolated (new file + 1-line dispatcher edit).
- **Duplication likelihood:** none seen.
- **Reviewer notes:** Confirm (1) the new file references template `sonic_deploy_202505.j2` (carried over) is intentional, not a stale name; (2) the IPv6 block runs only for asic_type in `[marvell-teralynx, mellanox, broadcom]` — other 202511 fanout asics silently skip IPv6 disabling.
- **Suggested recommendation:** Approve — correct sysctl-path fix, approved; just confirm the carried-over template name

### [PR #24787](https://github.com/sonic-net/sonic-mgmt/pull/24787) — [platform_tests][T2] Add test_sup_fan_recovery.py
- **Author / affiliation:** aeedara-nokia / Nokia
- **Type:** New test suite (single new T2 chassis regression test)
- **Complexity:** Low–Medium — one new self-contained file (+196/-0); no shared-lib edits. Medium-ish because it does a destructive minigraph override-reload + cold reboot.
- **Description summary:** Adds `test_sup_fan_status_after_reload_reboot` iterating supervisor nodes: snapshots `/var/core`, arms a LogAnalyzer for the thermalctld bug signature, minigraph override-reload, asserts fans OK, cold-reboots, re-asserts, checks no new cores. Targets a thermalctld/psu regression where fans returned `Not present`.
- **Existing reviews/comments:** None substantive — only EasyCLA. No human review.
- **Matches description?:** Yes — every described step implemented; VS skip + missing-minigraph skip are disclosed extras.
- **Conflict likelihood:** Low — file-isolated.
- **Duplication likelihood:** none seen.
- **Reviewer notes:** (1) `_all_fans_ok` calls `verify_show_platform_fan_output` which asserts internally — if it asserts on malformed output, `wait_until` may not retry cleanly. (2) Destructive (override-reload + cold reboot of a chassis sup), recovery leans on `reboot_and_check`; no `Fixes #` link.
- **Suggested recommendation:** Get another opinion — new destructive T2 chassis test with no human review yet — wants a platform/T2 SME; add a Fixes link

### [PR #24829](https://github.com/sonic-net/sonic-mgmt/pull/24829) — Fix: add port name for acl interface parsing
- **Author / affiliation:** ytzur1 / NVIDIA
- **Type:** Bug fix
- **Complexity:** Low — 2 added lines in `ansible/library/minigraph_facts.py` (a widely-used shared Ansible fact lib, so non-trivial blast radius despite the tiny change).
- **Description summary:** PR #22166 made `minigraph_dpg.j2` put interface names (not aliases) in ACL `AttachTo` on non-multi-ASIC setups; the parser only matched aliases → empty `acl_intfs`/`minigraph_acls` → KeyError on `mg_facts["minigraph_acls"]["DataAcl"]`. Adds an `elif member in ports` fallback.
- **Existing reviews/comments:** None (REVIEW_REQUIRED).
- **Matches description?:** Yes — exactly the described fallback after the alias branch.
- **Conflict likelihood:** Low — file-isolated.
- **Duplication likelihood:** none seen.
- **Reviewer notes:** Additive (can't regress existing matches). Confirm `ports` is in scope/populated at that point; change is unconditional (not ASIC-mode gated) — likely fine as a last-resort fallback. No test added (author validated via internal regression).
- **Suggested recommendation:** Approve — minimal additive last-resort fallback; low regression risk (a test would be nice-to-have)

### [PR #24845](https://github.com/sonic-net/sonic-mgmt/pull/24845) — ARS test script
- **Author / affiliation:** apannerselva / Marvell Technology
- **Type:** New test suite
- **Complexity:** Medium — 7 files, +797/-1; new `tests/ecmp/ars/` package + ptf script; only shared touch is an additive block in `tests_mark_conditions.yaml`.
- **Description summary:** New ARS (Adaptive Routing and Switching) suite implementing the ARS HLD test plan (SONiC#1958): per-packet/per-flowlet load balancing across NHG selector modes, an ACL "disable ARS" action, non-ARS behavior, and a stress test, with a new ptf dataplane test. T0-only, gated to Marvell-teralynx.
- **Existing reviews/comments:** github-advanced-security[bot] raised many CodeQL findings (unused imports, two "unmatchable caret/dollar" regex warnings). radha-danda triggered `/azpw run`; author pinged reviewers. No human approval.
- **Matches description?:** Yes — the 10 parametrized cases + marvell-teralynx gating match. Caveats: diff appears out of sync with some CodeQL-flagged symbols (post-scan cleanup), but unmatchable-regex findings still apply; `acl.json` defines action `DISABLE_ARS_FORWARDING` then sets it to `"DROP"` — looks semantically off.
- **Conflict likelihood:** Low — additive overlap with #24545 only (different region of the yaml).
- **Duplication likelihood:** none seen.
- **Reviewer notes:** Needs a human pass: fix the live CodeQL regex warnings, confirm the `acl.json` action/value mismatch, verify unused-import findings actually resolved. Heavy `time.sleep` + full `config_reload` per case → slow/flaky-prone.
- **Suggested recommendation:** Request changes — new suite with live CodeQL regex warnings and an acl.json action/value mismatch to resolve first

### [PR #24876](https://github.com/sonic-net/sonic-mgmt/pull/24876) — lldp_syncd failure due to not enough converge time
- **Author / affiliation:** Yogapriya-cisco / Cisco
- **Type:** Bug fix (test stabilization / flake fix)
- **Complexity:** Low — single file, +57/-0, one module-scoped autouse fixture; no shared-lib changes.
- **Description summary:** Adds `wait_for_lldp_appl_db` autouse fixture that polls `lldpctl` until the neighbor set is stable, then waits for APPL_DB `LLDP_ENTRY_TABLE` to cover it — stopping intermittent flakes from `lldpd`/APPL_DB still converging after a prior test's config reload.
- **Existing reviews/comments:** ZhaohuiS — APPROVED (asked about t0/t1; author confirmed t0). prhoskot — APPROVED. vrajeshe pinged for merge.
- **Matches description?:** Yes — two-phase stabilization; all helpers already exist.
- **Conflict likelihood:** Low — file-isolated.
- **Duplication likelihood:** none seen.
- **Reviewer notes:** Cosmetic nit: stability gate uses `stable_count > 2` (≈4 identical reads), more conservative than the "2 consecutive polls" the comment claims. Two approvals; sound flake fix.
- **Suggested recommendation:** Approve — sound flake fix with two approvals; only a cosmetic comment/code nit

### [PR #24884](https://github.com/sonic-net/sonic-mgmt/pull/24884) — [bgp scale] Reduce DUT-side observer load during route convergence tests
- **Author / affiliation:** yutongzhang-microsoft / Microsoft
- **Type:** Test improvement (measurement-fidelity tuning)
- **Complexity:** Low — single test file, +82/-4; no shared-lib touch, but an autouse fixture mutates live DUT state (stops `openbmpd`, disables redis RDB) so teardown/restore matters.
- **Description summary:** Profiling showed ~35% of DUT OnCPU during `test_sessions_flapping[500]` came from `openbmpd` + `redis-check-rdb` — observer noise inflating convergence numbers. Adds a fixture to stop openbmpd + disable redis saves (restored after), raises poll interval 1s→5s, caps sairedis-log reads at last 100MB, memoizes `_get_backplane_ports`.
- **Existing reviews/comments:** None.
- **Matches description?:** Yes — all four changes faithful, with save/restore guards (`module_ignore_errors=True`).
- **Conflict likelihood:** Low — file-isolated (sibling #25040 touches different bgp files).
- **Duplication likelihood:** none seen.
- **Reviewer notes:** (1) Redis `save` restore relies on `config get save` formatting; if it differs or has <2 lines, the original is silently left disabled. (2) 1s→5s coarsens convergence resolution 5× for *all* callers, not just the [500] case — confirm acceptable for sub-5s measurements.
- **Suggested recommendation:** Get another opinion — the 1s→5s poll change coarsens convergence resolution for ALL callers — wants a scale-test owner's eye

### [PR #24902](https://github.com/sonic-net/sonic-mgmt/pull/24902) — Handle pytest.fail.Exeption in wait_until
- **Author / affiliation:** wrideout-arista / Arista
- **Type:** Bug fix
- **Complexity:** Low — one-line change (+1/-1) in shared `tests/common/utilities.py`; narrow change but broad blast radius (`wait_until` is used everywhere).
- **Description summary:** `wait_until` catches `Exception`, but `pytest.fail()` raises `pytest.fail.Exception` (a `BaseException` subclass) which escapes the handler → immediate failure instead of retry. Adds `pytest.fail.Exception` to the `except` tuple. Fixes #24726.
- **Existing reviews/comments:** No formal reviews; author pinged wangxin/lolyu/yutongzhang-microsoft.
- **Matches description?:** Yes — exactly the widened `except`; rationale technically accurate (`pytest` already imported).
- **Conflict likelihood:** Low — file-isolated.
- **Duplication likelihood:** none seen.
- **Reviewer notes:** Behavioral nuance: a `pytest_assert`/`pytest.fail` inside a condition is now swallowed and retried to timeout — intended, but any call site relying on fast-fail changes behavior. Title typo ("Exeption").
- **Suggested recommendation:** Get another opinion — one-line fix but changes shared wait_until semantics repo-wide; have a common-infra maintainer confirm

### [PR #24927](https://github.com/sonic-net/sonic-mgmt/pull/24927) — Fix test_link_local_ip failures in dualtor active-active topology
- **Author / affiliation:** xixuej / NVIDIA (nvidia-sonic)
- **Type:** Bug fix
- **Complexity:** Low — single test file, +25/-11; no shared-lib touch.
- **Description summary:** Fixes `test_link_local_ip` failures on dualtor active-active after `SAI_NOT_DROP_SIP_DIP_LINK_LOCAL=1` was added. (1) Downlink ingress used global router MAC instead of shared VLAN MAC (dropped) → new `get_downlink_router_mac()` from config_facts; (2) adds the `dualtor_active_active_setup_standby_on_random_unselected_tor` marker and switches DUT-selection fixture to `rand_one_dut_hostname`.
- **Existing reviews/comments:** nhe-NV — APPROVED; yyynini — APPROVED ("lgtm").
- **Matches description?:** Yes — per-direction `router_mac` plumbed through; marker + fixture swap present.
- **Conflict likelihood:** Low — file-isolated.
- **Duplication likelihood:** none seen.
- **Reviewer notes:** (1) Fixture swap changes DUT-enumeration semantics for *all* topologies (test is `topology('any')`); sanity-check non-dualtor coverage. (2) `get_downlink_router_mac` indexes `config_facts['VLAN'][vlan_interface]` unguarded — KeyError possible in an unlikely config state. Double-approved.
- **Suggested recommendation:** Approve — faithful dualtor-aa fix, double-approved; note the all-topology fixture swap

### [PR #24930](https://github.com/sonic-net/sonic-mgmt/pull/24930) — [vxlan] Improve vnet bgp subintf cleanup diagnostics
- **Author / affiliation:** yyynini / **unknown** (profile name "Yawen"; no company/email; appears as approver on NVIDIA PRs #24927/#24876 → possible NVIDIA association, unconfirmed)
- **Type:** Test improvement (diagnostics + cleanup hardening)
- **Complexity:** Low — single test file, +78/-37; no shared-lib touch.
- **Description summary:** Adds bounded DUT-state diagnostic logging when the WL→T1 VXLAN encap verification fails, and refactors `cleanup()` into independent named phases so one failing phase doesn't abort the rest. Explicitly does not change dataplane expectations/timeout/topology/skip.
- **Existing reviews/comments:** None.
- **Matches description?:** Yes — `dump_encap_failure_diagnostics()` wraps verify in try/except, dumps the listed commands, re-raises; `cleanup()` split into `cleanup_step`-wrapped phases. Minor reasonable extras: backup-existence guard before `mv`, `mv -f`, `continue_on_fail`/`module_ignore_errors` on ptf shell cmds, `rm -f /tmp/{file}` on ptfhost.
- **Conflict likelihood:** Low — file-isolated.
- **Duplication likelihood:** none seen.
- **Reviewer notes:** (1) New `remove_temp_files` prefixes `/tmp/` to entries that may be full local paths — could target wrong path on PTF host; confirm what `temp_files` holds. (2) `cleanup_step` swallows per-phase exceptions by design (reduces signal if cleanup silently breaks).
- **Suggested recommendation:** Approve — behavior-preserving diagnostics/cleanup hardening; only confirm the temp-file path assumption

### [PR #24975](https://github.com/sonic-net/sonic-mgmt/pull/24975) — Fix the NTP polling step in deploy-mg playbook
- **Author / affiliation:** congh-nvidia / NVIDIA
- **Type:** Bug fix
- **Complexity:** Low — 1 file, +4/-0; a single inserted Ansible `pause` task.
- **Description summary:** `chronyc burst 4/4` right after a chrony restart can fail on slow platforms (e.g. SN2700-a0) because chrony isn't ready. Inserts a 3s `pause` before the forced-NTP-polling step.
- **Existing reviews/comments:** nhe-NV — APPROVED.
- **Matches description?:** Yes — exactly one `pause: seconds: 3` before the `chronyc burst` task.
- **Conflict likelihood:** Low — file-isolated.
- **Duplication likelihood:** none seen.
- **Reviewer notes:** Clean. A fixed 3s pause is a band-aid vs a `wait_for` readiness loop, but low-risk and approved.
- **Suggested recommendation:** Approve — small low-risk timing fix, approved by nhe-NV

### [PR #25000](https://github.com/sonic-net/sonic-mgmt/pull/25000) — Fix test_srv6_vlan_forwarding when no ipv6 mgmt for ptf docker
- **Author / affiliation:** ytzur1 / NVIDIA
- **Type:** Bug fix
- **Complexity:** Low — single test file, +6/-4, same fallback in three spots.
- **Description summary:** When the PTF docker has no IPv6 mgmt address, `ptfhost.mgmt_ipv6` is falsy and the test builds packets with an invalid source IP. Adds `ptf_mgmt_ipv6 = ptfhost.mgmt_ipv6 if ptfhost.mgmt_ipv6 else "1000::1"` used as `ipv6_src` in both packet builders. Targets 202605.
- **Existing reviews/comments:** None.
- **Matches description?:** Yes. Scope note: description says the same applies to `test_srv6_dataplane.py`, which is not included here.
- **Conflict likelihood:** Low — file-isolated.
- **Duplication likelihood:** none seen.
- **Reviewer notes:** (1) Confirm hardcoded `"1000::1"` is a valid non-conflicting source for the dataplane assertions. (2) Consider shipping the `test_srv6_dataplane.py` fix together per the author's own description.
- **Suggested recommendation:** Approve — correct fallback; optionally fold in the sibling test_srv6_dataplane.py fix the author mentions

### [PR #25012](https://github.com/sonic-net/sonic-mgmt/pull/25012) — Fixing PMON status test failures
- **Author / affiliation:** caleb-nexthop / NextHop
- **Type:** Bug fix
- **Complexity:** Medium — 7 files, +35/-55, localized to `tests/platform_tests/daemon/`. New module-scoped `conftest.py` (shared fixtures) consumed by 6 daemon modules.
- **Description summary:** PMON term/kill tests fail under `run_optimal` because `auto_restart=enabled` restarts the container and resets PIDs, breaking `post_pid > pre_pid`. Adds a shared fixture to disable pmon container autorestart (restored on teardown), consolidates per-module `check_daemon_status`, and swaps a `time.sleep(10)` for `wait_until(...)` in test_pcied.
- **Existing reviews/comments:** github-advanced-security (automated, empty body); liamkearney-msft (APPROVED). Author asked if anything blocks merge.
- **Matches description?:** Yes — new conftest with both fixtures, 6 modules drop duplicated fixture, per-module host overrides added, `time.sleep(10)`→`wait_until(120,10,0,...)`. Minor doc/code drift (desc says `wait_until(50,...)`).
- **Conflict likelihood:** Low — file-isolated.
- **Duplication likelihood:** none seen (references #24384 as the wait_until precedent).
- **Reviewer notes:** Clean, well-scoped. Confirm the module-scoped autorestart teardown ordering is fine for modules that previously had no autorestart handling. Note timeout discrepancy (50 vs 120).
- **Suggested recommendation:** Approve — clean, well-scoped consolidation, approved by liamkearney-msft

### [PR #25040](https://github.com/sonic-net/sonic-mgmt/pull/25040) — [bgp/agg] Make BGP aggregate-address tests solid against per-DUT flakiness
- **Author / affiliation:** nanali-msft / Microsoft
- **Type:** Bug fix (test-reliability)
- **Complexity:** Medium — 4 files, +111/-32, confined to the bgp aggregate suite (1 shared helper module + 3 test modules).
- **Description summary:** Hardens the suite against per-DUT flakiness: makes route verification origin-aware (filter M2 paths by the DUT's own ASN), forces a deterministic disabled→enabled BBR transition instead of trusting ambient state, and exempts the stress module from the memory-utilization monitor.
- **Existing reviews/comments:** shixizhang — APPROVED.
- **Matches description?:** Yes — `expected_asn` plumbed through with EOS/FRR token matching; BBR forced-transition with try/finally restore; `disable_memory_utilization` mark; baseline `safe_remove_aggregate` + expected-absent precheck.
- **Conflict likelihood:** Low — files isolated to bgp aggregate suite.
- **Duplication likelihood:** none seen (#25094 uses the same `disable_memory_utilization` marker on a different file — same pattern, not a dup).
- **Reviewer notes:** Verify `get_bbr_default_state` and `safe_remove_aggregate` already exist in the helper module (used but not defined in this diff) or imports break.
- **Suggested recommendation:** Approve — faithful flakiness hardening, approved; just verify the two helpers pre-exist

### [PR #25094](https://github.com/sonic-net/sonic-mgmt/pull/25094) — Add disable_memory_utilization option for fwutil test cases
- **Author / affiliation:** zypgithub / **unknown** (profile company empty; display name "Yanpeng Zhang")
- **Type:** Test improvement (test-infra marker)
- **Complexity:** Low — 1 file, +2/-1, a single `pytestmark` entry.
- **Description summary:** fwutil tests reboot the DUT, making the before/after memory-utilization plugin produce false failures. Adds `pytest.mark.disable_memory_utilization` to the module's `pytestmark`.
- **Existing reviews/comments:** nhe-NV — APPROVED.
- **Matches description?:** Yes — marker is a real recognized hook; no scope creep.
- **Conflict likelihood:** Low — file-isolated.
- **Duplication likelihood:** none seen (marker reused widely, distinct files).
- **Reviewer notes:** Clean, idiomatic, consistent with other modules using the marker. One maintainer approval. Nothing needing attention.
- **Suggested recommendation:** Approve — clean idiomatic marker, approved by nhe-NV

### [PR #25123](https://github.com/sonic-net/sonic-mgmt/pull/25123) — [TH6] test_po_cleanup fix for large number of lags(100s)
- **Author / affiliation:** sanjair-git / Nokia
- **Type:** Bug fix (labeled "Test case improvement")
- **Complexity:** Medium — single file, +79/-5; adds branching LAG-count logic, syslog sampling heuristics, and a custom BGP-wait path; confined to one test.
- **Description summary:** On TH6/large topologies with 100+ port channels, `test_po_cleanup_after_reload` fails falsely because (1) LogAnalyzer needs a per-LAG SIGTERM line for every LAG and rsyslog drops lines under CPU stress, and (2) the built-in BGP wait is unrealistic while CPUs are pegged. Keeps strict per-LAG matching at ≤64 LAGs; for >64, uses a broad SIGTERM regex + a stratified mandatory sample, then drops stress load before asserting BGP convergence.
- **Existing reviews/comments:** None.
- **Matches description?:** Yes — `LAG_LOG_STRICT_PER_PC_MAX=64` threshold, `stratified_lag_samples_for_syslog`, broad SIGTERM pattern, `wait_for_bgp=False` + `killall yes` + explicit wait.
- **Conflict likelihood:** Low — file-isolated.
- **Duplication likelihood:** none seen.
- **Reviewer notes:** (1) Author acknowledges a single broken LAG can slip through if not in the sample and its syslog line is dropped — an intentional sensitivity trade-off a maintainer should sign off (the test's purpose is catching missing-SIGTERM regressions). (2) `bgp_wait_seconds_after_config_reload` hardcodes platform `x86_64-nokia_ixr7220_h6_128-r0` and duplicates `config_reload`'s timeout math (will silently drift). No linked issue; `64` is a magic number with no >64-path test evidence shown.
- **Suggested recommendation:** Get another opinion — intentional syslog-sampling sensitivity trade-off weakens the test's core purpose — needs a maintainer sign-off; also a hardcoded platform string

### [PR #25134](https://github.com/sonic-net/sonic-mgmt/pull/25134) — [conditional_mark]: Enable NTP IPv6-only management test on sonic-vpp
- **Author / affiliation:** lunyue-ms / Microsoft
- **Type:** Bug fix (test-enablement — removes a stale skip)
- **Complexity:** Low — single file, 0 add / 11 del; removes a YAML skip block + an empty section header.
- **Description summary:** Removes the stale VPP conditional skip for `ip/test_mgmt_ipv6_only.py::test_ntp_ipv6_only` (placeholder reason "Failed/Errored: To be included"). The test has no VPP-specific skip logic and now passes on the SONiC-VPP KVM testbed, so the skip needlessly excluded IPv6-only NTP coverage.
- **Existing reviews/comments:** None.
- **Matches description?:** Yes — exactly the deletion of the skip block + orphaned header.
- **Conflict likelihood:** Low — file-isolated (other conditional_mark PRs touch a different file).
- **Duplication likelihood:** none seen.
- **Reviewer notes:** Links `Fixes sonic-net/sonic-buildimage#25768` but verification is a single local pass on `vlab-vpp-01` — re-enabling a previously-skipped test risks re-introducing flakiness in gating if it isn't stable across runs.
- **Suggested recommendation:** Approve — low-risk re-enable of skipped coverage; watch for gating flakiness after merge
