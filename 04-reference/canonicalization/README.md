# Canonicalization Profile

ICSL uses established canonicalization standards rather than defining a bespoke byte format. Canonical JSON is required wherever content identity or hashing depends on a stable representation.

## Normative Profile

1. Canonical bytes are produced using RFC 8785, the JSON Canonicalization Scheme (JCS).
2. Canonicalized documents satisfy I-JSON constraints under RFC 7493.
3. Legally meaningful quantities, monetary amounts, identifiers, dates, deadlines, and rates are encoded as JSON strings rather than JSON numbers.
4. Object member names in canonical ICSL artifacts are ASCII. Values may contain Unicode.
5. Hash-bearing fields use tagged lowercase strings of the form `sha256:<64 hexadecimal characters>`.
6. A ProtocolVersion is identified by the SHA-256 hash of its complete JCS canonical bytes. The object does not contain its own hash.
7. Package hash vectors contain a source-byte hash for every declared file and a canonical-JSON hash for every JSON artifact. `hashes.json` is self-exempt.

The ASCII member-name rule removes a cross-language ordering hazard. RFC 8785 sorts member names by UTF-16 code units, while some common runtimes sort Unicode strings by code point. Restricting keys to ASCII makes those orderings identical without limiting Unicode values.

## Verifier Requirements

Implementations should use a conforming RFC 8785 library. A verifier that uses compact, key-sorted JSON serialization as a fallback must first establish both of the following conditions and fail closed otherwise:

1. the document contains no non-string JSON numbers, excluding booleans; and
2. every member name is ASCII.

Under those constraints, the fallback used by the published Python checks is byte-identical for the supported input domain. It is not a general JCS implementation and must not be represented as one.

## Receipt Hash Preimage

`receipt_hash` is the SHA-256 digest of the RFC 8785 canonical bytes of the Receipt object with the `receipt_hash` member removed. `previous_hash` contains the prior Receipt's hash; the genesis Receipt uses `null`.

ProtocolVersion hashes, Receipt hashes, content hashes, and package hashes cover different preimages and must not be substituted for one another. The [candidate specification](../../03-specification/icsl-v0.1-candidate-spec.md) and [package format](../../03-specification/package-format.md) define those boundaries normatively.

## Outstanding Interoperability Work

The profile is precise, but independent cross-language vectors are still required before final v0.1. Those vectors should include Unicode values, nested objects, control characters, empty structures, receipt preimages, ProtocolVersion identity, and package dual hashes.
