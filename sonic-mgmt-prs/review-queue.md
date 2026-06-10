# sonic-net/sonic-mgmt — PRs awaiting my review (`bhouse-nexthop`)

_Generated 2026-06-10. Open PRs where I am a requested reviewer._

## Summary

- **Total PRs:** 61
- **CI:** 54 passing · 6 failing · 0 pending · 1 no checks
- **Merge:** 15 with conflicts · 46 clean
- **Review state:** 13 approved · 6 changes requested · 42 no review yet
- **Last sweep (2026-06-10):** pinged 15 conflicting PRs · triggered `/azp run` on 25 stale-CI PRs — see [Maintenance policy](#maintenance-policy-sweep-rules)

## Tracking table

| PR | Title | Author | CI | Last CI | Merge | Review decision | Approved by | Changes requested | Follow-up |
|----|-------|--------|----|---------|-------|-----------------|-------------|-------------------|-----------|
| [#25134](https://github.com/sonic-net/sonic-mgmt/pull/25134) | [conditional_mark]: Enable NTP IPv6-only management ... | lunyue-ms | ✅ PASS | 2026-06-05 | ✅ clean | Review required | — | — | — |
| [#25123](https://github.com/sonic-net/sonic-mgmt/pull/25123) | [TH6] test_po_cleanup fix for large number of lags(1... | sanjair-git | ✅ PASS | 2026-06-05 | ✅ clean | Review required | — | — | — |
| [#25094](https://github.com/sonic-net/sonic-mgmt/pull/25094) | Add disable_memory_utilization option for fwutil tes... | zypgithub | ✅ PASS | 2026-06-04 | ✅ clean | Approved | nhe-NV | — | — |
| [#25040](https://github.com/sonic-net/sonic-mgmt/pull/25040) | [bgp/agg] Make BGP aggregate-address tests solid aga... | nanali-msft | ✅ PASS | 2026-06-03 | ✅ clean | Approved | shixizhang | — | — |
| [#25012](https://github.com/sonic-net/sonic-mgmt/pull/25012) | Fixing PMON status test failures | caleb-nexthop | ✅ PASS | 2026-06-03 | ✅ clean | Approved | liamkearney-msft | — | — |
| [#25000](https://github.com/sonic-net/sonic-mgmt/pull/25000) | Fix test_srv6_vlan_forwarding when no ipv6 mgmt for ... | ytzur1 | ✅ PASS | 2026-06-03 | ✅ clean | Review required | — | — | — |
| [#24975](https://github.com/sonic-net/sonic-mgmt/pull/24975) | Fix the NTP polling step in deploy-mg playbook | congh-nvidia | ✅ PASS | 2026-06-04 | ✅ clean | Approved | nhe-NV | — | — |
| [#24930](https://github.com/sonic-net/sonic-mgmt/pull/24930) | [vxlan] Improve vnet bgp subintf cleanup diagnostics | yyynini | ✅ PASS | 2026-05-28 | ✅ clean | Review required | — | — | — |
| [#24927](https://github.com/sonic-net/sonic-mgmt/pull/24927) | Fix test_link_local_ip failures in dualtor active-ac... | xixuej | ✅ PASS | 2026-06-04 | ✅ clean | Approved | nhe-NV, yyynini | — | — |
| [#24913](https://github.com/sonic-net/sonic-mgmt/pull/24913) | Add hwsku Mellanox-SN5640-C508O1X2 into necessary files | echuawu | ✅ PASS | 2026-06-04 | ⚠️ CONFLICT | Approved | nhe-NV | — | 📨 [conflict ping 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/24913#issuecomment-4669782918) — awaiting author |
| [#24902](https://github.com/sonic-net/sonic-mgmt/pull/24902) | Handle pytest.fail.Exeption in wait_until | wrideout-arista | ✅ PASS | 2026-06-03 | ✅ clean | Review required | — | — | — |
| [#24884](https://github.com/sonic-net/sonic-mgmt/pull/24884) | [bgp scale] Reduce DUT-side observer load during rou... | yutongzhang-microsoft | ✅ PASS | 2026-05-27 | ✅ clean | Review required | — | — | — |
| [#24876](https://github.com/sonic-net/sonic-mgmt/pull/24876) | lldp_syncd failure due to not enough converge time | Yogapriya-cisco | ✅ PASS | 2026-05-27 | ✅ clean | Approved | prhoskot | — | — |
| [#24845](https://github.com/sonic-net/sonic-mgmt/pull/24845) | ARS test script | apannerselva | ✅ PASS | 2026-06-03 | ✅ clean | Review required | — | — | — |
| [#24829](https://github.com/sonic-net/sonic-mgmt/pull/24829) | Fix: add port name for acl interface parsing | ytzur1 | ✅ PASS | 2026-06-05 | ✅ clean | Review required | — | — | — |
| [#24802](https://github.com/sonic-net/sonic-mgmt/pull/24802) | [BGP] Align bgpmon tests with passive DUT peering | abdosi | ✅ PASS | 2026-05-22 | ✅ clean | Review required | — | — | 🔄 [/azp run 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/24802#issuecomment-4669828868) — CI re-triggered |
| [#24787](https://github.com/sonic-net/sonic-mgmt/pull/24787) | [platform_tests][T2] Add test_sup_fan_recovery.py to... | aeedara-nokia | ✅ PASS | 2026-05-27 | ✅ clean | Review required | — | — | — |
| [#24687](https://github.com/sonic-net/sonic-mgmt/pull/24687) | pfcwd: ignore benign cisco-8000 SAI/orchagent errors... | wsycqyz | ✅ PASS | 2026-05-18 | ✅ clean | Review required | — | — | 🔄 [/azp run 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/24687#issuecomment-4669828741) — CI re-triggered |
| [#24685](https://github.com/sonic-net/sonic-mgmt/pull/24685) | Modify test_sfp_util.py to run interfaces data comma... | IdanharelNV | ✅ PASS | 2026-06-05 | ⚠️ CONFLICT | Review required | — | — | 📨 [conflict ping 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/24685#issuecomment-4669782703) — awaiting author |
| [#24649](https://github.com/sonic-net/sonic-mgmt/pull/24649) | [dualtor] Add test for tunnel termination drop on st... | yyynini | ✅ PASS | 2026-05-18 | ✅ clean | Review required | — | — | 🔄 [/azp run 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/24649#issuecomment-4669828581) — CI re-triggered |
| [#24597](https://github.com/sonic-net/sonic-mgmt/pull/24597) | Update the fanout switch deploy step due to lack of ... | echuawu | ✅ PASS | 2026-06-04 | ✅ clean | Approved | nhe-NV | — | — |
| [#24591](https://github.com/sonic-net/sonic-mgmt/pull/24591) | [qos] Add SONiC fanout ingress ACL to block L2 noise... | XuChen-MSFT | ✅ PASS | 2026-05-19 | ✅ clean | Changes requested | ZhaohuiS | yxieca | 🔄 [/azp run 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/24591#issuecomment-4669828406) — CI re-triggered |
| [#24545](https://github.com/sonic-net/sonic-mgmt/pull/24545) | Fix test_monitoring_critical_processes timeout by ki... | xwjiang-ms | ✅ PASS | 2026-06-02 | ✅ clean | Review required | — | — | — |
| [#24507](https://github.com/sonic-net/sonic-mgmt/pull/24507) | conftest: fix temporarily_disable_route_check for lt... | bingwang-ms | ✅ PASS | 2026-05-11 | ✅ clean | Review required | — | — | 🔄 [/azp run 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/24507#issuecomment-4669828213) — CI re-triggered |
| [#24493](https://github.com/sonic-net/sonic-mgmt/pull/24493) | Update the gNMI setup without authentication for liq... | JibinBao | ✅ PASS | 2026-06-04 | ✅ clean | Approved | nhe-NV | — | — |
| [#24437](https://github.com/sonic-net/sonic-mgmt/pull/24437) | save pfcwd_timer_accuracy test result to file | wenjwang-nv | ✅ PASS | 2026-06-04 | ✅ clean | Approved | nhe-NV | — | — |
| [#24416](https://github.com/sonic-net/sonic-mgmt/pull/24416) | bgp test changes for support bgp confed based topolo... | arlakshm | ✅ PASS | 2026-05-22 | ⚠️ CONFLICT | Changes requested | Javier-Tan, YatishSVC | yxieca | 📨 [conflict ping 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/24416#issuecomment-4669782118) — awaiting author |
| [#24403](https://github.com/sonic-net/sonic-mgmt/pull/24403) | [dhcp_relay]  rework restart_dhcp_service to explici... | Xichen96 | ✅ PASS | 2026-05-07 | ✅ clean | Review required | — | — | 🔄 [/azp run 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/24403#issuecomment-4669828050) — CI re-triggered |
| [#24367](https://github.com/sonic-net/sonic-mgmt/pull/24367) | The monit reported memory usage exceeds increase thr... | yaopingz | ✅ PASS | 2026-05-07 | ⚠️ CONFLICT | Review required | — | — | 📨 [conflict ping 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/24367#issuecomment-4669782342) — awaiting author |
| [#24357](https://github.com/sonic-net/sonic-mgmt/pull/24357) | [mmu probing] Add ProbingBase PG counter false env U... | yyynini | ✅ PASS | 2026-05-06 | ✅ clean | Review required | — | — | 🔄 [/azp run 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/24357#issuecomment-4669827925) — CI re-triggered |
| [#24320](https://github.com/sonic-net/sonic-mgmt/pull/24320) | changes for port speed test enhancement | rawal01 | ✅ PASS | 2026-05-27 | ✅ clean | Review required | — | — | — |
| [#24247](https://github.com/sonic-net/sonic-mgmt/pull/24247) | [SNAPPI][AI]Finding the minimum frame size with no p... | vikumarks | ✅ PASS | 2026-04-29 | ✅ clean | Review required | — | — | 🔄 [/azp run 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/24247#issuecomment-4669827789) — CI re-triggered |
| [#24217](https://github.com/sonic-net/sonic-mgmt/pull/24217) | [Probe] Add xfail for HeadroomPool probe test on SPC... | XuChen-MSFT | ✅ PASS | 2026-05-12 | ✅ clean | Review required | — | — | 🔄 [/azp run 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/24217#issuecomment-4669827575) — CI re-triggered |
| [#24091](https://github.com/sonic-net/sonic-mgmt/pull/24091) | Adding confed configuration to topo_t2_single_node_m... | YatishSVC | ✅ PASS | 2026-05-12 | ✅ clean | Review required | — | — | 🔄 [/azp run 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/24091#issuecomment-4669827437) — CI re-triggered |
| [#23930](https://github.com/sonic-net/sonic-mgmt/pull/23930) | Update variables | SaiYasaswiniP | ✅ PASS | 2026-06-04 | ✅ clean | Review required | — | — | — |
| [#23606](https://github.com/sonic-net/sonic-mgmt/pull/23606) | Add tests for static route removal after config relo... | yxieca | ✅ PASS | 2026-04-04 | ✅ clean | Review required | — | — | 🔄 [/azp run 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/23606#issuecomment-4669827290) — CI re-triggered |
| [#23542](https://github.com/sonic-net/sonic-mgmt/pull/23542) | [ACL] Fix missing upstream ports in ACL table for to... | ccroy-arista | ✅ PASS | 2026-05-13 | ✅ clean | Review required | — | — | 🔄 [/azp run 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/23542#issuecomment-4669827167) — CI re-triggered |
| [#23346](https://github.com/sonic-net/sonic-mgmt/pull/23346) | SONiC BMC Redfish API and D-Bus test plan | chinmoy-nexthop | ✅ PASS | 2026-04-17 | ✅ clean | Review required | — | — | 🔄 [/azp run 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/23346#issuecomment-4669827015) — CI re-triggered |
| [#23283](https://github.com/sonic-net/sonic-mgmt/pull/23283) | test_qos_sai: prevent cascading failures after fixtu... | darius-nexthop | ✅ PASS | 2026-05-25 | ✅ clean | Changes requested | — | — | 🔄 [/azp run 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/23283#issuecomment-4669826888) — CI re-triggered |
| [#22569](https://github.com/sonic-net/sonic-mgmt/pull/22569) | Fix failures in tests/test_crm.py due to log overflow | sudheer-nexthop | ✅ PASS | 2026-04-03 | ✅ clean | Changes requested | YatishSVC | — | 🔄 [/azp run 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/22569#issuecomment-4669826766) — CI re-triggered |
| [#21925](https://github.com/sonic-net/sonic-mgmt/pull/21925) | fix the issue with skip_yang usage Issue 21923 | aronovic | ❌ FAIL (1) | 2026-01-15 | ⚠️ CONFLICT | Review required | — | — | 📨 [conflict ping 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/21925#issuecomment-4669780688) — awaiting author |
| [#21660](https://github.com/sonic-net/sonic-mgmt/pull/21660) | [AI - Snappi] Adding BGP convergence testcase for De... | selldinesh | ✅ PASS | 2026-04-02 | ✅ clean | Review required | — | — | 🔄 [/azp run 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/21660#issuecomment-4669826658) — CI re-triggered |
| [#21658](https://github.com/sonic-net/sonic-mgmt/pull/21658) | [AI - Snappi] Adding BGP convergence testcase for si... | selldinesh | ✅ PASS | 2026-01-29 | ✅ clean | Review required | — | — | 🔄 [/azp run 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/21658#issuecomment-4669826523) — CI re-triggered |
| [#21429](https://github.com/sonic-net/sonic-mgmt/pull/21429) | tests/bgp: Add mgmtd set-src regression coverage | Bojun-Feng | ✅ PASS | 2026-05-07 | ✅ clean | Review required | — | — | 🔄 [/azp run 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/21429#issuecomment-4669826369) — CI re-triggered |
| [#21411](https://github.com/sonic-net/sonic-mgmt/pull/21411) | Add test suite for PORT_PHY_ATTR flex counter feature | dhanasekar-arista | ✅ PASS | 2026-02-20 | ✅ clean | Approved | yxieca | — | 🔄 [/azp run 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/21411#issuecomment-4669826246) — CI re-triggered |
| [#21144](https://github.com/sonic-net/sonic-mgmt/pull/21144) | test_container_autorestart: ensure database containe... | qiluo-msft | ❌ FAIL (5) | 2025-12-30 | ✅ clean | Review required | — | — | 🔄 [/azp run 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/21144#issuecomment-4669826058) — CI re-triggered |
| [#21084](https://github.com/sonic-net/sonic-mgmt/pull/21084) | KeyError: 'secret_group_vars' in bgp/test_bgp_operat... | eyakubch | ✅ PASS | 2025-10-24 | ⚠️ CONFLICT | Review required | — | — | 📨 [conflict ping 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/21084#issuecomment-4669782497) — awaiting author |
| [#20841](https://github.com/sonic-net/sonic-mgmt/pull/20841) | PCBB Deadlock Snappi Test | rbpittman | ✅ PASS | 2025-10-20 | ⚠️ CONFLICT | Changes requested | — | lolyu | 📨 [conflict ping 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/20841#issuecomment-4669781163) — awaiting author |
| [#20456](https://github.com/sonic-net/sonic-mgmt/pull/20456) | Parameterize gNMI CONFIG DB tests with different VRFs | spandan-nexthop | ❌ FAIL (3) | 2026-06-02 | ⚠️ CONFLICT | Review required | — | — | 📨 [conflict ping 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/20456#issuecomment-4669783100) — awaiting author |
| [#20331](https://github.com/sonic-net/sonic-mgmt/pull/20331) | Fixing an issue in outer IPv6 VxLAN hash tests | mramezani95 | ✅ PASS | 2025-08-21 | ⚠️ CONFLICT | Approved | kperumalbfn | — | 📨 [conflict ping 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/20331#issuecomment-4669781341) — awaiting author |
| [#20001](https://github.com/sonic-net/sonic-mgmt/pull/20001) | Marking Sub port interface port-in lag cases xFAIL d... | apannerselva | ✅ PASS | 2026-03-10 | ✅ clean | Review required | — | — | 🔄 [/azp run 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/20001#issuecomment-4669825904) — CI re-triggered |
| [#19873](https://github.com/sonic-net/sonic-mgmt/pull/19873) | Azure CI/nightly latest skip markers | honllum | ❌ FAIL (2) | 2025-08-05 | ⚠️ CONFLICT | Review required | — | — | 📨 [conflict ping 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/19873#issuecomment-4669781947) — awaiting author |
| [#19374](https://github.com/sonic-net/sonic-mgmt/pull/19374) | Sonic-Mgmt cases for Unified TeamD | vrajeshe | ❌ FAIL (3) | 2026-03-23 | ⚠️ CONFLICT | Review required | Boxing923 | — | 📨 [conflict ping 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/19374#issuecomment-4669781713) — awaiting author |
| [#19187](https://github.com/sonic-net/sonic-mgmt/pull/19187) | Changes to modify the config_mode value to unified f... | vidyac86 | ❌ FAIL (4) | 2026-04-17 | ⚠️ CONFLICT | Review required | — | — | 📨 [conflict ping 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/19187#issuecomment-4669780981) — awaiting author |
| [#19067](https://github.com/sonic-net/sonic-mgmt/pull/19067) | Pre-commit errors fixed and Replaced noqa with noqa:... | v-jessgeorge | ✅ PASS | 2025-06-23 | ⚠️ CONFLICT | Approved | xwjiang-ms | — | 📨 [conflict ping 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/19067#issuecomment-4669780836) — awaiting author |
| [#19020](https://github.com/sonic-net/sonic-mgmt/pull/19020) | [Test gap]Test plan to verify vxlan tunnel name length | wsycqyz | ✅ PASS | 2025-06-23 | ✅ clean | Review required | — | — | 🔄 [/azp run 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/19020#issuecomment-4669825787) — CI re-triggered |
| [#18701](https://github.com/sonic-net/sonic-mgmt/pull/18701) | Fix missing PSU fans in test_psu_fan.py port to 202411 | eyakubch | ✅ PASS | 2025-07-10 | ✅ clean | Review required | — | — | 🔄 [/azp run 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/18701#issuecomment-4669825662) — CI re-triggered |
| [#18660](https://github.com/sonic-net/sonic-mgmt/pull/18660) | process crash utilities for ha test automation | nnelluri-cisco | ✅ PASS | 2025-08-26 | ✅ clean | Review required | — | — | 🔄 [/azp run 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/18660#issuecomment-4669825541) — CI re-triggered |
| [#18620](https://github.com/sonic-net/sonic-mgmt/pull/18620) | Changes related noqa and pre-commit in tests/dhcp_relay | v-jessgeorge | ✅ PASS | 2025-06-27 | ⚠️ CONFLICT | Review required | — | — | 📨 [conflict ping 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/18620#issuecomment-4669781523) — awaiting author |
| [#18108](https://github.com/sonic-net/sonic-mgmt/pull/18108) | Minor correction in tsa/tsb command output verificat... | ansrajpu-git | — | — | ⚠️ CONFLICT | Review required | — | — | 📨 [conflict ping 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/18108#issuecomment-4669782236) — awaiting author |
| [#17940](https://github.com/sonic-net/sonic-mgmt/pull/17940) | [ansible]: Add generate hosts script | Pterosaur | ✅ PASS | 2025-06-27 | ✅ clean | Changes requested | — | wangxin | 🔄 [/azp run 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/17940#issuecomment-4669825404) — CI re-triggered |

## Needs attention

### ⚠️ Merge conflicts (need rebase by author)

_On 2026-06-10 we commented on each of these asking the author to confirm the PR is still relevant and rebase/resolve conflicts, after which we will review. **Awaiting author response.**_

- [#24913](https://github.com/sonic-net/sonic-mgmt/pull/24913) Add hwsku Mellanox-SN5640-C508O1X2 into necessary files — echuawu — 📨 [asked 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/24913#issuecomment-4669782918)
- [#24685](https://github.com/sonic-net/sonic-mgmt/pull/24685) Modify test_sfp_util.py to run interfaces data comma... — IdanharelNV — 📨 [asked 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/24685#issuecomment-4669782703)
- [#24416](https://github.com/sonic-net/sonic-mgmt/pull/24416) bgp test changes for support bgp confed based topolo... — arlakshm — 📨 [asked 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/24416#issuecomment-4669782118)
- [#24367](https://github.com/sonic-net/sonic-mgmt/pull/24367) The monit reported memory usage exceeds increase thr... — yaopingz — 📨 [asked 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/24367#issuecomment-4669782342)
- [#21925](https://github.com/sonic-net/sonic-mgmt/pull/21925) fix the issue with skip_yang usage Issue 21923 — aronovic — 📨 [asked 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/21925#issuecomment-4669780688)
- [#21084](https://github.com/sonic-net/sonic-mgmt/pull/21084) KeyError: 'secret_group_vars' in bgp/test_bgp_operat... — eyakubch — 📨 [asked 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/21084#issuecomment-4669782497)
- [#20841](https://github.com/sonic-net/sonic-mgmt/pull/20841) PCBB Deadlock Snappi Test — rbpittman — 📨 [asked 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/20841#issuecomment-4669781163)
- [#20456](https://github.com/sonic-net/sonic-mgmt/pull/20456) Parameterize gNMI CONFIG DB tests with different VRFs — spandan-nexthop — 📨 [asked 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/20456#issuecomment-4669783100)
- [#20331](https://github.com/sonic-net/sonic-mgmt/pull/20331) Fixing an issue in outer IPv6 VxLAN hash tests — mramezani95 — 📨 [asked 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/20331#issuecomment-4669781341)
- [#19873](https://github.com/sonic-net/sonic-mgmt/pull/19873) Azure CI/nightly latest skip markers — honllum — 📨 [asked 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/19873#issuecomment-4669781947)
- [#19374](https://github.com/sonic-net/sonic-mgmt/pull/19374) Sonic-Mgmt cases for Unified TeamD — vrajeshe — 📨 [asked 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/19374#issuecomment-4669781713)
- [#19187](https://github.com/sonic-net/sonic-mgmt/pull/19187) Changes to modify the config_mode value to unified f... — vidyac86 — 📨 [asked 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/19187#issuecomment-4669780981)
- [#19067](https://github.com/sonic-net/sonic-mgmt/pull/19067) Pre-commit errors fixed and Replaced noqa with noqa:... — v-jessgeorge — 📨 [asked 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/19067#issuecomment-4669780836)
- [#18620](https://github.com/sonic-net/sonic-mgmt/pull/18620) Changes related noqa and pre-commit in tests/dhcp_relay — v-jessgeorge — 📨 [asked 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/18620#issuecomment-4669781523)
- [#18108](https://github.com/sonic-net/sonic-mgmt/pull/18108) Minor correction in tsa/tsb command output verificat... — ansrajpu-git — 📨 [asked 2026-06-10](https://github.com/sonic-net/sonic-mgmt/pull/18108#issuecomment-4669782236)

### ❌ Failing CI

- [#21925](https://github.com/sonic-net/sonic-mgmt/pull/21925) fix the issue with skip_yang usage Issue 21923 — ❌ FAIL (1), last green 2026-01-15
- [#21144](https://github.com/sonic-net/sonic-mgmt/pull/21144) test_container_autorestart: ensure database containe... — ❌ FAIL (5), last green 2025-12-30
- [#20456](https://github.com/sonic-net/sonic-mgmt/pull/20456) Parameterize gNMI CONFIG DB tests with different VRFs — ❌ FAIL (3), last green 2026-06-02
- [#19873](https://github.com/sonic-net/sonic-mgmt/pull/19873) Azure CI/nightly latest skip markers — ❌ FAIL (2), last green 2025-08-05
- [#19374](https://github.com/sonic-net/sonic-mgmt/pull/19374) Sonic-Mgmt cases for Unified TeamD — ❌ FAIL (3), last green 2026-03-23
- [#19187](https://github.com/sonic-net/sonic-mgmt/pull/19187) Changes to modify the config_mode value to unified f... — ❌ FAIL (4), last green 2026-04-17

### 🔴 Changes requested (waiting on author)

- [#24591](https://github.com/sonic-net/sonic-mgmt/pull/24591) [qos] Add SONiC fanout ingress ACL to block L2 noise... — by yxieca
- [#24416](https://github.com/sonic-net/sonic-mgmt/pull/24416) bgp test changes for support bgp confed based topolo... — by yxieca
- [#23283](https://github.com/sonic-net/sonic-mgmt/pull/23283) test_qos_sai: prevent cascading failures after fixtu... — by (see history)
- [#22569](https://github.com/sonic-net/sonic-mgmt/pull/22569) Fix failures in tests/test_crm.py due to log overflow — by (see history)
- [#20841](https://github.com/sonic-net/sonic-mgmt/pull/20841) PCBB Deadlock Snappi Test — by lolyu
- [#17940](https://github.com/sonic-net/sonic-mgmt/pull/17940) [ansible]: Add generate hosts script — by wangxin

### ✅ Approved by someone, CI green — likely mergeable

- [#25094](https://github.com/sonic-net/sonic-mgmt/pull/25094) Add disable_memory_utilization option for fwutil tes... — approved by nhe-NV
- [#25040](https://github.com/sonic-net/sonic-mgmt/pull/25040) [bgp/agg] Make BGP aggregate-address tests solid aga... — approved by shixizhang
- [#25012](https://github.com/sonic-net/sonic-mgmt/pull/25012) Fixing PMON status test failures — approved by liamkearney-msft
- [#24975](https://github.com/sonic-net/sonic-mgmt/pull/24975) Fix the NTP polling step in deploy-mg playbook — approved by nhe-NV
- [#24927](https://github.com/sonic-net/sonic-mgmt/pull/24927) Fix test_link_local_ip failures in dualtor active-ac... — approved by nhe-NV, yyynini
- [#24913](https://github.com/sonic-net/sonic-mgmt/pull/24913) Add hwsku Mellanox-SN5640-C508O1X2 into necessary files — approved by nhe-NV
- [#24876](https://github.com/sonic-net/sonic-mgmt/pull/24876) lldp_syncd failure due to not enough converge time — approved by prhoskot
- [#24597](https://github.com/sonic-net/sonic-mgmt/pull/24597) Update the fanout switch deploy step due to lack of ... — approved by nhe-NV
- [#24493](https://github.com/sonic-net/sonic-mgmt/pull/24493) Update the gNMI setup without authentication for liq... — approved by nhe-NV
- [#24437](https://github.com/sonic-net/sonic-mgmt/pull/24437) save pfcwd_timer_accuracy test result to file — approved by nhe-NV
- [#21411](https://github.com/sonic-net/sonic-mgmt/pull/21411) Add test suite for PORT_PHY_ATTR flex counter feature — approved by yxieca
- [#20331](https://github.com/sonic-net/sonic-mgmt/pull/20331) Fixing an issue in outer IPv6 VxLAN hash tests — approved by kperumalbfn
- [#19067](https://github.com/sonic-net/sonic-mgmt/pull/19067) Pre-commit errors fixed and Replaced noqa with noqa:... — approved by xwjiang-ms

### 🔄 CI re-run triggered via `/azp run` (2026-06-10)

_Clean (no-conflict) PRs whose last CI run was > 2 weeks old. Posted `/azp run` to force a fresh full pipeline run. Re-check CI on the next sweep._

- [#17940](https://github.com/sonic-net/sonic-mgmt/pull/17940) [ansible]: Add generate hosts script — was last run 2025-06-27 — 🔄 [/azp run](https://github.com/sonic-net/sonic-mgmt/pull/17940#issuecomment-4669825404)
- [#18660](https://github.com/sonic-net/sonic-mgmt/pull/18660) process crash utilities for ha test automation — was last run 2025-08-26 — 🔄 [/azp run](https://github.com/sonic-net/sonic-mgmt/pull/18660#issuecomment-4669825541)
- [#18701](https://github.com/sonic-net/sonic-mgmt/pull/18701) Fix missing PSU fans in test_psu_fan.py port to 202411 — was last run 2025-07-10 — 🔄 [/azp run](https://github.com/sonic-net/sonic-mgmt/pull/18701#issuecomment-4669825662)
- [#19020](https://github.com/sonic-net/sonic-mgmt/pull/19020) [Test gap]Test plan to verify vxlan tunnel name length — was last run 2025-06-23 — 🔄 [/azp run](https://github.com/sonic-net/sonic-mgmt/pull/19020#issuecomment-4669825787)
- [#20001](https://github.com/sonic-net/sonic-mgmt/pull/20001) Marking Sub port interface port-in lag cases xFAIL d... — was last run 2026-03-10 — 🔄 [/azp run](https://github.com/sonic-net/sonic-mgmt/pull/20001#issuecomment-4669825904)
- [#21144](https://github.com/sonic-net/sonic-mgmt/pull/21144) test_container_autorestart: ensure database containe... — was last run 2025-12-30 — 🔄 [/azp run](https://github.com/sonic-net/sonic-mgmt/pull/21144#issuecomment-4669826058)
- [#21411](https://github.com/sonic-net/sonic-mgmt/pull/21411) Add test suite for PORT_PHY_ATTR flex counter feature — was last run 2026-02-20 — 🔄 [/azp run](https://github.com/sonic-net/sonic-mgmt/pull/21411#issuecomment-4669826246)
- [#21429](https://github.com/sonic-net/sonic-mgmt/pull/21429) tests/bgp: Add mgmtd set-src regression coverage — was last run 2026-05-07 — 🔄 [/azp run](https://github.com/sonic-net/sonic-mgmt/pull/21429#issuecomment-4669826369)
- [#21658](https://github.com/sonic-net/sonic-mgmt/pull/21658) [AI - Snappi] Adding BGP convergence testcase for si... — was last run 2026-01-29 — 🔄 [/azp run](https://github.com/sonic-net/sonic-mgmt/pull/21658#issuecomment-4669826523)
- [#21660](https://github.com/sonic-net/sonic-mgmt/pull/21660) [AI - Snappi] Adding BGP convergence testcase for De... — was last run 2026-04-02 — 🔄 [/azp run](https://github.com/sonic-net/sonic-mgmt/pull/21660#issuecomment-4669826658)
- [#22569](https://github.com/sonic-net/sonic-mgmt/pull/22569) Fix failures in tests/test_crm.py due to log overflow — was last run 2026-04-03 — 🔄 [/azp run](https://github.com/sonic-net/sonic-mgmt/pull/22569#issuecomment-4669826766)
- [#23283](https://github.com/sonic-net/sonic-mgmt/pull/23283) test_qos_sai: prevent cascading failures after fixtu... — was last run 2026-05-25 — 🔄 [/azp run](https://github.com/sonic-net/sonic-mgmt/pull/23283#issuecomment-4669826888)
- [#23346](https://github.com/sonic-net/sonic-mgmt/pull/23346) SONiC BMC Redfish API and D-Bus test plan — was last run 2026-04-17 — 🔄 [/azp run](https://github.com/sonic-net/sonic-mgmt/pull/23346#issuecomment-4669827015)
- [#23542](https://github.com/sonic-net/sonic-mgmt/pull/23542) [ACL] Fix missing upstream ports in ACL table for to... — was last run 2026-05-13 — 🔄 [/azp run](https://github.com/sonic-net/sonic-mgmt/pull/23542#issuecomment-4669827167)
- [#23606](https://github.com/sonic-net/sonic-mgmt/pull/23606) Add tests for static route removal after config relo... — was last run 2026-04-04 — 🔄 [/azp run](https://github.com/sonic-net/sonic-mgmt/pull/23606#issuecomment-4669827290)
- [#24091](https://github.com/sonic-net/sonic-mgmt/pull/24091) Adding confed configuration to topo_t2_single_node_m... — was last run 2026-05-12 — 🔄 [/azp run](https://github.com/sonic-net/sonic-mgmt/pull/24091#issuecomment-4669827437)
- [#24217](https://github.com/sonic-net/sonic-mgmt/pull/24217) [Probe] Add xfail for HeadroomPool probe test on SPC... — was last run 2026-05-12 — 🔄 [/azp run](https://github.com/sonic-net/sonic-mgmt/pull/24217#issuecomment-4669827575)
- [#24247](https://github.com/sonic-net/sonic-mgmt/pull/24247) [SNAPPI][AI]Finding the minimum frame size with no p... — was last run 2026-04-29 — 🔄 [/azp run](https://github.com/sonic-net/sonic-mgmt/pull/24247#issuecomment-4669827789)
- [#24357](https://github.com/sonic-net/sonic-mgmt/pull/24357) [mmu probing] Add ProbingBase PG counter false env U... — was last run 2026-05-06 — 🔄 [/azp run](https://github.com/sonic-net/sonic-mgmt/pull/24357#issuecomment-4669827925)
- [#24403](https://github.com/sonic-net/sonic-mgmt/pull/24403) [dhcp_relay]  rework restart_dhcp_service to explici... — was last run 2026-05-07 — 🔄 [/azp run](https://github.com/sonic-net/sonic-mgmt/pull/24403#issuecomment-4669828050)
- [#24507](https://github.com/sonic-net/sonic-mgmt/pull/24507) conftest: fix temporarily_disable_route_check for lt... — was last run 2026-05-11 — 🔄 [/azp run](https://github.com/sonic-net/sonic-mgmt/pull/24507#issuecomment-4669828213)
- [#24591](https://github.com/sonic-net/sonic-mgmt/pull/24591) [qos] Add SONiC fanout ingress ACL to block L2 noise... — was last run 2026-05-19 — 🔄 [/azp run](https://github.com/sonic-net/sonic-mgmt/pull/24591#issuecomment-4669828406)
- [#24649](https://github.com/sonic-net/sonic-mgmt/pull/24649) [dualtor] Add test for tunnel termination drop on st... — was last run 2026-05-18 — 🔄 [/azp run](https://github.com/sonic-net/sonic-mgmt/pull/24649#issuecomment-4669828581)
- [#24687](https://github.com/sonic-net/sonic-mgmt/pull/24687) pfcwd: ignore benign cisco-8000 SAI/orchagent errors... — was last run 2026-05-18 — 🔄 [/azp run](https://github.com/sonic-net/sonic-mgmt/pull/24687#issuecomment-4669828741)
- [#24802](https://github.com/sonic-net/sonic-mgmt/pull/24802) [BGP] Align bgpmon tests with passive DUT peering — was last run 2026-05-22 — 🔄 [/azp run](https://github.com/sonic-net/sonic-mgmt/pull/24802#issuecomment-4669828868)

_Total `/azp run` posted this sweep: 25._

---

## Maintenance policy (sweep rules)

_These are the rules we apply when sweeping this review queue, recorded so future sweeps stay consistent. Last sweep: **2026-06-10**._

**Scope:** open PRs on `sonic-net/sonic-mgmt` where `bhouse-nexthop` is a requested reviewer.

### Rule 1 — Merge conflicts → ping the author
- **Trigger:** PR `mergeable == CONFLICTING`.
- **Action:** comment asking the author to confirm the PR is still relevant and to rebase/resolve conflicts, after which we will review. Mark **awaiting author** in the table.
- **Comment template:** `Hi @{author}, this PR currently has merge conflicts with the target branch. Could you confirm whether it's still relevant/active? If so, please rebase and resolve the conflicts, and we'll review it. Thanks!`
- **Do not** re-ping on every sweep — only ping PRs that newly entered CONFLICTING or that have been silent a long time since the last ping.

### Rule 2 — Clean PR with stale CI → force a fresh CI run
- **Trigger:** PR `mergeable == MERGEABLE` **and** last CI run (max `completedAt` across the status-check rollup) is **> 2 weeks** before the sweep date.
- **Action:** post a `/azp run` comment to force a brand-new full pipeline run.
- **Why `/azp run` (not the GitHub "Re-run failed checks" button):** plain `/azp run` queues a *new* run of **all** repo pipelines (new run number, picks up current YAML/config) — i.e. a full re-run. The "Re-run failed checks" UI button only retries the failed checks against the old run. This is also the repo convention (`mssonicbld` posts `/azp run`). Responses only appear in the PR if the repo uses the Azure Pipelines GitHub App.
- **Note:** `/azp run` is gated by Azure DevOps permissions; if a comment has no effect, the commenter may lack pipeline-trigger rights on that PR.

### Rule 3 — Clean PR with failing CI → force a fresh CI run
- **Trigger:** PR `mergeable == MERGEABLE`, latest CI = **FAIL**, and **not already tagged** this sweep (i.e. not covered by Rule 1 or Rule 2).
- **Action:** post `/azp run` to force a fresh full run (a stale failure may be a flake or already fixed upstream; re-running confirms the real state before we spend review time).
- **Why the "not already tagged" guard:** conflicting PRs (Rule 1) are pinged instead — re-running CI is pointless until the author rebases; stale clean PRs are already re-triggered by Rule 2. This rule only catches the remaining case: clean + failing + CI ran recently (< 2 weeks).
- **Matches on 2026-06-10:** 0 — all failing PRs were either conflicting (pinged via Rule 1) or already `/azp run` via Rule 2. Rule retained for future sweeps.

### Mergeability caveat
- GitHub computes `mergeable` lazily — the first API query often returns `UNKNOWN`. Query once to trigger computation, then re-poll until every PR resolves to `MERGEABLE`/`CONFLICTING` before acting on any rule.

### Re-sweep checklist
1. Re-fetch all requested-reviewer PRs + per-PR CI/review/mergeable.
2. Resolve `UNKNOWN` mergeability (trigger + re-poll).
3. Apply Rule 1 to **newly** conflicting PRs.
4. Apply Rule 2 to clean PRs with CI older than 2 weeks.
5. Apply Rule 3 to clean PRs with failing CI not already tagged by Rule 1/2.
6. Check whether previously-pinged conflict PRs got a rebase / author reply; clear or escalate.
7. Apply Rule 4 (deep review) to the eligible/"fresh" set.
8. Regenerate this file (timestamps + Follow-up column).

### Rule 4 — Deep review of eligible ("fresh") PRs
- **Eligibility (the "fresh" set):** a PR qualifies for deep review only when **all** of: (a) no merge conflicts (`mergeable == MERGEABLE`), (b) latest CI = **PASS**, and (c) CI ran **within the last 2 weeks**. PRs that are conflicting, failing, or stale are handled by Rules 1–3 first and are *not* deep-reviewed until they come back clean+green+fresh.
- **Goal:** confirm the PR actually matches its description and appears to do what it claims, and give the reviewer enough context to triage before approving.
- **For each eligible PR, produce a review brief with these fields:**
  1. **Description summary** — concise restatement of what the PR says it does.
  2. **Existing reviews/comments** — who has reviewed, their state (approved / changes requested / commented), and the gist of any substantive feedback.
  3. **Author affiliation** — the company/org the author is with, if determinable. Sources, in order: GitHub profile `company` field; verified email domain; login suffix convention (`-nexthop`, `-arista`, `-cisco`, `-nvidia`/`-nv`, `-msft`/`-microsoft`, `-nokia`, `[Marvell]`, etc.); org membership. Mark **"unknown"** if not determinable — do not guess.
  4. **PR type** — classify as **Bug fix**, **Feature enhancement**, or **New test suite** (or an explicit mix, e.g. "bug fix + new test").
  5. **Complexity** — **Low / Medium / High**, judged from files touched, lines changed, blast radius, and whether it touches shared fixtures/conftest/common libs vs. an isolated test.
  6. **Matches description?** — does the diff actually do what the description claims? **Yes / Partial / No**, with a one-line note on any mismatch, scope creep, or undisclosed change.
  7. **Conflict likelihood** — **Low / Med / High** chance of merge or logical conflict with other PRs under review, based on overlapping files / touched areas. Name the PRs it overlaps.
  8. **Duplication likelihood** — whether it may duplicate another open PR (same test, same fix, same area). Name the suspected duplicate(s) or "none seen".
- **Output:** present the briefs to the reviewer for triage **before** any approval is given. Approvals remain a human decision.
- **Notes:** judge file-overlap deterministically (compare changed-file lists across the eligible set) to seed the conflict/duplication fields, then have the reviewer reason over the diffs. Affiliation should never be fabricated.

