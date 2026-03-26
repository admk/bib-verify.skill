#!/usr/bin/env python3
"""Aggregate per-entry markdown reports into a single report."""

import argparse
import re
from pathlib import Path

STATUS_RE = re.compile(r"^Status:\s*(.+)\s*$", re.IGNORECASE | re.MULTILINE)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--in-dir", default="bbl_verify", help="Directory with per-entry md files")
    parser.add_argument("--out", default="bbl_verify_report.md", help="Output markdown file path")
    args = parser.parse_args()

    in_dir = Path(args.in_dir)
    out_path = Path(args.out)

    files = sorted(p for p in in_dir.glob("*.md") if p.is_file())
    if not files:
        raise SystemExit(f"No .md files found in {in_dir}")

    status_counts = {}
    blocks = []

    for path in files:
        text = path.read_text().rstrip()
        m = STATUS_RE.search(text)
        status = m.group(1).strip() if m else "Unknown"
        status_counts[status] = status_counts.get(status, 0) + 1
        blocks.append(text)

    summary_lines = ["# Bibliography Verification Report", "", "## Summary"]
    for status in sorted(status_counts.keys()):
        summary_lines.append(f"- {status}: {status_counts[status]}")
    summary_lines.append("")
    summary_lines.append("---")
    summary_lines.append("")

    combined = "\n\n---\n\n".join(blocks)
    out_path.write_text("\n".join(summary_lines) + combined + "\n")

    print(f"Aggregated {len(files)} entries into {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
