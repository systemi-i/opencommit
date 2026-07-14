# ADR-008: Commitment Act Taxonomy (`commitment_type`)

Status: Accepted

Date: 2026-07-13

## Context

Earlier IGSL specifications required a `commitment_type` field, and exploratory protocol encodings continued to use it. An intermediate ICSL v0.1 draft omitted the field without a recorded decision or migration rationale. That omission weakened comparability and left distinctions such as decision versus attestation, remedy versus override, and rule change versus case-level action implicit.

A closed taxonomy also presents a risk: institutional traditions may contain acts that do not fit the core categories. The model therefore needs both a stable core and a controlled extension path.

## Decision

Every CommitmentPoint has one primary `commitment_type` selected from eight core values:

- `DECIDE`
- `ATTEST`
- `APPEAL`
- `REMEDY`
- `OVERRIDE`
- `EVOLVE`
- `CLOSE`
- `DELEGATE`

The type is classificatory. It does not create authority, binding force, recourse, or institutional effect and never substitutes for the gates, outcomes, binding-effect basis, or act relationships.

At `Extended-L2`, a CommitmentPoint may use the marker `EXTENSION`. It must then declare a namespaced identifier, definition, rationale, and fallback semantics. A core type may carry a namespaced subtype for domain-level comparison, but the subtype has no normative v0.1 semantics.

The authoring placeholder `GENERIC` is not valid in canonical artifacts.

## Classification Procedure

Classification is applied to one atomic institutional act. Multi-act stages should be split before classification. The normative first-match order is:

1. `EVOLVE`
2. `DELEGATE`
3. `APPEAL`
4. `REMEDY`
5. `OVERRIDE`
6. `CLOSE`
7. `DECIDE`
8. `ATTEST`
9. `EXTENSION`

The candidate specification defines each test and the rules for legally indivisible instruments.

## Boundary Decisions

An `APPEAL` disposes of the merits of a challenge to an identified prior Commitment. Admissibility, timeliness, standing, and other procedural determinations within recourse are `DECIDE`, even where they terminate the challenge.

A `REMEDY` responds to a defect or wrong in a prior Commitment, its procurement, or its execution. An `OVERRIDE` displaces an otherwise valid Commitment under superseding authority or interest.

An `ATTEST` characterizes the truth, adequacy, or evidentiary state of a proposition. A `DECIDE` determines a right, obligation, permission, procedural course, or status. Where an outcome does both, it is `DECIDE` if it directly changes the subject's position without another Commitment intervening; otherwise it is `ATTEST` and a later `DECIDE` relies on it through the Dependency gate.

## Structural Consequences

Relational act types carry explicit structure. `APPEAL`, `REMEDY`, and `OVERRIDE` identify the CommitmentPoints whose receipts they may act on; `OVERRIDE` also identifies its authority basis. `EVOLVE` identifies the protocol or version changed. `DELEGATE` identifies the recipient and scope.

Receipts may copy the CommitmentPoint's type, but the hashed ProtocolVersion remains authoritative. Runtime validators check that an act targets only receipts of the CommitmentPoints permitted by its template.

Extensions are sealed in both directions: core-class artifacts cannot contain an `EXTENSION` type, and an artifact containing one must declare `Extended-L2`. Consumers that do not recognize an extension either process its declared core fallback with a warning or block when the fallback is `none`.

## Evidence and Limits

The taxonomy was informed by exploratory encodings across public-service families. That work supported design discovery but does not establish empirical validation. It was not independently encoded, inter-encoder reliability has not been measured, and the source material reflects a limited set of drafting and legal traditions.

Cross-tradition review is therefore a release requirement. `FACILITATE` remains a plausible extension candidate for mediation or conciliation acts. `ASSESS` currently appears more likely to resolve through the `ATTEST`/`DECIDE` boundary, but both questions require better corpus evidence.

## Consequences

- Existing experimental artifacts must migrate invalid or placeholder values.
- Validators can diagnose missing, invalid, or structurally inconsistent types.
- Domain profiles can add comparison through namespaced subtypes without changing core semantics.
- A proposal to change the eight core values requires a new ADR, migration analysis, and classification fixtures.

## References

- Candidate specification, Section 3.5a
- Conformance profile
- Reference schemas and rule catalog
- Worked permit package
