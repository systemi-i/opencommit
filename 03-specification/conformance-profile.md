# ICSL Conformance Profile Candidate

Status: candidate draft.  
Date: 2026-07-07.

## 1. Principle

ICSL conformance is multi-dimensional. A single unqualified claim such as `ICSL compliant`
is not valid.

Every conformance claim MUST identify:

- claim subject
- conformance class
- ICSL version
- test-suite version
- result

## 2. Claim Subjects

Conformance may be claimed by:

- protocol packages
- parsers
- validators
- composers
- registries
- runtime engines
- renderers
- corpus releases

The subject MUST be explicit.

## 3. Classes

### Core-L1

Core-L1 covers structural interoperability:

- parseable package
- ProtocolVersion present
- CommitmentPoints present
- six gates present
- canonical/runtime separation enforced
- conformance declaration present

### Core-L2

Core-L2 covers semantic interoperability:

- Core-L1 requirements
- binding effect basis
- authority distinctions
- recourse semantics
- adverse-outcome recourse checks
- canonicalization behavior
- receipt chain behavior where receipts are claimed
- package hash-vector completeness

### Core-L3

Core-L3 covers high-fidelity institutional semantics:

- Core-L2 requirements
- normative reference resolution
- governance addendum where triggered
- non-executing normative fields
- reason-giving sufficiency
- rendering fidelity checks

### Extended-L2

Extended-L2 covers profile, domain, or extension-aware implementations.

Unsupported extended features MUST block, warn, or downgrade according to the declared
conformance class.

### Corpus-L3

Corpus-L3 covers curated institutional corpora:

- Core-L3 requirements
- provenance expectations
- source confidence
- transparency-gap marking
- no unproven `unknown_unpublished` adverse recourse gaps without provenance

## 4. Encoding Depths

### L1

L1 records the existence and structure of institutional commitments.

### L2

L2 records enough semantics for independent validation of binding force, authority, evidence,
recourse, package integrity, canonicalization, and conformance claims.

### L3

L3 records publication-grade institutional semantics, including references, governance
fields, reason-giving, non-executing normative fields, renderings, and provenance.

## 5. Test Suite

A conformance declaration MUST name the test-suite version used.

The seed harness currently names:

- suite id: `icsl.conformance.seed`
- suite version: `2026-07-07.seed`
- ICSL version: `0.1-freeze`

Future public release SHOULD rename this from seed to candidate or release status.

## 6. Diagnostic Stability

Diagnostic IDs SHOULD remain stable across validator implementations.

When a rule is replaced, the old diagnostic ID SHOULD be deprecated rather than silently
reused for a different meaning.
