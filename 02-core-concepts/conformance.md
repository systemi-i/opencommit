# Conformance

Conformance states which ICSL requirements apply to a particular artifact or implementation and what evidence supports the claim.

ICSL distinguishes structural, semantic, extended, and corpus-oriented responsibilities. A package producer, validator, runtime, registry, renderer, and AI-assisted tool may interact with the same protocol while performing different functions. A useful conformance claim must therefore identify its subject rather than describe an entire product as simply “ICSL compliant.”

## Candidate Classes

`Core-L1` covers structural interoperability: required objects, six-gate presence, package structure, and canonical/runtime separation. `Core-L2` adds semantic checks for authority, outcomes, binding force, recourse, lifecycle, identity, and receipts. `Core-L3` adds high-fidelity governance and provenance requirements.

`Extended-L2` adds explicit extension negotiation to Core-L2. `Corpus-L3` adds source and encoding provenance needed for curated institutional corpora.

Encoding depth and conformance class are related but distinct. Depth describes how much institutional detail an encoding contains; class describes the requirements against which the claim is evaluated.

## Claim Discipline

A conformance statement must name the claim subject, ICSL version, conformance class, test-suite version, and result. It should also identify the validator or report that produced the result.

Passing the currently published checks demonstrates only what those checks cover. The schema-mutation suite tests selected structural protections; the worked-package verifier tests one synthetic package; the attack runner tests five specified adversarial changes. None constitutes final certification or proof of production interoperability.

The normative model is in the [Conformance Profile](../03-specification/conformance-profile.md).
