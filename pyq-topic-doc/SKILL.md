---
name: pyq-topic-doc
description: Build a verified, exam-ready markdown document covering every real past-year-question on one topic (e.g. "Huffman coding", "Matrix Chain Multiplication", "TSP") for a subject. Pulls every real question on that topic from the downloaded PYQ folders, reads the actual source PDFs, independently verifies every computation instead of trusting printed answer keys, flags ambiguous or buggy questions explicitly, and saves a polished per-topic study doc into the subject folder. Trigger whenever someone asks to "make a document/documentation for [topic] questions", "create a doc for [topic] problems", or similar, referencing CAT1/CAT2/FAT papers for a specific algorithm/topic.
---

# PYQ topic documentation

Build a single, trustworthy reference document for one named topic (an algorithm,
question type, or concept) by pulling together every real exam question on it —
not textbook problems, not invented ones unless explicitly asked for and clearly
labeled as such.

## Why this exists

Doing this by hand, one topic at a time, repeatedly surfaces the same value:
official answer keys and question papers have real errors (arithmetic mistakes,
miscounted frequencies, ambiguous wording, illegible handwritten scans) that
propagate silently if you just transcribe them. Independently re-deriving every
answer catches these before they end up in a student's memorized "correct"
answer. This skill exists to make that rigor the default, not an occasional
extra step.

## Steps

1. **Locate every real source for this topic.** Check, in order:
   - An existing module/topic-breakdown file if one exists (e.g.
     `pyqs/cat1/<CODE>_CAT1_by_module.md`) — grep it case-insensitively for the
     topic name and close synonyms (e.g. "TSP" AND "travelling salesman").
   - If no breakdown file exists, or to double-check its coverage, grep/search
     across every PDF folder for the subject: `pyqs/cat1/`, `pyqs/cat2/`,
     `pyqs/examcooker/cat1/`, `pyqs/examcooker/cat2/`, and any FAT folders.
     **Most of these PDFs are scanned images with no text layer** — `pdftotext`
     will silently return nothing. Don't trust an empty grep result as "no
     matches" until you've confirmed the PDF actually has extractable text.
   - Note which papers are official **answer keys** (usually from
     examcooker, filename or header says "ANSWER KEY" / "KEY") vs plain
     question papers — keys are worth extra scrutiny (see step 3) but plain
     papers may need you to solve from scratch.

2. **Read every matching source PDF directly** with the Read tool (it handles
   scanned PDFs as images natively — don't rely on OCR/pdftotext for these).
   Pull the *exact* question wording, all given data (tables, arrays,
   distance matrices, frequency counts), and any printed official answer.

3. **Independently verify every computation — never transcribe a key's final
   number without re-deriving it.** Use a script (Python via Bash) for
   anything numeric or constructive: DP tables, greedy traces, tree builds,
   graph algorithms. Compare your result to the official key if one exists.
   When they disagree:
   - Recompute at least once more, differently if possible (e.g. brute-force
     enumeration as a cross-check against a DP result).
   - If your independent computation is solid and the key is wrong, say so
     explicitly in the doc — don't silently "correct" it without telling the
     reader, and don't silently defer to a key that doesn't check out either.
     Flag it as a callout so the student knows to trust the re-derivation.

4. **Flag ambiguity instead of silently resolving it.** Real exam questions
   often have gaps: an undefined tie-break rule, a referenced character/value
   not actually given, a name that doesn't match its own worked example. When
   you hit one, state the gap plainly, pick a reasonable resolution, and say
   so in one line — this is itself something worth teaching the student,
   since they'll hit the same kind of gap live in the exam and need to know
   the move is "state your assumption and proceed," not "freeze."

5. **Write the document** using this structure (adapt section names to the
   topic, keep the shape):
   - Frontmatter: `tags: [<subject-lowercase>, <topic-lowercase>, exam-prep]`
   - Opening paragraph: how many real papers actually test this topic out of
     how many total — this framing (real frequency, not assumed importance)
     is what makes the doc worth trusting over a generic textbook summary.
   - **Algorithm/recurrence section**: the general method, in a form the
     student could reproduce from memory — recurrence relation, pseudocode,
     time complexity with a one-line justification, and a short numbered
     exam checklist (what to write, in what order, for partial credit even
     under time pressure).
   - **One section per real question**, each with:
     - The exact question text (quoted), which paper it's from, and marks.
     - The full worked solution — show the actual table/tree/trace, not just
       the final answer.
     - A `> [!exam] Answer` callout with the final answer, clearly boxed.
     - A `> [!med]` callout for any flagged discrepancy or ambiguity from
       steps 3–4, explaining what's wrong and why the doc's answer should be
       trusted over it.
   - **Quick-reference table** near the end summarizing every question's
     answer in one glance.
   - **Closing exam-triage note**: what to prioritize if time is short — which
     parts of the solution process earn the most marks per minute spent. Only
     include this framing if the user's project instructions establish a
     time/writing-speed constraint (check for a CLAUDE.md in the subject's
     directory tree); otherwise a plain checklist is enough.

6. **Cross-link, don't duplicate.** If a sibling doc already fully covers a
   related topic (e.g. a "Greedy" overview doc when Huffman and Knapsack
   already have their own dedicated docs), index and link to it with a
   one-line summary instead of re-solving the same questions again.

7. **Save as a `.md` file directly in the subject's folder** (e.g.
   `<Subject>/<Subject>_<Topic>_<ExamLabel>.md`), not only as a hosted
   artifact link — the student reads these in their local Obsidian vault.
   Match existing naming/casing conventions already used in that subject's
   folder if other topic docs exist there.

## What NOT to do

- Don't invent practice questions and present them as if they were real PYQs.
  If a topic is in the syllabus but genuinely untested in every available
  paper, say so explicitly at the top of the doc (see `DAA_Assembly_Line_
  Scheduling_Practice.md` and `DAA_TSP_CAT1.md` in this vault for the
  pattern) and label constructed examples as such.
- Don't pad with generic textbook filler unconnected to what's actually been
  asked — every worked example should trace back to a specific real paper.
- Don't skip verification because a key "looks official" — printed keys in
  this vault have been wrong more than once (miscounted frequencies,
  arithmetic slips in bit-counts). Re-derive first, defer second.
