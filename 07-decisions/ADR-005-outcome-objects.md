# ADR-005: Outcome Objects and Effect Classes

Status: Accepted

Date: 2026-07-09

## Context

`allowed_outcomes` was an array of bare tokens, and adverse-outcome protections keyed off a self-declared boolean. An encoder could evade recourse and notice obligations simply by not declaring an outcome adverse. Review identified this as a structural loophole in the protections the model exists to provide.

## Decision

`allowed_outcomes` becomes an array of outcome objects:

- `token` — the outcome identifier;
- `effect_class` — one of `favorable`, `adverse`, `mixed`, `procedural` (required);
- `recourse` — optional per-outcome override of the protocol-level recourse rule;
- `notice_state` — optional notice status for the outcome;
- `reason_giving` — optional declaration of the reason-giving requirement and legal basis;
- `dependencies` — optional dependencies on other outcomes or conditions.

Adverse-outcome rules (recourse, notice, and related protections) key off `effect_class`, not off a self-declared boolean.

## Consequences

- Every outcome must be classified; there is no unclassified default that silently escapes adverse-outcome protections.
- `mixed` and `procedural` classes let encoders be honest about outcomes that are neither purely favorable nor purely adverse.
- Earlier experimental encodings using bare tokens are invalid against the candidate schema and require migration.

## References

- 03-specification (outcome and recourse semantics)
- 04-reference/schemas (protocol schema, `allowed_outcomes`)
- Candidate specification, Section 3.9
