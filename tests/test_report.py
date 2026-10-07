"""Observable validation and reporting behaviour using controlled FITS inputs."""

from contextlib import ExitStack
import gzip
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import PropertyMock, patch

import numpy as np
from astropy.io import fits

from kopernik.inspection import inspect_fits
from kopernik.report import render_markdown_report, render_report


class FitsReportTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "image.fit"

    def create_image(self):
        primary = fits.PrimaryHDU(np.zeros((40, 50), dtype=np.int16))
        primary.header["OBJECT"] = "Test target"
        primary.header["EXPTIME"] = (30.0, "[s] Exposure duration")
        primary.header.add_history("First step")
        primary.header.add_history("Second step")
        primary.header.add_comment("First comment")
        primary.header.add_comment("Second comment")
        primary.writeto(self.path)

    def test_valid_report_preserves_metadata_and_repeated_cards_without_modification(self):
        self.create_image()
        before = self.path.read_bytes()
        result = inspect_fits(str(self.path))
        self.assertEqual(result.status, "PASSED", result.issues)
        report = render_report(result)
        for text in ("50 x 40", "Test target", "[s] Exposure duration", "FILTER     unavailable",
                     "First step", "Second step", "First comment", "Second comment",
                     "CHECKSUM/DATASUM are not verified", "No image analysis"):
            self.assertIn(text, report)
        self.assertLess(report.index("First step"), report.index("Second step"))
        self.assertEqual(before, self.path.read_bytes())

    def test_multiple_hdus_are_verified_without_loading_data(self):
        fits.HDUList([
            fits.PrimaryHDU(),
            fits.ImageHDU(np.zeros((2, 3), dtype=np.float32), name="SCI"),
            fits.BinTableHDU.from_columns([fits.Column(name="VALUE", format="J", array=[1])]),
        ]).writeto(self.path)
        with ExitStack() as stack:
            for cls in (fits.PrimaryHDU, fits.ImageHDU, fits.BinTableHDU):
                stack.enter_context(patch.object(cls, "data", new_callable=PropertyMock,
                                                side_effect=AssertionError("Pixel/table data was accessed")))
            result = inspect_fits(str(self.path))
        self.assertEqual(result.status, "PASSED", result.issues)
        self.assertEqual(len(result.hdus), 3)
        self.assertIn("HDU 1: SCI", render_report(result))

    def test_non_fits_is_invalid(self):
        self.path.write_bytes(b"not a FITS file")
        self.assertEqual(inspect_fits(str(self.path)).status, "FAILED")

    def test_missing_file_cannot_be_validated(self):
        result = inspect_fits(str(self.path))
        self.assertEqual(result.status, "NOT COMPLETED")
        self.assertIn("Check the path", render_report(result))

    def test_non_aligned_and_block_aligned_truncation_fail(self):
        self.create_image()
        original = self.path.read_bytes()
        for removed in (1, 2880):
            with self.subTest(removed=removed):
                self.path.write_bytes(original[:-removed])
                self.assertEqual(inspect_fits(str(self.path)).status, "FAILED")

    def test_invalid_bitpix_fails(self):
        self.create_image()
        raw = self.path.read_bytes().replace(b"BITPIX  =                   16", b"BITPIX  =                   17", 1)
        self.path.write_bytes(raw)
        self.assertEqual(inspect_fits(str(self.path)).status, "FAILED")

    def test_invalid_extension_header_fails(self):
        fits.HDUList([fits.PrimaryHDU(), fits.ImageHDU(np.zeros((2, 2))) ]).writeto(self.path)
        raw = self.path.read_bytes()
        self.path.write_bytes(raw[:2880] + raw[2880:].replace(b"BITPIX  =                  -64", b"BITPIX  =                   17", 1))
        self.assertNotEqual(inspect_fits(str(self.path)).status, "PASSED")

    def test_missing_end_is_invalid(self):
        self.create_image()
        self.path.write_bytes(self.path.read_bytes().replace(b"END" + b" " * 77, b" " * 80, 1))
        self.assertEqual(inspect_fits(str(self.path)).status, "FAILED")

    def test_simple_false_is_not_reported_as_valid_fits(self):
        self.create_image()
        self.path.write_bytes(self.path.read_bytes().replace(b"SIMPLE  =                    T", b"SIMPLE  =                    F", 1))
        result = inspect_fits(str(self.path))
        self.assertEqual(result.status, "FAILED")
        self.assertIn("SIMPLE", render_report(result))

    def test_parser_warning_is_visible_and_prevents_a_clean_pass(self):
        self.create_image()
        self.path.write_bytes(self.path.read_bytes().replace(b"Test target", b"Test \xffarget", 1))
        result = inspect_fits(str(self.path))
        self.assertNotEqual(result.status, "PASSED")
        self.assertIn("Parser warning:", render_report(result))

    def test_trailing_blocks_do_not_pass(self):
        self.create_image()
        with self.path.open("ab") as stream:
            stream.write(b" " * 2880)
        self.assertNotEqual(inspect_fits(str(self.path)).status, "PASSED")

    def test_compressed_inputs_are_explicitly_unsupported(self):
        self.create_image()
        self.path.write_bytes(gzip.compress(self.path.read_bytes()))
        result = inspect_fits(str(self.path))
        self.assertEqual(result.status, "NOT COMPLETED")
        self.assertIn("Compressed input is unsupported", render_report(result))

    def test_tile_compressed_input_is_unsupported(self):
        fits.HDUList([fits.PrimaryHDU(), fits.CompImageHDU(np.zeros((3, 4)))]).writeto(self.path)
        result = inspect_fits(str(self.path))
        self.assertEqual(result.status, "NOT COMPLETED")
        self.assertIn("Tile-compressed", render_report(result))

    def test_terminal_controls_are_escaped(self):
        report = render_report(inspect_fits("missing\x1b[31m.fit"))
        self.assertNotIn("\x1b", report)

    def test_cli_exit_status_and_report(self):
        self.create_image()
        for path, code, status in ((self.path, 0, "PASSED"), (self.path.with_name("missing.fit"), 1, "NOT COMPLETED")):
            completed = subprocess.run([sys.executable, "-m", "kopernik", str(path)], capture_output=True, text=True)
            self.assertEqual(completed.returncode, code, completed.stderr)
            self.assertIn(f"FITS structural validation: {status}", completed.stdout)
            self.assertEqual(completed.stderr, "")

    def run_markdown_cli(self, output):
        return subprocess.run(
            [sys.executable, "-m", "kopernik", str(self.path), "--markdown", str(output)],
            capture_output=True, text=True,
        )

    def test_markdown_export_preserves_report_content_and_input(self):
        self.create_image()
        original = self.path.read_bytes()
        output = self.path.with_name("report.md")
        completed = self.run_markdown_cli(output)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(completed.stderr, "")
        self.assertIn("FITS structural validation: PASSED", completed.stdout)
        report = output.read_text(encoding="utf-8")
        for text in ("# Kopernik", "**FITS structural validation:** PASSED", "## HDU 0: PRIMARY",
                     "50 x 40", "| EXPTIME | 30\\.0 |", "| FILTER | unavailable |",
                     "First step", "Second step", "First comment", "Second comment",
                     "CHECKSUM/DATASUM are not verified", "No image analysis"):
            self.assertIn(text, report)
        self.assertLess(report.index("First step"), report.index("Second step"))
        self.assertEqual(self.path.read_bytes(), original)

    def test_markdown_export_of_failed_validation_keeps_failure_exit_status(self):
        self.path.write_bytes(b"not FITS")
        output = self.path.with_name("invalid.md")
        completed = self.run_markdown_cli(output)
        self.assertEqual(completed.returncode, 1)
        report = output.read_text(encoding="utf-8")
        self.assertIn("**FITS structural validation:** FAILED", report)
        self.assertIn("## Validation details", report)

    def test_markdown_export_refuses_existing_files_including_input(self):
        self.create_image()
        existing = self.path.with_name("existing.md")
        existing.write_text("Keep this report", encoding="utf-8")
        for output in (existing, self.path):
            with self.subTest(output=output):
                original = output.read_bytes()
                completed = self.run_markdown_cli(output)
                self.assertEqual(completed.returncode, 1)
                self.assertIn("Unable to save Markdown report", completed.stderr)
                self.assertNotIn("Traceback", completed.stderr)
                self.assertEqual(output.read_bytes(), original)

    def test_markdown_export_reports_missing_output_directory(self):
        self.create_image()
        completed = self.run_markdown_cli(self.path.parent / "missing" / "report.md")
        self.assertEqual(completed.returncode, 1)
        self.assertIn("existing writable directory", completed.stderr)
        self.assertNotIn("Traceback", completed.stderr)

    def test_markdown_keeps_untrusted_metadata_literal(self):
        self.create_image()
        result = inspect_fits(str(self.path))
        result.path = "<img src=x> [link](https://example.com) \u017elu\u0165ou\u010dk\u00fd.fit"
        result.hdus[0].header["OBJECT"] = "a|b <script> & `ticks`"
        result.hdus[0].header.add_history("`````` <img src=x>")
        report = render_markdown_report(result)
        self.assertIn("&lt;img src=x&gt;", report)
        self.assertIn(r"\[link\]\(https://example\.com\)", report)
        self.assertIn(r"a\|b &lt;script&gt; &amp; \`ticks\`", report)
        self.assertIn("```````text\n", report)
        self.assertTrue(report.endswith("```````\n"))
        self.assertIn("\u017elu\u0165ou\u010dk\u00fd", report)


if __name__ == "__main__":
    unittest.main()
