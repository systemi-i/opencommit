# ADR-009: Conformance Claim-Subject Applicability

- Status: accepted for the v0.1 consultation candidate.
- Date: 2026-07-16.

This status records acceptance of the candidate design decision. It does not approve the
separate public consultation disposition, which remains pending steward action.

## Context

The conformance profile recognized protocol packages, parsers, validators, composers, registries, runtime engines, renderers, and corpus releases as claim subjects. A declaration identified the subject with an unconstrained string, while catalog rules identified only their minimum conformance class.

Class scope alone is not a complete applicability test. Package-manifest rules are direct requirements of a protocol-package claim, not direct properties of a parser or renderer. Conversely, validating one package does not demonstrate that a validator, runtime, or composer satisfies a subject-specific behavioral profile. Without a machine-readable subject type and explicit applicability, a harness could misapply rules or report a `pass` for behavior it never tested.

## Decision

1. `ConformanceDeclaration` requires `claim_subject_type` in addition to the descriptive `claim_subject` identity.
2. The registered types are `protocol_package`, `parser`, `validator`, `composer`, `registry`, `runtime_engine`, `renderer`, and `corpus_release`.
3. Every catalog rule carries `applicability.evaluation_target`, `applicability.direct_claim_subject_types`, and `applicability.artifact_condition`.
4. Direct applicability is the intersection of class inclusion and subject-type inclusion. An artifact-facing rule may still serve as a fixture oracle for an implementation suite without becoming a direct property of the implementation.
5. A `pass` result requires the named suite to publish a profile for the declared subject type. Until those profiles exist, implementation subjects use `not_run` or `partial` and identify the missing behavior.

## Consequences

- Existing candidate ConformanceDeclarations must add `claim_subject_type`.
- Catalog consumers must read the applicability object rather than selecting rules by `scope` alone.
- Package-rule diagnostics become `not_applicable`, not `not_assessed`, for direct implementation claims.
- Subject-specific implementation profiles and fixtures remain release work; this decision does not invent their behavioral requirements.
- The institutional object model, commitment taxonomy, six gates, lifecycle, receipt identity, ProtocolVersion identity, and canonical/runtime/package separation do not change.

## Evidence

The worked package declares `protocol_package`; the conformance schema enforces the discriminator; mutation M24 rejects its omission; and all catalog entries carry explicit applicability. The mutation suite, worked-package verifier, and package attack runner pass after the change.
