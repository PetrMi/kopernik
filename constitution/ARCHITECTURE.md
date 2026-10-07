# Architecture Principles

## Conceptual flow

```text
FITS Input
    ↓
Image Measurement
    ↓
Measurements
    ↓
Assessment
    ↓
Report
```

## Separation of concerns

Reading image data, calculating measurements, assessing measurements and presenting results are separate responsibilities.

## Scientific logic

Scientific algorithms MUST NOT depend on presentation concerns.

## Evolution

Architecture should support adding new independent measurements without requiring fundamental changes to existing measurements.

## Decisions

Significant architectural decisions SHALL be recorded as ADRs.

The agent may propose an ADR but MUST NOT consider it accepted until approved by a human.
