---
name: bib-verify
description: Verify BibTeX or .bbl bibliography entries against authoritative sources (publisher, proceedings, arXiv) and produce per-entry markdown reports plus a consolidated report. Use when checking citation metadata correctness (authors, title, venue/journal, year/date, pages, DOI/arXiv), verifying links inside entries, or generating audit reports for bibliography integrity.
---

# Bib Verify

## Overview
Locate the `.bbl` file in the current repo (often git-ignored), generate one report per entry with verified metadata and links, then aggregate into a single markdown report.

## Workflow
1. **Find the .bbl file**
   - Search the repo for `*.bbl` (including git-ignored build directories) and pick the most relevant one.
   - Prefer `build/` or `out/` paths if present; if multiple candidates exist, select the one tied to the active paper (e.g., `paper.bbl`).

2. **Generate per-entry report stubs**
   - Run `<SKILL_DIR>/scripts/extract_bbl_entries.py` to extract `\bibitem` blocks and create one `.md` stub per entry in a target directory (prefer `build/bbl_verify/` if exists).
   - Use `<SKILL_DIR>/references/report-template.md` as the template to ensure a consistent format.

3. **Assign one subagent per entry**
   - You MUST use one subagent per bib entry to verify metadata against authoritative sources.
   - Each subagent opens one stub file and fills in:
    - Status (**Verified** / **Minor** / **Mismatch**)
      - **Verified**: All metadata match authoritative source(s) after normalizing trivial formatting.
      - **Minor**: Allow minor discrepancies or acceptable variants, including:
        - Letter casing, punctuation, or spacing differences.
        - Abbreviated vs. full venue/journal names (if clearly the same venue).
        - arXiv vs. published version differences where the work is clearly the same.
          - if there is a final published version, prefer to suggest it over arXiv.
        - Missing non-critical fields (pages/issue/volume) when other metadata match.
      - **Mismatch**: Significant discrepancies found, or core metadata appear fabricated. It implies desk reject if the bib entry is used in submission; be explicit and cite evidence. Use when:
        - Title, authors, venue, or year conflict with authoritative source(s).
        - Title does not match any authoritative record.
        - Author order changes meaningfully (not just formatting) for the same work.
        - Author list includes non-existent authors, omits key authors, or order implies a different work.
        - DOI/URL does not resolve or points to a different real work.
        - Year/venue mismatch with no evidence of a real publication or preprint.
    - Verified metadata (authors, title, venue/journal, year/date, pages/volume/issue, DOI/arXiv)
    - **Links in entry verified** (URL/DOI present in the bib entry; confirm they resolve)
    - **Suggested .bib entry** (include a corrected BibTeX entry)
    - Issues list in required format
    - Sources (authoritative URLs)
   - Require `web.run` for all verification steps.
   - Allow up to 5 subagents working in parallel for efficiency, allocate new subagents as stubs are completed.

4. **Aggregate results**
   - Run `scripts/aggregate_bib_reports.py` to combine per-entry reports into a single `bbl_verify_report.md` file with a summary section.
   - If any stubs remain unfilled, list them under a “Missing entries” section in the combined report.

5. **Quality checks**
   - Ensure each report cites at least one authoritative source (publisher/proceedings/arXiv).
   - Provide a **verifiable URL** in the Sources section for user double-checking.
   - Verify links present in the bib entry; flag broken or mismatched links.

## Report Format
Use `references/report-template.md` verbatim. Required sections:
- `Status:` line near top.
- Current entry in a fenced code block.
- **Verified metadata** with a bullet for “Links in entry verified.”
- **Suggested .bib entry** in a fenced code block.
- **Issues** list with format: `- [field] [type] [details]`
  - Examples:
    - `[title] [mismatch] Current title differs from proceedings.`
    - `[authors] [missing] Missing Guanhong Tao.`
    - `[authors] [order] Author order incorrect; Alice Smith and Bob Jones swapped.`
    - `[venue] [mismatch] Listed as NDSS; verified as IEEE S&P Workshops.`
    - `[links] [broken] DOI link does not resolve.`
- **Sources** list with one URL per line; include at least one user-clickable authoritative URL.

## Scripts
- `<SKILL_DIR>/scripts/extract_bbl_entries.py`
  - Usage:
    - `python <SKILL_DIR>/scripts/extract_bbl_entries.py --bbl build/paper.bbl --out-dir build/bbl_verify --template references/report-template.md`
  - Output: one `.md` file per bib key in `reports/`.

- `<SKILL_DIR>/scripts/aggregate_bib_reports.py`
  - Usage:
    - `python <SKILL_DIR>/scripts/aggregate_bib_reports.py --in-dir build/bbl_verify --out bbl_verify_report.md`
  - Output: combined report with summary counts.

## Notes
- Verify any URLs present in the bib entry; if none exist, mark as “N/A.”
- Keep issues concise and tied to a specific field.
- `<SKILL_DIR>` refers to the root directory of this skill, not the current working directory.
