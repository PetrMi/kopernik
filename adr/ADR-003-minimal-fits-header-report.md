# ADR-003: Minimal FITS Header Report

Status: Accepted

Approved by the project owner on 2026-10-07.

## Context

The repository has no implementation, runtime choice, or tests. The current
request is a FITS validation and header report for `test-data/r_pp_ic1805.fit`,
explicitly excluding pixel analysis and image-quality assessment. README's
Star Count milestone describes a broader scope and needs to be updated when
this increment is implemented. No Constitution changes are required.

This affects FITS input, validation, presentation, dependency management and
testing. It introduces no scientific measurement, assessment or diagnosis.

## Decision

- Use Python 3.12 or later and Astropy's `astropy.io.fits` for FITS parsing and
  verification. Declare the supported dependency version in project metadata.
  Astropy provides an established FITS implementation; writing our own general
  FITS parser would add unnecessary correctness and maintenance risks.
- Provide a local CLI: `python -m kopernik PATH`. Print an English plain-text
  report to standard output, suitable for terminal reading or redirection.
  No web interface, external services or input-file modification is needed.
- Keep FITS inspection separate from report formatting. Do not introduce
  measurement or assessment abstractions before they are needed.
- Initially support local, uncompressed FITS files. Unsupported inputs and
  unreadable files produce clear errors and a nonzero exit status.
- Define validation narrowly and explicitly: verify all HDU headers using
  Astropy's strict verification without repairs, and check block alignment and
  whether the file contains the data spans declared by its headers. Merely
  opening a file successfully is insufficient. Report verification failures
  and parser warnings without silently treating them as a clean pass.
- A successful report says that FITS structural validation passed within this
  scope. It does not claim complete FITS conformance or image-data integrity.
  Do not access pixel arrays, compute statistics, interpret image quality, or
  verify CHECKSUM/DATASUM in this increment; explicitly disclose those limits.
- Show filename, file size, HDU count, HDU types, BITPIX and axis lengths from
  headers. Summarize available observation metadata, preserving keyword names
  and declared units, then list all header cards in order, including repeated
  COMMENT and HISTORY cards. Missing metadata remains explicitly unavailable;
  do not infer missing units, RGB semantics or scientific meaning.
- Return zero only for a clean structural validation result. Distinguish
  invalid input from inability to complete validation in report wording.

## Alternatives

- A custom standard-library FITS parser avoids a dependency but makes this
  project responsible for FITS parsing and verification edge cases.
- A graphical or web interface adds dependencies and presentation complexity
  without a requirement for interactive use.
- Star detection is deferred by the explicit current request.

## Verification plan

Use standard-library unittest with controlled FITS fixtures for a valid image,
multiple HDUs, absent optional metadata, repeated header cards, non-FITS input,
malformed headers, truncated data, unsupported input and missing paths. Exercise
the CLI's output and exit status. Verify inspection does not load pixel arrays
or modify the input. Run the CLI on the supplied reference file and review its
human-readable report, including the explicit validation limits.

The reference file is local user-provided data. Its provenance and redistribution
permission have not been established; do not commit or upload it. Record the
verification procedure and result locally in English.

## Consequences

Python and Astropy become the initial technology choices. Astropy introduces
transitive dependencies, justified by its FITS support. Structural verification
does not detect every possible corruption in data values. Future checksum
verification, compressed-input support and scientific analysis require explicit
scope extensions. The report must keep these limitations visible.

This decision was explicitly approved by the project owner before implementation.

## References

- [Architecture principles](../constitution/ARCHITECTURE.md)
- [ADR status rules](README.md)
- [Astropy FITS verification](https://docs.astropy.org/en/stable/io/fits/usage/verification.html)
- [Astropy FITS file handling](https://docs.astropy.org/en/stable/io/fits/api/files.html)
