# FITS Header Report Verification

Verified on 2026-10-07 using Windows, Python 3.12.10, Astropy 8.0.1 and
NumPy 2.5.3. The scope follows accepted ADR-003.

## Automated checks

Run `.venv/Scripts/python -m unittest discover -s tests -v`.
All 20 tests passed in the verified environment, including Markdown export tests.
Synthetic fixtures cover valid and invalid headers, missing END, SIMPLE = F,
non-FITS input, multiple HDUs, truncated data (including whole-block truncation),
trailing bytes and parser warnings, unsupported compression, missing files,
absent metadata, repeated cards, terminal-control escaping and CLI exit status.
Data properties are guarded in a test to detect any access to image or table
arrays. A byte-for-byte comparison verifies input preservation.

Run `.venv/Scripts/python -m pip check` to check installed dependency consistency.
The check passed with no broken requirements.

## Local reference verification

Command: `.venv/Scripts/python -m kopernik test-data/r_pp_ic1805.fit`.

The CLI returned 0, reported structural validation PASSED, emitted no warnings
or standard-error output, and produced a readable report at
`reports/r_pp_ic1805.txt`. The 155,664,000-byte input contains two HDUs:

- Primary image: BITPIX 16; FITS axis lengths 6224 x 4168 x 3.
- Image extension named ICCProfile: BITPIX 8; axis length 1256.

The report includes available observation metadata with original keyword names
and comments, explicitly marks missing summary fields, and preserves ordered
COMMENT and HISTORY entries. Metadata is treated as declarations from the file,
not independent scientific measurements. The third axis is not inferred to have
any particular physical meaning.

SHA-256 before and after the CLI run was identical:
`f520877761ac8a0951ed9ff10898971c8a570ecf67435175f67ba59e2a8a14f3`.
Hashing was an external test of input preservation, not application pixel analysis.

The reference file and its generated report are ignored by Git because
redistribution permission has not been established. They were not uploaded.

## Markdown export verification

The CLI was also run with `--markdown reports/r_pp_ic1805.md`. It returned 0,
emitted no errors, and saved a UTF-8 Markdown report containing the PASSED status,
both HDUs, metadata tables and ordered header cards. Input SHA-256 remained
identical to the value above. The generated Markdown stays local with other
reports. Its structure and content were reviewed from the generated source;
no particular Markdown viewer is required by the application.

Automated export tests cover successful saving, failed-validation reports,
existing-file and input-file protection, missing destination directories, and
escaping untrusted Markdown/HTML, including backticks inside fenced header cards.

## Validation limits

Validation checks Astropy-supported header constraints, FITS block alignment and
declared HDU extents. It does not inspect pixel values, verify CHECKSUM/DATASUM,
or establish exhaustive FITS conformance, scientific correctness, or image
quality. Parser warnings prevent a clean validation pass. Unsupported inputs
and I/O failures are distinguished from detected structural violations.
