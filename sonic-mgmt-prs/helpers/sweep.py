#!/usr/bin/env python3
"""
Review-queue sweep tool (see ../../POLICY.md).

Fetches all open PRs where REVIEWER is a requested reviewer on REPO, classifies
each PR, and applies the ledger-gated rules:

  Rule 1  CONFLICTING                       -> conflict_ping  (once per episode)
  Rule 2  clean + stale CI (>2 wks)         -> azp_run        (once per episode)
  Rule 3  clean + failing CI, not retried   -> azp_run        (once per episode)
  Rule 4  clean + passing + fresh           -> deep_review    (once per head SHA)
  Rule 5  azp_run'd PR failed again         -> ci_fail_notify (once per episode)

DRY-RUN BY DEFAULT: prints the plan and never posts or mutates the ledger.
Pass --apply to post comments and append to actions.jsonl. Deep review (Rule 4)
is intentionally NOT automated here -- the tool only flags eligible PRs; the
review itself is driven separately (subagents) and recorded via --record-review.

Usage:
  ./sweep.py                       # dry-run plan + regenerate review-queue.md
  ./sweep.py --apply               # post comments for rules 1,2,3,5; update ledger
  ./sweep.py --record-review 25012 # append a deep_review ledger entry for a PR

Requires: gh (authenticated), python3. No third-party deps.
"""
import argparse, json, subprocess, sys, os, datetime

REPO = os.environ.get("REVIEW_REPO", "sonic-net/sonic-mgmt")
REVIEWER = os.environ.get("REVIEW_REVIEWER", "bhouse-nexthop")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                       # the per-repo dir (sonic-mgmt-prs)
LEDGER = os.path.join(ROOT, "actions.jsonl")
QUEUE_MD = os.path.join(ROOT, "review-queue.md")

STALE_DAYS = 14
ESCALATE_DAYS = 14

PING_TMPL = ("Hi @{author}, this PR currently has merge conflicts with the target "
             "branch. Could you confirm whether it's still relevant/active? If so, "
             "please rebase and resolve the conflicts, and we'll review it. Thanks!")
FAIL_TMPL = ("Hi @{author}, we re-triggered CI on this PR and it's still failing. "
             "Could you take a look at the latest run and address the failures? "
             "Once CI is green we'll proceed with review. Thanks!")
AZP_BODY = "/azp run"

AFFIL_SUFFIX = {"-nexthop": "NextHop", "-arista": "Arista", "-cisco": "Cisco",
                "-nvidia": "NVIDIA", "-nv": "NVIDIA", "-msft": "Microsoft",
                "-microsoft": "Microsoft", "-ms": "Microsoft", "-nokia": "Nokia",
                "-marvell": "Marvell"}


def gh_json(args):
    out = subprocess.run(["gh"] + args, capture_output=True, text=True)
    if out.returncode != 0:
        sys.stderr.write(out.stderr)
        raise SystemExit(f"gh failed: {' '.join(args)}")
    return json.loads(out.stdout) if out.stdout.strip() else None


def today():
    return datetime.date.today().isoformat()


def load_ledger():
    rows = []
    if os.path.exists(LEDGER):
        for line in open(LEDGER):
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def append_ledger(entry):
    with open(LEDGER, "a") as f:
        f.write(json.dumps(entry) + "\n")


def affiliation(login, profile_company):
    c = (profile_company or "").lstrip("@").strip()
    if c:
        return c
    low = login.lower()
    for suf, name in AFFIL_SUFFIX.items():
        if low.endswith(suf):
            return name
    return "unknown"


def ci_state(checks):
    """Return (state, last_completed_iso)."""
    if not checks:
        return ("none", "")
    last = ""
    fail = pend = succ = 0
    for c in checks:
        st = c.get("state")           # StatusContext
        concl = c.get("conclusion")   # CheckRun
        status = c.get("status")
        comp = c.get("completedAt") or ""
        if comp and comp > last:
            last = comp
        if st:
            if st == "SUCCESS":
                succ += 1
            elif st in ("FAILURE", "ERROR"):
                fail += 1
            elif st in ("PENDING", "EXPECTED"):
                pend += 1
        else:
            if status and status != "COMPLETED":
                pend += 1
            elif concl in ("SUCCESS", "NEUTRAL", "SKIPPED"):
                succ += 1
            elif concl in ("FAILURE", "TIMED_OUT", "ACTION_REQUIRED", "STARTUP_FAILURE"):
                fail += 1
            elif concl == "CANCELLED":
                pass
            else:
                pend += 1
    if fail:
        return ("FAIL", last)
    if pend:
        return ("PENDING", last)
    if succ:
        return ("PASS", last)
    return ("none", last)


def fetch_prs():
    prs = gh_json(["pr", "list", "--repo", REPO, "--search",
                   f"review-requested:{REVIEWER}", "--state", "open",
                   "--json", "number", "--limit", "200"]) or []
    nums = [p["number"] for p in prs]
    # trigger mergeable computation (lazy), then fetch full detail
    for n in nums:
        subprocess.run(["gh", "pr", "view", str(n), "--repo", REPO,
                        "--json", "mergeable"], capture_output=True, text=True)
    detail = []
    for n in nums:
        d = gh_json(["pr", "view", str(n), "--repo", REPO, "--json",
                     "number,title,author,mergeable,statusCheckRollup,reviews,"
                     "headRefOid,isDraft"])
        detail.append(d)
    return detail


def resolved_mergeable(d):
    return d.get("mergeable", "UNKNOWN")


def days_since(iso_date):
    if not iso_date:
        return 10**6
    d = datetime.date.fromisoformat(iso_date[:10])
    return (datetime.date.today() - d).days


def has_action_after(ledger, pr, action, after_iso):
    """True if a ledger action for pr exists with date > after_iso[:10]."""
    cut = after_iso[:10] if after_iso else ""
    for e in ledger:
        if e["pr"] == pr and e["action"] == action and e["date"] > cut:
            return True
    return False


def any_action(ledger, pr, action):
    return any(e["pr"] == pr and e["action"] == action for e in ledger)


def last_action_date(ledger, pr, action):
    ds = [e["date"] for e in ledger if e["pr"] == pr and e["action"] == action]
    return max(ds) if ds else None


def classify_and_plan(detail, ledger):
    """Return list of plan dicts: {pr, title, author, state, last_ci, decision, action, reason}."""
    plan = []
    for d in detail:
        pr = d["number"]
        author = (d.get("author") or {}).get("login", "?")
        merge = resolved_mergeable(d)
        state, last = ci_state(d.get("statusCheckRollup"))
        row = {"pr": pr, "title": d["title"], "author": author, "merge": merge,
               "ci": state, "last_ci": last[:10], "action": None, "reason": ""}

        if merge == "UNKNOWN":
            row["action"] = "skip"; row["reason"] = "mergeable UNKNOWN (re-poll)"
        elif merge == "CONFLICTING":
            if any_action(ledger, pr, "conflict_ping"):
                lp = last_action_date(ledger, pr, "conflict_ping")
                if days_since(lp) >= ESCALATE_DAYS:
                    row["action"] = "escalate"
                    row["reason"] = f"pinged {lp}, still conflicting >{ESCALATE_DAYS}d -> escalate to human"
                else:
                    row["action"] = "none"; row["reason"] = f"already pinged {lp}, within window"
            else:
                row["action"] = "conflict_ping"; row["reason"] = "Rule 1: new conflict"
        elif state == "FAIL":
            # was it azp_run'd in this failing episode (azp after last ci)?
            if has_action_after(ledger, pr, "azp_run", last):
                if has_action_after(ledger, pr, "ci_fail_notify", last):
                    row["action"] = "none"; row["reason"] = "Rule 5: already notified this failing run"
                else:
                    row["action"] = "ci_fail_notify"; row["reason"] = "Rule 5: failed after our /azp run"
            else:
                row["action"] = "azp_run"; row["reason"] = "Rule 3: clean+failing, not yet retried"
        elif state == "PASS":
            if days_since(last) > STALE_DAYS:
                if has_action_after(ledger, pr, "azp_run", last):
                    row["action"] = "none"; row["reason"] = "Rule 2: already re-triggered this episode"
                else:
                    row["action"] = "azp_run"; row["reason"] = "Rule 2: clean+stale CI"
            else:
                # fresh & eligible
                sha = d.get("headRefOid", "")
                reviewed = any(e["pr"] == pr and e["action"] == "deep_review"
                               and e.get("sha", "") in ("", sha) for e in ledger)
                if reviewed:
                    row["action"] = "none"; row["reason"] = "Rule 4: already deep-reviewed (current SHA)"
                else:
                    row["action"] = "deep_review"; row["reason"] = "Rule 4: ELIGIBLE for deep review"
        elif state == "PENDING":
            row["action"] = "none"; row["reason"] = "CI run in flight; wait"
        else:
            row["action"] = "none"; row["reason"] = f"CI={state}"
        plan.append(row)
    return plan


def post_comment(pr, body):
    out = subprocess.run(["gh", "pr", "comment", str(pr), "--repo", REPO,
                          "--body", body], capture_output=True, text=True)
    if out.returncode != 0:
        sys.stderr.write(out.stderr)
        return None
    return out.stdout.strip()


def execute(plan, apply):
    for row in plan:
        act = row["action"]
        if act in (None, "none", "skip", "escalate", "deep_review"):
            continue  # deep_review is recorded separately after the review runs
        body = {"conflict_ping": PING_TMPL.format(author=row["author"]),
                "ci_fail_notify": FAIL_TMPL.format(author=row["author"]),
                "azp_run": AZP_BODY}[act]
        if not apply:
            print(f"  WOULD {act:14} #{row['pr']}: {body[:60]}")
            continue
        url = post_comment(row["pr"], body)
        if url:
            append_ledger({"pr": row["pr"], "action": act, "date": today(), "detail": url})
            print(f"  DID  {act:14} #{row['pr']}: {url}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="post comments + update ledger")
    ap.add_argument("--record-review", type=int, metavar="PR",
                    help="append a deep_review ledger entry for PR (after a review is done)")
    ap.add_argument("--review-detail", default="", help="detail string for --record-review")
    ap.add_argument("--no-render", action="store_true", help="skip writing review-queue.md")
    args = ap.parse_args()

    if args.record_review:
        append_ledger({"pr": args.record_review, "action": "deep_review",
                       "date": today(), "detail": args.review_detail})
        print(f"recorded deep_review for #{args.record_review}")
        return

    ledger = load_ledger()
    detail = fetch_prs()
    plan = classify_and_plan(detail, ledger)

    print(f"# Sweep {today()} — {REPO} — reviewer:{REVIEWER} — {len(plan)} PRs "
          f"({'APPLY' if args.apply else 'DRY-RUN'})\n")
    from collections import Counter
    c = Counter(r["action"] for r in plan)
    print("plan:", dict(c), "\n")
    for r in sorted(plan, key=lambda x: x["action"] or ""):
        if r["action"] not in ("none", None):
            print(f"  [{r['action']:14}] #{r['pr']:5} {r['merge']:11} CI={r['ci']:7} "
                  f"last={r['last_ci'] or '—':10} — {r['reason']}")
    print()
    execute(plan, args.apply)

    if not args.no_render:
        render_table(detail, plan, ledger)
        print(f"\nwrote {QUEUE_MD}")


def render_table(detail, plan, ledger):
    pmap = {r["pr"]: r for r in plan}
    rows = sorted(detail, key=lambda d: -d["number"])
    out = [f"# {REPO} — PRs awaiting review (`{REVIEWER}`)\n",
           f"_Generated {today()}. See ../POLICY.md for the rules._\n",
           "| PR | Title | Author | CI | Last CI | Merge | Next action | Last logged action |",
           "|----|-------|--------|----|---------|-------|-------------|--------------------|"]
    for d in rows:
        pr = d["number"]
        r = pmap[pr]
        title = d["title"].replace("|", "\\|")
        if len(title) > 55:
            title = title[:52] + "..."
        merge = {"CONFLICTING": "⚠️ conflict", "MERGEABLE": "✅ clean"}.get(d.get("mergeable"), "—")
        acts = [e for e in ledger if e["pr"] == pr]
        last_act = max(acts, key=lambda e: e["date"]) if acts else None
        la = f'{last_act["action"]} {last_act["date"]}' if last_act else "—"
        nxt = r["action"] if r["action"] not in ("none", None) else "—"
        out.append(f"| [#{pr}](https://github.com/{REPO}/pull/{pr}) | {title} | "
                   f"{(d.get('author') or {}).get('login','?')} | {r['ci']} | "
                   f"{r['last_ci'] or '—'} | {merge} | {nxt} | {la} |")
    with open(QUEUE_MD, "w") as f:
        f.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
