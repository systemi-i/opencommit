# ICSL Implementation Guide Candidate

Status: candidate draft.  
Date: 2026-07-07.

## 1. Audiences

This guide is for:

- parser builders
- validator builders
- composer builders
- registry operators
- runtime engine builders
- public-service integration teams
- AI-assisted protocol drafting systems

## 2. Implementation Order

Recommended implementation order:

1. Parse package and ProtocolVersion JSON.
2. Validate CommitmentPoint structure.
3. Enforce six-gate presence.
4. Enforce canonical/runtime separation.
5. Validate binding effect basis.
6. Validate authority semantics.
7. Validate recourse semantics.
8. Implement canonicalization and hashes.
9. Verify receipt chains.
10. Emit stable diagnostics.
11. Run the conformance suite.

## 3. Validator Behavior

A validator SHOULD emit a ValidationReport with:

- artifact kind
- harness or validator version
- validity result
- diagnostics

Each diagnostic SHOULD include:

- rule id
- severity
- JSON pointer path
- message

Validators SHOULD fail closed for unknown required semantics at the claimed conformance
class.

## 4. Runtime Behavior

A runtime MUST evaluate a GovernedContext against a pinned ProtocolVersion.

A runtime MUST NOT let deployment bindings alter canonical gate outcomes.

A runtime SHOULD distinguish:

- durable facts
- derived state
- attempted commitment
- accepted commitment
- blocked or rejected evaluation

Accepted commitments MUST produce receipts.

Blocked or rejected attempted commitments SHOULD produce evaluation records.

## 5. Composer Behavior

A composer helps authors create ICSL artifacts.

A composer SHOULD:

- warn when a likely CommitmentPoint is missing
- warn when a stage appears advisory but has downstream binding effect
- require binding effect basis
- require six gates
- distinguish task owner from authority
- mark recourse gaps
- keep runtime bindings outside canonical protocol truth

A composer MUST NOT hide uncertainty by producing overconfident conformance claims.

## 6. Registry Behavior

A registry stores, indexes, and distributes ProtocolVersions and packages.

A registry SHOULD:

- preserve immutable ProtocolVersion hashes
- expose conformance declarations
- expose package hash vectors
- track supersession
- reject mutable overwrite of published versions
- distinguish canonical artifacts from renderings and bindings

## 7. Rendering Behavior

A renderer presents ICSL artifacts to humans.

A renderer MUST NOT add semantics that are absent from canonical protocol truth.

A renderer SHOULD make the following visible when relevant:

- binding effect
- authority
- evidence requirements
- recourse state
- version pin
- dependencies
- adverse outcome consequences
- uncertainty or transparency gaps

## 8. AI-Assisted Systems

AI systems may help draft, explain, classify, and review ICSL artifacts.

AI systems SHOULD be treated as drafting and analysis aids unless explicitly bound by an
institutional protocol.

AI-generated content MUST NOT silently become gate truth. It must be converted into accepted
facts, rules, human decisions, or institutional commitments before it can affect deterministic
evaluation.

## 9. Common Failure Modes

High-risk implementation failures:

- treating workflow tasks as commitments
- treating task owners as legal authorities
- omitting recourse for adverse outcomes
- allowing runtime connector fields into canonical protocol JSON
- claiming conformance without naming class and test-suite version
- allowing UI renderings to add or suppress legal semantics
- treating AI classification as deterministic institutional truth
