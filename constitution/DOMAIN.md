# Domain Principles

## FITS Image

An astronomical image stored in FITS format and provided as input for analysis.

## Measurement

An objectively calculated property of an image.

Examples:

- detected star count,
- FWHM,
- background level,
- star eccentricity.

A measurement describes what was measured.

It does not by itself explain why the value occurred.

## Assessment

An interpretation of one or more measurements according to explicitly defined rules.

Examples:

- focus appears degraded,
- tracking quality appears degraded,
- background is elevated compared with reference.

## Diagnosis

A hypothesis about the physical or technical cause of an observed condition.

A diagnosis MUST NOT be presented as a measurement.

## Fundamental rule

Measurement, assessment and diagnosis MUST remain distinguishable throughout the application.
