#!/usr/bin/env python3
"""Extract \bibitem blocks from a .bbl file and write per-entry report stubs."""

import argparse
import re
from pathlib import Path


def load_template(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Template not found: {path}")
    return path.read_text()


def sanitize_filename(name: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9._-]+", "-", name).strip("-")
    return safe or "entry"


def extract_entries(text: str):
    pattern = re.compile(
        r"(\\bibitem\[[^\]]+\]\{([^}]+)\}(.+?))(?=\\bibitem|\\end\{thebibliography\})",
        flags=re.S,
    )
    for full, key, _body in pattern.findall(text):
        yield key, full.strip()


def default_template_path() -> Path:
    # Skill layout: <skill>/scripts/extract_bbl_entries.py
    # Template at: <skill>/references/report-template.md
    return Path(__file__).resolve().parent.parent / "references" / "report-template.md"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bbl", required=True, help="Path to .bbl file")
    parser.add_argument("--out-dir", default="bbl-verify", help="Directory for per-entry md files")
    parser.add_argument(
        "--template",
        default="",
        help="Path to a markdown template with {{BIBKEY}} and {{CURRENT_ENTRY}}",
    )
    args = parser.parse_args()

    bbl_path = Path(args.bbl)
    out_dir = Path(args.out_dir)

    template_path = Path(args.template) if args.template else default_template_path()
    template = load_template(template_path)

    text = bbl_path.read_text()
    out_dir.mkdir(parents=True, exist_ok=True)

    count = 0
    for key, entry in extract_entries(text):
        filename = sanitize_filename(key) + ".md"
        content = template.replace("{{BIBKEY}}", key).replace("{{CURRENT_ENTRY}}", entry)
        (out_dir / filename).write_text(content)
        count += 1

    print(f"Wrote {count} report stubs to {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
