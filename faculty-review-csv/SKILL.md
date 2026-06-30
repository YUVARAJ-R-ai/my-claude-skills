---
name: faculty-review-csv
description: Generate a faculty/teacher review CSV from a WhatsApp group chat export. Mines an exported WhatsApp chat (.zip or .txt) for what students say about a list of faculty (from a VIT program-sheet xlsx, a CSV/txt of names, or inline names), classifies each into Take / Avoid / Mixed with sentiment, traits, confidence, and verbatim evidence, and writes a CSV. Use when someone wants reviews/ratings of teachers, professors, or faculty extracted from a WhatsApp group, FFCS chat, or any chat export — especially for course/slot registration planning.
---

# Faculty Review CSV from WhatsApp chat

Turn a noisy WhatsApp group export into a structured review CSV for a specific
set of faculty. Built for VIT FFCS registration ("which teacher is lenient / low
class avg?") but works for any chat + name list.

## Inputs to gather (ask only for what's missing)

1. **Chat export** — the WhatsApp `.zip` (Export chat → Without media) or the
   `.txt` inside it. Required.
2. **Faculty list** — ONE of:
   - a **program-sheet `.xlsx`** with a `FACULTY NAME` column (VIT 24BCE/25BCE
     style: also reads `FACULTY ID` and forward-fills `Course title`),
   - a **CSV** with a name column, a **txt** of one name per line, or
   - **inline names** if the user just lists a few.

If the user references a file that exists in the working directory, use it.

## Steps

1. **Locate files.** Check the working directory for `*.zip` (chat) and `*.xlsx`
   (program sheet). Confirm with the user if ambiguous.
2. **Ensure openpyxl** is importable only if the faculty source is `.xlsx`. If
   not available, create a venv and install it (don't pollute system Python):
   `python3 -m venv /tmp/revenv && PIP_USER=0 /tmp/revenv/bin/pip install -q openpyxl`
   then use `/tmp/revenv/bin/python` to run the script.
3. **Run the bundled script** (do NOT re-implement the parsing/classification by
   hand — that wastes tokens and is less consistent):
   ```
   python extract_reviews.py --chat "<chat.zip|.txt>" \
       --faculty "<programsheet.xlsx>" --out "<reviews.csv>"
   ```
   Variants: `--names "A,B,C"` for inline names; `--faculty file.csv`/`.txt`;
   `--all` to also emit rows with no data. The script lives next to this file.
4. **Read the CSV back**, then present a short, scannable summary grouped by
   course/recommendation (Take / Avoid / Mixed) — not the raw CSV dump.
5. **State the caveats every time** (these are baked into the script's `caveat`
   column and confidence, but call them out in prose too):
   - **The chat may be from an old registration cycle** — faculty discussed may
     not match the user's current sections. Check the export's date range.
   - **Name collisions**: common first names (e.g. "Sudha", "Karthikeyan",
     "Preetha") match multiple faculty across courses; rows flagged with a
     `caveat` or `Low` confidence are unreliable — verify before trusting.
   - **"Best teacher" ≠ "easy grade."** A great teacher often raises the class
     average. If the user wants high marks under relative grading, prioritize the
     `low_class_avg` / `easy_marks` / `lenient` traits, not `good_teaching`.
6. **Offer the follow-up**: a ready-to-paste group message asking for fresh
   reviews on the faculty that came back `Insufficient data` / `No data`.

## Output CSV columns

`faculty_id, faculty_name, course, mentions, recommendation, sentiment, traits,
confidence, caveat, evidence`

- **recommendation**: Take · Avoid · Mixed / verify · Insufficient data · No data
- **traits**: any of lenient, strict, easy_marks, low_class_avg, good_teaching,
  no_S_grade, chill_low_effort, gives_notes
- **confidence**: High (≥3 clear opinions) · Medium (1–2) · Low (generic name or
  only list-mentions)
- **evidence**: up to 3 verbatim quotes (truncated) so the user can judge for
  themselves

## Notes

- The script is token-cheap: it filters to messages that mention a faculty AND
  contain a teaching/grading keyword, so you never read the whole chat.
- Rows with zero relevant mentions are dropped unless `--all` is passed.
- If the user later wants a styled view, offer to render the CSV as an HTML
  review card — but the CSV is the primary deliverable for this skill.
