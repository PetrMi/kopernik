# Kopernik

Kopernik is an experimental astronomy image-analysis application developed primarily by an AI engineering agent.

The goal of the project is not only to build the application, but to explore Product Engineering Constitution driven development.

Humans define intent, principles and decisions. Kopernik analyzes, proposes, implements and verifies changes within those boundaries.

> AI has expertise. Humans have authority.

## Product vision

Kopernik helps astrophotographers objectively evaluate the quality of astronomical FITS images.

The application will gradually provide measurements and assessments that help identify images affected by problems such as:

- poor focus,
- tracking errors,
- high background,
- clouds or reduced transparency,
- other image-quality degradation.

Scientific measurements must always be distinguishable from their interpretation.

## Current version

### v0.1 — FITS header report

The first version intentionally has a very small scope.

Given a local, uncompressed FITS file, Kopernik:

1. verifies FITS headers, block alignment and declared HDU data spans,
2. reports basic file information and available header metadata,
3. produces an English, human-readable text report with all header cards.

No pixel arrays are loaded and no image analysis or quality assessment is
performed. CHECKSUM/DATASUM and pixel-value integrity are not verified.
Passing structural validation does not establish full FITS conformance.
Star detection remains a future increment. See [ADR-003](adr/ADR-003-minimal-fits-header-report.md).

### Install and run (PowerShell, Python 3.12+)

```powershell
python -m venv .venv
.venv/Scripts/python -m pip install -e .
.venv/Scripts/python -m kopernik test-data/r_pp_ic1805.fit
```

To save the report locally:

```powershell
New-Item -ItemType Directory -Force reports | Out-Null
.venv/Scripts/python -m kopernik test-data/r_pp_ic1805.fit | Out-File -Encoding utf8 reports/r_pp_ic1805.txt
```

Exit status is 0 only for a clean structural validation, 1 for failed or
incomplete validation or report-write failures, and 2 for incorrect CLI usage. Parser warnings are
included in the report and prevent a clean pass. Reports distinguish invalid
structure from unsupported or inaccessible input. Available header information
can be partial when validation fails; check the overall status first.

### Markdown export

Use `--markdown PATH` to also save a structured Markdown report with headings,
metadata tables and literal header cards:

```powershell
New-Item -ItemType Directory -Force reports | Out-Null
.venv/Scripts/python -m kopernik test-data/r_pp_ic1805.fit --markdown reports/r_pp_ic1805.md
```

The terminal still receives the usual text report. The Markdown file uses UTF-8
and includes the same validation result, limitations and metadata. Reports for
failed or incomplete validation can also be saved; their exit status remains 1.
The destination directory must exist. Existing files (including the FITS input)
are never overwritten; select a new filename for another export. Markdown syntax
and HTML in header values are displayed literally.

This adds a presentation format to the CLI from ADR-003 without changing FITS
inspection, scientific scope, dependencies or the default text output.

Only local regular files are supported. Whole-file compression and tile-compressed
images are explicitly unsupported. Input is opened read-only, never repaired or
transmitted. Reports reproduce header metadata, which may contain personal or
location information; generated reports and the supplied sample stay local.

### Tests

```powershell
.venv/Scripts/python -m unittest discover -s tests -v
```

Tests generate their own FITS fixtures and do not require the private reference
file. The manual reference-file verification is documented in
[docs/VERIFICATION.md](docs/VERIFICATION.md).

The implementation shall be developed by the Kopernik agent according to `AGENTS.md` and the Product Engineering Constitution.

## Wishlist

- [x] v0.1 — FITS header report
- [ ] small FITS image preview in markdown report
- [ ] FITS star count report
- [ ] Measure FWHM
- [ ] Measure star eccentricity / elongation
- [ ] Measure image background
- [ ] Compare images against a reference image
- [ ] Detect focus degradation
- [ ] Detect tracking degradation
- [ ] Evaluate image quality across an imaging session
- [ ] Produce machine-readable reports
- [ ] Visualize detected stars and measurements
- [ ] Define an overall quality assessment methodology
