# ICSL Conformance Profile Candidate

- Status: candidate draft.
- Date: 2026-07-07.

## 1. Principle

ICSL conformance is multi-dimensional. A single unqualified claim such as `ICSL compliant`
is not valid.

Every conformance claim MUST identify:

- claim subject
- conformance class
- ICSL version
- test-suite version
- result

## 2. Claim Subjects

Conformance may be claimed by:

- protocol packages
- parsers
- validators
- composers
- registries
- runtime engines
- renderers
- corpus releases

The subject MUST be explicit.

## 3. Classes

Class lattice: the Core classes
form a strict inclusion chain, Core-L1 ⊂ Core-L2 ⊂ Core-L3 — each class includes every
requirement of the classes below it. Extended-L2 = Core-L2 + extension negotiation.
Corpus-L3 = Core-L3 + provenance. A rule's catalog `scope` is the minimum class at which
it is evaluated; higher Core classes inherit it.

### Core-L1

Core-L1 covers structural interoperability:

- parseable package
- ProtocolVersion present, with institution identification and governed-context declaration
- CommitmentPoints present
- commitment type present and valid, no GENERIC placeholder
- six gates present
- binding effect basis stated per CommitmentPoint
- canonical/runtime separation enforced
- rendering boundary: renderings introduce no new semantics
- conformance declaration present

### Core-L2

Core-L2 covers semantic interoperability:

- Core-L1 requirements
- authority distinctions
- outcome effect classes and adverse-flag consistency
- binding-force semantics
- recourse semantics
- adverse-outcome recourse checks (keyed off Outcome.effect_class adverse or mixed)
- evidence durability
- lifecycle status resolution (acts_on chains)
- trigger and temporal evaluation
- dependency grammar and reference resolution
- canonicalization behavior
- receipt content core and chain behavior where receipts are claimed
- non-executing normative fields
- normative reference versioning
- package hash-vector completeness (dual hashes)
- AI authority boundary: actor typing and the delegation rule (spec section 8)
- discretion representation (anti-fettering) and fact-acceptance governance
- AI-assistance, encoding-provenance, and publisher declarations
- recourse-exclusion legal basis
- adverse-outcome notice and reason-giving declarations
- personal data excluded from canonical receipt content
- relational commitment-type consistency and receipt type match
- receipt protocol-version identity: protocol_version_hash matches the canonical hash of the named ProtocolVersion
- acts_on target membership: a receipt acts only on receipts of CommitmentPoints listed in the acting CommitmentPoint's acts_on_allowed.targets

### Core-L3

Core-L3 covers high-fidelity institutional semantics:

- Core-L2 requirements
- governance addendum where triggered
- reason-giving sufficiency

### Extended-L2

Extended-L2 covers profile, domain, or extension-aware implementations:
Core-L2 plus extension negotiation.

Unsupported extended features MUST block, warn, or downgrade according to the declared
conformance class.

The EXTENSION commitment-type marker is valid only at Extended-L2 and requires a full
extension declaration.

Extension-class coupling: an
artifact declaring any core class (Core-L1, Core-L2, Core-L3, or Corpus-L3) MUST NOT
contain a CommitmentPoint with commitment_type EXTENSION — the ProtocolVersion schema
enforces this conditionally and CP_EXTENSION_REQUIRES_EXTENDED_CLASS diagnoses it. The
schema also enforces the reverse: a ProtocolVersion containing any EXTENSION-typed
CommitmentPoint MUST declare `conformance_class: "Extended-L2"` — omitting the
conformance class does not license EXTENSION.

Deterministic extension fallback: a consumer processing an artifact and encountering an EXTENSION-typed
CommitmentPoint MUST behave per this fixed table; there is no per-artifact override
field. This table mirrors the normative statement in the specification and is diagnosed
by EXTENSION_FALLBACK_BEHAVIOR_REQUIRED.

| Consumer | Recognizes the extension id | fallback_semantics | Required behavior |
| --- | --- | --- | --- |
| Core classes only | (n/a — cannot process EXTENSION natively) | names a core type | Process the CommitmentPoint as that core type AND emit a warning diagnostic |
| Core classes only | (n/a) | `"none"` | Block (error) |
| Extended-L2 | yes | (any) | Process natively per the extension declaration |
| Extended-L2 | no | names a core type | Process as that core type AND emit a warning diagnostic |
| Extended-L2 | no | `"none"` | Block (error) |

Silent acceptance is prohibited in all cases.

### Corpus-L3

Corpus-L3 covers curated institutional corpora: Core-L3 plus provenance:

- provenance expectations
- source confidence
- transparency-gap marking
- no unproven `unknown_unpublished` adverse recourse gaps without provenance

## 3a. Requirement-to-Rule Traceability


Each class bullet above maps to catalog rule IDs (04-reference/rules/catalog.json) or is
marked fixture-only.

| Class | Requirement | Rule IDs |
| --- | --- | --- |
| Core-L1 | parseable package | PACKAGE_MANIFEST_REQUIRED, PACKAGE_MANIFEST_FILE_EXISTS, PACKAGE_MANIFEST_SELF_DECLARED |
| Core-L1 | ProtocolVersion present, institution, governed context | INSTITUTION_IDENTIFICATION_REQUIRED, GOVERNED_CONTEXT_REQUIRED |
| Core-L1 | CommitmentPoints present | PROTOCOL_COMMITMENT_POINTS_REQUIRED |
| Core-L1 | commitment type present, valid, no GENERIC placeholder | CP_COMMITMENT_TYPE_REQUIRED, CP_COMMITMENT_TYPE_INVALID, CP_GENERIC_TYPE_FORBIDDEN |
| Core-L1 | six gates present | CP_ALL_GATES_REQUIRED, VERSION_PIN_REQUIRED |
| Core-L1 | binding effect basis | CP_BINDING_EFFECT_REQUIRED |
| Core-L1 | outcomes declared | CP_ALLOWED_OUTCOMES_REQUIRED |
| Core-L1 | canonical/runtime separation | CANONICAL_NO_DEPLOYMENT_BINDINGS |
| Core-L1 | rendering boundary | RENDERING_NO_NEW_SEMANTICS |
| Core-L1 | conformance declaration | CONFORMANCE_DECLARATION_REQUIRED, CONFORMANCE_CLASS_INVALID, CONFORMANCE_RESULT_INVALID |
| Core-L2 | authority distinctions | TASK_OWNER_NOT_AUTHORITY, AI_NOT_GATE_AUTHORITY, OPERATION_OF_LAW_REQUIRES_LEGAL_SOURCE |
| Core-L2 | AI authority boundary (actor typing, delegation rule) | AI_AUTHORITY_DELEGATION_BASIS_REQUIRED |
| Core-L2 | discretion representation (anti-fettering) | DISCRETION_NOT_FETTERED (warning) |
| Core-L2 | fact-acceptance governance | FACT_ACCEPTANCE_GOVERNED (warning) |
| Core-L2 | AI-assistance provenance on receipts | AI_ASSISTED_COMMITMENT_PROVENANCE (warning) |
| Core-L2 | encoding provenance declared | ENCODING_PROVENANCE_RECOMMENDED (warning) |
| Core-L3 | encoding provenance required | ENCODING_PROVENANCE_REQUIRED (error) |
| Core-L2 | publisher relationship declared | PUBLISHER_RELATIONSHIP_DECLARED (warning) |
| Core-L2 | recourse-exclusion legal basis | RECOURSE_EXCLUSION_REQUIRES_BASIS |
| Core-L2 | adverse-outcome notice and reason-giving declarations | ADVERSE_OUTCOME_NOTICE_REQUIRED, ADVERSE_OUTCOME_REASON_GIVING_DECLARED |
| Core-L2 | personal data excluded from canonical receipt content | PERSONAL_DATA_NOT_IN_CANONICAL_RECEIPT |
| Core-L2 | outcome effect classes and adverse-flag consistency | OUTCOME_EFFECT_CLASS_REQUIRED, ADVERSE_FLAG_OUTCOME_CONSISTENCY |
| Core-L2 | binding-force semantics | BINDING_FORCE_REQUIRED, BINDING_FORCE_MIXED_REQUIRES_COMPONENTS |
| Core-L2 | recourse semantics | RECOURSE_STATE_INVALID |
| Core-L2 | adverse-outcome recourse checks | ADVERSE_OUTCOME_RECOURSE_STATE_REQUIRED, ADVISORY_CP_REQUIRES_SHADOW_BINDING |
| Core-L2 | evidence durability | DURABLE_FACTS_REQUIRED (warning) |
| Core-L2 | lifecycle status resolution | ACTS_ON_TARGET_RESOLVABLE |
| Core-L2 | trigger and temporal evaluation | TRIGGER_TEMPORAL_REQUIRES_CONDITION, CURRENT_TIME_REQUIRED |
| Core-L2 | dependency grammar and reference resolution | DEPENDENCY_EXPRESSION_INVALID, DEPENDENCY_REFERENCE_UNRESOLVED |
| Core-L2 | canonicalization behavior | CANONICALIZATION_PROFILE_JCS, HASH_FORMAT_INVALID |
| Core-L2 | receipt content core and chain behavior | RECEIPT_CONTENT_CORE_REQUIRED, RECEIPT_HASH_CHAIN_VALID |
| Core-L2 | non-executing normative fields | NON_EXECUTING_FIELDS_DO_NOT_AFFECT_GATES |
| Core-L2 | normative reference versioning | REFERENCE_VERSION_REQUIRED (warning) |
| Core-L2 | package hash-vector completeness (dual hashes) | PACKAGE_HASH_VECTOR_VALID, PACKAGE_HASH_VECTOR_COMPLETE, PACKAGE_DUAL_HASH_REQUIRED |
| Core-L3 | governance addendum where triggered | GOVERNANCE_ADDENDUM_REQUIRED (warning), GOVERNANCE_ADDENDUM_INCOMPLETE |
| Core-L3 | reason-giving sufficiency | ADVERSE_OUTCOME_REASON_GIVING_DECLARED (inherited from Core-L2; sufficiency of the reasons themselves remains fixture-only in v0.1) |
| Core-L2 | relational commitment-type consistency | APPEAL_TARGET_REQUIRED, OVERRIDE_TARGET_AND_BASIS_REQUIRED, EVOLVE_TARGET_VERSION_REQUIRED, DELEGATE_SCOPE_REQUIRED, REMEDY_TARGET_IDENTIFIED (warning), CLOSE_TERMINAL_TRANSITION (warning) |
| Core-L2 | receipt commitment-type copy matches the referenced CommitmentPoint | RECEIPT_COMMITMENT_TYPE_MATCH |
| Core-L2 | receipt protocol-version identity (protocol_version_hash matches the canonical hash of the named ProtocolVersion) | RECEIPT_PROTOCOL_VERSION_HASH_MATCH |
| Core-L2 | acts_on target membership (a receipt's acts_on.target_receipt_id resolves to a receipt of a CommitmentPoint listed in acts_on_allowed.targets) | ACTS_ON_TARGET_MEMBERSHIP |
| Core-L2 | governed-context protocol-version identity (a runtime GovernedContext's protocol_version_hash matches the canonical hash of the named ProtocolVersion) | GOVERNED_CONTEXT_PROTOCOL_VERSION_HASH_MATCH |
| Core-L1 | class–depth consistency (a declared conformance class -Ln requires encoding depth Ln or greater) | ENCODING_DEPTH_CLASS_CONSISTENT |
| Extended-L2 | extension negotiation | UNSUPPORTED_EXTENDED_FEATURE_MUST_BLOCK_OR_WARN_BY_CLASS |
| Extended-L2 | extension commitment-type declaration | CP_EXTENSION_TYPE_DECLARATION_REQUIRED |
| Extended-L2 | extension-class coupling (no EXTENSION-typed CommitmentPoints in core-class artifacts) | CP_EXTENSION_REQUIRES_EXTENDED_CLASS |
| Extended-L2 | deterministic extension fallback (fallback_semantics then class-declared unsupported-extension behavior; silent acceptance prohibited) | EXTENSION_FALLBACK_BEHAVIOR_REQUIRED |
| Corpus-L3 | no unproven unknown_unpublished adverse recourse | UNKNOWN_RECOURSE_BLOCKS_L3_CORPUS |
| Corpus-L3 | provenance expectations, source confidence, transparency-gap marking | fixture-only, no diagnostic in v0.1 |

## 4. Encoding Depths

### L1

L1 records the existence and structure of institutional commitments.

### L2

L2 records enough semantics for independent validation of binding force, authority, evidence,
recourse, package integrity, canonicalization, and conformance claims.

### L3

L3 records publication-grade institutional semantics, including references, governance
fields, reason-giving, non-executing normative fields, renderings, and provenance.

### Class–Depth Rule


A conformance class with suffix `-Ln` requires the claim subject's encoding depth to be
`Ln` or greater. A package encoded at depth L1 cannot claim Core-L2; a Corpus-L3 claim
requires depth L3.

This coupling is schema-enforced on ProtocolVersion: when `conformance_class` is present, `encoding_depth` is REQUIRED
and constrained per class (Core-L1 → L1/L2/L3; Core-L2 and Extended-L2 → L2/L3; Core-L3
and Corpus-L3 → L3), and catalog rule ENCODING_DEPTH_CLASS_CONSISTENT diagnoses
violations at Core-L1.

## 5. Test Suites

A conformance declaration MUST name the test-suite identifier and version used. A result
applies only to the declared claim subject, class, ICSL version, suite version, and
validator. Passing one of the narrower checks published with the candidate MUST NOT be
reported as a pass against the future full conformance suite.

The current machine-readable ICSL version is `0.1-freeze`. The candidate, release-candidate,
and final labels are described in [Status and Roadmap](../STATUS.md).

## 6. Diagnostic Stability

Diagnostic IDs SHOULD remain stable across validator implementations.

When a rule is replaced, the old diagnostic ID SHOULD be deprecated rather than silently
reused for a different meaning.
