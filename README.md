# ICSL

The Institutional Commitment Specification Language (ICSL) is an open specification language for institutional protocols: governed processes composed of commitment-bearing acts. It expresses the governed structure of those processes and specifies the actions through which they produce institutional effects, in a form software can interpret without obscuring authority, accountability, or recourse.

Public systems already exchange identity data, payments, records, and workflow events. They are much less capable of exchanging the institutional meaning of an action. A downstream system may receive a permit decision, referral, eligibility result, or inspection record without being able to determine who was authorized to act, which rule governed the action, what evidence supported it, what effect followed, or how the action may be challenged.

ICSL addresses that gap by making the institutional protocol a first-class, versioned artifact.

## How ICSL Works

An ICSL **ProtocolVersion** is an immutable publication of a governed process. It identifies the responsible institution, the class of matters governed, and the CommitmentPoints at which reliance-worthy institutional action may occur.

A **CommitmentPoint** defines one atomic institutional act, such as a decision, attestation, appeal disposition, remedy, override, protocol change, closure, or delegation. Its Authority, Evidence, Reasoning, Dependency, Version, and Recourse gates state the conditions under which the act may be accepted.

An accepted act is a **Commitment**. A **Receipt** records that Commitment and pins it to the exact ProtocolVersion, CommitmentPoint, governed context, authority, and outcome involved. Later acts can suspend, remedy, override, or supersede an earlier Commitment without rewriting its history.

This structure separates institutional rules from the software used to administer them. Workflow engines, case-management products, registries, rules systems, and AI assistants may support execution, but they do not silently redefine what the institution has authorized.

## Why It Matters

For an individual institution, ICSL can make consequential procedures easier to inspect, test, compare, and move between technology providers. It can preserve institutional knowledge, reveal missing governance requirements, and give AI-assisted systems explicit operational limits.

Across institutions, common protocol semantics can make public actions easier to interpret and rely on without requiring a shared platform or uniform substantive policy. This could support interoperable public services and, over time, an open governance network in which institutions coordinate at greater speed and scale while retaining legal and operational autonomy.

## Candidate Status

ICSL v0.1 is published for external consultation. Its conceptual model is frozen, and this repository contains the candidate specification, schemas, diagnostic catalog, implementation guidance, worked package, and reviewer-runnable verification tools.

ICSL is not a final standard, and no production-interoperability claim is made. Remaining work includes a broader conformance fixture set, cross-language canonicalization vectors, independent validator implementations, and applied institutional pilots. See [Status and Roadmap](STATUS.md) and [What v0.1 Claims and Does Not Claim](05-public-review/v0.1-scope-contract.md).

## Read the Documentation

- [What Is ICSL?](01-overview/what-is-icsl.md) provides a short orientation.
- [Introducing ICSL](01-overview/concept-note.md) presents the problem, model, value, boundaries, and tests for success.
- [Five Practical Applications](01-overview/five-tangible-unlocks.md) applies the model across domains.
- [Core Concepts](02-core-concepts/README.md) explains protocols, CommitmentPoints, gates, receipts, conformance, and AI boundaries.
- [ICSL v0.1 Candidate Specification](03-specification/icsl-v0.1-candidate-spec.md) contains the normative model.
- [Protocol Assessment Guide](04-reference/protocol-assessment-guide.md) defines how to assess source fidelity, ICSL representability, and candidate conformance.
- [Agent Protocol-Alignment Brief](04-reference/agent-protocol-alignment-brief.md) is a copy-ready operating document for protocol-review agents.
- [Public Review Guide](05-public-review/README.md) explains how to review the candidate and submit feedback.

ICSL is developed through OpenCommit, the initiative responsible for its open stewardship and consultation process. Feedback is welcome through [GitHub issues](https://github.com/systemi-i/opencommit/issues).

Documentation is licensed under CC BY 4.0. Schemas, rules, and verification code are licensed under Apache-2.0. See [Stewardship](STEWARDSHIP.md) and the repository license files for details.
