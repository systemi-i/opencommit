# ICSL v0.1 Candidate Specification

- Status: candidate draft.
- Date: 2026-07-16.

The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, NOT RECOMMENDED, MAY, and OPTIONAL in this document are to be interpreted as described in BCP 14 [RFC 2119] [RFC 8174] when, and only when, they appear in all capitals.

## 1. Purpose

The Institutional Commitment Specification Language (ICSL) is a specification language
for institutional protocols: governed processes composed of commitment-bearing acts. It
defines a common model and JSON representation for the commitment-bearing structure of
those processes and the institutional acts through which they produce effects.

Authoring that representation is a semantic and institutional judgment. ICSL does not
determine a unique encoding of an underlying law, policy, or practice. Once an artifact
has been authored, the canonicalization, identity, hashing, and derived-status rules in
this specification produce deterministic technical results for the same conforming JSON
value. That determinism does not establish semantic equivalence between independently
authored encodings, fidelity to source, legal adequacy, or production interoperability.

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
- a complete workflow or orchestration engine — a conformant ICSL protocol specifies
  governable institutional action and its evidence; it does not by itself provide task
  management, scheduling, or execution orchestration

ICSL v0.1 also does not specify protocol composition, federation governance, discovery,
cross-institution trust negotiation, authorization to disclose Receipts, or end-to-end
execution. Its objects may be used by systems that provide those capabilities, but
conformance to this specification does not demonstrate them.

## 3. Core Model

### 3.0 Terminology: CommitmentPoint, Commitment, Receipt


This specification distinguishes template from instance:

- A **CommitmentPoint** is the versioned template inside a ProtocolVersion. It declares
  the gates, trigger, allowed outcomes, and binding-effect basis for a class of
  institutional acts.
- A **Commitment** is an accepted instance of a CommitmentPoint in a GovernedContext.
- A **Receipt** records a Commitment.

A CommitmentPoint does not itself bind; only a Commitment binds. This document uses
CommitmentPoint for the template and Commitment for the accepted instance, and MUST NOT
be read as using the two interchangeably.

### 3.1 Institution

An Institution is the top-level authority and trust boundary for an ICSL protocol.

An Institution MAY be a public body, service provider, regulator, governing association,
program operator, delegated delivery entity, or other body that can create reliance-worthy
institutional effects.

An ICSL artifact MUST identify the Institution or institutional boundary whose commitments
are being encoded. This identification is schema-carried: a ProtocolVersion MUST include
an `institution` object as defined in 3.3.

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
- an `institution` object: `{ id, name, jurisdiction?, reference? }`
- a `governed_context` **GovernedContextDescriptor** (see below)
- one or more CommitmentPoints
- version metadata sufficient to pin runtime evaluation

The embedded `governed_context` member is a GovernedContextDescriptor: a description of
the CLASS of matters the protocol governs, not a runtime case:

```
governed_context = GovernedContextDescriptor = {
  description,        // REQUIRED
  subject_class?,
  scope?,
  jurisdiction_note?
}
```

The descriptor is closed (`additionalProperties: false` in the schema) and MUST NOT
carry any runtime member: `protocol_version_id`, `protocol_version_hash`,
`governed_context_id`, and `current_time` are all absent from a descriptor. Runtime
GovernedContexts are separate artifacts (see 3.4). One consequence is reaffirmed
plainly: no object embedded inside a ProtocolVersion carries the version's own hash, so
no zero-hash or placeholder-hash convention exists anywhere in a ProtocolVersion.

A ProtocolVersion MAY include `encoding_provenance`:

```
encoding_provenance = {
  drafting_method: human | ai_assisted | automated_conversion,
  drafting_tool?,
  approved_by,
  approval_basis?,
  sources_consulted?: [reference ids]
}
```

Within the object, `approved_by` (a string naming the approving authority) is REQUIRED;
the remaining members are OPTIONAL. `encoding_provenance` SHOULD be present at `Core-L2`
and MUST be present at `Core-L3` and `Corpus-L3`. This clause grounds two catalog rules:
`ENCODING_PROVENANCE_RECOMMENDED` (warning, `Core-L2`) and `ENCODING_PROVENANCE_REQUIRED`
(error, `Core-L3` and above). See Section 8.5 for the AI-assisted drafting rules.

ProtocolVersion identity is `protocol_version_hash`: a tagged string
`"sha256:<64 lowercase hex>"` computed over the RFC 8785 (JCS) canonical bytes of the
complete protocol-version JSON object (see Section 6). The protocol-version object
contains no hash of itself, so the hash preimage is non-self-referential:
`protocol_version_hash` is computed over the object exactly as published, with no member
removed and no member added.

Artifacts that consume a ProtocolVersion pin it by hash, not only by name: a
GovernedContext carries `protocol_version_hash` (see 3.4), and every Receipt carries
`protocol_version_hash`, which MUST equal the canonical hash of the ProtocolVersion its
`protocol_version_id` names (see 5.2; catalog rule
`RECEIPT_PROTOCOL_VERSION_HASH_MATCH`, error, `Core-L2`).

Once published, a ProtocolVersion MUST NOT be changed in place. Corrections, amendments,
and supersession MUST create a new ProtocolVersion.

### 3.4 GovernedContext

A GovernedContext is a runtime case, matter, service episode, process instance, or other
container evaluated under a pinned ProtocolVersion.

A runtime GovernedContext is a SEPARATE artifact from the GovernedContextDescriptor
embedded in a ProtocolVersion (see 3.3): the descriptor says what class of matters the
protocol governs; the runtime GovernedContext is an individual matter, and it — not the
descriptor — carries the runtime members `governed_context_id`, `protocol_version_id`,
`protocol_version_hash`, and (where required) `current_time`.

A GovernedContext MUST be evaluated against a specific ProtocolVersion. In v0.1 a
GovernedContext MUST NOT be evaluated against any ProtocolVersion other than its pinned
one; migration and supersession semantics are reserved for a later version.

A GovernedContext MUST carry `protocol_version_hash` — the canonical hash of its pinned
ProtocolVersion (see 3.3) — in addition to the version identifier. The field is REQUIRED
in the GovernedContext schema, so that pinning is verifiable by hash rather than by name
alone. A runtime
GovernedContext's `protocol_version_hash` MUST equal the canonical hash of the
ProtocolVersion its `protocol_version_id` names. This clause grounds catalog rule
`GOVERNED_CONTEXT_PROTOCOL_VERSION_HASH_MATCH` (error, `Core-L2`). Because the
ProtocolVersion embeds only a
descriptor, this hash lives exclusively in artifacts OUTSIDE the ProtocolVersion
(runtime GovernedContexts and Receipts); non-self-referential identity (see 3.3 and 6.2)
is preserved with no placeholder-hash convention.

Any evaluation involving deadlines, durations, or lapse REQUIRES an explicit
`current_time` in the GovernedContext. This clause grounds catalog rule
`CURRENT_TIME_REQUIRED` (see Section 10).

### 3.5 CommitmentPoint

A CommitmentPoint is the template for the atomic institutional act in ICSL. Its accepted
instance in a GovernedContext is a Commitment (see 3.0).

A stage, event, document, action, or decision is encoded as a CommitmentPoint if and only
if it records an institutional act that creates, denies, certifies, modifies, delegates,
remedies, appeals, supersedes, or closes a reliance-worthy institutional effect.

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

The verbs of the inclusion rule above (creates, denies, certifies, modifies, delegates,
remedies, appeals, supersedes, closes) describe the reliance-worthy effects that qualify a
stage for CommitmentPoint treatment; `commitment_type` (see 3.5a) classifies the act
character of the CommitmentPoint itself. The two vocabularies are related but distinct,
and neither substitutes for the other.

### 3.5a Commitment Types


Every CommitmentPoint MUST declare `commitment_type`. This clause grounds catalog rules
`CP_COMMITMENT_TYPE_REQUIRED` and `CP_COMMITMENT_TYPE_INVALID` (both error, `Core-L1`;
see Section 10). The core values are:

- `DECIDE` — establishes an authoritative disposition among allowed outcomes, whether
  discretionary, rule-determined, algorithmically determined, or arising by operation of
  law.
- `ATTEST` — formally asserts, verifies, certifies, or accepts a proposition or
  evidentiary state, without determining rights or obligations. Covers both verificatory
  attestation (confirming pre-existing facts) and constitutive attestation (registration
  that creates an institutional fact).
- `APPEAL` — disposes of a challenge to an identified prior Commitment or outcome on
  the merits, through an authorized recourse process. Boundary test: APPEAL means disposition of the challenge
  on the merits. Procedural determinations within the recourse process (admissibility,
  timeliness, standing), even when they terminate the challenge, are DECIDE.
- `REMEDY` — commits correction, restoration, cure, compensation, or other redress for an
  identified defect or wrong in a prior commitment, its procurement, or its execution.
  A REMEDY CommitmentPoint is the commitment to redress (the order); execution or
  delivery of the redress is discharge, evidenced against the existing receipt rather
  than encoded as a new CommitmentPoint, unless execution independently creates a
  reliance-worthy effect, in which case the atomicity rule below forces a separate
  CommitmentPoint.
- `OVERRIDE` — displaces or alters an operative, valid Commitment under exceptional or
  superseding authority or interest, without asserting the prior commitment was
  defective. REMEDY/OVERRIDE boundary test (justification-based): if the act's
  justification is a defect (unlawfulness, fraud, error) in the prior commitment, its
  procurement, or its execution, the act is REMEDY; if it displaces a valid commitment
  for a supervening interest or by competing authority, it is OVERRIDE.
- `EVOLVE` — changes the governing protocol or institutional rules prospectively
  (meta-governance; typically publisher-side, cohering with Section 11). An EVOLVE
  CommitmentPoint must reference the protocol or version being changed.
- `CLOSE` — formally transitions a governed context to a terminal state.
- `DELEGATE` — transfers bounded institutional authority to an identified recipient with
  a defined scope, creating the delegated authority that later Authority gates rely on.

DECIDE/ATTEST boundary test:
an act whose outcomes characterize the truth, adequacy, or state of a proposition or
evidentiary matter is ATTEST, even when the finding is authoritative and enumerates
multiple outcomes; an act whose outcomes determine a right, obligation, permission,
procedural course, or status of a subject is DECIDE. Where outcomes do both, the act is
DECIDE if any outcome directly alters a subject's rights, obligations, permissions, or
status without a further Commitment intervening; otherwise it is ATTEST and its
reliance travels through the Dependency gate of a later DECIDE. Worked contrast: a
technical review whose outcomes are `compliant` / `minor-issues` / `major-issues` is
ATTEST — the outcomes characterize a proposition, and their effect reaches the
applicant only through the decision CommitmentPoint that depends on the review; a
completeness determination is DECIDE — its outcome directly changes the application's
procedural status.

`commitment_type` is classificatory. It creates no institutional effect by itself; it
does not determine binding force, outcome effect, recourse availability, legal validity,
or authority; and it never substitutes for the structural fields it is checked against.

A CommitmentPoint carries exactly one atomic institutional act and therefore exactly one
`commitment_type`. A stage performing multiple institutional acts SHOULD be split into
separate CommitmentPoints. Where a legally indivisible instrument performs multiple
institutional acts, the encoder chooses one primary type from the recourse perspective —
the act the instrument would be challenged as — and carries the other effects explicitly
(additional outcomes, `acts_on` entries, or dependent CommitmentPoints). An atomic-bundle
model for indivisible multi-act instruments is a named v0.2 open item.

#### Ordered classification procedure


Encoders MUST classify by the following precedence tree; the tree, not intuition,
resolves overlaps between the definitions above. The procedure is applied per atomic
act, AFTER the atomicity rule above has been applied: split a multi-act stage into
separate CommitmentPoints first, then classify each resulting act. Evaluate the tests in
order; the first test that matches determines `commitment_type`:

1. The act changes the governing protocol or rules prospectively → `EVOLVE`.
2. The act transfers bounded authority to another actor → `DELEGATE`.
3. The act disposes of a challenge to an identified prior Commitment on the merits →
   `APPEAL`.
4. The act is justified as cure of a defect or wrong in a prior commitment, its
   procurement, or its execution → `REMEDY`.
5. The act displaces a valid operative commitment under superseding authority or
   interest → `OVERRIDE`.
6. The act terminates a governed context → `CLOSE`.
7. The act establishes an authoritative disposition among allowed outcomes → `DECIDE`.
   Steps 7 and 8 are resolved by the DECIDE/ATTEST boundary test above: outcomes that determine a right,
   obligation, permission, procedural course, or status of a subject match here.
8. The act asserts, verifies, certifies, or accepts a proposition or evidentiary state →
   `ATTEST`. Apply the DECIDE/ATTEST boundary test above: outcomes that only
   characterize the truth, adequacy, or state of a proposition or evidentiary matter
   match here, even when the finding is authoritative and enumerates multiple outcomes.
9. Otherwise → `EXTENSION` (permitted at `Extended-L2` only; see the extension boundary
   below).

Step 3 applies the APPEAL boundary test above: only the merits disposition of a
challenge matches step 3. Procedural determinations within the recourse process
(admissibility, timeliness, standing), even when they terminate the challenge, fall
through and classify as DECIDE at step 7.

#### Typed act relationships

Relational types are consistency-checked against reference structure rather than trusted
as labels. Three template-level structures carry the relationships:

- `acts_on_allowed` — `{ allowed_effects, targets, basis_reference? }`.
  `allowed_effects` (REQUIRED, at least one entry) lists the permitted `acts_on` effects
  (see 3.11). `targets` (REQUIRED, at least one entry) lists the ids of the
  CommitmentPoints whose receipts Commitments at this CommitmentPoint may act on.
  `basis_reference` (OPTIONAL, a Reference id) identifies the authority basis for
  acting.
- `evolves` — `{ protocol_id?, protocol_version_id?, reference? }`; at least one member
  is REQUIRED within the object. It names the protocol or version an EVOLVE act changes
  prospectively.
- `delegation` — `{ recipient (REQUIRED), scope (REQUIRED), basis_reference? }`. It
  names the recipient and the bounded scope a DELEGATE act transfers.

Type-conditioned requirements, enforced by schema conditionals where expressible and by
catalog rules in all cases:

- `APPEAL`, `OVERRIDE`, and `REMEDY` REQUIRE `acts_on_allowed` (with its REQUIRED
  `targets`).
- `OVERRIDE` additionally REQUIRES `acts_on_allowed.basis_reference`.
- `EVOLVE` REQUIRES `evolves`.
- `DELEGATE` REQUIRES `delegation`.

These requirements ground catalog rules `APPEAL_TARGET_REQUIRED`,
`OVERRIDE_TARGET_AND_BASIS_REQUIRED`, `EVOLVE_TARGET_VERSION_REQUIRED`, and
`DELEGATE_SCOPE_REQUIRED` (all error, `Core-L2`), plus `REMEDY_TARGET_IDENTIFIED`
(warning, `Core-L2`; the structural presence of `acts_on_allowed.targets` is already
enforced at error level by the schema conditionals above, so target sufficiency stays
advisory) and `CLOSE_TERMINAL_TRANSITION` (warning, `Core-L2`) (see Section 10). No rule derives or constrains binding force,
effect class, recourse availability, or automation from the type.

Runtime target membership: a Receipt's `acts_on.target_receipt_id` MUST reference a
receipt whose `commitment_point_id` is listed in the acting CommitmentPoint's
`acts_on_allowed.targets` (catalog rule `ACTS_ON_TARGET_MEMBERSHIP`, error, `Core-L2`;
see 3.11). Without this membership check, a relational Commitment (for example an
appeal) could act on an unrelated receipt anywhere in the chain; the check closes that
path.

A CommitmentPoint MAY carry `commitment_subtype`, an OPTIONAL namespaced string (pattern
`^urn:`) refining a core type. Subtypes are comparability hooks for domain profiles and
carry no normative semantics in v0.1 beyond format validation.

#### Extension boundary

At `Extended-L2` only, `commitment_type` MAY be the marker `EXTENSION`, declaring
`commitment_type_extension` with `id` (namespaced), `definition`, `fallback_semantics`,
and `rationale`. The boundary is sealed in both directions:

- `commitment_type: EXTENSION` REQUIRES `commitment_type_extension` (catalog rule
  `CP_EXTENSION_TYPE_DECLARATION_REQUIRED`, error, `Extended-L2`) and PROHIBITS
  `commitment_subtype` — subtypes refine core types only.
- A core `commitment_type` value PROHIBITS `commitment_type_extension`.
- Class coupling: a ProtocolVersion whose declared conformance class is `Core-L1`,
  `Core-L2`, `Core-L3`, or `Corpus-L3` MUST NOT contain any CommitmentPoint with
  `commitment_type: EXTENSION` (schema conditional; catalog rule
  `CP_EXTENSION_REQUIRES_EXTENDED_CLASS`, error). EXTENSION-typed CommitmentPoints are
  permitted only in artifacts declaring `Extended-L2`.
- Reverse class coupling: IF a
  ProtocolVersion's `commitment_points` contains any CommitmentPoint with
  `commitment_type: EXTENSION`, THEN `conformance_class` is REQUIRED on that
  ProtocolVersion and MUST be `Extended-L2` (schema conditional: `if` with `contains`,
  `then` with `required` and `const`). Omitting `conformance_class` therefore cannot
  smuggle an EXTENSION-typed CommitmentPoint past the class coupling above.

`fallback_semantics` is REQUIRED and is either a core type or the explicit value
`"none"`.

The fallback obligation has fixed behavior by consumer class. A consumer processing an artifact that
encounters an EXTENSION-typed CommitmentPoint MUST behave exactly as this table
prescribes; silent acceptance is prohibited in all cases:

| Consumer capability | Extension recognized? | `fallback_semantics` | Required behavior |
| --- | --- | --- | --- |
| Supports Core classes only | n/a (Core consumers do not recognize extensions natively) | names a core type | process the CommitmentPoint as that core type AND emit a warning diagnostic |
| Supports Core classes only | n/a | `"none"` | block (error) |
| Supports `Extended-L2` | yes (recognizes the extension `id`) | any | process natively under the declared extension semantics |
| Supports `Extended-L2` | no | names a core type | process the CommitmentPoint as that core type AND emit a warning diagnostic |
| Supports `Extended-L2` | no | `"none"` | block (error) |

This table is mirrored in the conformance profile (03-specification/conformance-profile.md);
catalog rule `EXTENSION_FALLBACK_BEHAVIOR_REQUIRED` states these fixed behaviors.

Receipts copy EXTENSION as EXTENSION: where the referenced CommitmentPoint's type is
`EXTENSION`, a Receipt carrying the derived `commitment_type` copy carries the value
`EXTENSION` and MAY carry `commitment_type_extension_id` (a string) naming the extension
id (see 5.2). `RECEIPT_COMMITMENT_TYPE_MATCH` matches EXTENSION to EXTENSION.

The authoring placeholder `GENERIC` is forbidden in canonical artifacts (catalog rule
`CP_GENERIC_TYPE_FORBIDDEN`, error, `Core-L1`).

Migration note: `commitment_type` is restored from IGSL v1/v1.1 §5.4.1; its absence from
earlier v0.1 drafts was an unrecorded regression, not a design decision (see ADR-008 in
07-decisions/).

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

Of these, `effect_type` and `adverse_outcome_possible` are REQUIRED; the remaining fields
are OPTIONAL.
`adverse_outcome_possible` is derived and consistency-checked against `allowed_outcomes`
(see 3.9).

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

`advisory_nonbinding` MUST NOT be a CommitmentPoint unless shadow-binding analysis establishes
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

The Authority gate carries an OPTIONAL `authority_basis`, one of:

- `institutional_actor` (default)
- `operation_of_law`

When `authority_basis` is `operation_of_law`, `legal_source` (a Reference id) is REQUIRED.
An Authority gate validates only when it declares at least one of `legal_authority_holder`,
`delegated_authority`, or `authority_basis: operation_of_law` with `legal_source`;
`task_owner` alone does not validate.

The Authority gate carries an OPTIONAL `actor_type`, one of:

- `human_officeholder`
- `institutional_role`
- `delegated_entity`
- `automated_deterministic_system`
- `ai_probabilistic_system`
- `hybrid_human_ai`

Whether an automated or AI system may hold `delegated_authority` is governed exclusively
by the delegation rule in Section 8.2. Catalog rule `AI_AUTHORITY_DELEGATION_BASIS_REQUIRED`
(error, `Core-L2`) enforces that rule against declared `actor_type`.

#### Evidence Gate

The Evidence gate defines the durable facts, documents, attestations, observations, or
records required before the CommitmentPoint can be accepted.

Evidence requirements SHOULD distinguish durable facts from derived runtime state.

The Evidence gate MUST declare `required` (a non-empty list of durable facts or documents)
and MAY declare `attested_absence` entries referencing CommitmentPoints. An attested-absence statement is the explicit
exception to the prohibition on derived runtime state serving as evidence (see 3.10).

#### Reasoning Gate

The Reasoning gate defines the rule, standard, test, calculation, discretion model, or
reason-giving requirement used to evaluate the CommitmentPoint.

Probabilistic or AI-generated reasoning MAY assist a human or system, but it MUST NOT become
deterministic gate truth unless mapped into explicit canonical rules or accepted facts
(see Section 8, which is the sole normative AI-boundary statement).

The Reasoning gate carries a `mode` field, one of:

- `deterministic_rule`
- `calculation`
- `guided_discretion`
- `open_discretion`
- `ai_assisted`
- `external_judgment`
- `mixed`

Anti-fettering rule: where the underlying law confers discretion, the Reasoning gate MUST
represent it as `guided_discretion` or `open_discretion`, identifying the discretion
holder and the relevant factors, and MUST NOT convert the discretion into a deterministic
rule. Because fettering is detectable from artifacts only heuristically, the corresponding
catalog rule `DISCRETION_NOT_FETTERED` carries severity warning at `Core-L2`.

#### Dependency Gate

The Dependency gate defines upstream commitments, facts, versions, receipts, events, or
external institutional states that must exist before the CommitmentPoint can be accepted.

Dependencies SHOULD be explicit enough for independent implementers to determine whether
the gate is open, blocked, or unverifiable.

The Dependency gate content is `{ requires: [DependencyExpression] }`. A DependencyExpression is exactly one of:

- `{ commitment_point: id, outcome?: token }` — a Commitment exists at the referenced CommitmentPoint, optionally with the named outcome token
- `{ absent: { commitment_point: id } }` — attested absence of a Commitment at the referenced CommitmentPoint
- `{ external: reference_id }` — an external institutional state identified by a Reference
- `{ temporal: { anchor: { commitment_point_id, event: "receipt_created" }, operator: "elapsed", duration: <ISO-8601 duration> } }` — the stated duration has elapsed since the anchoring receipt was created
- `{ any_of: [DependencyExpression] }`
- `{ all_of: [DependencyExpression] }`

No other DependencyExpression forms are defined in v0.1.

#### Version Gate

The Version gate pins the CommitmentPoint to the relevant ProtocolVersion and any normative
references needed for evaluation.

Runtime systems MUST evaluate against the pinned version. In v0.1 there is no migration
exception (see 3.4).

The Version gate content is `{ protocol_version_id (REQUIRED), references? }`.

#### Recourse Gate

The Recourse gate declares the challenge, cure, appeal, remedy, oversight, or transparency
state associated with the CommitmentPoint.

`recourse_state` MUST be one of:

- `available`
- `external_only`
- `not_applicable`
- `unknown_unpublished`
- `legally_unavailable`

An adverse outcome (`effect_class` of `adverse` or `mixed`; see 3.9) MUST declare an
explicit recourse state.

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

The Recourse gate carries an OPTIONAL `legal_basis` — a string holding a citation or a
Reference id. Two
exclusion-basis rules apply:

- `recourse_state: legally_unavailable` ALWAYS requires `legal_basis` (catalog rule
  `RECOURSE_EXCLUSION_REQUIRES_BASIS`, error, `Core-L2`).
- `recourse_state: not_applicable` on an outcome whose `effect_class` is `adverse` or
  `mixed` requires `legal_basis` (same rule, error, `Core-L2`).

A recourse-exclusion assertion is an encoder claim about the law. It is rebuttable, and
it does not extinguish recourse that exists in law.

### 3.9 Outcomes


Every CommitmentPoint MUST declare `allowed_outcomes` with at least one Outcome object
(catalog rule `CP_ALLOWED_OUTCOMES_REQUIRED`, error, `Core-L1`): the adverse-outcome
recourse, notice, and reason-giving protections in this section all key off Outcome
`effect_class`, so a CommitmentPoint without declared outcomes would evade them.

`allowed_outcomes` on a CommitmentPoint is an array of Outcome objects:

- `token` (REQUIRED) — the outcome identifier string recorded in a Receipt
- `effect_class` (REQUIRED) — one of `favorable`, `adverse`, `mixed`, `procedural`
- `recourse` (OPTIONAL) — a per-outcome RecourseGate override
- `notice_state` (OPTIONAL)
- `reason_giving` (OPTIONAL) — `{ expectation: reasons_required | none_required_by_law, legal_basis? }`
- `dependencies` (OPTIONAL) — an array of DependencyExpression (see 3.8, Dependency gate)

Adverse-outcome rules — recourse, notice, and related protections — key off `effect_class`
(`adverse` or `mixed`), NOT a self-declared boolean. There is no unclassified default that
escapes adverse-outcome treatment.

At `Core-L2`, every outcome whose `effect_class` is `adverse` or `mixed` has the following requirements:

- `notice_state` MUST be declared (catalog rule `ADVERSE_OUTCOME_NOTICE_REQUIRED`, error).
- `reason_giving` MUST be declared (catalog rule
  `ADVERSE_OUTCOME_REASON_GIVING_DECLARED`, error). Declaring
  `expectation: none_required_by_law` requires `legal_basis`.

`binding_effect_basis.adverse_outcome_possible` remains but is derived and
consistency-checked: it MUST be true if and only if at least one outcome in
`allowed_outcomes` has `effect_class` `adverse` or `mixed`.

### 3.10 Triggers


Every CommitmentPoint has a `trigger`, one of:

- `institutional_act` (default) — an institutional actor performs the act
- `temporal_lapse` — the effect arises by operation of time
- `external_event` — the effect arises from an event outside the GovernedContext

For `temporal_lapse`, the CommitmentPoint MUST declare `trigger_condition`:

```
trigger_condition = {
  anchor: { commitment_point_id, event: "receipt_created" },
  duration: <ISO-8601 duration string>,
  requires_absence: [commitment_point_id,...]
}
```

The lapse fires when `duration` has elapsed since the anchoring receipt was created and no
Commitment exists at any CommitmentPoint listed in `requires_absence`.

Authority for operation-of-law effects uses `authority_basis: operation_of_law` with a
REQUIRED `legal_source` (see 3.8, Authority gate).

The runtime evaluating the GovernedContext mints the receipt for a deemed effect, with
`deemed: true` and an attested evaluation `current_time` (see 5.4). Absence-of-receipt
evidence is expressed as an attested-absence statement in the Evidence gate; this is an
explicit exception to the prohibition on derived runtime state serving as evidence.

Failure to decide is itself institutionally significant: where law so provides, a lapsed
decision deadline is a challengeable adverse event, and SHOULD be encoded as a
`temporal_lapse` CommitmentPoint whose outcomes carry `effect_class` `adverse` or `mixed`
with full recourse machinery.

### 3.11 Commitment Lifecycle and Status


A Commitment carries a derived status, one of:

`accepted` | `suspended` | `revoked` | `quashed` | `superseded` | `expired` | `varied`

Status changes are recorded as ordinary Receipts whose `acts_on` field targets an earlier
receipt:

```
Receipt.acts_on = {
  target_receipt_id: string,
  effect: suspend | revive | revoke_ex_tunc | revoke_ex_nunc | quash | supersede | vary | expire
}
```

A CommitmentPoint MAY declare, at template level (see 3.5a):

```
acts_on_allowed = {
  allowed_effects: [suspend | revive | revoke_ex_tunc | revoke_ex_nunc | quash | supersede | vary | expire],
                                          // REQUIRED, at least one
  targets: [commitment_point id,...],    // REQUIRED, at least one
  basis_reference?: Reference id
}
```

marking it as one whose Commitments act on prior commitments and enumerating the
CommitmentPoints whose receipts they may act on. A Receipt's `acts_on.target_receipt_id`
MUST reference a receipt whose `commitment_point_id` is in the acting CommitmentPoint's
`acts_on_allowed.targets` (catalog rule `ACTS_ON_TARGET_MEMBERSHIP`, error, `Core-L2`;
see 3.5a).

Derived-status algebra (normative, deterministic): a Commitment's current status is
computed by applying its own receipt (`accepted`), then all valid `acts_on` receipts
targeting it, in chain order. `suspend` and `revive` toggle between `suspended` and the
prior effective status. `revoke_ex_tunc`, `revoke_ex_nunc`, `quash`, and `supersede` are
terminal. `expire` is terminal. `vary` leaves the Commitment accepted-with-variation
(`varied`).

Consumers of a receipt MUST be able to resolve the current status of the recorded
Commitment from the chain.

`revoke_ex_tunc` voids the Commitment from the start (ex tunc); `revoke_ex_nunc` revokes
it from now on (ex nunc), leaving effects arising before the acting receipt intact. The
receipt chain remains append-only: status never changes by editing or deleting a receipt.

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

A Commitment MUST produce a Receipt. A Receipt is immutable memory of a Commitment.
Receipts are hash-linked into a chain (see 5.3).

### 5.1 Acceptance


Acceptance is the institutional act by which a runtime records that the conditions
declared by the pinned ProtocolVersion evaluate as satisfied for a GovernedContext. It is
an assertion under the encoding, not a validator's determination that the actor possessed
lawful authority or that all six gates were legally adequate. Runtimes MUST distinguish
attempted from accepted commitments. An accepted adverse outcome (e.g. a denial) is a
Commitment producing a Receipt with full recourse machinery. A blocked or rejected attempt
produces an EvaluationRecord, never a Receipt.

### 5.2 Receipt Content Core


A Receipt MUST include:

- `kind` — the string `"Receipt"`
- `receipt_id`
- `protocol_version_id`
- `protocol_version_hash` — the canonical hash (see 3.3) of the ProtocolVersion named by
  `protocol_version_id`; it MUST equal that ProtocolVersion's canonical hash (catalog
  rule `RECEIPT_PROTOCOL_VERSION_HASH_MATCH`, error, `Core-L2`)
- `commitment_point_id`
- `governed_context_id`
- `outcome` — an outcome token string (see 3.9)
- `authority` — a string naming the acting authority, or `"operation_of_law:<legal_source>"`
- `created_at` — an RFC 3339 date-time
- `receipt_hash`
- `previous_hash` — a string, or null only for the genesis receipt

A Receipt MAY include:

- `effective_at`
- `acts_on` (see 3.11)
- `deemed` (boolean)
- `content` (object) and `content_hash` — a receipt carrying `content` MUST carry `content_hash`
- `ai_assistance` — `{ involved: boolean, role: fact_extraction | recommendation | drafting | routing | none, human_review: attested | none }` (see 8.4)
- `issuer` (reserved; see 5.5)
- `signatures` (reserved; an array of `{ signer, key_id, alg, value }`; see 5.5)
- `commitment_type` — a derived copy of the referenced CommitmentPoint's
  `commitment_type`: a core value, or the marker `EXTENSION` where the CommitmentPoint
  is EXTENSION-typed (see 3.5a)
- `commitment_type_extension_id` — a string that MAY accompany
  `commitment_type: EXTENSION` to name the extension id

Receipts SHOULD carry the derived `commitment_type` copy at `Core-L2`; if present it MUST
equal the referenced CommitmentPoint's `commitment_type` (catalog rule
`RECEIPT_COMMITMENT_TYPE_MATCH`, error, `Core-L2`). For an EXTENSION-typed
CommitmentPoint the copy is the value `EXTENSION`, matched as EXTENSION to EXTENSION
(see 3.5a).

### 5.3 Hashing and Chain Order


`receipt_hash` is the SHA-256 digest over the RFC 8785 (JCS) canonical bytes (Section 6)
of the receipt object with the `receipt_hash` member removed.

`previous_hash` is the `receipt_hash` of the prior receipt in the chain. Chain order is
`previous_hash` linkage; the genesis receipt carries `previous_hash: null`.

Every hash-bearing field is a tagged string `"sha256:<64 lowercase hex>"` (see Section 6).

### 5.4 Deemed Receipts


For operation-of-law effects (see 3.10), the runtime evaluating the GovernedContext mints
the receipt with `deemed: true` and an attested evaluation `current_time`.
Absence-of-receipt evidence supporting a deemed effect is expressed as an attested-absence
statement, an explicit exception to derived-state prohibitions.

### 5.5 Trust Model and Limitations


v0.1 receipts are unsigned. The hash chain provides tamper-evidence only relative to an
externally retained copy of the chain head. Authenticity, non-repudiation, timestamping,
and fork detection are out of scope for v0.1. No v0.1 claim may describe receipts as
signed, authenticated, or non-repudiable; consumers that need authenticity MUST retain the
chain head through an external mechanism.

The `issuer` and `signatures` fields are reserved for forward compatibility. The v0.2
direction is profiling receipts as W3C Verifiable Credentials.

### 5.6 Status of Receipts


A Receipt is a record that a Commitment was accepted under a declared ProtocolVersion. It
is evidence of process, and it is rebuttable. A Receipt does not establish the substantive
legality of the underlying institutional act, is not legal advice, and does not transfer
or discharge institutional legal responsibility to validators, composers, or runtimes.

### 5.7 Evaluation Records

A blocked or rejected attempted commitment produces an EvaluationRecord.

An EvaluationRecord records why a submission, context, or attempted action was not accepted.
It is distinct from a Receipt because it does not represent a Commitment. An
EvaluationRecord MUST NOT enter the receipt chain.

## 6. Canonical JSON and Temporal Profile


Canonical JSON is the normative byte-level representation for ICSL v0.1 candidate
artifacts. Canonicalization starts from an already-authored JSON value; it does not select
institutional semantics or make independently authored encodings equivalent.

### 6.1 Canonicalization Profile

ICSL adopts RFC 8785 (JSON Canonicalization Scheme, JCS) by reference as its
canonicalization profile. All canonicalized documents MUST satisfy I-JSON (RFC 7493)
constraints.

Legal quantities, monetary amounts, case identifiers, dates, deadlines, and rates MUST be
encoded as JSON strings, never as JSON numbers.

ASCII member names: member
names (object keys) in canonical ICSL artifacts MUST be ASCII. Values MAY be any
Unicode. Rationale: RFC 8785 sorts object members by UTF-16 code units, while a
common shortcut (Python's sorted `json.dumps`) sorts by Unicode code points; the two
orders diverge for member names containing non-BMP characters. Member-name ordering is
the only divergence risk — given the no-JSON-numbers rule above, value serialization is
identical between the two — so constraining member names to ASCII removes it entirely.

Verifiers MUST use an RFC 8785 implementation (e.g. the `rfc8785` library) when one is
available. A verifier without one MUST assert BOTH preconditions — no non-string JSON
numbers anywhere in the artifact AND all member names ASCII — and MUST fail closed if
either is violated; under those preconditions, sorted compact `json.dumps` output is
byte-identical to RFC 8785. This fallback is valid only under both asserted
preconditions and MUST NOT be presented or used as a general JCS implementation.

### 6.2 Hash Format and Identity

Every hash-bearing field is a tagged string `"sha256:<64 lowercase hex>"` (schema pattern
`^sha256:[0-9a-f]{64}$`).

ProtocolVersion identity is `protocol_version_hash`, the sha256-tagged hash over the JCS
canonical bytes of the complete protocol-version JSON object. The object contains no
hash of itself, so the preimage is non-self-referential (see 3.3).

### 6.3 Package Hashes

Package hash vectors carry source-byte hashes for every file in the package, plus
canonical-JSON hashes for JSON artifacts (dual hashes).

### 6.4 Temporal Format Profile

Instants MUST be RFC 3339 UTC date-time strings (schema format `date-time`). Durations
MUST be ISO-8601 duration strings (pattern `^P`). Where a deadline object is needed, it is
`{ duration, anchor_event, suspension_rules? }`.

(Editorial note: this profile is fixed by ADR-002 in 07-decisions/, accepted-provisional.
The prior seed-harness serialization rule is deprecated; seed-era hashes are not comparable
to hashes computed under this profile.)

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


This section is the sole normative statement of the ICSL AI boundary. Any other document
in this corpus that describes the AI boundary is informative and defers to this section.

### 8.1 Assistance and Gate Truth

AI systems MAY assist with:

- drafting protocol encodings
- extracting candidate facts
- explaining rules
- summarizing evidence
- generating implementation aids
- recommending human review

AI systems MUST NOT be treated as deterministic gate authority unless their output is
converted into explicit accepted facts, rules, or human/institutional commitments under the
ProtocolVersion. Fact conversion is governed by 8.3.

ICSL conformance MUST NOT depend on hidden model behavior.

The Authority gate's OPTIONAL `actor_type` field (see 3.8) is how an encoding declares
what kind of actor binds: `human_officeholder`, `institutional_role`, `delegated_entity`,
`automated_deterministic_system`, `ai_probabilistic_system`, or `hybrid_human_ai`.

### 8.2 Delegation Rule

An automated or AI system MAY hold `delegated_authority` at an Authority gate ONLY where
all of the following hold:

- (a) a versioned Reference documents the legal basis for the delegation;
- (b) `actor_type` is declared on the Authority gate; and
- (c) recourse to a human forum is available for adverse outcomes.

Where any of these conditions fails, an AI or probabilistic system MUST NOT satisfy the
Authority gate.

This rule grounds catalog rule `AI_AUTHORITY_DELEGATION_BASIS_REQUIRED` (error,
`Core-L2`), which refines the semantics of the earlier `AI_NOT_GATE_AUTHORITY`; both IDs
remain in the catalog, the older one restated by reference to `actor_type`.

### 8.3 Fact Acceptance

Acceptance of an externally derived fact — including an AI-extracted fact — into
deterministic gate evaluation is itself an institutional act. It is governed by the
Authority and Evidence gates of the consuming CommitmentPoint, or, where facts are
accepted in advance or in bulk, it MUST be its own `evidentiary_binding` CommitmentPoint.
This clause grounds catalog rule `FACT_ACCEPTANCE_GOVERNED` (warning, `Core-L2`).

### 8.4 AI Assistance Provenance in Receipts

A Receipt MAY carry `ai_assistance` (see 5.2):

```
ai_assistance = {
  involved: boolean,
  role: fact_extraction | recommendation | drafting | routing | none,
  human_review: attested | none
}
```

Where a runtime declares AI assistance in a governed context, accepted Commitments SHOULD
carry `ai_assistance` in their Receipts. This clause grounds catalog rule
`AI_ASSISTED_COMMITMENT_PROVENANCE` (warning, `Core-L2`).

### 8.5 Encoding Provenance

AI-assisted drafting of protocol encodings is permitted, but it MUST NOT be invisible. A
ProtocolVersion MAY carry `encoding_provenance` (see 3.3) declaring `drafting_method`
(`human`, `ai_assisted`, or `automated_conversion`), the drafting tool where applicable,
the REQUIRED `approved_by`, the approval basis, and the sources consulted.
`encoding_provenance` SHOULD be present at `Core-L2` and MUST be present at `Core-L3` and
`Corpus-L3` (catalog rule `ENCODING_PROVENANCE_REQUIRED`).

### 8.6 Routing and Shadow Binding

Routing and triage performed by or on behalf of an institution — whether by humans,
deterministic rules, or AI systems — are subject to shadow-binding analysis (see 3.6) and
become CommitmentPoints (typically `procedural_binding` or `evidentiary_binding`) when
they effectively foreclose or gate access to a service. Independent third-party advice
tools operating outside the institution's trust boundary are outside ICSL's scope.

## 9. Conformance Model

ICSL conformance is not a single unqualified binary claim.

A conformance declaration MUST identify:

- claim subject identity (`claim_subject`)
- claim subject type (`claim_subject_type`): `protocol_package`, `parser`, `validator`,
  `composer`, `registry`, `runtime_engine`, `renderer`, or `corpus_release`
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

- `L1` - the minimum institutional skeleton: a parseable encoding containing the required
  institutional boundary, governed-context descriptor, CommitmentPoints, commitment
  types, six gate slots, outcomes, and binding-effect declarations. Core-L1 establishes
  presence and structural placement, not semantic adequacy, source fidelity, legal
  validity, privacy compliance, runtime executability, receipt-chain behavior, or
  cross-system interoperability.
- `L2` - semantic encoding sufficient for binding, authority, recourse, canonicalization, and package claims.
- `L3` - high-fidelity encoding with references, governance addendum, reason-giving, renderings, and corpus-grade provenance.

Class-depth coupling: on a
ProtocolVersion, when `conformance_class` is present, `encoding_depth` is REQUIRED and
is constrained to the depth the class name declares, or deeper:

- `Core-L1` → `L1`, `L2`, or `L3`
- `Core-L2` and `Extended-L2` → `L2` or `L3`
- `Core-L3` and `Corpus-L3` → `L3`

The constraint is expressed in the ProtocolVersion schema as an `allOf` of `if`/`then`
conditionals. This clause grounds catalog rule `ENCODING_DEPTH_CLASS_CONSISTENT`
(error, `Core-L1`): a declared conformance class `…-Ln` requires encoding depth `Ln` or
greater.

No implementation MAY claim unqualified `ICSL compliant` status. Claims MUST name class,
ICSL version, and test-suite version.

Catalog-rule applicability is the intersection of class scope and claim-subject type. A
rule applies directly only when the claimed class includes the rule's `scope` and the
claim's `claim_subject_type` appears in the rule's
`applicability.direct_claim_subject_types`. An artifact-facing rule MAY serve as a fixture
oracle for an implementation suite without becoming a direct property of that
implementation. A `pass` result requires a published test-suite profile for the declared
subject type.

Conformance validates the declared representation, not the legality or practical adequacy
of the represented action. A validator MAY determine that a notice, reason-giving,
recourse, or legal-basis posture is present and structurally consistent. It MUST NOT
represent that result as proof that notice was legally effective, reasons were
substantively adequate, recourse was accessible in practice, evidence was true, or the
cited authority was valid in the applicable jurisdiction.

## 10. Diagnostics

Validators SHOULD report stable diagnostic IDs.

The machine-readable catalog at `04-reference/rules/catalog.json` is the authoritative
normative diagnostic registry.
A catalog rule backed by a normative MUST carries severity `error`; a rule backed by a
normative SHOULD carries severity `warning`. A rule's scope names the minimum conformance
class at which it is evaluated; higher Core classes inherit lower.

The following rule IDs are illustrative only; the catalog is authoritative:

- `CP_ALL_GATES_REQUIRED`
- `ADVERSE_OUTCOME_RECOURSE_STATE_REQUIRED`
- `RECEIPT_HASH_CHAIN_VALID`
- `CURRENT_TIME_REQUIRED`

## 11. Encoding Authority and Precedence


An ICSL artifact is a representation of underlying institutional or legal sources. In any
conflict between an encoding and the underlying source, the underlying source PREVAILS.
An encoding confers no independent legal effect.

A PackageManifest MAY declare a `publisher` object:

```
publisher = {
  name,
  relationship: authoritative_self_published | delegated_publisher | third_party_unofficial
}
```

`publisher` SHOULD be declared at `Core-L2`. This clause grounds catalog rule
`PUBLISHER_RELATIONSHIP_DECLARED` (warning, `Core-L2`).

Publishing an encoding is an institutional act. Modeling that publication as a
CommitmentPoint of a publisher-side protocol is RECOMMENDED where the publisher itself
operates under ICSL, and is expected machinery for `Corpus-L3` in a later version of this
specification. v0.1 does not require it.

## 12. Privacy and Data Protection Considerations


Receipts and receipt chains are not public by default. Publication of a ProtocolVersion
does not imply publication of the Receipts produced under it. Disclosure or
cross-institution sharing requires a separately established purpose, lawful basis,
authorization, access policy, retention policy, and security controls outside ICSL.

Personal data MUST NOT be embedded directly in hash-chained canonical Receipt content.
This clause grounds catalog rule `PERSONAL_DATA_NOT_IN_CANONICAL_RECEIPT` (error,
`Core-L2`). Removing direct identifiers does not by itself anonymize a Receipt:
`receipt_id`, `governed_context_id`, authority, outcome, timestamps, protocol identifiers,
content hashes, and chain relationships can enable singling out, correlation, or
linkability. Hashing is neither encryption nor anonymization. Implementations SHOULD use
non-meaningful, context-specific identifiers and MUST assess metadata and chain-level
linkability.

Personal-data payloads belong outside the canonical Receipt. A `content_hash` is a content
commitment; it is not a locator, disclosure authorization, or privacy guarantee. v0.1
defines direct SHA-256 verification when `content` and `content_hash` are both present. It
does not define an interoperable salted or keyed content-commitment profile, including key
or salt handling and verification after rectification or erasure. Implementations MUST
NOT describe v0.1 conformance as supplying those properties.

Evidence gates SHOULD minimize personal data to what the gate requires. ICSL does not
provide a lawful basis for processing or determine controller and processor roles.
Public or cross-institution Receipt publication requires a documented threat model
covering linkability, enumeration, selective disclosure, retention, residency,
rectification, and erasure. v0.1 defines no general profile for those obligations.

## 13. Publication Status

The conceptual model is frozen for external consultation. The next release work covers
fixture publication, conformance-suite expansion, independent validator implementation,
and implementation review.

It is not yet a final public standard.
