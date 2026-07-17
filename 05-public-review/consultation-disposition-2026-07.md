# Consultation Disposition: July 2026 Field Review

Status: approved public disposition.

Review date: 2026-07-16.

Approved by the steward: 2026-07-17.

## Purpose

This record explains the disposition of an implementation-informed consultation submission on the ICSL v0.1 candidate. It distinguishes corrections to current documentation from release evidence, companion specifications, profiles, and longer-term research. The submission drew on systems that connect institutional protocols to operational capabilities; it was not an independent conformance assessment.

## Governing Disposition

The review identified no blocking defect that requires reopening the frozen v0.1 conceptual model. The object model, eight commitment types, six gates, outcome protections, lifecycle algebra, ProtocolVersion pinning, receipt identity, and canonical/runtime/package separation remain unchanged.

That conclusion does not mean the current candidate is complete. Cross-language canonicalization vectors, a broader fixture set, and an independent validator remain requirements for final v0.1. The review also identified a substantial body of work at the boundary between institutional semantics and execution. Those topics are tracked as companion specifications or profiles so they can be tested against real implementations without allowing runtime systems to redefine canonical protocol truth.

## Dispositions

| Topic | Disposition | Consequence |
| --- | --- | --- |
| Canonical identity and lexical forms | JCS correctly identifies a published object. Lexically different values such as `"1000"` and `"1000.00"` are different artifacts even when a domain treats them as equivalent. | Keep the core rule. Define domain lexical forms in profiles where equivalence matters; publish cross-language vectors before final v0.1. |
| Core-L1 binding-effect declaration | Binding effect is part of the inclusion test for a CommitmentPoint, not optional semantic enrichment. | Keep the rule. Describe Core-L1 more accurately as the minimum institutional skeleton. |
| Notice and reason-giving at Core-L2 | Core-L2 requires a declared posture, including a legally grounded declaration that reasons are not required. It does not require a validator to judge the legal adequacy of the posture or the reasons. | Keep the rule and state the validation limit explicitly. |
| Commitment distinct from Receipt | The accepted institutional act and its technical record are conceptually different, even when an implementation persists them together. | Keep the distinction. |
| Pinned cases and institutional learning | Version pinning protects the governing terms of a case. It does not prevent analysis across cases or proposals for future versions. | Keep pinning. Develop shadow evaluation, evidence-linked amendment proposals, and cross-case learning outside the pinned case. |
| Receipt privacy | Adverse posture is derived from a receipt and its pinned ProtocolVersion, not copied directly into the receipt. Derivability and linkability can still create privacy risks. | State that receipts are not public by default and develop privacy, selective-disclosure, retention, residency, and erasure profiles. |
| Canonicalization performance | No credible performance defect was demonstrated. Receipt chains serialize within a context; contexts can be processed independently. | No current change. Measure real implementations rather than weakening integrity requirements speculatively. |
| Typed execution bindings | A governed protocol needs a testable interface to operational capabilities without importing deployment state into canonical truth. | Develop a non-canonical companion specification. A binding may supply candidate inputs or invoke capabilities; it must not determine gate truth. |
| Rail effects and reconciliation | A Commitment may require a payment, registry, notification, or other external effect whose application can fail after institutional acceptance. | Develop effect-obligation and reconciliation records with at least `pending`, `applied`, `failed`, and `compensated` states. |
| Cross-protocol composition | Federation requires references and dependencies across independently governed protocols and institutions. | Develop composition and cross-institution receipt-verification rules as a companion specification. Do not claim that v0.1 already delivers federation. |
| Typed, resolvable references | Human-readable citations alone are insufficient for reliable automated resolution. | Develop typed, versioned, and where appropriate content-addressed reference profiles. |
| Semantic authoring | Human and agent authoring is interpretive; canonicalization and hashing must be deterministic. | Document the authoring-to-canonicalization contract now and develop richer authoring provenance as companion work. |
| Protocol evolution | A new ProtocolVersion may be informed by evidence from prior operation without changing the rules applied to earlier cases. | Develop evidence-linked amendment rationale, proposal, review, and shadow-evaluation records as companion work. |
| Conformance and registry governance | A decentralized implementation ecosystem can still centralize control through one test authority or registry. | Develop pluralistic governance, discovery, and implementation-reporting arrangements. |
| Lifecycle extensions | The closed effect algebra supports comparison and deterministic status resolution. | Do not add effects without a concrete institutional act that cannot be represented without material loss. |
| Structured preconditions and workflow projection | Operational projections can help runtimes and agents but are not universal institutional semantics. | Develop optional execution and workflow companions; exclude them from core protocol conformance. |
| Temporal and deemed execution | The protocol defines governed temporal conditions; dependable scheduling and reconstruction require runtime responsibilities. | Develop an execution profile for scheduling, attested time, absence evidence, and recovery. |
| Data residency and erasure | Receipt existence, linkability, retention, and cross-border sharing raise legal and operational questions beyond field-level minimization. | Address through privacy and deployment profiles, backed by jurisdiction-specific review. |
| Class/depth terminology, subtypes, and Corpus-L3 | The distinctions remain defensible, but some have limited implementation evidence. | Clarify current terminology. Keep `commitment_subtype` semantics deferred and test Corpus-L3 through corpus methodology work. |
| Generalized undetermined values | Some domains may need an explicit way to distinguish unknown, unavailable, contested, and not-yet-determined values without silently satisfying a gate. | Research a cross-cutting value-state model only after collecting examples that cannot be represented honestly through current evidence, recourse, and transparency-gap fields. |

## Design Constraint for Execution Companions

Any future execution binding must preserve one direction of authority: a protocol governs whether an institutional act may be accepted; a connector, workflow, model, or rail does not make that act valid merely by producing an output. A binding may therefore declare `supplies_input_to`, an `output_contract`, an `accepted_via` path, `binding_status`, `failure_semantics`, and resulting `effect_obligation`. It must not use a field such as `satisfies_when` to let an adapter determine a gate result without the protocol's evidence and acceptance rules.

No binding shape should become normative before at least one runtime consumes it and conformance tests can detect drift between the declaration and actual behavior.

## What Changed in This Publication Pass

This disposition accompanies documentation changes to conformance-claim applicability, Core-L1 terminology, validation limits, semantic authoring, receipt privacy, and claims about execution and federation. The remaining proposed work is recorded in the [Companion Specifications and Research Roadmap](companion-roadmap.md).
