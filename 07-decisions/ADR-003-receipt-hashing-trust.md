# ADR-003: Receipt Hashing and Trust Model

Status: Accepted

Date: 2026-07-09

## Context

Receipts are the evidentiary artifact of ICSL. The prior text did not define exactly which bytes are hashed, how chaining works, or what security property the chain actually provides. Review found this both underspecified and at risk of overclaiming: an unsigned hash chain does not prove authenticity.

## Decision

- `receipt_hash` is the SHA-256 digest over the JCS canonical bytes (per ADR-002) of the receipt object with the `receipt_hash` member removed.
- `previous_hash` is the `receipt_hash` of the prior receipt in the chain; the genesis receipt carries `null`.
- `created_at` is an RFC 3339 UTC timestamp.
- v0.1 receipts are unsigned. The chain provides tamper-evidence only relative to an externally retained chain head; it does not provide authenticity or non-repudiation. This limitation is stated, not hidden.
- The receipt schema reserves optional `issuer` and `signatures[]` fields for forward compatibility.
- v0.2 direction: receipts should be profileable as W3C Verifiable Credentials.

## Consequences

- Independent verifiers can recompute `receipt_hash` byte-for-byte and detect chain tampering, given a trusted chain head.
- No v0.1 claim may describe receipts as signed, authenticated, or non-repudiable.
- Consumers that need authenticity must retain the chain head through an external mechanism until signatures land.
- A future authenticated-receipt profile must define signatures, key governance, and revocation without changing the v0.1 content preimage silently.

## References

- ADR-002 (canonicalization)
- 03-specification (receipt semantics); 04-reference/schemas (receipt schema)
- 05-public-review/claim-guardrails.md
- 05-public-review/v0.1-scope-contract.md
