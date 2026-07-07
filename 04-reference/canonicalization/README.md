# Canonicalization Seed Rules

These are P0 rules for deterministic JSON canonicalization in the seed harness.
They are sufficient for fixture work but should become a normative byte-level section
before publication.

## Seed Rules

1. JSON object keys are sorted by Unicode code point order.
2. Arrays preserve source order.
3. Null values are retained.
4. Numbers are emitted using JavaScript JSON serialization.
5. Strings are emitted using JSON string escaping.
6. Whitespace is omitted from the canonical byte stream.
7. Hashes are SHA-256 over UTF-8 canonical JSON bytes.
8. Package hash vectors hash source file bytes in the seed harness.
9. `hashes.json` is not required to include a hash of itself.

## Open Standards Questions

- Whether final ICSL canonicalization adopts RFC 8785 directly or a named profile.
- Whether numeric domains should be restricted to strings for legal quantities and dates.
- Whether null retention remains universal or is profile-specific.
- Whether package hash vectors continue to hash source bytes, canonical JSON, or both.
