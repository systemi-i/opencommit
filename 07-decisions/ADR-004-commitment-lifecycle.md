# ADR-004: Commitment Lifecycle and Derived Status

Status: Accepted

Date: 2026-07-09

## Context

Real institutional commitments do not end at acceptance. Decisions are suspended pending appeal, revoked, quashed by courts, superseded by later decisions, varied, or expire. The prior model had no lifecycle beyond acceptance, so two verifiers reading the same chain could disagree about whether a commitment was still in force.

## Decision

- Commitment status set: `accepted`, `suspended`, `revoked`, `quashed`, `superseded`, `expired`, `varied`.
- Status changes are append-only Receipts. Each carries an `acts_on` object with `target_receipt_id` and an effect: `suspend`, `revive`, `revoke_ex_tunc`, `revoke_ex_nunc`, `quash`, `supersede`, `vary`, or `expire`.
- A CommitmentPoint that may act on earlier Commitments declares `acts_on_allowed`, including permitted effects and target CommitmentPoint identifiers.
- A deterministic derived-status algebra defines how the current status of a commitment is computed from the ordered sequence of records acting on it, so that independent verifiers compute the same current status from the same chain.
- Consumers MUST be able to resolve the current status of any commitment in a chain.

## Consequences

- The receipt chain remains append-only; nothing is edited or deleted to change status.
- Ex tunc and ex nunc revocation are distinguishable, matching legal practice.
- Verifier implementations gain a testable requirement (status resolution) that belongs in the conformance suite.
- Conformance fixtures must cover order, target resolution, terminal effects, and invalid revival.

## References

- ADR-003 (receipt chain)
- 03-specification (commitment semantics)
- 04-reference/schemas (status/correction records)
- Candidate specification, Section 3.11
