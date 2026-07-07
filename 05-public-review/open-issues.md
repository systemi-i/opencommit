# Open Issues Before Public v0.1

Date: 2026-07-07.

These issues do not reopen the frozen conceptual model. They must be resolved before a
public v0.1 release claim.

## Normative Model

- Decide exact field placement for `binding_force`.
- Decide whether governance addendum fields are Core, profile-specific, or outcome-triggered.
- Define exact enum values for governance addendum fields.
- Define the minimum required fields inside `binding_effect_basis`.

## Canonicalization

- Decide whether to adopt RFC 8785 or publish a named ICSL canonical JSON profile.
- Decide number handling for legal quantities, dates, and monetary values.
- Decide whether final package hashes require source-byte hash, canonical hash, or both.

## Package Format

- Finalize `bindings/` placement and hash behavior.
- Decide whether packages require `dependencies.json`.
- Decide how package profiles declare unsupported extensions.

## References

- Define reference resolution semantics.
- Define minimum provenance for Corpus-L3.
- Define how unavailable public sources are marked.

## Conformance

- Expand seed fixtures from 8 to at least 25 publishable fixtures.
- Create negative package fixtures.
- Create receipt hash-chain fixtures with canonical content hashes.
- Create rendering fidelity fixtures.
- Create extension feature-negotiation fixtures.

## Implementation

- Harden schemas beyond skeleton state.
- Add schema validation to the CLI harness or formalize schema validation as a separate tool.
- Produce implementation reports from at least two independent validator paths.
- Add deterministic test vectors for canonicalization.
