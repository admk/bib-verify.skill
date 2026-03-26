# Bib Verify

`$bib-verify` is a Codex skill for checking BibTeX or `.bbl` bibliography
entries against authoritative sources such as publisher pages, conference
proceedings, and arXiv.

It is designed for workflows where Codex needs to:

- verify citation metadata such as authors, title, venue, year, pages, DOI, or
  arXiv ID
- check whether links embedded in bibliography entries actually resolve
- produce one report per entry and a consolidated verification report
- suggest corrected BibTeX entries when mismatches are found

## Files

- `SKILL.md`: the skill definition and workflow instructions
- `agents/openai.yaml`: UI metadata for the skill
- `scripts/extract_bbl_entries.py`: generate one report stub per `\bibitem`
- `scripts/aggregate_bib_reports.py`: combine per-entry reports into one summary
- `references/report-template.md`: template used for each verification report

## Usage

Install or place this repo under your Codex skills directory so the skill is
available as `$bib-verify`.

Example prompt:

```text
Use $bib-verify to verify the bibliography entries in build/paper.bbl and
produce a consolidated report.
```

## Workflow Summary

1. Find the relevant `.bbl` file in the current repo.
2. Extract `\bibitem` blocks into report stubs.
3. Verify each entry against authoritative sources.
4. Aggregate the per-entry reports into one markdown summary.

The detailed operational instructions live in `SKILL.md`.
