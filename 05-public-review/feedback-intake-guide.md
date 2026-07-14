# Feedback Intake Guide

Review feedback should be recorded in a way that preserves the evidence, decision, and resulting change. Freezing the conceptual model means that changes require reasons; it does not mean that foundational criticism is out of scope.

## Categories

Classify each issue as one of the following:

- conceptual model;
- normative specification;
- schema or diagnostic;
- package or canonicalization;
- fixture or conformance;
- governance, authority, or recourse;
- privacy or provenance;
- implementation;
- documentation;
- future profile or extension.

## Severity

- **Blocking:** the candidate would be unsafe, contradictory, or unimplementable without resolution.
- **Important:** material to the quality or interoperability of v0.1 but not a foundational contradiction.
- **Improvement:** useful within v0.1 if it can be made without destabilizing the candidate.
- **Clarification:** wording or examples can resolve the issue without changing requirements.
- **Future:** valuable but properly addressed by a later version, profile, or extension.

## Required Information

A useful issue identifies the affected artifact and section, describes the observed problem, explains its consequence, and provides a concrete example or counterexample where possible. It should distinguish a disagreement with the model from an implementation defect or unclear explanation.

Submit issues through the [OpenCommit GitHub repository](https://github.com/systemi-i/opencommit/issues).

## Triage and Decision

Maintainers should assign a category and severity, identify whether the issue challenges a frozen invariant, and map accepted findings to a specification edit, schema or rule change, fixture, documentation correction, or future-work record. Rejected findings should receive a reason that another reviewer can examine.

Changes to the conceptual model require an architecture decision record and regression evidence. Examples include replacing CommitmentPoint as the central primitive, changing the six-gate set, allowing accepted Commitments without Receipts, changing canonical identity, or permitting runtime bindings to alter canonical semantics.
