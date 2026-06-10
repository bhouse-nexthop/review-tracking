# Deep-review prompt template (Rule 4)

Used to drive a per-PR deep review (one agent/pass per PR). Substitute `<N>`.
The reviewer must read the actual diff, not just metadata.

---

Deep-review ONE pull request in the `sonic-net/sonic-mgmt` repo (SONiC network
test-automation). PR number: **<N>**.

Steps:
1. Gather metadata: title, author login + affiliation (resolve per POLICY.md §8;
   never guess — mark "unknown"), description body, existing reviews/comments,
   changed files, +/- line counts. Also compare the changed-file list against
   the other eligible PRs in this sweep for duplication/conflict signal.
2. Run `gh pr diff <N> --repo sonic-net/sonic-mgmt` and read the diff (sample
   representative files if very large).
3. Judge whether the code actually does what the description claims.

Output ONLY this brief:

```
### PR #<N> — <title>
- **Author / affiliation / trust:** <login> / <affiliation> / <Expert|High|Medium|Low|Unproven — from `sweep.py --trust <login>`: merged-PR history + top-20 company bump (capped at High; Expert is individual-only)>
- **Type:** Bug fix | Feature enhancement | New test suite | (mix)
- **Complexity:** Low | Medium | High — <files/LOC/blast radius; flag shared conftest/fixtures/common libs>
- **Description summary:** <2-3 sentences>
- **Existing reviews/comments:** <who + state + gist; or "none">
- **Matches description?:** Yes | Partial | No — <mismatch / scope creep / undisclosed change>
- **Conflict likelihood:** Low | Med | High — <name overlapping eligible PRs, or "file-isolated">
- **Duplication likelihood:** <suspected dup PR# or "none seen"> — <reason>
- **CI actually runs the test?:** Yes | No | Partial | N-A (not a test) — <does the VS/KVM PR-gate execute it, or is it skipped: hardware-only / is_vs_device / platform/ASIC / topology (t2, dualtor) / conditional_mark / skipif / manual? If No/Partial, CI green did NOT validate it → deeper review needed>
- **Reviewer notes:** <1-2 sentences flagging anything for human attention, or "clean">
- **Linked issue(s):** <repo#num (issue/PR, state) — auto-close | MANUAL close on merge | track-only; or "none">
- **Suggested recommendation:** Approve | Request changes | Get another opinion | Reject — <short rationale; if CI doesn't run the test, lean Get-another-opinion / request a real hardware pass>
```

Reviewing rules (see POLICY.md §5 Rule 4):
- **Affiliation-aware:** defer to the author's company on facts about their own
  hardware/platform; still review shared-infra / cross-vendor / correctness.
- **Recommendation** is a suggestion for the human, who makes the call. Use
  "Get another opinion" for domain expertise we lack or broad shared-infra
  changes; "Reject" only for wrong/harmful/duplicative changes.

Do NOT approve, comment, or post anything to GitHub. Return only the brief.
After the review, record it: `helpers/sweep.py --record-review <N> --review-detail review-findings-<date>.md`.
