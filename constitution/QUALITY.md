# Quality Principles

Quality is defined by correctness and trustworthiness of results, not only by code coverage.

## Scientific correctness

Measurement algorithms MUST be verified using known or controlled input whenever practical.

## Behaviour testing

Tests SHOULD verify observable behaviour rather than implementation details.

## Regression

A bug fix SHOULD include a test demonstrating the incorrect behaviour when practical.

## Test data

Representative FITS images SHOULD gradually become part of the project's reference test dataset.

Synthetic data MAY be used where it allows a property to be tested more reliably.

## Agent responsibility

For every change Kopernik SHALL determine:

- what can fail,
- what behaviour needs verification,
- which test level is appropriate,
- whether automated testing is sufficient.

Code coverage alone MUST NOT be treated as evidence of sufficient quality.
