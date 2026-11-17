#!/usr/bin/env python3
"""agy_gate.py — quality gate between "worker finished" and "merge".

  prepare ID        run the task's `accept` commands, mechanical scope check, fingerprint the worktree,
                    write .agy/ID.evidence.json and the reviewer prompt .agy/ID.reviewer.txt
  score ID          read the reviewer's .agy/ID.review.json, validate it, compute the verdict
                    (PASS | REWORK | ESCALATE) per references/rubric.md, write .agy/ID.gate.json
  rework-prompt ID  write the step-by-step rework prompt for a REWORK verdict (used by `agy_parallel.py rework`)
  show ID           print the last verdict

Exit: 0 ok / PASS · 1 REWORK · 4 ESCALATE · 3 invalid review/evidence · 2 usage/setup error.
Manifest tasks need `accept`: list of shell commands (run in the task worktree) that must exit 0.
"""
import argparse, hashlib, json, os, subprocess, sys

# Acceptance commands run worker-written tests. Run them in their own PID namespace when
# possible, so a test that signals kill(-1) cannot take down the user's whole session.
_SB = ["unshare", "--user", "--map-root-user", "--pid", "--fork", "--mount-proc"]
try:
    _SANDBOX = _SB if subprocess.run([*_SB, "true"], capture_output=True).returncode == 0 else []
except OSError:
    _SANDBOX = []

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import agy_parallel as P  # noqa: E402

REFS = os.path.join(os.path.dirname(HERE), "references")
RUBRIC = {  # criterion: (weight, floor) — keep in sync with references/rubric.md
    "correctness": (25, 3), "spec_compliance": (20, 3), "tests": (15, 2), "robustness": (10, 2),
    "code_quality": (10, 2), "scope_discipline": (10, 3), "security": (5, 3), "consistency": (5, 2),
}
THRESHOLD = 85
MAX_ATTEMPTS = 3
SEV = {"blocker": 0, "major": 1, "minor": 2}


def die(msg, rc=2):
    print(msg); sys.exit(rc)


def ap(m, tid, suffix):
    return os.path.join(m["workdir"], ".agy", f"{tid}.{suffix}")


def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def load_gate(m, tid):
    return load_json(ap(m, tid, "gate.json"))


def junk(p):
    return "__pycache__" in p or p.endswith((".pyc", ".log")) or p.startswith(".agy/")


def changed_files(wt):
    out = P.sh(["git", "status", "--porcelain", "-uall"], cwd=wt).stdout.splitlines()
    return sorted(p for p in (l[3:].split(" -> ")[-1].strip('"') for l in out) if not junk(p))


def fingerprint(wt):
    h = hashlib.sha256()
    for p in changed_files(wt):
        h.update(p.encode() + b"\0")
        try:
            with open(os.path.join(wt, p), "rb") as f:
                h.update(f.read())
        except (IsADirectoryError, FileNotFoundError):
            h.update(b"<gone>")
    return h.hexdigest()[:16]


def task_and_dir(m, tid):
    t = next((x for x in m["tasks"] if x["id"] == tid), None)
    if not t:
        die(f"unknown task {tid}")
    s = P.load_state(m).get(tid, {})
    if s.get("state") not in ("done", "failed"):
        die(f"{tid}: state is {s.get('state')!r}; run it first")
    wt = s.get("dir") or P.worktree_dir(m, tid)
    if not P.is_git(wt):
        die("the review gate needs a git worktree (run the batch in a git repo)")
    return t, wt


def cmd_prepare(m, tid):
    t, wt = task_and_dir(m, tid)
    acc = t.get("accept") or []
    if not acc:
        die(f"{tid}: manifest task has no `accept` commands — define at least one runnable check")
    res = []
    for c in acc:
        try:
            # In the sandbox, bash is PID 1 and must stay alive to reap orphans: run the
            # command as its background job and wait for it.
            cmd = [*_SANDBOX, "bash", "-c", f"( {c} ) & wait $!"] if _SANDBOX else ["bash", "-c", c]
            r = subprocess.run(cmd, cwd=wt, capture_output=True, text=True, timeout=300,
                               env={**os.environ, "_ZO_DOCTOR": "0"})
            res.append({"cmd": c, "rc": r.returncode, "tail": (r.stdout + r.stderr)[-1500:]})
        except subprocess.TimeoutExpired:
            res.append({"cmd": c, "rc": 124, "tail": "timeout after 300s"})
    ch = changed_files(wt)
    prev = load_gate(m, tid) or {}
    old = ap(m, tid, "review.json")
    if os.path.exists(old):  # never let a previous attempt's review be mistaken for the new one
        os.replace(old, ap(m, tid, f"review.attempt{prev.get('attempt', 0)}.json"))
    ev = {"task": tid, "dir": wt, "fingerprint": fingerprint(wt), "attempt": prev.get("attempt", 0) + 1,
          "accept": res, "changed": ch, "out_of_scope": [p for p in ch if not P.in_scope(p, t["files"])]}
    with open(ap(m, tid, "evidence.json"), "w") as f:
        json.dump(ev, f, indent=2)
    spec = open(t["prompt_file"]).read().replace("{{WORKDIR}}", wt)
    acc_txt = "\n".join(f"- `{a['cmd']}` -> rc={a['rc']}\n{a['tail'].strip()[-600:]}" for a in res)
    body = open(os.path.join(REFS, "reviewer-prompt.md")).read()
    for k, v in {"{{TASK_ID}}": tid, "{{WORKDIR}}": wt, "{{FINGERPRINT}}": ev["fingerprint"],
                 "{{ALLOWED_FILES}}": ", ".join(t["files"]), "{{CHANGED}}": ", ".join(ch) or "(none)",
                 "{{OUT_OF_SCOPE}}": ", ".join(ev["out_of_scope"]) or "(none)", "{{ACCEPTANCE}}": acc_txt,
                 "{{RUBRIC_PATH}}": os.path.join(REFS, "rubric.md"), "{{REVIEW_PATH}}": ap(m, tid, "review.json"),
                 "{{SPEC}}": spec}.items():  # SPEC last: spec text must not be re-expanded
        body = body.replace(k, v)
    with open(ap(m, tid, "reviewer.txt"), "w") as f:
        f.write(body)
    bad = [a["cmd"] for a in res if a["rc"] != 0]
    print(f"{tid}: attempt {ev['attempt']}/{MAX_ATTEMPTS} fingerprint={ev['fingerprint']} changed={len(ch)} "
          f"out_of_scope={len(ev['out_of_scope'])} acceptance_failed={len(bad)}")
    print(f"reviewer prompt: {ap(m, tid, 'reviewer.txt')}")
    print(f"reviewer must write: {ap(m, tid, 'review.json')}")
    return 0


def validate(rv, ev):
    errs = []
    if rv.get("fingerprint") != ev["fingerprint"]:
        errs.append("review fingerprint mismatch (stale review, or wrong worktree reviewed)")
    sc = rv.get("scores") or {}
    for k in RUBRIC:
        v = sc.get(k)
        if not isinstance(v, int) or isinstance(v, bool) or not 0 <= v <= 5:
            errs.append(f"score {k!r} must be an integer 0-5")
    fs = rv.get("findings")
    if not isinstance(fs, list):
        return errs + ["findings must be a list"]
    for i, f in enumerate(fs):
        if not isinstance(f, dict) or f.get("severity") not in SEV or f.get("criterion") not in RUBRIC \
                or not str(f.get("issue", "")).strip() or not str(f.get("fix", "")).strip():
            errs.append(f"finding #{i}: needs severity(blocker|major|minor), criterion(one of 8), issue, fix")
    if not rv.get("commands_run"):
        errs.append("commands_run is empty: the reviewer must run at least one command itself")
    if not errs:
        for k in RUBRIC:
            if sc[k] < 4 and not any(f["criterion"] == k for f in fs):
                errs.append(f"{k}={sc[k]} (<4) has no finding naming it — review is not actionable")
    return errs


def cmd_score(m, tid):
    ev = load_json(ap(m, tid, "evidence.json"))
    rv = load_json(ap(m, tid, "review.json"))
    if not ev:
        die("no evidence: run `prepare` first")
    if not rv:
        die(f"{ap(m, tid, 'review.json')} missing or not valid JSON: the reviewer did not deliver")
    errs = validate(rv, ev)
    if fingerprint(ev["dir"]) != ev["fingerprint"]:
        errs.append("worktree changed since `prepare`: rerun prepare and review again")
    if errs:
        print(f"{tid}: INVALID REVIEW\n  " + "\n  ".join(errs))
        return 3
    sc, fs = rv["scores"], rv["findings"]
    total = round(sum(w * sc[k] / 5 for k, (w, _) in RUBRIC.items()), 1)
    failed = [a for a in ev["accept"] if a["rc"] != 0]
    gates = []
    if failed:
        gates.append("acceptance failed: " + "; ".join(f"`{a['cmd']}` rc={a['rc']}" for a in failed))
    if ev["out_of_scope"]:
        gates.append("out-of-scope files changed: " + ", ".join(ev["out_of_scope"]))
    if any(f["severity"] == "blocker" for f in fs):
        gates.append("blocker finding(s) open")
    low = [f"{k}={sc[k]}<{fl}" for k, (_, fl) in RUBRIC.items() if sc[k] < fl]
    if low:
        gates.append("below floor: " + ", ".join(low))
    if total < THRESHOLD:
        gates.append(f"total {total} < {THRESHOLD}")
    attempt = ev["attempt"]
    if not gates:
        verdict, nxt = "PASS", "merge"
    elif attempt >= MAX_ATTEMPTS:
        verdict, nxt = "ESCALATE", "claude_takeover"
    else:
        verdict, nxt = "REWORK", ("resume" if attempt == 1 else "fresh")
    g = {"task": tid, "attempt": attempt, "verdict": verdict, "next_action": nxt, "total": total, "scores": sc,
         "gates": gates, "findings": sorted(fs, key=lambda f: SEV[f["severity"]]), "accept_failed": failed,
         "fingerprint": ev["fingerprint"], "dir": ev["dir"], "summary": rv.get("summary", "")}
    with open(ap(m, tid, "gate.json"), "w") as f:
        json.dump(g, f, indent=2)
    print(f"{tid}: {verdict}  score={total}/{100} (need {THRESHOLD})  attempt {attempt}/{MAX_ATTEMPTS}  next={nxt}")
    print("  scores: " + " ".join(f"{k}={sc[k]}" for k in RUBRIC))
    for x in gates:
        print(f"  GATE: {x}")
    for fnd in g["findings"]:
        print(f"  [{fnd['severity']}] {fnd['criterion']} {fnd.get('file', '')}:{fnd.get('line', '')} {fnd['issue']}")
    return {"PASS": 0, "REWORK": 1, "ESCALATE": 4}[verdict]


def rework_prompt(m, tid):
    """Write the rework prompt for the last REWORK verdict; return (path, mode)."""
    g = load_gate(m, tid)
    if not g or g["verdict"] != "REWORK":
        die(f"{tid}: no REWORK verdict to act on")
    t = next(x for x in m["tasks"] if x["id"] == tid)
    wt, n, mode = g["dir"], g["attempt"], g["next_action"]
    must = [f for f in g["findings"] if f["severity"] != "minor"]
    nits = [f for f in g["findings"] if f["severity"] == "minor"]
    fmt = lambda i, f: (f"{i}. [{f['severity'].upper()}] ({f['criterion']}) {f.get('file', '')}:{f.get('line', '')}\n"
                        f"   PROBLEM: {f['issue']}\n   FIX: {f['fix']}")
    parts = [f"REWORK REQUEST — attempt {n + 1} of {MAX_ATTEMPTS}. An independent reviewer rejected your previous "
             f"implementation (score {g['total']}/100, need {THRESHOLD}). Gates failed: {'; '.join(g['gates'])}.",
             "Work STEP BY STEP. Do not rewrite from scratch unless a finding says the approach itself is wrong.",
             "STEP 1. Re-read the task spec (below) and every file you changed.",
             "STEP 2. Fix the findings below IN ORDER, one at a time. After each fix, run the acceptance commands "
             "and confirm the output before moving on.",
             "REQUIRED FIXES:\n" + ("\n".join(fmt(i, f) for i, f in enumerate(must, 1)) or "(none — see gates above)")]
    if nits:
        parts.append("NICE-TO-FIX (only if trivial):\n" + "\n".join(fmt(i, f) for i, f in enumerate(nits, 1)))
    if g["accept_failed"]:
        parts.append("ACCEPTANCE COMMANDS THAT FAILED (real output):\n" + "\n".join(
            f"$ {a['cmd']}  (rc={a['rc']})\n{a['tail'].strip()[-800:]}" for a in g["accept_failed"]))
    parts.append(f"STEP 3. Re-run ALL acceptance commands: {'; '.join(t.get('accept', []))}\n"
                 f"STEP 4. Reply in the original FINAL REPLY FORMAT, listing which finding numbers you fixed.\n"
                 f"CONSTRAINTS (unchanged): work only in {wt}; edit only: {', '.join(t['files'])}; "
                 "no git commands, no new dependencies, no network, no deleting files, no TODO/stub bodies. "
                 "If a finding is wrong or impossible, say so under BLOCKERS instead of guessing.")
    if mode == "fresh":
        parts.append("A previous attempt failed review, and you are starting clean. The ORIGINAL TASK SPEC follows; "
                     "satisfy it AND the required fixes above:\n<<<SPEC\n" + open(t["prompt_file"]).read() + "\nSPEC>>>")
    path = ap(m, tid, f"rework{n}.txt")
    with open(path, "w") as f:
        f.write("\n\n".join(parts) + "\n")
    return path, mode


def main():
    ap_ = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap_.add_argument("--manifest", default=os.path.join(os.getcwd(), ".agy", "manifest.json"))
    ap_.add_argument("cmd", choices=["prepare", "score", "rework-prompt", "show"])
    ap_.add_argument("id")
    a = ap_.parse_args()
    try:
        m = P.load(a.manifest)
    except Exception as e:
        die(f"cannot load manifest {a.manifest}: {e}")
    if a.cmd == "prepare":
        return cmd_prepare(m, a.id)
    if a.cmd == "score":
        return cmd_score(m, a.id)
    if a.cmd == "show":
        print(json.dumps(load_gate(m, a.id), indent=2)); return 0
    path, mode = rework_prompt(m, a.id)
    print(f"{mode} {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
