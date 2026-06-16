# Deep-review findings — sonic-net/sonic-mgmt

**PRs awaiting our action**, sorted by recommendation — each links to its full brief (click → read → back → next). A PR drops off this doc once it's **approved/merged** or **handed back to the author** (changes/info/evidence requested, conflicting, COI-waiting); full state + history live in `actions.jsonl` + git. Recommendations fold in: does the diff match the description, complexity, **author trust** (§8.1), and **whether CI actually runs the test** (a green check on a skipped test proves nothing — see CI column). _Decision support; approval is the human reviewer's call._

**Tally:** Approve: 6 · Request changes: 2 · Get another opinion: 2 · Hold (your call): 1 · Blocked (COI): 1
_(Third sweep 2026-06-16: re-evaluation cleared three handed-off PRs — **#24975** (our change-request satisfied + nhe-NV approved) and **#25000** (passing-run evidence + yaopingz approved) are now **ready for your approve+merge**; **#24829**'s evidence is a pdb dump with no independent approval → **held for your call**. #25012 merged upstream (off-doc). Mechanical: 5 `ci_fail_notify` posted (Rule 3/5); 6 already-notified failing PRs were correctly **suppressed** after a tool idempotency fix (re-notify now keys off the failing-run timestamp per POLICY §3, not a wall-clock cooldown). Author/reviewer-ball (off-doc): #24247, #24367, #20456, #24913, #24802, #21144, #24902-followups.)_

## Recommendations

| PR | Title | Author / Trust | CI runs test? | ➡ Recommendation |
|----|-------|----------------|---------------|------------------|
| [#24975](#pr-24975) | Fix the NTP polling step in deploy-mg playbook | congh-nvidia / Expert | Indirect (deploy) | **Approve — ready** — our CR satisfied (poll-for-readiness) + nhe-NV approved; awaiting your approve+merge |
| [#25000](#pr-25000) | Fix test_srv6_vlan_forwarding when no ipv6 mgmt | ytzur1 / High | No (srv6 vs-skip) | **Approve — ready** — passing-run evidence + yaopingz approved; awaiting your approve+merge |
| [#24217](#pr-24217) | Add xfail for HeadroomPool probe on SPC1/SPC3 | XuChen-MSFT / Expert | N-A (mark yaml) | **Approve** — issue-gated xfail (#24558 open), narrowly scoped |
| [#24091](#pr-24091) | Add confed config to topo_t2_single_node_max_64p | YatishSVC / High | N-A (topo data) | **Approve** — confed config consistent across both files; threads resolved |
| [#21429](#pr-21429) | Add mgmtd set-src regression coverage | Bojun-Feng / Low | Yes (t0/t1/t2) | **Approve** — all 7 reviewer points resolved; refresh stale description |
| [#23542](#pr-23542) | Fix missing upstream ports in ACL (mixed LAG/non-LAG) | ccroy-arista / High | Partial (gate no-op) | **Approve** — small correct fix; author validated on mixed topo |
| [#24591](#pr-24591) | Fanout ingress ACL to block L2 noise (headroom pool) | XuChen-MSFT / Expert | No (hw fanout) | **Request changes** — open yxieca CR + CodeQL empty-except at HEAD |
| [#17940](#pr-17940) | Add generate_hosts script | Pterosaur / Expert | N-A (script) | **Request changes** — wangxin CR + 16 open inline issues, 3mo stale |
| [#24902](#pr-24902) | Handle pytest.fail.Exception in wait_until | wrideout-arista / High | Partial (shared helper) | **Get another opinion** — anders found 4 silent-no-op sites; awaiting @wangxin/@lolyu |
| [#23283](#pr-23283) | Prevent cascading qos_sai failures after fixture error | darius-nexthop / Medium | Partial (off-gate) | **Get another opinion (COI)** — open ZhaohuiS concern; NextHop can't self-approve |
| [#24829](#pr-24829) | Fix: add port name for acl interface parsing | ytzur1 / High | No (alias==name on gate) | **Hold (your call)** — evidence is a pdb dump, no independent approval |
| [#23346](#pr-23346) | SONiC BMC Redfish API and D-Bus test plan | chinmoy-nexthop / Unproven | N-A (doc) | **Blocked (COI)** — NextHop test plan; needs non-NextHop approval |

---

## Briefs

_Ordered by recommendation, same as above._

<a id="pr-24975"></a>

### [PR #24975](https://github.com/sonic-net/sonic-mgmt/pull/24975) — Fix the NTP polling step in deploy-mg playbook
- **Author / affiliation / trust:** congh-nvidia (Cong Hou) / NVIDIA / Expert (merged PRs=100, top-company rank #2)
- **➡ Recommendation:** **Approve — ready (re-eval cleared)** — our 2026-06-10 change-request (the added `pause: seconds: 3` was a racy fixed sleep) is **fully addressed**: congh replaced it with a readiness-gated retry on the burst itself (`chronyc burst 4/4` with `until: chrony_burst_result.rc == 0`, `retries: 3`, `delay: 2`, `changed_when: false`) — exactly the poll-don't-sleep fix we proposed (we suggested 5 retries; 3 is acceptable). **nhe-NV (NVIDIA) independently APPROVED (06-13).** CI green, MERGEABLE. Awaiting **your** approve+merge. Backport `Request for 202605` is valid (deploy-time NTP reliability fix, appropriate for a stable branch) → flip to `Approved for 202605 branch` on merge.
- **Type:** Bug fix (test-infra reliability — ansible deploy-mg NTP step).
- **Complexity:** Low — 1 file, +5/-0, `ansible/config_sonic_basedon_testbed.yml`; adds retry/until directives to the existing `chronyc burst` task. No blast radius beyond the deploy-mg NTP step.
- **Description summary:** The NTP polling step could race chronyd not yet being ready; the fix makes the rapid-polling `chronyc burst` resilient by retrying until it succeeds instead of failing or sleeping a fixed interval.
- **Existing reviews/comments:** bhouse-nexthop changes-requested (06-10, racy fixed sleep); congh-nvidia updated, "I have update the change with 3 retries" (06-12); **nhe-NV APPROVED (06-13)**.
- **Matches description?:** Yes — diff is exactly the readiness-gated burst retry.
- **CI actually runs the test?:** Indirect — not a pytest; the `chronyc burst` task runs during testbed deploy-mg (NTP setup). Green CI means the deploy path ran; the fix is judged on the readiness-poll logic (no magic-constant sleep).
- **Linked issue(s):** none (no `Fixes` keyword).
- **Reviewer notes:** Adopts the recommended pattern (poll the real readiness condition, tolerate slow platforms). NVIDIA author + independent NVIDIA maintainer approval → not a COI concern (author is not NextHop).

[↑ back to recommendations](#deep-review-findings--sonic-netsonic-mgmt)

<a id="pr-25000"></a>

### [PR #25000](https://github.com/sonic-net/sonic-mgmt/pull/25000) — Fix test_srv6_vlan_forwarding when no ipv6 mgmt for ptf docker
- **Author / affiliation / trust:** ytzur1 / NVIDIA / High (merged PRs=22, top-company rank #2)
- **➡ Recommendation:** **Approve — ready (re-eval cleared)** — our 2026-06-10 evidence-request (CI doesn't exercise this — `conditional_mark` skips `test_srv6_vlan_forwarding` on any ASIC other than mellanox/broadcom, and the PR-gate is `asic_type=vs`) is **satisfied**: ytzur1 posted a passing run for all four variants (`test_srv6_uN_forwarding_towards_vlan[True/False]`, `test_srv6_uN_no_vlan_flooding[True/False]` → passed) on a real (Arista) testbed, and **yaopingz (Microsoft) independently APPROVED (06-15)**, explaining the mechanism (forcing `1000::1` as the packet `ipv6_src` keeps it out of the expected-packet filter so both cases pass; cites precedent #18609). CI green, MERGEABLE. Awaiting **your** approve+merge. Backport `Request for 202605` valid (test fix) → `Approved for 202605 branch` on merge.
- **Type:** Bug fix (test correctness on testbeds that have ptf ipv6 mgmt).
- **Complexity:** Low — 1 file, +6/-4, `tests/.../srv6/test_srv6_vlan_forwarding.py`; uses `ptfhost.mgmt_ipv6` when available and forces a fixed `ipv6_src`.
- **Description summary:** Fixes `test_srv6_vlan_forwarding` to use `ptf_mgmt_ipv6` when present instead of assuming there is none.
- **Existing reviews/comments:** bhouse-nexthop changes-requested (06-10, CI doesn't run it — share a pass); ytzur1 "added logs of passed tests" (06-14, all 4 variants passed); **yaopingz APPROVED (06-15)** with a non-blocking architectural question (should the testbed SRv6 config be fixed instead of patching test code — they approved anyway, citing #18609).
- **Matches description?:** Yes.
- **CI actually runs the test?:** **No** — `conditional_mark` skips it on the `vs` PR-gate ASIC; confidence comes from the author's passing run on real hardware + yaopingz's independent approval/explanation.
- **Linked issue(s):** none (no `Fixes` keyword).
- **Reviewer notes:** Evidence + independent Microsoft approval cover the CI gap. yaopingz's "fix testbed config vs patch test code everywhere" point is a non-blocking design preference (they approved). NVIDIA author → no COI gate.

[↑ back to recommendations](#deep-review-findings--sonic-netsonic-mgmt)

<a id="pr-24217"></a>

### [PR #24217](https://github.com/sonic-net/sonic-mgmt/pull/24217) — [Probe] Add xfail for HeadroomPool probe test on SPC1 and SPC3
- **Author / affiliation / trust:** XuChen-MSFT / Microsoft / Expert
- **➡ Recommendation:** **Approve** — correctly-scoped, issue-gated xfail (open issue #24558 with real evidence) that auto-deactivates on fix; low risk, established file idioms, affects only two Mellanox SKUs. _Note: SPC3 end-to-end xfail behavior not yet observed on hardware (setup error); diff is trivially correct, failure well-documented for SPC1._
- **Type:** Bug fix (test-masking / xfail mark)
- **Complexity:** Low — 1 file, +6/-0, single `conditional_mark` yaml entry; blast radius limited to `testQosHeadroomPoolProbe` on Mellanox SPC1/SPC3 only.
- **Description summary:** Adds an `xfail` for `qos/test_qos_probe.py::TestQosProbe::testQosHeadroomPoolProbe` on Mellanox SPC1 (`Mellanox-SN2700`) and SPC3 (`Mellanox-SN4600C-C64`). On these platforms the test fails at iteration #2 (all packets to pg=4 ingress-dropped after a successful pg=3 probe), so the probe never finds a PFC threshold. Gated on tracking issue #24558 being open; auto-deactivates when closed.
- **Existing reviews/comments:** none (confirmed empty).
- **Matches description?:** Yes — the 6-line diff adds exactly the described xfail with SPC1+SPC3 condition and issue-#24558 gate; reason text matches body.
- **Conflict likelihood:** Low — file-isolated; new map key. (#24591 same author concerns headroom-pool noise but edits `qos_sai_base.py` — no overlap.)
- **Duplication likelihood:** none seen — consolidates SPC1-only #24215 to also cover SPC3.
- **CI actually runs the test?:** N-A (not a test — `conditional_mark` yaml). Mark is correctly gated: `asic_gen in ['spc1','spc3']` (valid idiom, 27 uses) + the file's "open-issue ⇒ condition true" pattern → applies only on SPC1/SPC3 while #24558 is open; no risk of masking other platforms.
- **Linked issue(s):** #24558 (sonic-mgmt, OPEN, `bug` — the gating issue; correctly NOT auto-closed by merge); #24215 (OPEN, SPC1 history, track-only); #22608 (CLOSED, context, track-only).
- **Reviewer notes:** Well-justified xfail. #24558 is OPEN with detailed raw INGRESS_DROP counter evidence, authored by the same MSFT expert. Masking narrowly scoped to two Mellanox SKUs, auto-expires on fix. Disclosed caveat: SPC3 hw verification still pending (setup error before reaching probe); SPC1 fully verified. Mellanox-platform fact → defer to author's company.

[↑ back to recommendations](#deep-review-findings--sonic-netsonic-mgmt)

<a id="pr-24091"></a>

### [PR #24091](https://github.com/sonic-net/sonic-mgmt/pull/24091) — Adding confed configuration to topo_t2_single_node_max_64p.yml
- **Author / affiliation / trust:** YatishSVC / microsoft / High
- **➡ Recommendation:** **Approve** — data internally consistent across both files, semantics match how the framework consumes confed keys, and both reviewer threads (ASN value, v2 file) are addressed at head. Only nit is stale prose in the body (`65200` vs the correct committed `65300`).
- **Type:** Feature enhancement (testbed/framework — topology data)
- **Complexity:** Low — 2 files, +327/-131. Pure ansible topology var data (no Python/template logic); blast radius limited to the two `topo_t2_single_node_max_64p` SKU var files. Mechanical edits across 32 core + 32 leaf VM blocks.
- **Description summary:** Adds BGP confederation config to the 64-port T2 single-node topology (both `.yml` and `_v2.yml`). Follow-up to #23527. Sets `dut_asn 65100→66000`, adds `dut_confed_asn: 65100` / `dut_confed_peers: 65300`; adds `peer_in_bgp_confed: true` to all 32 core (T3) VMs; on all 32 leaf (LT2) VMs sets `asn: 65300`, adds `confed_asn: 65100`/`confed_peers: 66000`, repoints the peers map key 65100→66000.
- **Existing reviews/comments:** arlakshm COMMENTED — inline "this ASN is 65300" (correcting `dut_confed_peers`) → **addressed** (current diff has 65300). arista-nwolfe COMMENTED — "update `_v2.yml` as well? Arista uses this SKU" → **addressed** (both files in the diff). YatishSVC "Thanks, updated".
- **Matches description?:** Partial — diff fully implements the intent and is correct, but the body text is stale (summary line says `dut_confed_peers: 65200`; the committed/correct value is `65300`). Documentation-only drift, not a code defect.
- **Conflict likelihood:** Low — file-isolated; no overlap with other eligible PRs.
- **Duplication likelihood:** none seen — explicit follow-up to #23527.
- **CI actually runs the test?:** N-A (not a pytest) — topology ansible-var data, exercised via `add-topo` deployment, not the VS/KVM PR-gate. Author verified via `add-topo`. Judged on internal consistency instead.
- **Linked issue(s):** #23527 (predecessor PR, mentioned) — track-only, no auto-close.
- **Reviewer notes:** Verified internally consistent at head: the two files are in lockstep (identical confed values and counts: 32× `peer_in_bgp_confed` core, 32× leaf `confed_asn/confed_peers/asn/peers`, zero leftover old per-leaf ASNs). ASN topology self-consistent: core VMs key peers on `65100`=`dut_confed_asn` (per `topo_facts.py`); leaf VMs key peers on `66000`=`dut_asn`; `dut_confed_peers: 65300` matches leaf member-AS. Two-pattern split matches existing confed topo files — all keys live/consumed.

[↑ back to recommendations](#deep-review-findings--sonic-netsonic-mgmt)

<a id="pr-21429"></a>

### [PR #21429](https://github.com/sonic-net/sonic-mgmt/pull/21429) — tests/bgp: Add mgmtd set-src regression coverage
- **Author / affiliation / trust:** Bojun-Feng / unknown / Low (merged PRs=2, no top-company bump)
- **➡ Recommendation:** **Approve** — all reviewer points resolved, test is correct and CI-selectable on t0/t1/t2. Minor: ask author to refresh the PR description (stale `frr_mgmt_framework_config`/"512 static routes"/`#24694` wording) and ideally confirm a real FRR-10.x hardware pass (on KVM the asserting body may be skipped).
- **Type:** New test suite
- **Complexity:** Low — 1 file, +328/-0, isolated new file (`tests/bgp/test_frr_set_src_route_map.py`, renamed from `test_frr_set_src_mgmtd.py`); consumes the pre-existing `dut_with_default_route` fixture (unmodified here).
- **Description summary:** Adds regression coverage for the mgmtd FRR-replay race that dropped the default-route `set src` (Loopback0) entry under large configs. Two tests: plain config_reload, and reload after injecting 512 FRR prefix-lists/route-map to widen the vulnerable `vtysh -f` window; both verify IPv4/IPv6 default routes and `RM_SET_SRC`/`RM_SET_SRC6` route-maps survive, with checkpoint/rollback cleanup.
- **Existing reviews/comments:** Gfrom2016 + StormLiangMS LGTM (both DISMISSED, stale); github-advanced-security CodeQL on a now-removed helper; **deepak-singhal0408 — 7 substantive points** + a description-staleness nit, author posted "Feedback N resolved by <commit>" for all → **all 7 verified addressed at head** (see notes).
- **Matches description?:** Partial — code does what the title claims, but the body is out of date (mentions `frr_mgmt_framework_config` gating and CONFIG_DB static routes, both replaced; stale `Fix sonic-buildimage#24694`). Behavior correct; only prose lags.
- **Conflict likelihood:** Low — new file, no overlap.
- **Duplication likelihood:** none seen — unique mgmtd set-src regression.
- **CI actually runs the test?:** **Yes** — `pytest.mark.topology('t0','t1','t2')` in the current diff (the scaffold heuristic's "t2-only" guess was WRONG; t0/t1 present → default gate selects it). Caveat: meaningful assertions only run where mgmtd is live + a default route exists (`pytest_require(_mgmtd_running(...))` skips on non-FRR-10.x); on KVM the body may no-op, so a real FRR-10.x pass is what validates the regression.
- **Linked issue(s):** sonic-mgmt#21342 (auto-close on merge via "Fix #21342" — verify repo/issue); sonic-buildimage#24694 ("Fix" — cross-repo, won't auto-close, stale/self-filed — drop it); #21931, FRRouting/frr#18541/#18601 track-only.
- **Reviewer notes:** All 7 deepak-singhal0408 points genuinely addressed at SHA 4f491a4: (1) gate now `_mgmtd_running` `pgrep -x mgmtd`+`pytest_require`; (2) topology t0/t1/t2, T2 via `dut_with_default_route`; (3) active `_start/_stop_vtysh_race_loop` amplification; (4) bloat now 512 FRR prefix-lists via `vtysh -f` (not CONFIG_DB); (5) implicit-None helper deleted (CodeQL nullified); (6) file renamed; (7) cleanup collapsed. Only loose end is the stale description prose. Low-trust author but the work is sound and reviewer-vetted.

[↑ back to recommendations](#deep-review-findings--sonic-netsonic-mgmt)

<a id="pr-23542"></a>

### [PR #23542](https://github.com/sonic-net/sonic-mgmt/pull/23542) — [ACL] Fix missing upstream ports in ACL table for topologies with a mix of LAG and non-LAG upstream ports
- **Author / affiliation / trust:** ccroy-arista / Arista / High
- **➡ Recommendation:** **Approve** — small, correct, well-scoped bug fix from a High-trust Arista author who validated on the affected topology. PR-gate proves no regression on standard topologies; the actual mixed-topology fix is verified by the author's manual run (clear no-op on all gated paths).
- **Type:** Bug fix
- **Complexity:** Low — 1 file, +10/-0; isolated to the `setup()` fixture's `acl_table_ports` assembly in `tests/acl/test_acl.py`, no shared infra.
- **Description summary:** On mixed topologies (e.g. t1-isolated-d448u15-lag) most upstream/T2 links are individual ports, not PortChannels. The PortChannel branch and the upstream-port branch were mutually exclusive, so non-LAG upstream ports were never bound to the ACL table → ingress ACL rules not applied → drop-expected packets forwarded. Fix adds upstream ports belonging to no PortChannel into the ACL table while still inside the PortChannel branch.
- **Existing reviews/comments:** none (0 reviews/comments).
- **Matches description?:** Yes — computes `pc_members` across all port_channels and appends only upstream ports not in that set, mirroring the existing multi-asic host+namespace dual-append pattern.
- **Conflict likelihood:** Low — file-isolated; no other eligible PR touches `tests/acl/test_acl.py`.
- **Duplication likelihood:** none seen.
- **CI actually runs the test?:** Partial — KVM PR-gate runs ACL on t0/t1-lag/multi-asic-t1/t2 (green). The new lines execute on t1-lag, but there all upstream T2 links are PortChannels so `non_pc_ports` is empty → the added code is a **no-op** on gated topos. The bug only manifests on a MIXED topology (not in the gate). So green confirms safe/non-regressing but does NOT validate the fix path; author validated manually on t1-isolated-d448u15-lag.
- **Linked issue(s):** none (body has placeholder "Fixes # (issue)" only).
- **Reviewer notes:** Logic correct and safe. `v['members']` is the established minigraph_portchannels key; `.get('members', [])` is defensively safe. No duplication risk (upstream individual ports disjoint from downstream + PortChannel names). Confined to the `if len(port_channels) and (...)` branch → other topos unchanged. Only caveat: green check didn't exercise the fixed path with non-empty `non_pc_ports`.

[↑ back to recommendations](#deep-review-findings--sonic-netsonic-mgmt)

<a id="pr-24591"></a>

### [PR #24591](https://github.com/sonic-net/sonic-mgmt/pull/24591) — [qos] Add SONiC fanout ingress ACL to block L2 noise during headroom pool tests (#24236)
- **Author / affiliation / trust:** XuChen-MSFT / Microsoft / Expert
- **➡ Recommendation:** **Request changes** — not on substance (approach is sound and hardware-verified by an Expert author) but a standing blocking review (yxieca CHANGES_REQUESTED) + CodeQL finding on the empty `except` are unaddressed at HEAD. Trivial fix; approvable once the swallow is justified/logged. Test path isn't CI-validated → rely on the author's physical pass as validation of record.
- **Type:** Bug fix (test-infra reliability) — fixes intermittent `testQosSaiHeadroomPoolWatermark` failures from L2 noise.
- **Complexity:** Medium — 1 file (`tests/qos/qos_sai_base.py`), +248/-46, **shared QoS test infra** (the `permit_only_test_traffic_on_fanout` fixture used across the QoS SAI suite). Blast radius is the SONiC-fanout branch only; EOS path untouched.
- **Description summary:** Completes the #24212 (EOS egress MAC ACL) / #24317 (SONiC LLDP-stop) series by adding a hardware ingress ETHER_TYPE ACL on SONiC-fanout VM-facing ports, dropping LLDP (0x88CC)/LACP (0x8809) noise that inflates DUT InDiscard and flakes headroom-pool watermark tests. Blacklist (deny LLDP/LACP, permit all) via `sonic-cfggen --write-to-db`, CONFIG_DB convergence polling, drop-counter logging, sequential teardown.
- **Existing reviews/comments:** ZhaohuiS COMMENTED (05-14) then **APPROVED (05-20)** — the two 05-14 inline threads were on `sai_qos_tests.py`, which the author confirmed was erroneously included and **removed** → **moot/superseded**. github-advanced-security CodeQL (05-19): empty `except Exception: pass` at `qos_sai_base.py:~3687` → **OPEN**. **yxieca CHANGES_REQUESTED (05-22)** — current `reviewDecision`; blocking ask = comment/log that empty except → **OPEN** (last commit 93ed17e predates the review).
- **Matches description?:** Yes — diff matches the body; earlier scope-creep (`sai_qos_tests.py`) removed; current scope is the single fixture file.
- **Conflict likelihood:** Low — file-isolated. (#24217 same author edits a different file.)
- **Duplication likelihood:** none seen — completing increment of the #24212/#24317 series.
- **CI actually runs the test?:** **No** — the `fanout_os == 'sonic'` branch requires a real physical testbed with a SONiC fanout switch (live `fanout.host.command`, conn_graph_facts, ASIC counters). CI green did NOT validate this path; validation is the author's documented physical run on a Cisco-8101 SONiC fanout with drop-counter evidence. Defer to MSFT/Expert on SAI/Broadcom facts.
- **Linked issue(s):** #24236 (the flaky-test issue this fixes — no `Fixes:` keyword → **MANUAL close on merge** / verify); #24212/#24317 (merged predecessors, track-only).
- **Reviewer notes:** Code clean and well-documented with strong physical evidence. The one true open item is mechanical: yxieca's blocking CR + CodeQL both target the same `except Exception: pass` in `_wait_sonic_acl_ready`, unaddressed because the last commit predates yxieca's review. ZhaohuiS's inline threads are moot. Non-blocking correctness note: `_wait_sonic_acl_ready` only confirms CONFIG_DB key presence (config plane), not ASIC programming — the counter-logging step is what proves ASIC.
- **Requested changes (to post):**
    - `tests/qos/qos_sai_base.py`, in `_wait_sonic_acl_ready` (~L3687): the `except Exception:` / `pass` is an empty silent swallow — flagged by both CodeQL and yxieca (CHANGES_REQUESTED, still blocking). Please either log the exception (e.g. `logger.debug("ACL readiness poll on %s raised %s; retrying", fanout_name, e)`) or add a comment stating the swallow is intentional because the loop is a bounded poll that times out on its own. (The last commit 93ed17e predates yxieca's review, so this hasn't been picked up.)
    - Non-blocking (yxieca): add a one-line note that readiness is confirmed via **CONFIG_DB key presence (config plane), not ASIC_DB** — ASIC programming is instead evidenced by `_log_sonic_acl_counters`.

[↑ back to recommendations](#deep-review-findings--sonic-netsonic-mgmt)

<a id="pr-17940"></a>

### [PR #17940](https://github.com/sonic-net/sonic-mgmt/pull/17940) — [ansible]: Add generate hosts script
- **Author / affiliation / trust:** Pterosaur / Microsoft / Expert (Expert trust does NOT override an unresolved maintainer change-request)
- **➡ Recommendation:** **Request changes** — maintainer change-request (wangxin) plus 16 substantive reviewer issues all remain open against the current code; PR is stale (~3 months) with no follow-up commits.
- **Type:** Feature enhancement (new testbed utility script; can modify system-critical files like /etc/hosts).
- **Complexity:** Low — 1 file, +202/-0; standalone ansible utility script, no shared blast radius.
- **Description summary:** Adds `ansible/scripts/generate_hosts.py`, which generates a hosts file by merging device info from CSVs (ManagementIp/Hostname) with an existing base hosts file — preserves comments/blank lines/formatting, natural-sorts, dedups, and offers an interactive/`--override` path for IP conflicts.
- **Existing reviews/comments:** yutongzhang-microsoft COMMENTED (4 inline); banidoru COMMENTED ×3 (12 inline); yxieca DISMISSED (AI-bot "no issues" — no weight); **wangxin CHANGES_REQUESTED (2026-04-08) — still OPEN**.
- **Matches description?:** Partial — the script does merge CSVs with comment preservation + natural sort as described, but overstates robustness ("no duplicate entries", "options for overriding") given the unaddressed gaps (silent drops, KeyError, no validation, non-interactive hang, exit-0-on-error).
- **Conflict likelihood:** Low — new file, no overlap.
- **Duplication likelihood:** none seen.
- **CI actually runs the test?:** N-A (not a test) — standalone ansible script; VS/KVM PR-gate doesn't execute it. **No unit tests exist** for a script that can rewrite /etc/hosts (flagged by banidoru, confirmed). CI green does NOT validate behavior.
- **Linked issue(s):** none.
- **Reviewer notes:** All 16 inline issues from two reviewers remain unaddressed at the current head (SHA unchanged since 2026-03; now ~3 months stale). Maintainer wangxin explicitly requested changes 2026-04-08, unresolved. The only "no issues" review (yxieca) was a dismissed AI-bot review. Confirmed: script has no `import sys`, so the stderr/exit-code/TTY fixes aren't present.
- **Requested changes (to post):**
    - `:83` / `:141` — Make parsing consistent + multi-hostname-aware: in `load_existing_hosts` use `len(parts) >= 2`, take `parts[0]` as IP and `parts[1:]` as hostnames, matching `write_hosts_file`.
    - `:96` — Use `row.get('ManagementIp')`/`row.get('Hostname')` (or check `reader.fieldnames`) and print a meaningful error naming the file/row on missing columns, not an uncaught KeyError.
    - `:155` (main loop) — Build the existing-hostname set once before the loop (`{h for ips in existing_hosts.values() for h in ips}`) instead of rebuilding per hostname (O(n*m)→O(n+m)).
    - `:158` — When a hostname already maps to a different IP, warn (stale mapping) instead of silently `continue`.
    - `:150` — Emit the multi-hostname `# Warning` comment once per IP, not once per shared hostname.
    - `:163` — Guard `input()` with `sys.stdin.isatty()`; default to skip/error in non-interactive (CI/cron/piped) contexts so it doesn't hang.
    - `:175` — Detect `--base-hosts` == `--output` and write-temp-then-rename (or error), to avoid truncating the source before it's fully read.
    - `:98` — Validate the IP with `ipaddress.ip_address()`; skip+warn on malformed/empty.
    - `:99` / `:100` — `.strip()` IP and hostname; skip+warn rows with empty hostname or IP.
    - `:107` — If `glob.glob(csv_pattern)` is empty, warn naming the pattern instead of silently returning empty.
    - `:131` — Trailing-newline guard before appending: `if original_lines and not original_lines[-1].endswith('\n'): f.write('\n')`.
    - `:186` — `import sys` and `sys.exit(1)` on conflicts/warnings so CI/Makefile callers can detect failure.
    - `:68` — PEP8: group stdlib imports.
    - (general) Add unit tests covering merge logic, conflict handling, and edge cases.

[↑ back to recommendations](#deep-review-findings--sonic-netsonic-mgmt)

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
