# ICSL v0.1 Candidate Specification

Status: candidate draft.  
Date: 2026-07-07.  
Normative keywords: MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY are used in their ordinary standards sense.

## 1. Purpose

The Institutional Commitment Specification Language (ICSL) defines a canonical way to
represent institutional protocols as interoperable, auditable, versioned, and testable
commitment systems.

ICSL exists so that public services, governed processes, institutional workflows, and
interoperable delivery systems can describe not only what tasks happen, but which
institutional acts bind, deny, certify, modify, delegate, remedy, supersede, or close a
governed context.

ICSL turns governance from passive compliance documentation into an operational layer:
governance shapes execution by defining the commitments, gates, evidence, authority,
recourse, versions, receipts, and accountability semantics that execution must respect.

## 2. Scope

ICSL specifies:

- canonical institutional protocol objects
- commitment point semantics
- six universal gates
- receipt and evaluation memory
- canonical/runtime/package separation
- conformance classes and encoding depths
- validation and diagnostic expectations

ICSL does not specify:

- a particular runtime engine
- a particular user interface
- a particular public-service domain
- a particular AI model or reasoning provider
- legal conclusions outside the encoded institutional protocol

## 3. Core Model

### 3.1 Institution

An Institution is the top-level authority and trust boundary for an ICSL protocol.

An Institution MAY be a public body, service provider, regulator, governing association,
program operator, delegated delivery entity, or other body that can create reliance-worthy
institutional effects.

An ICSL artifact MUST identify the Institution or institutional boundary whose commitments
are being encoded.

### 3.2 Protocol

A Protocol is a named governed institutional process. It describes the institutional logic
for a class of contexts, cases, applications, requests, incidents, decisions, obligations,
or remedies.

A Protocol is not itself immutable. It is the named lineage under which immutable versions
are published.

### 3.3 ProtocolVersion

A ProtocolVersion is an immutable published snapshot of a Protocol.

A ProtocolVersion MUST include:

- an identifier
- an ICSL version
- a governed context description or reference
- one or more CommitmentPoints
- version metadata sufficient to pin runtime evaluation

Once published, a ProtocolVersion MUST NOT be changed in place. Corrections, amendments,
and supersession MUST create a new ProtocolVersion or an explicit erratum mechanism.

### 3.4 GovernedContext

A GovernedContext is a runtime case, matter, service episode, process instance, or other
container evaluated under a pinned ProtocolVersion.

A GovernedContext MUST be evaluated against a specific ProtocolVersion. A runtime MUST NOT
silently evaluate a context against a later ProtocolVersion unless the protocol explicitly
defines migration or supersession semantics.

### 3.5 CommitmentPoint

A CommitmentPoint is the atomic institutional act in ICSL.

A stage, event, document, action, or decision is a CommitmentPoint if and only if it records
an institutional act that creates, denies, certifies, modifies, delegates, remedies, appeals,
supersedes, or closes a reliance-worthy institutional effect.

An institutional effect is reliance-worthy when at least one of the following is true:

- downstream institutional action depends on it
- a person or institution may rely on it as a formal status, permission, denial, certification, obligation, or constraint
- the effect has validity, expiry, supersession, or appeal consequences
- the effect changes a governed context's legal, administrative, service, eligibility, or accountability state
- the effect can be challenged, cured, remedied, reversed, or superseded

A stage is not a CommitmentPoint merely because:

- a form was submitted
- a task was assigned
- a document was drafted
- a queue state changed
- a system sent a notification
- an institution gave indicative guidance
- a human or AI system produced reasoning before commitment

Institutional labels are not determinative. A stage described as preliminary, advisory,
indicative, non-binding, or informal is still a CommitmentPoint when its practical effect
satisfies the inclusion rule.

Every CommitmentPoint MUST include `binding_effect_basis`.

### 3.6 Binding Effect Basis

`binding_effect_basis` explains why the CommitmentPoint does or does not create binding
institutional effect.

It SHOULD include:

- `effect_type`
- `relied_on_by`
- `downstream_consequence`
- `adverse_outcome_possible`
- `shadow_binding_analysis`
- `source_confidence`

A protocol MUST NOT rely only on labels such as advisory, preliminary, operational, or
non-binding to exclude a stage from CommitmentPoint treatment.

### 3.7 Binding Force

Binding force describes how a CommitmentPoint binds.

Allowed binding-force concepts are:

- `substantive_binding`
- `procedural_binding`
- `evidentiary_binding`
- `recommendatory`
- `advisory_nonbinding`
- `mixed`

`mixed` MUST enumerate its components. It MUST NOT be used as an ambiguity sink.

`advisory_nonbinding` cannot be a CommitmentPoint unless shadow-binding analysis establishes
downstream reliance or institutional effect.

### 3.8 Six Gates

Every CommitmentPoint MUST declare the six gates:

- Authority
- Evidence
- Reasoning
- Dependency
- Version
- Recourse

The six gates are universal. Profiles MAY add detail, but they MUST NOT remove a gate.

#### Authority Gate

The Authority gate defines who or what can bind the institution at the CommitmentPoint.

Authority semantics MUST distinguish:

- `legal_authority_holder`
- `authority_selection_rule`
- `delegated_authority`
- `task_owner`
- `fallback_owner`

Task ownership and fallback ownership MUST NOT satisfy the Authority gate unless they also
satisfy legal authority or delegated authority requirements.

#### Evidence Gate

The Evidence gate defines the durable facts, documents, attestations, observations, or
records required before the CommitmentPoint can be accepted.

Evidence requirements SHOULD distinguish durable facts from derived runtime state.

#### Reasoning Gate

The Reasoning gate defines the rule, standard, test, calculation, discretion model, or
reason-giving requirement used to evaluate the CommitmentPoint.

Probabilistic or AI-generated reasoning MAY assist a human or system, but it MUST NOT become
deterministic gate truth unless mapped into explicit canonical rules or accepted facts.

#### Dependency Gate

The Dependency gate defines upstream commitments, facts, versions, receipts, events, or
external institutional states that must exist before the CommitmentPoint can be accepted.

Dependencies SHOULD be explicit enough for independent implementers to determine whether
the gate is open, blocked, or unverifiable.

#### Version Gate

The Version gate pins the CommitmentPoint to the relevant ProtocolVersion and any normative
references needed for evaluation.

Runtime systems MUST evaluate against the pinned version unless migration or supersession
is explicitly encoded.

#### Recourse Gate

The Recourse gate declares the challenge, cure, appeal, remedy, oversight, or transparency
state associated with the CommitmentPoint.

`recourse_state` MUST be one of:

- `available`
- `external_only`
- `not_applicable`
- `unknown_unpublished`
- `legally_unavailable`

An adverse outcome MUST declare an explicit recourse state.

For non-`not_applicable` recourse states, implementations SHOULD capture:

- forum or body
- internal or external classification
- deadline or window
- remedy type
- suspensive effect
- source or provenance
- accessibility or language note when public-facing

`unknown_unpublished` is a transparency gap. It MUST NOT be treated as equivalent to
`not_applicable`.

## 4. Governance Addendum

Protocols that affect public rights, benefits, eligibility, obligations, enforcement,
appeals, public money, access to service, or institutional accountability SHOULD declare
governance addendum fields.

Governance addendum fields include:

- `notice_state`
- `participation_opportunity`
- `discretion_model`
- `remedy_effect`
- `oversight_actor`
- `reason_giving_sufficiency`

These fields may be required by profile, domain, or conformance depth.

## 5. Receipts and Evaluation Records

An accepted CommitmentPoint MUST produce a Receipt.

A Receipt is immutable memory of an accepted institutional commitment. Receipts SHOULD be
hash-linked when ordered memory or audit continuity matters.

A blocked or rejected attempted commitment SHOULD produce an EvaluationRecord.

An EvaluationRecord records why a submission, context, or attempted action was not accepted.
It is distinct from a Receipt because it does not represent an accepted commitment.

## 6. Canonical JSON

Canonical JSON is the normative representation for ICSL v0.1 candidate artifacts.

Object key ordering, null handling, array ordering, string encoding, numeric handling, and
hashing rules MUST be specified by the canonicalization profile used by a conformance claim.

The seed harness uses:

- sorted object keys
- preserved array order
- retained null values
- whitespace-free JSON
- SHA-256 over UTF-8 canonical JSON bytes for canonical hashes

Final publication MUST decide whether this profile adopts RFC 8785 or a named ICSL profile.

## 7. Layer Separation

Canonical ICSL protocol truth MUST NOT contain deployment-specific execution material.

Canonical artifacts MAY declare:

- institutional commitments
- gates
- evidence requirements
- authority requirements
- dependencies
- outcome tokens
- recourse structures
- semantic annotations
- abstract capability needs

Canonical artifacts MUST NOT contain:

- connector ids
- MCP server or tool references
- credential references
- endpoint URLs
- secrets or environment config
- retry policies
- timeout policies
- runtime worker ids
- UI component ids
- vendor-specific workflow-node references

Execution bindings, runtime config, credentials, endpoints, and interface projections MUST
be outside canonical protocol truth. They MUST NOT change gate outcomes.

## 8. AI Boundary

AI systems MAY assist with:

- drafting protocol encodings
- extracting candidate facts
- explaining rules
- summarizing evidence
- generating implementation aids
- recommending human review

AI systems MUST NOT be treated as deterministic gate authority unless their output is
converted into explicit accepted facts, rules, or human/institutional commitments under the
ProtocolVersion.

ICSL conformance MUST NOT depend on hidden model behavior.

## 9. Conformance Model

ICSL conformance is not a single unqualified binary claim.

A conformance declaration MUST identify:

- claim subject
- conformance class
- ICSL version
- test-suite version
- result

Candidate conformance classes:

- `Core-L1`
- `Core-L2`
- `Core-L3`
- `Extended-L2`
- `Corpus-L3`

Protocol encoding depths:

- `L1` - structural encoding sufficient for basic parsing and gate presence.
- `L2` - semantic encoding sufficient for binding, authority, recourse, canonicalization, and package claims.
- `L3` - high-fidelity encoding with references, governance addendum, reason-giving, renderings, and corpus-grade provenance.

No implementation MAY claim unqualified `ICSL compliant` status. Claims MUST name class,
ICSL version, and test-suite version.

## 10. Diagnostics

Validators SHOULD report stable diagnostic IDs.

The seed rule catalog includes:

- `PROTOCOL_COMMITMENT_POINTS_REQUIRED`
- `CP_ALL_GATES_REQUIRED`
- `CP_BINDING_EFFECT_REQUIRED`
- `ADVISORY_CP_REQUIRES_SHADOW_BINDING`
- `ADVERSE_OUTCOME_RECOURSE_STATE_REQUIRED`
- `CANONICAL_NO_DEPLOYMENT_BINDINGS`
- `TASK_OWNER_NOT_AUTHORITY`
- `CONFORMANCE_DECLARATION_REQUIRED`
- `RECEIPT_HASH_CHAIN_VALID`
- `UNKNOWN_RECOURSE_BLOCKS_L3_CORPUS`
- `BINDING_FORCE_REQUIRED`
- `NON_EXECUTING_FIELDS_DO_NOT_AFFECT_GATES`
- `REFERENCE_VERSION_REQUIRED`
- `RENDERING_NO_NEW_SEMANTICS`
- `UNSUPPORTED_EXTENDED_FEATURE_MUST_BLOCK_OR_WARN_BY_CLASS`
- `PACKAGE_MANIFEST_REQUIRED`
- `PACKAGE_HASH_VECTOR_VALID`
- `PACKAGE_MANIFEST_FILE_EXISTS`
- `PACKAGE_HASH_VECTOR_COMPLETE`

Final v0.1 publication SHOULD include a normative diagnostic registry.

## 11. Publication Status

This candidate spec is ready for schema hardening, conformance-suite expansion, and invited
implementation review.

It is not yet a final public standard.
