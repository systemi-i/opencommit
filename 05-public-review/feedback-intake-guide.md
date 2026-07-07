# Feedback Intake Guide

Date: 2026-07-07.

## Principle

Feedback should be triaged without immediately changing the conceptual model. The v0.1
candidate is frozen for review. Feedback should be classified, not absorbed impulsively.

## Intake Classes

- Conceptual issue
- Normative spec issue
- Schema issue
- Rule/diagnostic issue
- Fixture/conformance issue
- Package format issue
- Governance/recourse issue
- Implementation issue
- Documentation issue
- Out of scope for v0.1

## Severity

- Blocking for public v0.1
- Important before public v0.1
- Useful improvement
- Clarification only
- Future profile or extension

## Triage Steps

1. Record the feedback in the relevant template.
2. Identify the affected artifact.
3. Identify whether it challenges the frozen conceptual spine.
4. Assign severity.
5. Decide whether it affects release-candidate status or public-v0.1 readiness only.
6. If accepted, map it to a concrete edit or fixture.
7. If rejected, record the reason.

## Reopening The Conceptual Model

Escalate before accepting feedback that would:

- replace CommitmentPoint as the central primitive
- remove one of the six gates
- allow accepted commitments without receipts
- make AI/probabilistic inference deterministic gate truth
- allow canonical protocol truth to depend on deployment bindings
- allow unqualified conformance claims
