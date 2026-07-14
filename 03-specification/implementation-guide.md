# ICSL Implementation Guide Candidate

Status: candidate draft.  
Date: 2026-07-09.

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
5. Validate binding effect basis and outcome effect classes.
6. Validate authority semantics, including operation-of-law authority bases.
7. Validate recourse semantics, keyed off Outcome.effect_class.
8. Validate the dependency grammar.
9. Implement RFC 8785 (JCS) canonicalization and dual hashes (tagged hash format).
10. Validate receipt content core and verify receipt chains.
11. Implement derived-status resolution over acts_on chains.
12. Implement trigger evaluation (institutional_act, temporal_lapse, external_event).
13. Emit stable diagnostics and EvaluationRecords.
14. Run the conformance suite.

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

At Core-L2 and above a validator MUST additionally check:

- every Outcome carries token and effect_class, and adverse_outcome_possible is
  consistent with the declared effect classes;
- every DependencyExpression matches the dependency grammar and resolves;
- receipts carry the receipt content core, tagged sha256 hashes, and a valid
  previous_hash chain;
- acts_on targets resolve to earlier receipts, so current commitment status is
  computable by the derived-status algebra;
- canonical bytes are RFC 8785 (JCS)-conformant;
- a recourse_state of legally_unavailable carries a legal_basis, and a recourse_state
  of not_applicable on an adverse or mixed outcome carries a legal_basis
  (RECOURSE_EXCLUSION_REQUIRES_BASIS);
- adverse and mixed outcomes declare notice_state and reason_giving
  (ADVERSE_OUTCOME_NOTICE_REQUIRED, ADVERSE_OUTCOME_REASON_GIVING_DECLARED);
- canonical receipt content embeds no personal data directly
  (PERSONAL_DATA_NOT_IN_CANONICAL_RECEIPT);
- an AuthorityGate whose actor_type is automated_deterministic_system,
  ai_probabilistic_system, or hybrid_human_ai satisfies the delegation rule of spec
  section 8 (AI_AUTHORITY_DELEGATION_BASIS_REQUIRED);
- relational commitment types are structurally consistent: an APPEAL identifies the challenged commitment or outcome
  (APPEAL_TARGET_REQUIRED), an OVERRIDE identifies its target and superseding authority
  basis (OVERRIDE_TARGET_AND_BASIS_REQUIRED), an EVOLVE references the protocol or
  version changed (EVOLVE_TARGET_VERSION_REQUIRED), a DELEGATE identifies recipient and
  scope (DELEGATE_SCOPE_REQUIRED); REMEDY_TARGET_IDENTIFIED and CLOSE_TERMINAL_TRANSITION
  are advisory warnings;
- where a receipt carries commitment_type, it equals the referenced CommitmentPoint's
  type (RECEIPT_COMMITMENT_TYPE_MATCH). These are structure-consistency checks only: a
  validator MUST NOT derive or constrain binding_force, effect_class, recourse
  availability, or automation from commitment_type.

## 4. Runtime Behavior

A runtime MUST evaluate a GovernedContext against a pinned ProtocolVersion.

A runtime MUST NOT let deployment bindings alter canonical gate outcomes.

A runtime MUST distinguish:

- durable facts
- derived state
- attempted commitment
- accepted commitment
- blocked or rejected evaluation

Accepted commitments MUST produce Receipts. A blocked or rejected attempt MUST produce
an EvaluationRecord (see `04-reference/schemas/EvaluationRecord.schema.json`), never a
Receipt.

A runtime MUST additionally:

- resolve the current status of any commitment from its acts_on chain using the
  derived-status algebra;
- require an explicit current_time in the GovernedContext for any evaluation involving
  deadlines, durations, or lapse;
- evaluate temporal_lapse triggers against the declared trigger_condition and mint
  deemed receipts (deemed: true) with an attested evaluation current_time, using
  attested-absence statements for absence-of-receipt evidence;
- where the runtime declares AI assistance in a governed context, record ai_assistance
  (involved, role, human_review) on accepted commitments
  (AI_ASSISTED_COMMITMENT_PROVENANCE).

At Core-L2, receipts SHOULD copy the commitment_type of the referenced CommitmentPoint. The authoritative type lives
only in the hashed ProtocolVersion; the receipt copy makes receipt streams independently
indexable by act kind, and if present it MUST equal the referenced CommitmentPoint's
type (RECEIPT_COMMITMENT_TYPE_MATCH).

## 5. Composer Behavior

A composer helps authors create ICSL artifacts.

A composer SHOULD:

- warn when a likely CommitmentPoint is missing
- warn when a stage appears advisory but has downstream binding effect
- require binding effect basis
- require six gates
- require an effect_class on every declared outcome
- require trigger_condition when a trigger is temporal_lapse, and legal_source when
  authority_basis is operation_of_law
- emit dependencies only in the dependency grammar
- distinguish task owner from authority
- mark recourse gaps
- keep runtime bindings outside canonical protocol truth
- warn when discretionary language in the underlying source is encoded as a
  deterministic rule, and offer guided_discretion or open_discretion instead
  (DISCRETION_NOT_FETTERED)
- prompt for legal_basis when recourse is declared legally_unavailable or
  not_applicable on an adverse or mixed outcome
- prompt for encoding_provenance on the ProtocolVersion and publisher on the
  PackageManifest
- suggest a commitment_type early in authoring, since the type frames the recourse
  perspective from which the other gates are drafted
- warn when a single stage appears to perform multiple institutional acts, suggesting a
  split into separate CommitmentPoints under the atomicity rule

A composer MUST NEVER auto-derive binding_force, allowed_outcomes, or any other
structural field from commitment_type: the type is classificatory and creates no
institutional effect by itself.

Authoring heuristics keyed to commitment types (for example, "an ATTEST usually needs
declared evidence") are composer guidance only. They are NOT conformance rules, produce
no diagnostics, and MUST NOT be presented to authors as validation failures.

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
- notice expectations and reason-giving for adverse or mixed outcomes
- the legal basis claimed for any recourse exclusion
- uncertainty or transparency gaps

## 8. AI-Assisted Systems

AI systems may help draft, explain, classify, and review ICSL artifacts.

AI systems SHOULD be treated as drafting and analysis aids unless explicitly bound by an
institutional protocol.

AI-generated content MUST NOT silently become gate truth. It MUST be converted into accepted
facts, rules, human decisions, or institutional commitments before it can affect deterministic
evaluation.

The normative AI boundary, including the delegation rule for automated and AI systems
holding delegated authority, is spec section 8; this guide defers to it.

Acceptance of an externally derived fact — including an AI-extracted fact — into
deterministic gate evaluation is itself an institutional act: it is governed by the
Authority and Evidence gates of the consuming CommitmentPoint, or, where facts are
accepted in advance or in bulk, it MUST be its own evidentiary_binding CommitmentPoint
(FACT_ACCEPTANCE_GOVERNED).

## 9. Common Failure Modes

High-risk implementation failures:

- treating workflow tasks as commitments
- treating task owners as legal authorities
- omitting recourse for adverse outcomes
- allowing runtime connector fields into canonical protocol JSON
- claiming conformance without naming class and test-suite version
- allowing UI renderings to add or suppress legal semantics
- treating AI classification as deterministic institutional truth
