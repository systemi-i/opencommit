# ADR-002: Canonicalization Profile

Status: Accepted

Date: 2026-07-09

## Context

The prior canonicalization rule was defined as "JavaScript JSON serialization". Review verified that this rule diverges across languages and runtimes: integers above 2^53 are silently truncated, small magnitudes serialize differently (`1e-7` in JavaScript vs `1e-07` in other stacks), and negative zero is handled inconsistently. A hash defined over an ambiguous byte stream cannot anchor identity or tamper-evidence.

## Decision

- Adopt RFC 8785 (JSON Canonicalization Scheme, JCS) by reference as the canonicalization profile, with I-JSON (RFC 7493) constraints on all canonicalized documents.
- Legally meaningful quantities, monetary amounts, case identifiers, dates, deadlines, and rates are encoded as JSON strings rather than JSON numbers.
- Member names in canonical ICSL artifacts are restricted to ASCII; values may contain Unicode.
- ProtocolVersion identity is the SHA-256 digest over the JCS canonical bytes of the protocol document.
- The package hash vector carries source-byte hashes for all files, plus canonical-JSON hashes for JSON artifacts.

## Consequences

- Canonical bytes are reproducible across independent implementations; the prior JavaScript-specific rule is deprecated.
- Encoders must not rely on native number types for legally meaningful quantities.
- Hashes computed under the deprecated serialization rule are not comparable with hashes computed under this profile.
- Cross-language interoperability vectors remain required before final v0.1.

## References

- RFC 8785 (JCS); RFC 7493 (I-JSON)
- 03-specification (canonicalization and identity sections)
- 04-reference/schemas (hash vector fields)
- 04-reference/canonicalization
