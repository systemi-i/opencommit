# Open Issues

The conceptual model is frozen for consultation, but several matters remain unresolved before a final v0.1 release. This page lists current questions only; resolved design decisions are recorded in the [decision log](../07-decisions/README.md).

## Governance and Authority

- Define the profile conditions under which governance-addendum fields become required and close their vocabularies where interoperability depends on them.
- Represent joint and collegial authority, including boards, panels, quorum, and co-signature requirements.
- Test the commitment taxonomy and Authority gate across legal traditions and multilateral institutions.

## Sources and Provenance

- Define reference-resolution behavior, including unavailable or superseded public sources.
- Complete the minimum provenance requirements for `Corpus-L3`.
- Specify how publication of a source encoding is itself authorized, reviewed, and versioned.
- Establish a public corpus methodology covering sampling, source rights, encoder instructions, quality review, and inter-encoder reliability.

## Privacy and Retention

- Define profiles for detachable personal-data payloads, including keyed or salted hashes, erasure workflows, and verification after erasure.
- Determine when retention information is required and whether a null or unspecified retention profile is ever conformant.

## Conformance and Interoperability

- Publish at least 25 positive, negative, adversarial, and package-level fixtures.
- Add canonicalization vectors exercised across multiple languages and implementations.
- Add receipt-chain, extension-negotiation, rendering-fidelity, and runtime-leakage fixtures.
- Produce independent validator implementations and implementation reports.
- Define the process by which candidate testing may eventually support certification or formal conformance claims.

## Implementation

- Separate the worked-package verifier from a reusable validator architecture.
- Define registry behavior for version discovery, source resolution, and immutable publication.
- Test integration profiles with established domain standards, beginning with carefully bounded examples.
- Measure the cost of creating and maintaining source-grounded encodings in real institutions.

## Deferred Beyond v0.1

- Migration semantics between candidate, release-candidate, and final identifiers and hashes.
- Receipt signatures, key management, revocation, and possible Verifiable Credentials profiling.
- Atomic bundles for legally indivisible instruments that perform more than one institutional act.
- Cross-protocol transactions and distributed rollback or compensation semantics.

An item may be deferred only if v0.1 remains internally coherent and the deferral is explicit in the specification or decision record.
