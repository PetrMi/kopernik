"""Command-line interface for local FITS header reports."""

import argparse
from pathlib import Path
import sys

from .inspection import inspect_fits
from .report import render_markdown_report, render_report, safe_text


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate local FITS structure and report header metadata.")
    parser.add_argument("path", help="Path to a local, uncompressed FITS file")
    parser.add_argument("--markdown", metavar="PATH", help="Also save a Markdown report as a new UTF-8 file")
    args = parser.parse_args()
    result = inspect_fits(args.path)
    print(render_report(result), end="")
    if args.markdown:
        try:
            with Path(args.markdown).open("x", encoding="utf-8", newline="\n") as output:
                output.write(render_markdown_report(result))
        except (OSError, ValueError) as exc:
            print(f"Unable to save Markdown report: {safe_text(exc)}. "
                  "Choose a new file in an existing writable directory.", file=sys.stderr)
            return 1
    return 0 if result.status == "PASSED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
