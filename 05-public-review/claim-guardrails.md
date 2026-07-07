# Claim Guardrails

Date: 2026-07-07.

## Allowed Claims

The project may claim:

- ICSL has a v0.1 release-candidate package.
- The conceptual model is frozen for candidate review.
- A candidate normative spec exists.
- A candidate package format exists.
- A candidate conformance profile exists.
- A standards harness exists.
- The harness currently passes 40 fixtures.
- The release is ready for internal and invited external review.

## Prohibited Claims

The project must not claim:

- ICSL is a final public standard.
- Any implementation is unqualified `ICSL compliant`.
- Production interoperability has been proven.
- The package format is final.
- The canonicalization profile is final.
- The validator is a complete reference implementation.
- ICSL produces legal advice or legal authority by itself.
- AI systems are authorized as deterministic gate authorities.

## Required Claim Shape

Any conformance claim must include:

- claim subject
- conformance class
- ICSL version
- test-suite version
- result

Example:

```text
Example Validator X reports pass for ICSL 0.1-freeze Core-L2 using test suite 2026-07-07.seed.
```

Avoid:

```text
Example Validator X is ICSL compliant.
```
