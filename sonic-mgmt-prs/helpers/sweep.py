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
import argparse, json, subprocess, sys, os, datetime, re

REPO = os.environ.get("REVIEW_REPO", "sonic-net/sonic-mgmt")
REVIEWER = os.environ.get("REVIEW_REVIEWER", "bhouse-nexthop")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                       # the per-repo dir (sonic-mgmt-prs)
LEDGER = os.path.join(ROOT, "actions.jsonl")
QUEUE_MD = os.path.join(ROOT, "review-queue.md")

STALE_DAYS = 14
ESCALATE_DAYS = 14
NOTIFY_COOLDOWN_DAYS = 3   # don't re-notify the same failing PR within this window

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


def now_ts():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def entry_ts(e):
    """Full-timestamp of a ledger entry; legacy date-only entries -> start of day."""
    return e.get("ts") or (e["date"] + "T00:00:00Z")


def load_ledger():
    rows = []
    if os.path.exists(LEDGER):
        for line in open(LEDGER):
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def append_ledger(entry):
    entry.setdefault("ts", now_ts())
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


CLOSE_KW = r'(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)'
_kw = re.compile(CLOSE_KW + r'\s*:?\s+(?:https?://github\.com/([\w.-]+/[\w.-]+)/issues/(\d+)'
                 r'|([\w.-]+/[\w.-]+)#(\d+)|#(\d+))', re.I)
_url = re.compile(r'https?://github\.com/([\w.-]+/[\w.-]+)/issues/(\d+)', re.I)
_cross = re.compile(r'\b([\w.-]+/[\w.-]+)#(\d+)\b')
_hash = re.compile(r'(?<![\w/])#(\d+)\b')


def extract_issue_refs(body, title):
    """Return {(repo,num): has_closing_keyword} from PR body+title."""
    text = (title or "") + "\n" + (body or "")
    refs = {}
    for m in _kw.finditer(text):
        if m.group(2):
            repo, num = m.group(1), m.group(2)
        elif m.group(4):
            repo, num = m.group(3), m.group(4)
        else:
            repo, num = REPO, m.group(5)
        refs[(repo.lower(), num)] = True
    for m in _url.finditer(text):
        refs.setdefault((m.group(1).lower(), m.group(2)), False)
    for m in _cross.finditer(text):
        refs.setdefault((m.group(1).lower(), m.group(2)), False)
    for m in _hash.finditer(text):
        refs.setdefault((REPO, m.group(1)), False)
    return refs


def ref_type_state(repo, num):
    """('issue'|'pr'|'missing', state) via API."""
    d = gh_json(["api", f"repos/{repo}/issues/{num}"]) if True else None
    if not d:
        return ("missing", "")
    return ("pr" if d.get("pull_request") else "issue", d.get("state", ""))


def close_candidates(refs, merged_to_default=True):
    """Resolve refs to a list of issues needing MANUAL close on merge.
    Returns (candidates, autoclosers, notes). Network: one API call per ref."""
    cands, autos, notes = [], [], []
    for (repo, num), kw in sorted(refs.items()):
        typ, state = ref_type_state(repo, num)
        tag = f"{repo}#{num}"
        if typ != "issue":
            notes.append(f"{tag} ({typ})")        # PR ref or missing -> track only
            continue
        same = (repo == REPO)
        if same and kw and merged_to_default:
            autos.append(tag)                       # GitHub will auto-close
        else:
            reason = "cross-repo" if not same else ("no keyword" if not kw else "non-default branch")
            cands.append(f"{tag} [{state}] ({reason})")
    return cands, autos, notes


_affil_cache = {}
_author_map = None
AUTHOR_MAP_CSV = os.path.join(ROOT, "data", "author_org_map.csv")


def load_author_map():
    """SII author->org map (sonic-tsc); login(lowercase) -> org. 'null' filtered out.
    Refresh: gh api repos/sonic-net/sonic-tsc/contents/sii_author_map/author.csv
             --jq .content | base64 -d > data/author_org_map.csv"""
    global _author_map
    if _author_map is not None:
        return _author_map
    _author_map = {}
    if os.path.exists(AUTHOR_MAP_CSV):
        import csv
        with open(AUTHOR_MAP_CSV, newline="") as f:
            for row in csv.reader(f):
                if len(row) >= 3 and row[0] and row[2] and row[2] != "null":
                    _author_map[row[0].lower()] = row[2].strip()
    return _author_map


def affil_of(login):
    """Resolve a login's affiliation (cached). Order: SII author->org map (authoritative)
    -> GitHub profile company -> login-suffix heuristic -> unknown."""
    if not login:
        return "unknown"
    if login in _affil_cache:
        return _affil_cache[login]
    org = load_author_map().get(login.lower())
    if not org:
        d = gh_json(["api", f"users/{login}"]) or {}
        org = affiliation(login, d.get("company"))
    _affil_cache[login] = org
    return org


def is_nexthop(login, affil=None):
    a = (affil or affil_of(login) or "").lower()
    return "nexthop" in a or (login or "").lower().endswith("-nexthop")


_top_orgs = None
ORG_PREDICT_CSV = os.path.join(ROOT, "data", "sii_org_predict.csv")
MIN_COMPANY_SCORE = 1500.0


def load_top_companies():
    """SONiC contributor orgs with sii_org_predict score > MIN_COMPANY_SCORE,
    EXCLUDING 'Others'. Returns a list of (org_lower, rank) — rank is overall
    position by score among non-Others orgs."""
    global _top_orgs
    if _top_orgs is not None:
        return _top_orgs
    rows = []
    if os.path.exists(ORG_PREDICT_CSV):
        import csv
        with open(ORG_PREDICT_CSV, newline="") as f:
            r = csv.reader(f)
            next(r, None)                                   # header: Organization,Score
            for row in r:
                if len(row) >= 2 and row[0].strip().lower() != "others":
                    try:
                        rows.append((row[0].strip(), float(row[1])))
                    except ValueError:
                        pass
    rows.sort(key=lambda x: -x[1])
    _top_orgs = [(o.lower(), i + 1) for i, (o, s) in enumerate(rows) if s > MIN_COMPANY_SCORE]
    return _top_orgs


def top_company_rank(affil):
    """If the affiliation matches a contributor company with score > MIN_COMPANY_SCORE,
    return its rank, else None."""
    if not affil or affil.lower() == "unknown":
        return None
    a = affil.lower()
    for org, rank in load_top_companies():
        first = org.split()[0]
        if org in a or a in org or first == a.split()[0]:
            return rank
    return None


def author_merged_count(login):
    """Number of the author's MERGED PRs in the repo (capped at 100 for tiering)."""
    out = gh_json(["search", "prs", "--repo", REPO, "--author", login,
                   "--merged", "--limit", "100", "--json", "number"]) or []
    return len(out)


def author_trust(login):
    """Trust = primarily merged-PR history, with a one-level bump for a top-20 company.
    Returns (level, detail-dict). Never overrides hard gates (CI-coverage, COI, etc.)."""
    merged = author_merged_count(login)
    affil = affil_of(login)
    rank = top_company_rank(affil)
    top = rank is not None
    LADDER = ["Unproven", "Low", "Medium", "High", "Expert"]
    if merged >= 50:
        base = "Expert"
    elif merged >= 25:
        base = "High"
    elif merged >= 8:
        base = "Medium"
    elif merged >= 1:
        base = "Low"
    else:
        base = "Unproven"
    # secondary: one-level bump up the ladder for a top-20 company, BUT capped at
    # High — Expert is an individual-only achievement (merge history), never granted
    # by company. Unproven is never bumped (a top-company first-timer still proves it).
    level = base
    if top and base != "Unproven":
        i = min(LADDER.index(base) + 1, LADDER.index("High"))
        if i > LADDER.index(base):
            level = LADDER[i]
    return level, {"login": login, "merged_prs": merged, "affiliation": affil,
                   "top_company": top, "company_rank": rank, "base": base}


def has_write_access(login):
    """Best-effort: does this user have write/maintain/admin on the repo?"""
    d = gh_json(["api", f"repos/{REPO}/collaborators/{login}/permission"]) or {}
    return d.get("permission") in ("write", "maintain", "admin")


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
                     "headRefOid,isDraft,body,baseRefName"])
        detail.append(d)
    return detail


def resolved_mergeable(d):
    return d.get("mergeable", "UNKNOWN")


def days_since(iso_date):
    if not iso_date:
        return 10**6
    d = datetime.date.fromisoformat(iso_date[:10])
    return (datetime.date.today() - d).days


def any_action(ledger, pr, action):
    return any(e["pr"] == pr and e["action"] == action for e in ledger)


def last_action_date(ledger, pr, action):
    ds = [e["date"] for e in ledger if e["pr"] == pr and e["action"] == action]
    return max(ds) if ds else None


def last_action_ts(ledger, pr, action):
    """Full timestamp of the most recent matching action, or None."""
    ts = [entry_ts(e) for e in ledger if e["pr"] == pr and e["action"] == action]
    return max(ts) if ts else None


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
            azp_ts = last_action_ts(ledger, pr, "azp_run")
            notify_ts = last_action_ts(ledger, pr, "ci_fail_notify")
            cmp_last = last or ""
            if azp_ts is None:
                # never triggered -> retry once to confirm the failure is real
                row["action"] = "azp_run"; row["reason"] = "Rule 3: clean+failing, not yet retried"
            elif azp_ts < cmp_last:
                # this failing run completed AFTER our /azp run -> the re-run failed
                notify_date = last_action_date(ledger, pr, "ci_fail_notify")
                in_cooldown = notify_date and days_since(notify_date) < NOTIFY_COOLDOWN_DAYS
                if (notify_ts and notify_ts >= cmp_last) or in_cooldown:
                    row["action"] = "none"; row["reason"] = "Rule 5: already notified (or within cooldown)"
                else:
                    row["action"] = "ci_fail_notify"; row["reason"] = "Rule 5: failed after our /azp run"
            else:
                # we triggered after this run; a newer run should be in flight
                row["action"] = "none"; row["reason"] = "re-run triggered; awaiting new result"
        elif state == "PASS":
            if days_since(last) > STALE_DAYS:
                azp_ts = last_action_ts(ledger, pr, "azp_run")
                if azp_ts and azp_ts > (last or ""):
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


WEAK_MSG = re.compile(r'^(wip|fix(es|ed)?|update|changes?|address(ed)? comments?|review comments?|'
                      r'minor|cleanup|\.+|tmp|temp|test)\.?$', re.I)


def pr_commits(pr):
    d = gh_json(["pr", "view", str(pr), "--repo", REPO, "--json", "commits"]) or {}
    return d.get("commits", [])


def commit_signoff_author(commits):
    """(name, email) for the Signed-off-by, from the PR's commit author metadata."""
    for c in commits:
        for a in (c.get("authors") or []):
            if a.get("email") and a.get("name"):
                return a["name"], a["email"]
    return None, None


def dco_status(checks):
    """Authoritative sign-off signal: the repo's DCO check conclusion (or None)."""
    for c in checks or []:
        if (c.get("name") or c.get("context")) == "DCO":
            return c.get("conclusion") or c.get("state")
    return None


def compose_squash_message(d, commits):
    """Return (subject, body) for the squash commit, preferring the author's
    commit message, guaranteeing a Signed-off-by, and never a Co-authored-by."""
    if len(commits) == 1:
        subject = commits[0].get("messageHeadline") or d["title"]
        body_src = commits[0].get("messageBody") or ""
    else:
        subject = d["title"]
        body_src = "\n".join(f"- {c.get('messageHeadline','')}" for c in commits)
    # strip any Co-authored-by lines and collect existing Signed-off-by lines
    body_lines, signoffs = [], []
    for ln in body_src.splitlines():
        if re.match(r'\s*Co-authored-by:', ln, re.I):
            continue
        if re.match(r'\s*Signed-off-by:', ln, re.I):
            signoffs.append(ln.strip())
            continue
        body_lines.append(ln)
    if not signoffs:
        name, email = commit_signoff_author(commits)
        if email:
            signoffs.append(f"Signed-off-by: {name} <{email}>")
    body = "\n".join(body_lines).strip()
    if signoffs:
        body = (body + "\n\n" + "\n".join(dict.fromkeys(signoffs))).strip()
    return subject, body


def merge_pr(pr, apply):
    """Squash-merge (or rebase for large auditable PRs) after verifying preconditions."""
    d = gh_json(["pr", "view", str(pr), "--repo", REPO, "--json",
                 "title,author,mergeable,reviewDecision,isDraft,statusCheckRollup,"
                 "additions,deletions,headRefName,baseRefName,reviews"])
    if not d:
        raise SystemExit(f"PR #{pr} not found")
    # mergeable is lazy: re-poll a few times if UNKNOWN
    tries = 0
    while d.get("mergeable") == "UNKNOWN" and tries < 4:
        tries += 1
        d2 = gh_json(["pr", "view", str(pr), "--repo", REPO, "--json", "mergeable"]) or {}
        d["mergeable"] = d2.get("mergeable", "UNKNOWN")
    ci, _ = ci_state(d.get("statusCheckRollup"))
    ledger = load_ledger()
    miss = []
    if d.get("reviewDecision") != "APPROVED":
        miss.append(f"reviewDecision={d.get('reviewDecision')} (need human APPROVED)")
    if d.get("mergeable") != "MERGEABLE":
        miss.append(f"mergeable={d.get('mergeable')}")
    if ci != "PASS":
        miss.append(f"CI={ci}")
    if d.get("isDraft"):
        miss.append("draft")
    if any(e["pr"] == pr and e["action"] == "misleading_flag" for e in ledger):
        miss.append("open misleading_flag (not reviewable)")
    # Cross-company (COI) gate: a NextHop-authored PR needs a non-NextHop approval
    author_login = (d.get("author") or {}).get("login", "")
    if is_nexthop(author_login):
        latest = {}
        for rv in (d.get("reviews") or []):
            who = (rv.get("author") or {}).get("login")
            if who:
                latest[who] = rv.get("state")
        approvers = [w for w, s in latest.items() if s == "APPROVED"]
        cross = [w for w in approvers if not is_nexthop(w)]
        if not cross:
            miss.append(f"NextHop-authored PR ({author_login}) lacks a non-NextHop "
                        f"approval (COI) — run: sweep.py --suggest-reviewers {pr}")
    if miss:
        print(f"#{pr}: NOT merging — preconditions unmet: {'; '.join(miss)}")
        return
    commits = pr_commits(pr)
    total = (d.get("additions", 0) or 0) + (d.get("deletions", 0) or 0)
    rebase = (total > 1000 and len(commits) > 1)
    method = "rebase" if rebase else "squash"
    subject, body = compose_squash_message(d, commits)
    print(f"#{pr}: merge method = {method}  (lines={total}, commits={len(commits)})")
    if rebase:
        print("  large + multi-commit: preserving commits (verify they're independently auditable)")
        print("  each commit keeps its own message + Signed-off-by")
    else:
        print(f"  squash subject: {subject}")
        print("  squash body:\n    " + body.replace("\n", "\n    "))
    if not apply:
        print("  (dry-run — pass --apply to merge)")
        return
    if rebase:
        cmd = ["gh", "pr", "merge", str(pr), "--repo", REPO, "--rebase"]
    else:
        cmd = ["gh", "pr", "merge", str(pr), "--repo", REPO, "--squash",
               "--subject", subject, "--body", body]
    out = subprocess.run(cmd, capture_output=True, text=True)
    if out.returncode != 0:
        sys.stderr.write(out.stderr); raise SystemExit("merge failed")
    append_ledger({"pr": pr, "action": "merge", "date": today(), "detail": f"{method}: {subject}"})
    print(f"  MERGED (#{pr}, {method}).")
    # close-on-merge for linked issues (Rule 6)
    close_issues_for_merged_pr(pr, apply=True)


def suggest_reviewers(pr):
    """List candidate external (non-NextHop) reviewers who recently contributed to
    the paths this PR touches — for the cross-company gate (Rule 8)."""
    d = gh_json(["pr", "view", str(pr), "--repo", REPO,
                 "--json", "files,author,title"]) or {}
    author = (d.get("author") or {}).get("login", "")
    files = [f["path"] for f in (d.get("files") or [])]
    # touched paths: the files themselves + their immediate dirs
    paths = set(files)
    for f in files:
        parts = f.split("/")
        for depth in (3, 2):                          # narrow then broader parent dir
            if len(parts) > depth:
                paths.add("/".join(parts[:depth]))
    print(f"# Suggested cross-company reviewers for #{pr} — {d.get('title','')}")
    print(f"# author: {author} ({affil_of(author)}); touched {len(files)} file(s)\n")
    tally = {}
    for p in sorted(paths):
        commits = gh_json(["api", f"repos/{REPO}/commits?path={p}&per_page=20"]) or []
        for c in commits:
            login = ((c.get("author") or {}) or {}).get("login")
            if login:
                tally[login] = tally.get(login, 0) + 1
    cands = []
    for login, cnt in tally.items():
        if login == author or login.endswith("[bot]") or login in ("mssonicbld",):
            continue
        a = affil_of(login)
        if is_nexthop(login, a):
            continue
        cands.append((cnt, login, a))
    cands.sort(reverse=True)
    if not cands:
        print("(no non-NextHop recent contributors found in these paths)")
        return
    print(f"{'commits':>7}  {'login':22} {'affiliation':18} write-access?")
    for cnt, login, a in cands[:8]:
        wa = "yes" if has_write_access(login) else "?"
        print(f"{cnt:>7}  {login:22} {a:18} {wa}")
    print("\nRequest a review from one of the above (gh pr edit --add-reviewer <login>) "
          "or tag them in a comment.")


COMMIT_MSG_NOTICE = (
    "Heads-up on commit-message hygiene: please make sure each commit has a "
    "clear, descriptive message and a `Signed-off-by: Full Name <email>` trailer "
    "(the DCO check requires the sign-off). On merge we squash and **prefer your "
    "commit message** as the permanent record, so a meaningful message helps "
    "everyone later. Please also avoid `Co-authored-by` lines. Fixing this now "
    "(a quick interactive rebase / amend) keeps things moving — thanks!")


def commit_hygiene_issues(commits, dco):
    """Return specific problems with a PR's commit messages, or [].
    Sign-off compliance comes from the repo's DCO check (authoritative), NOT from
    parsing commit bodies (gh under-reports trailers; merge commits lack signoff)."""
    problems = []
    weak = [c.get("messageHeadline", "") for c in commits
            if WEAK_MSG.match((c.get("messageHeadline") or "").strip())]
    if weak:
        problems.append(f"non-descriptive commit subject(s): {weak}")
    if dco == "FAILURE":
        problems.append("DCO check failing (missing/invalid Signed-off-by)")
    return problems


def commit_hygiene_sweep(pr_list, ledger, apply):
    """Per-sweep (Rule 9): post a one-time commit-message policy notice to PRs with
    weak/missing-signoff commit messages, so the author can fix it BEFORE merge."""
    posted = 0
    for d in pr_list:
        pr = d["number"]
        if any(e["pr"] == pr and e["action"] == "commit_msg_notice" for e in ledger):
            continue                                   # already notified (idempotent)
        problems = commit_hygiene_issues(pr_commits(pr), dco_status(d.get("statusCheckRollup")))
        if not problems:
            continue
        if not apply:
            print(f"  WOULD commit_msg_notice #{pr}: {'; '.join(problems)}")
            continue
        url = post_comment(pr, COMMIT_MSG_NOTICE)
        if url:
            append_ledger({"pr": pr, "action": "commit_msg_notice", "date": today(), "detail": url})
            posted += 1
            print(f"  DID  commit_msg_notice #{pr}: {url}")
    return posted


def report_commit_hygiene():
    """Flag PRs whose commit messages are weak or missing Signed-off-by (Rule 9)."""
    lst = gh_json(["pr", "list", "--repo", REPO, "--search",
                   f"review-requested:{REVIEWER}", "--state", "open",
                   "--json", "number,author,statusCheckRollup", "--limit", "200"]) or []
    print(f"# Commit-message hygiene — {REPO} (Rule 9)\n")
    for d in sorted(lst, key=lambda x: -x["number"]):
        problems = commit_hygiene_issues(pr_commits(d["number"]), dco_status(d.get("statusCheckRollup")))
        if problems:
            print(f"#{d['number']} ({(d.get('author') or {}).get('login','?')}) — {'; '.join(problems)}")


def report_issue_linkage():
    """Print, per PR, linked issues and which need a MANUAL close on merge."""
    detail = fetch_prs()
    print(f"# Issue linkage — {REPO} (Rule 6)\n")
    any_manual = False
    for d in sorted(detail, key=lambda x: -x["number"]):
        refs = extract_issue_refs(d.get("body"), d.get("title"))
        if not refs:
            continue
        default = (d.get("baseRefName") in ("master", "main"))
        cands, autos, notes = close_candidates(refs, merged_to_default=default)
        if not (cands or autos or notes):
            continue
        print(f"#{d['number']} {d['title'][:60]}")
        if autos:
            print(f"   auto-close on merge: {', '.join(autos)}")
        if cands:
            any_manual = True
            print(f"   ** MANUAL close on merge: {', '.join(cands)}")
        if notes:
            print(f"   refs (not issues / track-only): {', '.join(notes)}")
    if not any_manual:
        print("\nNo manual-close candidates among open PRs.")


def close_issues_for_merged_pr(pr, apply):
    """For a merged PR, close its manual-close issue candidates and log issue_close."""
    d = gh_json(["pr", "view", str(pr), "--repo", REPO,
                 "--json", "title,body,baseRefName,state,mergedAt"])
    if not d:
        raise SystemExit(f"PR #{pr} not found")
    if not d.get("mergedAt"):
        raise SystemExit(f"PR #{pr} is not merged ({d.get('state')}); refusing to close issues")
    refs = extract_issue_refs(d.get("body"), d.get("title"))
    default = (d.get("baseRefName") in ("master", "main"))
    cands, autos, notes = close_candidates(refs, merged_to_default=default)
    ledger = load_ledger()
    print(f"#{pr} merged. auto-close: {autos or 'none'} | manual: {cands or 'none'}"
          f"{' | track-only: ' + ', '.join(notes) if notes else ''}")
    for c in cands:
        ref = c.split()[0]                       # "owner/repo#num [state] (reason)"
        if any(e["pr"] == pr and e["action"] == "issue_close" and e.get("detail", "").startswith(ref)
               for e in ledger):
            print(f"   already closed {ref}; skip")
            continue
        repo, num = ref.rsplit("#", 1)
        msg = f"Resolved by {REPO}#{pr} (merged)."
        if not apply:
            print(f"   WOULD close {ref}: {msg}")
            continue
        out = subprocess.run(["gh", "issue", "close", num, "--repo", repo, "-c", msg],
                             capture_output=True, text=True)
        if out.returncode == 0:
            append_ledger({"pr": pr, "action": "issue_close", "date": today(), "detail": ref})
            print(f"   closed {ref}")
        else:
            sys.stderr.write(out.stderr)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="post comments + update ledger")
    ap.add_argument("--record-review", type=int, metavar="PR",
                    help="append a deep_review ledger entry for PR (after a review is done)")
    ap.add_argument("--review-detail", default="", help="detail string for --record-review")
    ap.add_argument("--no-render", action="store_true", help="skip writing review-queue.md")
    ap.add_argument("--issues", action="store_true",
                    help="report issue linkage + manual-close-on-merge candidates (uses API)")
    ap.add_argument("--close-issues", type=int, metavar="PR",
                    help="after MERGE: close the manual-close issue candidates for PR + log issue_close")
    ap.add_argument("--merge", type=int, metavar="PR",
                    help="squash-merge (rebase if large+auditable) PR after checking preconditions (Rule 8)")
    ap.add_argument("--commits", action="store_true",
                    help="report commit-message hygiene across the queue (Rule 9)")
    ap.add_argument("--suggest-reviewers", type=int, metavar="PR",
                    help="list candidate non-NextHop reviewers for a NextHop PR (Rule 8 cross-company gate)")
    ap.add_argument("--trust", metavar="LOGIN",
                    help="compute an author's trust level (merge history + top-20 company)")
    args = ap.parse_args()

    if args.trust:
        level, d = author_trust(args.trust)
        print(f"{args.trust}: TRUST={level}  (merged PRs={d['merged_prs']}, "
              f"affiliation={d['affiliation']}, top-company(score>1500)={d['top_company']}"
              f"{' rank #'+str(d['company_rank']) if d['company_rank'] else ''})")
        return

    if args.merge:
        merge_pr(args.merge, args.apply)
        return
    if args.suggest_reviewers:
        suggest_reviewers(args.suggest_reviewers)
        return
    if args.commits:
        report_commit_hygiene()
        return
    if args.close_issues:
        close_issues_for_merged_pr(args.close_issues, args.apply)
        return
    if args.issues:
        report_issue_linkage()
        return
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

    # Rule 9: commit-message hygiene runs as part of the sweep (NOT at merge), so
    # the author gets a chance to fix it before the PR is ready to merge.
    print("\ncommit-message hygiene (Rule 9):")
    commit_hygiene_sweep(detail, ledger, args.apply)
    if not args.apply:
        print("  (dry-run — pass --apply to post commit-message notices)")

    if not args.no_render:
        render_table(detail, plan, ledger)
        print(f"\nwrote {QUEUE_MD}")


def render_table(detail, plan, ledger):
    pmap = {r["pr"]: r for r in plan}
    rows = sorted(detail, key=lambda d: -d["number"])
    out = [f"# {REPO} — PRs awaiting review (`{REVIEWER}`)\n",
           f"_Generated {today()}. See ../POLICY.md for the rules._\n",
           "| PR | Title | Author | CI | Last CI | Merge | Reviews | Linked issues | Next action | Last logged action |",
           "|----|-------|--------|----|---------|-------|---------|---------------|-------------|--------------------|"]
    for d in rows:
        pr = d["number"]
        r = pmap[pr]
        title = d["title"].replace("|", "\\|")
        if len(title) > 55:
            title = title[:52] + "..."
        merge = {"CONFLICTING": "⚠️ conflict", "MERGEABLE": "✅ clean"}.get(d.get("mergeable"), "—")
        # linked issues (regex only; ⚑ = closing keyword present). Resolve
        # issue-vs-PR + manual-close disposition with `sweep.py --issues`.
        refs = extract_issue_refs(d.get("body"), d.get("title"))
        if refs:
            li = ", ".join((f"{rp}#{nm}".replace(REPO + "#", "#")) + ("⚑" if kw else "")
                           for (rp, nm), kw in sorted(refs.items()))
        else:
            li = "—"
        # latest review state per author
        latest = {}
        for rv in (d.get("reviews") or []):
            who = (rv.get("author") or {}).get("login")
            if who:
                latest[who] = rv.get("state")
        appr = [w for w, s in latest.items() if s == "APPROVED"]
        chg = [w for w, s in latest.items() if s == "CHANGES_REQUESTED"]
        rev = ", ".join(f"✓{w}" for w in appr) + (" " if appr and chg else "") + \
              ", ".join(f"✗{w}" for w in chg)
        rev = rev or "—"
        acts = [e for e in ledger if e["pr"] == pr]
        last_act = max(acts, key=lambda e: e["date"]) if acts else None
        la = f'{last_act["action"]} {last_act["date"]}' if last_act else "—"
        nxt = r["action"] if r["action"] not in ("none", None) else "—"
        out.append(f"| [#{pr}](https://github.com/{REPO}/pull/{pr}) | {title} | "
                   f"{(d.get('author') or {}).get('login','?')} | {r['ci']} | "
                   f"{r['last_ci'] or '—'} | {merge} | {rev} | {li} | {nxt} | {la} |")
    with open(QUEUE_MD, "w") as f:
        f.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
