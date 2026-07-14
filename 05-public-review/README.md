# Public Review Guide

ICSL v0.1 is published as a candidate for critical external review. The consultation is intended to test whether the model is institutionally sound, technically implementable, appropriately scoped, and useful across different legal and administrative settings.

The conceptual model is frozen for this review cycle. That freeze creates a stable object of review; it does not place the model beyond challenge. Evidence of a blocking contradiction, unsafe boundary, or unimplementable requirement can reopen it through the documented decision process.

## Areas for Review

Reviewers are invited to examine:

- whether CommitmentPoint identifies the right unit of governed action;
- whether the eight act types are coherent across legal and administrative traditions;
- whether the six gates capture the necessary conditions of institutional acceptance;
- whether authority, evidence, discretion, binding force, adverse outcomes, and recourse are represented honestly;
- whether ProtocolVersion identity, receipts, and lifecycle semantics are reproducible;
- whether the canonical/runtime/package separation can be implemented in existing systems;
- whether extension and conformance rules permit variation without undermining interoperability;
- whether the AI boundary catches hidden authority and shadow binding;
- whether privacy and source-precedence limits are adequate;
- whether an independent implementer can produce compatible validation results.

## Review Evidence

The repository includes reviewer-runnable schemas, a 72-rule diagnostic catalog, a 26-expectation mutation suite, a synthetic Core-L2 package, a package verifier, and five persisted semantic attacks. These artifacts demonstrate internal consistency over a limited surface. They do not establish complete conformance or production interoperability.

The larger conformance fixture set and independent implementation reports remain future release requirements. Reviewers should treat absence of that evidence as a current limitation, not infer it from the existence of the smaller checks.

## Submitting Feedback

Submit feedback through [GitHub issues](https://github.com/systemi-i/opencommit/issues). A useful issue identifies the affected section or artifact, explains the practical consequence, provides an example where possible, and states whether the issue should block v0.1 or be scheduled for later work.

Use the [Feedback Intake Guide](feedback-intake-guide.md) for categories and severity. The [Reviewer Quickstart](reviewer-quickstart.md) provides a short technical path through the repository.

## Review Posture

The purpose of consultation is not to confirm the project team's assumptions. It is to expose where the specification is ambiguous, culturally or legally narrow, technically brittle, too permissive, or too costly to implement. Findings that narrow claims or reveal a failed design assumption are useful outcomes of the process.
