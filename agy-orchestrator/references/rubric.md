# Review rubric for agy worker output

Scored by an independent Claude reviewer subagent; the verdict is computed by `scripts/agy_gate.py`, not by anyone's judgment.
Every criterion is an integer 0–5. Total = Σ weight × score / 5 (max 100).

**PASS requires ALL of:** total ≥ **85** · every criterion ≥ its floor · no hard-gate violation.

| Criterion | Weight | Floor | What it measures |
|---|---|---|---|
| `correctness` | 25 | 3 | Does it actually do the right thing? Logic, off-by-ones, wrong results, race/ordering bugs. The reviewer must exercise it, not just read it. |
| `spec_compliance` | 20 | 3 | Every requirement in the spec implemented; signatures/interfaces/formats unchanged; nothing required is missing. |
| `tests` | 15 | 2 | Tests exist where the spec asks, are meaningful (assert behaviour, cover edge cases), are not weakened, hard-coded, or skipped. |
| `robustness` | 10 | 2 | Error handling, input validation at boundaries, edge cases (empty, None, huge, unicode, concurrency) handled; no swallowed exceptions. |
| `code_quality` | 10 | 2 | Readable, no dead code/duplication, no stubs/TODOs/placeholders, sensible names, simplest thing that works. |
| `scope_discipline` | 10 | 3 | Only the allowed files touched; no new dependencies, config, lockfile, or unrelated edits; no extra features. |
| `security` | 5 | 3 | No secrets, injection, unsafe `eval`/shell/`subprocess`, path traversal, network calls, or destructive operations that the spec did not ask for. |
| `consistency` | 5 | 2 | Matches the surrounding code's style, idioms, error handling and conventions; integrates cleanly with neighbouring modules. |

## Score anchors (apply to every criterion)
- **5** Excellent. Nothing to fix. Rare — do not hand it out by default.
- **4** Good. Only nits (minor findings).
- **3** Acceptable but with a real, non-blocking issue.
- **2** Significant problems; would not merge.
- **1** Mostly wrong or missing.
- **0** Absent or actively harmful.

Any criterion scored **below 4 must be backed by at least one finding naming that criterion** (otherwise the review is rejected as unactionable).

## Hard gates (any one blocks PASS regardless of score)
1. An acceptance command (`accept` in the manifest) exits non-zero — run by the orchestrator, not the worker.
2. A file outside the task's allowed `files` was changed (mechanical check).
3. Any finding with severity `blocker`.
4. Any criterion below its floor.
5. Review is stale: the worktree fingerprint changed after the review started, or the review echoes a different fingerprint.
6. The reviewer ran no command of its own (`commands_run` empty) — reading alone is not review.

## Severity
- `blocker` — wrong, unsafe, or violates the spec. Must be fixed.
- `major` — should be fixed before merge (real bug risk, missing test, missing edge case).
- `minor` — nit; fix if cheap.

## Attempts
| Scoring # | Fails → | What happens |
|---|---|---|
| 1 | `REWORK` | `rework`: **resume** the same agy conversation with the findings, fix step by step |
| 2 | `REWORK` | `rework`: **fresh** worker in a clean worktree, original spec + all findings from the failed attempts |
| 3 | `ESCALATE` | Claude takes the task over (or splits it). Do not send it to agy again |
