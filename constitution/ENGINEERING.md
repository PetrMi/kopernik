# Engineering Principles

## Purpose

Engineering choices should keep Kopernik understandable, testable and easy to evolve while avoiding complexity that is not justified by current product needs.

## Principles

### Smallest sufficient solution

Implement the smallest solution that satisfies the current requirement and the Constitution.

### Explicit over hidden behaviour

Important behaviour, configuration and assumptions SHOULD be explicit and discoverable.

### Prefer established project patterns

When the project already contains a suitable pattern, new code SHOULD follow it unless there is a documented reason to change it.

### Dependency discipline

New dependencies MUST have a clear purpose and SHOULD be justified by the value they provide compared with implementing or using existing capabilities.

### Maintainability

Code SHOULD favor clear responsibilities, meaningful naming and straightforward control flow over unnecessary abstraction.

### Durable knowledge

Reusable engineering knowledge discovered during implementation SHOULD be captured in the Constitution, an ADR or other appropriate project documentation rather than remaining only in a prompt or conversation.
