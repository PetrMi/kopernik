# Security Principles

## Least privilege

Kopernik SHOULD require only the permissions necessary for the requested operation.

## Untrusted input

Input files and external data MUST be treated as untrusted.

Malformed or unsupported input MUST fail safely and produce a clear error rather than causing uncontrolled behaviour.

## Data protection

The application MUST NOT transmit user data, FITS files or derived information to external services unless that behaviour is explicitly defined and approved.

## Dependencies

Third-party dependencies SHOULD be obtained from trusted sources and kept to the minimum necessary for the product capability.

## Secrets

Secrets and credentials MUST NOT be stored in source code, committed configuration or test data.

## Agent authority

The agent MUST NOT weaken security controls or introduce external data sharing as an implementation shortcut without explicit human approval.
