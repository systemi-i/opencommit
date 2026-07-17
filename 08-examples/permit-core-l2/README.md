# Core-L2 Proof Exemplar: Municipal Construction Permit (Fictional)


This directory is a complete, verifiable ICSL v0.1 package encoding a **fictional**
municipal construction-permit protocol for the **Example City Building Authority**
(Republic of Exampleland, which does not exist). Every statute section, decree,
officeholder, case number, and locator in this package is invented. The package is
illustrative only: it demonstrates the current v0.1 candidate model at conformance
class Core-L2 and is not legal advice, not an encoding of any real jurisdiction, and
not a template whose legal content should be reused. Per the specification, an ICSL
encoding is a representation of underlying institutional sources; in any conflict the
underlying source prevails, and a Receipt is rebuttable evidence of process, not proof
of the substantive legality of the underlying act.

## What the example exercises

- **Commitment types**:
  a required `commitment_type` on all 11 CommitmentPoints (core values `ATTEST`,
  `DECIDE`, `APPEAL`, `REMEDY` in use), derived `commitment_type` copies on every
  receipt (SHOULD at Core-L2; mismatch is `RECEIPT_COMMITMENT_TYPE_MATCH`), the
  APPEAL-vs-DECIDE and REMEDY-vs-OVERRIDE boundary tests exercised on real CPs
  (see "Boundary cases documented" below), and the appeal split as the canonical
  atomicity worked example.
- **Outcome objects** (`token` + `effect_class`), with per-outcome `recourse`,
  `notice_state`, and `reason_giving` on every adverse or mixed outcome
  (`cp-03`, `cp-05`, `cp-06`, `cp-07`, `cp-08`, `cp-09`, `cp-10`, `cp-11`).
- **Recourse-exclusion basis**: `not_applicable` on an adverse outcome with
  `legal_basis` (`cp-06-technical-review`), and `legally_unavailable` with
  `legal_basis` (`cp-09-appeal-admissibility` inadmissibility) — both flagged in
  the encoding as rebuttable encoder claims about the law.
- **Reason-giving**: `reasons_required` with legal basis on adverse decisions, and
  `none_required_by_law` with legal basis on the deemed approval (`cp-08`).
- **Actor typing and the AI boundary** (spec section 8): `actor_type` on every
  Authority gate (`human_officeholder`, `institutional_role`,
  `hybrid_human_ai`, `automated_deterministic_system`); Reasoning-gate `mode`
  values `deterministic_rule`, `calculation`, `ai_assisted`, `guided_discretion`
  (anti-fettering at `cp-07`), and `mixed`; fact acceptance as its own
  evidentiary-binding CommitmentPoint (`cp-02`); and `ai_assistance` provenance
  on receipts.
- **Triggers and deemed receipts**: `cp-08` fires on `temporal_lapse` with a
  `trigger_condition` (anchor + `P90D` + `requires_absence`), authority
  `operation_of_law` with a versioned `legal_source`, attested-absence evidence,
  and a runtime-minted receipt with `deemed: true`.
- **Commitment lifecycle**: appeal admission (`cp-09-appeal-admissibility`)
  suspends the decision (`acts_on: suspend`), dismissal at disposition
  (`cp-10-appeal-disposition`) revives it (`acts_on: revive`), upholding would
  quash it (`quash` is declared in `acts_on_allowed`), and revocation (`cp-11`)
  declares `revoke_ex_tunc`.
- **Typed act relationships**: every `acts_on_allowed` now carries both `allowed_effects`
  and `targets` — the CommitmentPoint ids whose receipts the acting CP may act
  on (`cp-07-decision` and `cp-08-deemed-approval` for all three relational CPs
  here; `cp-11-revocation` also carries the optional `basis_reference`). At
  runtime, a receipt's `acts_on.target_receipt_id` must resolve to a receipt
  whose `commitment_point_id` is in the acting CP's `acts_on_allowed.targets`
  (`ACTS_ON_TARGET_MEMBERSHIP`, error) — so an appeal receipt cannot suspend or
  revive an unrelated receipt.
- **Version identity**:
  every receipt carries a required `protocol_version_hash` — `sha256:<64 hex>`
  over the RFC 8785 (JCS) canonical bytes of the complete
  `protocol-version.json` object. The ProtocolVersion contains no hash of
  itself, so the preimage is non-self-referential; `verify.py` recomputes the
  hash and checks every receipt against it
  (`RECEIPT_PROTOCOL_VERSION_HASH_MATCH`, error).
- **GovernedContextDescriptor**: the ProtocolVersion's embedded
  `governed_context` is a purely descriptive `GovernedContextDescriptor`
  (`description` required; optional `subject_class`, `scope`,
  `jurisdiction_note`; `additionalProperties: false`). It MUST NOT carry
  runtime members (`protocol_version_id`, `protocol_version_hash`,
  `governed_context_id`, `current_time`), so **no zero-hash placeholder
  convention exists anywhere** — the ProtocolVersion contains no hash of
  itself, full stop. Runtime `GovernedContext` instances are separate
  artifacts that pin this ProtocolVersion by id **and** canonical hash
  (`GOVERNED_CONTEXT_PROTOCOL_VERSION_HASH_MATCH`); no runtime GovernedContext
  ships in this package (the deemed receipt's `governed_context_id` names one
  from a second, truncated context). Because the reshape changed the
  ProtocolVersion's canonical bytes, every receipt's `protocol_version_hash`
  and the hash vector reflect the current ProtocolVersion.
- **Dependency grammar**: `commitment_point`/`outcome`, `absent`, `external`,
  `temporal` (elapsed), `any_of`, `all_of` — including outcome-level dependencies.
- **Encoding provenance and publisher**: `encoding_provenance`
  (`drafting_method: ai_assisted`, approved by a named fictional official) on the
  ProtocolVersion, and `publisher` (`third_party_unofficial`) on the manifest.
- **Canonicalization and hashing**: real, recomputable RFC 8785 (JCS) hashes for
  the receipt chain and the dual-hash package vector.

## Package layout

| File | Role |
| --- | --- |
| `manifest.json` | package manifest (declares every file, including itself and the publisher) |
| `protocol-version.json` | the ProtocolVersion with 11 CommitmentPoints |
| `references/building-act.json` | versioned Reference for the fictional Building Act |
| `receipts/chain-01.json` | one hash-linked chain of 6 receipts (see below) |
| `receipts/deemed-example.json` | a single deemed receipt (`deemed: true`) from a second, truncated context |
| `conformance.json` | ConformanceDeclaration (result `not_run` — see below) |
| `hashes.json` | HashVector: source-byte hashes for every file, canonical-JSON hashes for JSON artifacts (self-exempt) |
| `verify.py` | the verification script used to check this package (manifest role `extension`: tooling, not canonical protocol data) |
| `attacks.py` | persisted attack runner: control run plus five tampering attacks that `verify.py` must catch (role `extension`) |

## CommitmentPoints and commitment types


| CommitmentPoint | `commitment_type` | Note |
| --- | --- | --- |
| `cp-01-intake` | `ATTEST` | constitutive attestation (filing-date certification) |
| `cp-02-fact-acceptance` | `ATTEST` | the AI-boundary conversion CP |
| `cp-03-completeness` | `DECIDE` | procedural_binding |
| `cp-04-public-notice` | `ATTEST` | |
| `cp-05-objection-registration` | `DECIDE` | |
| `cp-06-technical-review` | `ATTEST` | shadow-binding advisory |
| `cp-07-decision` | `DECIDE` | |
| `cp-08-deemed-approval` | `DECIDE` | trigger `temporal_lapse`, operation of law |
| `cp-09-appeal-admissibility` | `DECIDE` | procedural_binding; `acts_on_allowed`: effect `suspend`, targets `cp-07-decision` + `cp-08-deemed-approval` |
| `cp-10-appeal-disposition` | `APPEAL` | `acts_on_allowed`: effects `revive`, `quash`, same targets |
| `cp-11-revocation` | `REMEDY` | `acts_on_allowed`: effect `revoke_ex_tunc`, same targets, `basis_reference: ref-building-act`; justification test |

The type is classificatory only: it creates no institutional effect by itself,
does not determine binding force, outcome effect, recourse availability, legal
validity, or authority, and never substitutes for the structural fields it is
checked against.

### Boundary cases documented

- **Why revocation-for-fraud is `REMEDY`, not `OVERRIDE`** (`cp-11-revocation`).
  Under the REMEDY-vs-OVERRIDE justification test, the classification turns on
  the act's *justification*, not its mechanical effect: here the justification
  is a defect in the permit's procurement (fraudulent evidence), so the act
  cures a defect — ex tunc — and is `REMEDY`. The contrast case: if Example City
  displaced a *validly obtained* permit for a supervening public interest (say,
  an emergency flood-plain reclassification), asserting no defect in the permit
  itself, that displacement would be `OVERRIDE`. The two acts can carry the very
  same `acts_on` effect while being legally opposite, with different
  consequences for liability and legitimate expectations — which is why the type
  is not derivable from `acts_on` and must be declared.
- **Why the appeal is two CommitmentPoints** (`cp-09-appeal-admissibility` +
  `cp-10-appeal-disposition`). The atomicity rule: each independently
  reliance-worthy institutional act is its own CommitmentPoint. Suspensive
  effect attaches at *admission* (Building Act s.47(2)), not at disposition, and
  the admissibility ruling and the merits disposition are separately
  challengeable — so bundling them into one CP would hide a reliance point.
  The admissibility determination is `DECIDE`, not `APPEAL`: under the
  APPEAL-vs-DECIDE boundary test, procedural determinations *within* the
  recourse process are `DECIDE`; only the disposition of the challenge itself —
  where the relation to the challenged commitment dominates — is `APPEAL`.
  The audit-adopted clarification of the ordered classification procedure states this
  precisely: APPEAL means disposition of the challenge **on the merits**;
  procedural determinations within the recourse process (admissibility,
  timeliness, standing), even when they terminate the challenge, classify as
  DECIDE. That clarification *confirms* this package's existing classification
  (admissibility = `DECIDE`, disposition = `APPEAL`); no receipt or CP here
  changed type because of it.

## The receipt chain

`receipts/chain-01.json` records one governed context (`gc-ec-2026-000123`):

1. intake registered (genesis, `previous_hash: null`; AI-assisted fact extraction, human review attested) — `commitment_type` copy `ATTEST`
2. completeness: `complete` (starts the deemed-approval clock) — copy `DECIDE`
3. technical review: `conforming` (AI-assisted recommendation, engineer-certified) — copy `ATTEST`
4. decision: `approved` — copy `DECIDE`
5. appeal admissibility (`cp-09-appeal-admissibility`): `admissible_effect_suspended`, `acts_on` **suspend** targeting the decision receipt — copy `DECIDE`
6. appeal disposition (`cp-10-appeal-disposition`): `appeal_dismissed_effect_revived`, `acts_on` **revive** targeting the decision receipt — copy `APPEAL`

Every receipt carries a derived `commitment_type` copy (SHOULD at Core-L2); the
authoritative type lives only in the hashed ProtocolVersion, and a mismatching
copy is the error `RECEIPT_COMMITMENT_TYPE_MATCH`.

Every receipt also carries the required `protocol_version_hash`: the canonical JCS + sha256 hash of
the complete `protocol-version.json` object, binding each receipt to the exact
protocol text it was minted under, not merely to the version *identifier*. Both
`acts_on` receipts (suspend, revive) target the `cp-07-decision` receipt, which
is in the acting CPs' declared `acts_on_allowed.targets` — the membership check
that closes the acting-on-an-unrelated-receipt attack.

The chain is deliberately abbreviated for illustration: the context's `cp-04`
public-notice and `cp-05` objection receipts are elided, so a validator evaluating
full dependency satisfaction over the context (as opposed to verifying the chain
itself) would flag their absence. `receipts/deemed-example.json` is a single receipt
from a second context (`gc-ec-2026-000777`); its `previous_hash` points at that
context's completeness receipt, which is not shipped. The predecessor value is
illustrative and cannot be independently validated from this package; only the deemed
receipt's self-hashes are verifiable here.

Receipt `content` carries no personal data. Applicant dossiers and decision reasons are
treated as detachable payloads managed by the fictional authority under deployment
controls outside this package. The example's deployment notes do not define or claim an
interoperable salting, key-management, rectification, erasure, or verification profile;
ICSL v0.1 provides none of those properties.

## How to re-verify

```
python3 verify.py        # requires: pip install jsonschema
```

`verify.py` validates every JSON artifact against the schemas in
`04-reference/schemas/` (JSON Schema draft 2020-12, local `$ref` registry, with
`FormatChecker` enforcing format assertions such as `date-time`), recomputes the
receipt chain and the hash vector, and checks manifest completeness.
It exits 0 when everything verifies.

The verifier applies the following additional protections:

- **JCS discipline**: `verify.py` uses a real RFC 8785 implementation when
  installed (`pip install rfc8785`); otherwise it MUST — and does — assert
  **both** preconditions before every hash and fail closed if either is
  violated: (1) no non-string JSON numbers anywhere (quantities are strings,
  ADR-002), and (2) all member names (object keys) are ASCII. The second
  precondition exists because RFC 8785 sorts members by UTF-16 code units
  while Python's `sort_keys` sorts by code points, and the orderings diverge
  for non-BMP member names; member-name ordering is the only divergence risk
  (values may be any Unicode). Under both preconditions, sorted compact
  `json.dumps` is byte-identical to RFC 8785; the guarded fallback is **not**
  a general JCS implementation. The ASCII-member-name rule is also an
  artifact conformance constraint, so `verify.py` asserts it even when
  `rfc8785` is installed.
- **Descriptor shape**: the embedded `governed_context` must be
  descriptor-shaped — `description` plus optional `subject_class`, `scope`,
  `jurisdiction_note`, and no runtime members.
- **Manifest path safety**: declared paths (manifest and hash vector) are
  rejected if absolute or containing `..` segments.
- **Version identity**: every receipt's `protocol_version_hash` must equal the
  recomputed canonical hash of `protocol-version.json`
  (`RECEIPT_PROTOCOL_VERSION_HASH_MATCH`).
- **Target membership**: every `acts_on` receipt's target must resolve to a
  receipt whose `commitment_point_id` is in the acting CP's
  `acts_on_allowed.targets` (`ACTS_ON_TARGET_MEMBERSHIP`), and every declared
  target must be an existing CommitmentPoint id.

## The attack runner


```
python3 attacks.py       # requires: pip install jsonschema
```

`attacks.py` demonstrates that `verify.py` catches **semantic** tampering, not
just byte corruption. It copies `04-reference/` and `08-examples/` into a
fresh temp tree **preserving the repo-relative layout** (`verify.py` resolves
the schemas relatively; a flat copy crashes — this was demonstrated during the
audit), runs `verify.py` unmodified as a control (must pass), then applies
each attack in a fresh copy with receipt and hash-vector hashes legitimately
recomputed so **only the semantic violation remains**, and requires
`verify.py` to fail with the expected diagnostic:

| Attack | Tampering | Caught by |
| --- | --- | --- |
| A1 | disposition receipt's `acts_on` retargeted at the intake receipt | `ACTS_ON_TARGET_MEMBERSHIP` |
| A2 | one chain receipt's `protocol_version_hash` corrupted | `RECEIPT_PROTOCOL_VERSION_HASH_MATCH` |
| A3 | deemed receipt's pinned hash mutated (context/receipt version mismatch) | `RECEIPT_PROTOCOL_VERSION_HASH_MATCH` |
| A4 | manifest path containing a `..` segment | path safety |
| A5 | non-ASCII member name injected into a canonical artifact copy | JCS guard (fail closed) |

It exits 0 iff the control passes and every attack is caught. See also the
schema-level mutation suite in `04-reference/mutations/`.

The core recomputation, if you would rather do
it yourself (valid here because the package contains no JSON numbers at all —
quantities are strings per ADR-002 — and all member names are ASCII, so
`json.dumps` with sorted keys emits RFC 8785 canonical bytes):

```python
import json, hashlib
jcs = lambda o: json.dumps(o, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
tag = lambda b: "sha256:" + hashlib.sha256(b).hexdigest()

pvh = tag(jcs(json.load(open("protocol-version.json"))))

chain = json.load(open("receipts/chain-01.json"))
prev = None
for r in chain:
    assert r["receipt_hash"] == tag(jcs({k: v for k, v in r.items() if k != "receipt_hash"}))
    assert r["previous_hash"] == prev
    assert r["protocol_version_hash"] == pvh
    if "content" in r:
        assert r["content_hash"] == tag(jcs(r["content"]))
    prev = r["receipt_hash"]

for e in json.load(open("hashes.json"))["entries"]:
    assert e["source_hash"] == tag(open(e["path"], "rb").read())
    if "canonical_hash" in e:
        assert e["canonical_hash"] == tag(jcs(json.load(open(e["path"]))))
print("chain and hash vector verified")
```

## Conformance posture (honest)

`conformance.json` declares Core-L2 with result **`not_run`**, pinned to test-suite
version `icsl.conformance.seed/2026-07-07.seed`. The ICSL conformance suite is
unpublished, so no suite run exists. Schema validation plus hash recomputation
(`verify.py`) is **not** a conformance-suite pass, and this package makes no claim
beyond its declaration. Per the specification, no unqualified "ICSL compliant" claim
is permitted.
