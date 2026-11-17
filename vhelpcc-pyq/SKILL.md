---
name: vhelpcc-pyq
description: Download VIT past year question papers (PYQs) from vhelpcc.com for a given course. Determines the course code (from the syllabus folder or the user), searches the vhelpcc Wix backend for CAT 1 / CAT 2 / FAT papers, and saves the PDFs into a pyqs/ folder (cat1/ and cat2/ subfolders). Use whenever someone wants VIT previous year question papers, PYQs, CAT/FAT papers, or exam papers for a subject — especially when they say "download PYQs", "fetch past papers", or reference vhelp.
---

# vhelpcc PYQ download

Download VIT past-year question papers from vhelpcc.com. Talks directly to the
same Wix backend the website uses (no browser, no scraping, no MCP client).

## How it works

The vhelpcc website stores papers in a Wix Cloud Data collection (`Jobs1`). This
skill queries that backend with a Base64URL-encoded JSON payload, then downloads
each paper's PDF from the Wix CDN.

Two known quirks are handled by the bundled script (upstream
`vhelpcc-pyq-mcp-server` does NOT handle them):
- **PDF URL**: upstream resolves to `usc1.usrfiles.com` which returns HTTP 403.
  This skill uses `https://static.wixstatic.com/ugd/<file_id>.pdf` instead.
- **SSL**: this machine's proxy presents a self-signed cert, so cert verification
  is disabled for the download.

## Steps

1. **Get the course code.** If the subject folder has a `syllabus/` subfolder,
   read the course code from the syllabus PDF filename (e.g.
   `BCSE204L_DESIGN-AND-ANALYSIS-OF-ALGORITHMS_TH_1.0_67_BCSE204L.pdf` → `BCSE204L`).
   Fallback order: syllabus filename → module/lecture PDF names in `source/` →
   ask the user. Confirm the code if ambiguous (e.g. `BCSE301` vs `BCSE301L`).

2. **Pick the filter.** Ask the user (only if not already stated):
   - exam types: `CAT 1`, `CAT 2`, `FAT` (default: all)
   - academic years, e.g. `24-25`, `25-26` (default: all)
   - slots, e.g. `F2` (default: all)

3. **Run the bundled script** (do NOT re-implement the API logic by hand):
   ```
   python ~/.claude/skills/vhelpcc-pyq/download_pyqs.py \
       --subject BCSE301L --out "<subject_dir>/pyqs" \
       --cat "CAT 1" --cat "CAT 2" --year 24-25 --year 25-26
   ```
   - `--list` prints matching papers without downloading (useful to confirm
     before pulling files).
   - Omit `--cat`/`--year`/`--slot` to take everything.
   - Stdlib only — no venv/pip needed. Run with `python3` if `python` is missing.

4. **Verify.** Check the output PDFs are non-trivial in size and start with the
   `%PDF` magic bytes. Papers are saved as
   `pyqs/cat1/<CODE>_CAT1_<year>_<slot>.pdf` and `pyqs/cat2/...`; FAT goes
   directly into `pyqs/`. If two papers share a slot/year, the second gets the
   uploader name appended to avoid overwriting.

5. **Report.** Summarise how many CAT 1 / CAT 2 / FAT papers were downloaded and
   where they went. Flag any papers with no PDF attached (they're skipped).

## Notes

- No auth, cookies, or rate limiting needed — it's the same public API the
  website uses. Downloading is quick (each PDF ~0.4–3 MB).
- If the API returns 0 results for a code, the code may be wrong or the paper
  simply isn't uploaded yet — double-check the course code before concluding.
- `FAT` papers are saved flat (no cat1/cat2 subfolder) since they're one-per-slot.
