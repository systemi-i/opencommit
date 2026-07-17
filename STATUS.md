# Status and Roadmap

## Current Maturity

ICSL v0.1 is a consultation candidate published for external review. Its conceptual model is frozen: changes that alter the core objects, commitment taxonomy, six gates, lifecycle, receipt identity, or layer boundaries require an explicit decision record and a demonstrated blocking defect.

The candidate is suitable for review, experimental implementation, fixture development, and carefully scoped pilots. It is not a final public standard, a certification scheme, or evidence of production interoperability.

## Available Artifacts

The repository currently provides:

- the ICSL v0.1 candidate specification;
- package-format and conformance profiles;
- an implementation guide;
- twelve Draft 2020-12 JSON Schemas;
- a machine-readable catalog of 74 diagnostics;
- canonicalization and hashing requirements;
- a synthetic Core-L2 worked package;
- a 28-expectation schema-mutation suite;
- a package verifier and five persisted semantic attacks;
- public-review, scope, lineage, stewardship, and contribution documents.

The worked package and test tools are evidence that the published artifacts are internally consistent. They are not a substitute for independent implementations or a full conformance suite.

The July 2026 field review has a proposed public [disposition record](05-public-review/consultation-disposition-2026-07.md) pending steward approval. It did not identify a blocking defect in the frozen model. It did sharpen current documentation and establish a [companion roadmap](05-public-review/companion-roadmap.md) for execution bindings, effects and reconciliation, composition, references, privacy, and conformance governance.

## Release Milestones

### 1. Conceptual-Model Freeze

**Status: complete.** The candidate model, schemas, rules, and proof package are aligned and the published regression checks pass.

### 2. Consultation Candidate

**Status: complete.** The candidate is published with an identified steward and licensor, an ICSL-first public identity, a coherent documentation set, decision records, and an explicit consultation and feedback process.

### 3. Public v0.1

**Status: future.** A final v0.1 release requires evidence beyond internal consistency:

- at least 25 public conformance fixtures covering positive, negative, adversarial, and package-level behavior;
- canonicalization interoperability vectors;
- at least one independent validator implementation and implementation report;
- subject-specific conformance profiles or explicit limitations for each supported claim subject;
- resolution or explicit deferral of the issues listed in [Open Issues](05-public-review/open-issues.md).

## Version Labels

- `0.1-freeze` identifies the current machine-readable candidate used by the schemas and examples.
- `0.1-rc` identifies the external consultation release-candidate stage.
- `0.1` will identify a final public standard if the release requirements are met.

These labels describe maturity, not legal authority or certification.

### Candidate Revision: 2026-07-16

This consultation pass requires `ConformanceDeclaration.claim_subject_type` and adds
explicit subject applicability to every diagnostic rule. Existing candidate declarations
must add the appropriate registered subject token, and catalog consumers must select rules
by both class and subject type. The catalog now contains 74 rules and is identified as
`icsl.rules.candidate.2026-07-16`. The change is recorded in
[ADR-009](07-decisions/ADR-009-conformance-claim-subject-applicability.md) and does not
alter the frozen institutional object model.

## Evidence and Research Corpus

Exploratory encodings across public-service families informed development of the model and commitment taxonomy. They remain research material rather than a public benchmark. They have not yet undergone independent encoding, systematic source review, or inter-encoder reliability measurement.

A future corpus release will require documented selection methods, source provenance, licensing, jurisdictional coverage, encoder instructions, review status, known gaps, and clear separation between illustrative, source-grounded, and conformance-grade artifacts.

## Public Claims

Implementations should describe themselves as testing or implementing the ICSL v0.1 candidate and should identify the claim subject identity, subject type, version, conformance class, suite version, and result involved. Unqualified claims of being “ICSL compliant” are premature. See [Claims and Maturity](05-public-review/claim-guardrails.md).
