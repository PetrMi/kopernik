# ADR-002: Separate Measurement from Assessment

Status: Accepted

## Context

Astronomical image analysis combines objective measurements with interpretation of those measurements.

Mixing these concepts would make results difficult to explain and could cause hypotheses to be presented as facts.

## Decision

Kopernik shall explicitly separate:

1. measurement,
2. assessment,
3. diagnosis.

Measurement algorithms shall not contain product-level quality judgements unless explicitly defined by the Constitution.

## Consequences

Measurements can be reused by different assessment methods.

Reports can explain why an assessment was produced.

New assessment methodologies can evolve without changing the underlying measurements.
