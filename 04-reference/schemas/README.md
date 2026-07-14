# Reference Schemas

The twelve schemas in this directory provide the JSON Schema portion of the ICSL v0.1
candidate. They enforce object structure, required fields, closed vocabularies, and selected
cross-field conditions. The prose specification and rule catalog remain necessary for
requirements that JSON Schema cannot express.

All schemas use JSON Schema draft 2020-12 and a provisional `$id` under
`https://igsl.dev/icsl/schemas/0.1-freeze/`.

## Contents

Canonical objects:

- `ProtocolVersion.schema.json` — the versioned protocol document; carries a required
  `institution` object and a required `governed_context` **descriptor** (the
  `GovernedContextDescriptor` definition in `ICSLCommon`; see the descriptor/runtime split
  below).
- `CommitmentPoint.schema.json` — the versioned template for a Commitment; carries a
  required `commitment_type`, typed `allowed_outcomes` (Outcome objects), an optional
  `trigger` (`institutional_act` | `temporal_lapse` | `external_event`, with
  `trigger_condition` required for `temporal_lapse`), and `acts_on_allowed` / `evolves` /
  `delegation` (optional in general, required by type-conditioned conditionals — see the
  taxonomy section below).
- `GateConfig.schema.json` — the six-gate configuration attached to every CommitmentPoint.
- `Reference.schema.json` — external source references (hash field is a tagged
  `sha256:<hex>` string).

Runtime and evidence objects:

- `GovernedContext.schema.json` — the governed instance that pins exactly one
  ProtocolVersion; carries the explicit `current_time` required for temporal evaluation
  and a required `protocol_version_hash` pinning the exact protocol-version content (see
  the version-identity section below).
- `Receipt.schema.json` — the evidentiary record of an accepted Commitment; full content
  core per ADR-003 (hash chaining via `receipt_hash`/`previous_hash`, `acts_on` lifecycle
  effects per ADR-004, `deemed` receipts, reserved unsigned `issuer`/`signatures`), plus a
  required `protocol_version_hash` in the content core.
- `EvaluationRecord.schema.json` — the record of a blocked or rejected attempt; a blocked
  or rejected attempt never produces a Receipt.
- `HashVector.schema.json` — the package hash vector: source-byte hashes for every file
  plus canonical-JSON hashes for JSON artifacts (dual-hash decision, ADR-002).

Packaging and conformance:

- `PackageManifest.schema.json`, `ConformanceDeclaration.schema.json`,
  `ValidationReport.schema.json`.

`ICSLCommon.schema.json` contains shared definitions: conformance classes, binding force,
recourse states and gates, binding-effect basis, authority gates, diagnostics,
`TaggedHash`, `CommitmentStatus`, `Outcome`,
`ActsOn`/`ActsOnAllowed`, `Evolves`, `Delegation`, `DependencyExpression`,
`TriggerCondition`, and `Deadline`. Object schemas should reuse these definitions rather
than restating enums.

## AI boundary and legal shell fields

The schemas include optional fields supporting the AI boundary in specification Section 8
and the legal context:

- `AuthorityGate.actor_type` — enum typing the actor holding authority
  (`human_officeholder` … `hybrid_human_ai`); AI/automated actors are subject to the
  delegation rule of spec section 8.
- `GateConfig` reasoning `mode` — previously a free string, now an enum
  (`deterministic_rule`, `calculation`, `guided_discretion`, `open_discretion`,
  `ai_assisted`, `external_judgment`, `mixed`); discretion must not be fettered into a
  deterministic rule.
- `Outcome.reason_giving` — `{ expectation: reasons_required | none_required_by_law,
  legal_basis? }`; `notice_state` is unchanged.
- `RecourseGate.legal_basis` — citation or Reference id backing a recourse-exclusion
  assertion.
- New `$defs` in `ICSLCommon`: `AiAssistance` (used by the optional
  `Receipt.ai_assistance`) and `EncodingProvenance` (used by the optional
  `ProtocolVersion.encoding_provenance`).
- `PackageManifest.publisher` — `{ name, relationship: authoritative_self_published |
  delegated_publisher | third_party_unofficial }`.

These fields are optional at the schema layer; their conformance obligations live in
the rule catalog (`../rules/catalog.json`) and the conformance profile.

## Commitment act taxonomy

ADR-008 restored the commitment act taxonomy dropped without record between IGSL v1.1 and
the ICSL draft:

- New `$defs` in `ICSLCommon`: `CoreCommitmentType` — the eight-value enum
  `DECIDE | ATTEST | APPEAL | REMEDY | OVERRIDE | EVOLVE | CLOSE | DELEGATE` — and
  `CommitmentTypeExtension` — the declaration object for extension types
  (`id` (urn-namespaced), `definition`, `fallback_semantics`, `rationale`; all four
  required, `fallback_semantics` is either a core type or the explicit `"none"`).
- `CommitmentPoint.commitment_type` — **required**; one of the eight core values or
  `EXTENSION`. The extension boundary is sealed bidirectionally: `commitment_type: EXTENSION` requires
  `commitment_type_extension` **and prohibits** `commitment_subtype`; a core
  `commitment_type` **prohibits** `commitment_type_extension` (expressed with
  `"not": {"required": [...]}` conditionals, plus rule
  `CP_EXTENSION_TYPE_DECLARATION_REQUIRED`). An optional `commitment_subtype`
  (`^urn:`-namespaced string) refines a core type; it has no semantics beyond format
  validation in v0.1.
- Class coupling: on
  `ProtocolVersion`, a conditional forbids any `EXTENSION`-typed CommitmentPoint when
  `conformance_class` is `Core-L1`, `Core-L2`, `Core-L3`, or `Corpus-L3`;
  `EXTENSION`-typed CommitmentPoints are permitted only in artifacts declaring
  `Extended-L2` (also rule `CP_EXTENSION_REQUIRES_EXTENDED_CLASS`). The coupling is now
  bidirectional — see the conditional-families section below.
- `Receipt.commitment_type` — optional derived copy: one of the eight core values, or
  the literal `EXTENSION` when the referenced CommitmentPoint is extension-typed. When `EXTENSION`, the
  optional `commitment_type_extension_id` string may carry the declared extension id.
  If present, the copy must match the referenced CommitmentPoint's type — `EXTENSION`
  matches `EXTENSION` (`RECEIPT_COMMITMENT_TYPE_MATCH`).
- Deterministic fallback: a consumer that does not recognize an extension type must
  apply the declared `fallback_semantics` — treat the CommitmentPoint as the named core
  type, or as opaque when `"none"` — and then apply its declared conformance-class
  behavior for unsupported extended features; silent acceptance is prohibited (spec
  text; the schema carries the required `fallback_semantics` field).

`GENERIC` is not in the enum by design: it is an Elinor authoring placeholder, not an
institutional act type, and it is forbidden in canonical artifacts (rule
`CP_GENERIC_TYPE_FORBIDDEN` gives Elinor's exporter a stable diagnostic). The type is
classificatory only — it creates no institutional effect by itself and never substitutes
for the structural fields the relational consistency rules check it against.

## Typed act relationships

The candidate defines a template-level act relationship and two type-specific
relationship objects:

- `ActsOnAllowed` (ICSLCommon) is now
  `{ allowed_effects: [ActsOnEffect] (required, minItems 1),
  targets: [commitment_point id] (required, minItems 1),
  basis_reference?: Reference id }`. `targets` names the CommitmentPoints whose receipts
  this CommitmentPoint may act on. At runtime, a Receipt's `acts_on.target_receipt_id`
  must reference a receipt whose `commitment_point_id` is in the acting CommitmentPoint's
  `acts_on_allowed.targets` (rule `ACTS_ON_TARGET_MEMBERSHIP`, error, Core-L2) — this
  closes the demonstrated attack of an appeal acting on an unrelated receipt.
- `Evolves` (ICSLCommon; `CommitmentPoint.evolves`) —
  `{ protocol_id?, protocol_version_id?, reference? }`, at least one required.
- `Delegation` (ICSLCommon; `CommitmentPoint.delegation`) —
  `{ recipient (required), scope (required), basis_reference? }`.

Type-conditioned requirements (schema `if`/`then`, mirrored by catalog rules):

| `commitment_type` | Schema requirement |
|---|---|
| `APPEAL`, `REMEDY` | `acts_on_allowed` required (with its required `targets`) |
| `OVERRIDE` | `acts_on_allowed` required **and** `acts_on_allowed.basis_reference` required |
| `EVOLVE` | `evolves` required |
| `DELEGATE` | `delegation` required |

`acts_on_allowed.targets` is required. Earlier experimental objects without `targets` do
not validate against the candidate schema.

## Governed-context descriptor vs runtime GovernedContext

The candidate separates the two roles previously carried by a free-form `governed_context` object:

- **Descriptor** — `ProtocolVersion.governed_context` is now a
  `GovernedContextDescriptor` (`ICSLCommon` def): what class of matters the protocol
  governs. Shape: `{ description (required), subject_class?, scope?,
  jurisdiction_note? }`, `additionalProperties: false`. Runtime members —
  `protocol_version_id`, `protocol_version_hash`, `governed_context_id`, `current_time` —
  are all prohibited by `additionalProperties: false`. Consequence: the ProtocolVersion
  contains no hash of itself, full stop, and the zero-hash placeholder convention is
  removed from every embedded object.
- **Runtime** — `GovernedContext.schema.json` (shape unchanged) is the governed instance:
  a separate top-level artifact that pins exactly one ProtocolVersion by
  `protocol_version_id` **and** `protocol_version_hash` (both still required). New
  catalog rule `GOVERNED_CONTEXT_PROTOCOL_VERSION_HASH_MATCH` (error, Core-L2): a runtime
  GovernedContext's `protocol_version_hash` must equal the canonical hash of the
  ProtocolVersion its `protocol_version_id` names.

This descriptor shape is an intentional backward break: pre-existing artifacts that
embedded runtime-shaped (or zero-hash) `governed_context` objects in a ProtocolVersion no
longer validate and must move that material to a runtime GovernedContext artifact.

## ProtocolVersion conditional families

Two conditional families on `ProtocolVersion` use JSON Schema `allOf` with `if`/`then`:

1. **Bidirectional extension–class coupling.** A core or corpus
   `conformance_class` (`Core-L1`, `Core-L2`, `Core-L3`, `Corpus-L3`) forbids any
   `EXTENSION`-typed CommitmentPoint. Conversely, if
   `commitment_points` `contains` any CommitmentPoint with `commitment_type: EXTENSION`,
   then `conformance_class` is **required** and must be `const "Extended-L2"`. The
   reverse direction closes the omission bypass: omitting `conformance_class` can no
   longer smuggle an `EXTENSION` CommitmentPoint past the class gate (mutation M20 probes
   exactly this).
2. **Class-depth coupling.** When `conformance_class` is present, `encoding_depth` is
   **required** and constrained per class — a class declared at `-Ln` requires encoding
   depth `Ln` or greater: `Core-L1` → `L1`/`L2`/`L3`; `Core-L2` and `Extended-L2` →
   `L2`/`L3`; `Core-L3` and `Corpus-L3` → `L3` (also catalog rule
   `ENCODING_DEPTH_CLASS_CONSISTENT`, error, Core-L1).

## Protocol-version identity

`protocol_version_hash` is the canonical content identity of a ProtocolVersion:
`sha256:<64 lowercase hex>` (the shared `TaggedHash` def) over the RFC 8785 (JCS)
canonical bytes of the complete ProtocolVersion JSON object. The ProtocolVersion object
contains no hash of itself (its `governed_context` is a hash-free descriptor), so the
preimage is non-self-referential.

- `Receipt.protocol_version_hash` — **required** (part of the receipt content core); must
  equal the canonical hash of the ProtocolVersion named by `protocol_version_id` (rule
  `RECEIPT_PROTOCOL_VERSION_HASH_MATCH`, error, Core-L2).
- `GovernedContext.protocol_version_hash` — **required**; pins the exact protocol-version
  content, not just its id (rule `GOVERNED_CONTEXT_PROTOCOL_VERSION_HASH_MATCH`, error,
  Core-L2).

## Seed-strict gate tightening

The four content gates are no longer free-form objects. Evidence, reasoning, dependency,
and version gates now have defined vocabularies with `additionalProperties: false` and
required minimums; the authority gate requires one of `legal_authority_holder`,
`delegated_authority`, or `authority_basis: operation_of_law` with a `legal_source`
(`task_owner` alone no longer validates). Extension material belongs in namespaced
extensions, not arbitrary gate keys.

Related decisions:

- [ADR-002](../../07-decisions/ADR-002-canonicalization.md) — RFC 8785 (JCS)
  canonicalization, I-JSON constraints, tagged `sha256:` hash strings, dual-hash vector.
- [ADR-003](../../07-decisions/ADR-003-receipt-hashing-trust.md) — receipt content core,
  hash chaining, unsigned-in-v0.1 trust model, reserved signature fields.
- [ADR-004](../../07-decisions/ADR-004-commitment-lifecycle.md) — commitment status enum,
  `acts_on` effects, derived-status algebra.
- [ADR-005](../../07-decisions/ADR-005-outcome-objects.md) — Outcome objects with required
  `effect_class`; adverse-outcome rules key off `effect_class`, not a self-declared boolean.
- [ADR-008](../../07-decisions/ADR-008-commitment-act-taxonomy.md) — commitment act
  taxonomy restoration: the eight core types, the `EXTENSION` marker at Extended-L2, and
  the receipt-copy rule.

These remain candidate schemas. Final publication still needs a full JSON Schema
validation path in the CLI or a separate reference validator.
