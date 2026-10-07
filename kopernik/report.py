"""Human-readable presentation of FITS inspection results."""

import html
import re

from . import __version__
from .inspection import Inspection


METADATA = (
    "OBJECT", "DATE-OBS", "EXPTIME", "TELESCOP", "INSTRUME", "OBSERVER",
    "FILTER", "IMAGETYP", "CCD-TEMP", "XBINNING", "YBINNING", "GAIN",
    "OFFSET", "STACKCNT", "LIVETIME", "PROGRAM",
)


def safe_text(value: object) -> str:
    """Prevent untrusted text from emitting terminal control sequences."""
    return "".join(c if c.isprintable() else ascii(c)[1:-1] for c in str(value))


def render_report(result: Inspection) -> str:
    lines = [
        f"Kopernik {__version__} - FITS header report",
        "=" * 64,
        f"File: {safe_text(result.path)}",
        f"Size: {result.size:,} bytes" if result.size is not None else "Size: unavailable",
        f"FITS structural validation: {result.status}",
        "Scope: strict Astropy header verification, block alignment and HDU data spans.",
        "Pixel values and CHECKSUM/DATASUM are not verified; full FITS conformance",
        "and image-data integrity are not established by these checks.",
        "No image analysis or image-quality assessment was performed.",
    ]
    if result.issues:
        lines.extend(["", "Validation details:"])
        lines.extend(f"  - {safe_text(issue)}" for issue in result.issues)
        lines.append("Check the source file or export an uncompressed, standards-compliant FITS copy.")
    lines.extend(["", f"Verified HDU headers: {len(result.hdus)}"])
    for index, info in enumerate(result.hdus):
        header = info.header
        axes = [header[f"NAXIS{i}"] for i in range(1, header["NAXIS"] + 1)]
        lines.extend([
            "", f"HDU {index}: {safe_text(header.get('EXTNAME', 'PRIMARY' if index == 0 else 'unnamed'))}",
            f"  Type: {info.kind}",
            f"  BITPIX: {header['BITPIX']}",
            f"  NAXIS: {header['NAXIS']}",
            "  Axis lengths (FITS order): " + (" x ".join(map(str, axes)) if axes else "none"),
            "", "  Observation metadata (as declared in the header):",
        ])
        for keyword in METADATA:
            cards = [card for card in header.cards if card.keyword == keyword]
            if not cards:
                lines.append(f"    {keyword:<10} unavailable")
            for card in cards:
                comment = f" / {safe_text(card.comment)}" if card.comment else ""
                lines.append(f"    {keyword:<10} {safe_text(card.value)}{comment}")
        lines.extend(["", "  All header cards (in source order; END terminator omitted):"])
        for card in header.cards:
            lines.append(f"    {safe_text(card.image.rstrip())}")
    return "\n".join(lines) + "\n"


def markdown_text(value: object) -> str:
    """Render untrusted metadata as literal Markdown text, never HTML or links."""
    escaped = re.sub(r"([\\`*_{}\[\]()#+.!|~-])", r"\\\1", safe_text(value))
    return html.escape(escaped, quote=False)


def render_markdown_report(result: Inspection) -> str:
    lines = [
        f"# Kopernik {__version__} - FITS header report", "",
        f"**File:** {markdown_text(result.path)}", "",
        f"**Size:** {result.size:,} bytes" if result.size is not None else "**Size:** unavailable", "",
        f"**FITS structural validation:** {result.status}", "",
        "Scope: strict Astropy header verification, block alignment and HDU data spans.", "",
        "Pixel values and CHECKSUM/DATASUM are not verified; full FITS conformance "
        "and image-data integrity are not established by these checks.", "",
        "No image analysis or image-quality assessment was performed.",
    ]
    if result.issues:
        lines.extend(["", "## Validation details", ""])
        lines.extend(f"- {markdown_text(issue)}" for issue in result.issues)
        lines.extend(["", "Check the source file or export an uncompressed, standards-compliant FITS copy."])
    lines.extend(["", f"**Verified HDU headers:** {len(result.hdus)}"])
    for index, info in enumerate(result.hdus):
        header = info.header
        axes = [header[f"NAXIS{i}"] for i in range(1, header["NAXIS"] + 1)]
        name = header.get("EXTNAME", "PRIMARY" if index == 0 else "unnamed")
        lines.extend([
            "", f"## HDU {index}: {markdown_text(name)}", "",
            f"- Type: {info.kind}", f"- BITPIX: {header['BITPIX']}",
            f"- NAXIS: {header['NAXIS']}",
            "- Axis lengths (FITS order): " + (" x ".join(map(str, axes)) if axes else "none"),
            "", "### Observation metadata", "",
            "As declared in the header; units are preserved in the comments.", "",
            "| Keyword | Value | Comment |", "| --- | --- | --- |",
        ])
        for keyword in METADATA:
            cards = [card for card in header.cards if card.keyword == keyword]
            if not cards:
                lines.append(f"| {keyword} | unavailable | |")
            for card in cards:
                lines.append(f"| {keyword} | {markdown_text(card.value)} | {markdown_text(card.comment)} |")
        cards_text = "\n".join(safe_text(card.image.rstrip()) for card in header.cards)
        # A longer fence keeps any backticks in untrusted header cards literal.
        fence = "`" * max(3, 1 + max((len(run) for run in re.findall(r"`+", cards_text)), default=0))
        lines.extend(["", "### All header cards", "",
                      "In source order; END terminator omitted.", "",
                      fence + "text", cards_text, fence])
    return "\n".join(lines) + "\n"
