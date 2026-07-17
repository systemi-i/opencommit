# ICSL Schema-Mutation Suite


This directory persists the schema-level mutation regression suite so that any
reviewer can re-run it independently. It contains:

| File | Role |
|---|---|
| `baseline.json` | A minimal ProtocolVersion (two CommitmentPoints, `DECIDE` + `ATTEST`, all six gates, structured outcomes) that MUST validate cleanly against `../schemas/ProtocolVersion.schema.json`. Its embedded `governed_context` is a **GovernedContextDescriptor** — a description of what class of matters the protocol governs — and carries no runtime members and no hash fields. |
| `baseline_governed_context.json` | The sample **runtime** GovernedContext used by context cases. It pins `protocol_version_id` AND `protocol_version_hash` — the latter is the REAL canonical hash of `baseline.json`, verified by the runner (control C00). |
| `baseline_receipt.json` | A minimal Receipt that MUST validate cleanly against `../schemas/Receipt.schema.json`. Its `protocol_version_hash` is the REAL canonical hash of `baseline.json`, and its `receipt_hash` is the REAL ADR-003 preimage hash (canonical receipt bytes minus the `receipt_hash` member); the runner recomputes and verifies both (control R00). |
| `baseline_conformance.json` | A minimal ConformanceDeclaration with an explicit `claim_subject_type`; control D00 validates it against `ConformanceDeclaration.schema.json`. |
| `mutations.json` | The expectations manifest: cases M01–M24, each either a set of JSON-pointer operations applied to a deep copy of a baseline with the expected verdict, or a runner self-test probe. |
| `run_mutations.py` | The runner. Exit status 0 if and only if every expectation (including baseline validity and the baseline hash bindings) is met. |

There is no placeholder-hash convention anywhere in this suite: the
ProtocolVersion contains no hash of itself (its embedded governed context is a
descriptor, not a runtime object), and every hash the baseline files do carry
is real and recomputed by the runner. If `baseline.json` is edited, the suite
fails until the pinned hashes in `baseline_receipt.json` and
`baseline_governed_context.json` are recomputed.

## Running

```sh
python3 04-reference/mutations/run_mutations.py
```

Requirements: Python 3.9+ with `jsonschema >= 4.18` (for the Draft 2020-12
`referencing` registry). Optional: `rfc8785` (used automatically when
installed), `rfc3339-validator` (jsonschema's native date-time checker; the
runner registers a fallback checker when it is absent, so date-time formats
are always enforced).

For package-level attacks — semantic tampering with legitimately recomputed
hashes against the worked example's full verification pipeline — run the
companion attack runner: `python3 08-examples/permit-core-l2/attacks.py`
(exit 0 = the untampered package verifies AND every attack is caught).

## Expectation vocabulary

- **`schema_reject`** — JSON Schema validation alone (Draft 2020-12,
  format-checked) MUST produce at least one error for the mutant. These cases
  prove that a structural protection lives in the schemas themselves.
- **`schema_accept_rule_covers`** — the schemas accept the mutant by design
  (the defect is a cross-field consistency property JSON Schema cannot express
  locally); the named rule in `../rules/catalog.json` is the normative
  protection, and the runner verifies the rule exists in the catalog.
- **`guard_trip`** — runner self-test: the runner's own JCS guard MUST reject
  the case's probe object before hashing anything (no schema involved).

## The cases

- **M01–M12** — structural and semantic regressions: empty gates; junk `binding_effect_basis`; task_owner-only
  authority; missing `recourse_state`; adverse-flag inconsistency (covered by
  rule `ADVERSE_FLAG_OUTCOME_CONSISTENCY`); deployment keys in the evidence
  gate; deleted `governed_context`; an invented seventh gate; prose
  dependencies; bare-string outcomes; invalid `binding_force`; mixed
  `binding_force` with one component.
- **M13–M18** — the commitment-type restoration (ADR-008) and extension
  boundary sealing: `commitment_type` stripped from every CommitmentPoint;
  `GENERIC` leaking into a canonical artifact; `EXTENSION` without its
  declaration; a declaration without `fallback_semantics`; a fully declared
  EXTENSION-typed CommitmentPoint inside a `Core-L2` artifact (class
  coupling); a core-typed CommitmentPoint carrying a
  `commitment_type_extension` (bidirectional sealing). M15 and M16 raise
  `conformance_class` to `Extended-L2` inside the mutation so that each case
  is rejected by exactly the constraint it targets, not by class coupling.
- **M19** — version identity: a Receipt missing the REQUIRED
  `protocol_version_hash`.
- **M20–M23** — audit regressions: a fully
  declared EXTENSION CommitmentPoint with `conformance_class` omitted (the
  reverse conditional makes omission a schema
  rejection, not a bypass); the JCS-guard self-test (non-ASCII member name
  MUST trip the guard); `encoding_depth` L1 declared alongside
  `conformance_class` Core-L3 (class-depth coupling); and an embedded
  `governed_context` descriptor carrying runtime members
  (`protocol_version_hash` / `current_time` — descriptor prohibition).
- **M24** — conformance applicability: removing `claim_subject_type` is a
  schema rejection, so a harness never has to infer the subject profile from
  a descriptive name.

## Version identity

`protocol_version_hash` is `"sha256:<64 lowercase hex>"` over the RFC 8785
(JCS) canonical bytes of the complete ProtocolVersion JSON object. The
ProtocolVersion object contains no hash of itself — its embedded
`governed_context` is a GovernedContextDescriptor with no runtime members
(enforced by the schema; probed by M23) — so the preimage is
non-self-referential with no placeholder convention. Runtime binding lives in
the artifacts that reference the ProtocolVersion: the baseline Receipt and the
baseline runtime GovernedContext each pin the REAL canonical hash of
`baseline.json`, and the runner recomputes and verifies both bindings as
positive controls (mirroring catalog rules
`RECEIPT_PROTOCOL_VERSION_HASH_MATCH` and
`GOVERNED_CONTEXT_PROTOCOL_VERSION_HASH_MATCH`). Whether such hashes match at
runtime across arbitrary artifacts is those rules' job; this suite proves the
format-level binding end-to-end against the shipped baselines.

## Canonicalization and number discipline (ADR-002)

Compact, key-sorted `json.dumps` output is JCS-equivalent **only** under TWO
preconditions, both asserted by the runner before anything is hashed
(`assert_jcs_preconditions`), failing closed on violation:

1. the document contains **no JSON numbers** anywhere (booleans excluded) —
   conforming ICSL artifacts encode all quantities as strings; and
2. **all member names (object keys) are ASCII** — RFC 8785 sorts object
   members by UTF-16 code units while Python sorts by code points, and the
   orderings diverge for member names containing non-BMP characters
   (member-name ordering is the only divergence risk once numbers are
   excluded; values may be any Unicode).

Case M21 self-tests the guard: an object with a non-ASCII member name MUST be
rejected before hashing. When a real RFC 8785 implementation (`rfc8785`) is
installed the runner uses it instead of the guarded approximation, and still
asserts both preconditions because canonical ICSL artifacts must satisfy them
either way (canonicalization profile, `../canonicalization/README.md`). The
guarded approximation is NOT a general JCS implementation. Independent
verifiers MUST implement the same discipline. The runner also rejects manifest
file references that are absolute paths or contain `..` segments.

## What this suite does and does not prove

**Does prove:** that each named structural protection is enforced by the
published schemas (or, for `schema_accept_rule_covers` cases, that the
covering catalog rule exists), against known-valid baselines whose hash
bindings are recomputed and verified, reproducibly, with format checking on;
and that the runner's own JCS guard fails closed (M21).

**Does not prove:** rule-level (catalog) enforcement beyond rule existence —
that is the conformance suite's job (`../conformance-suite.md`); receipt-chain
hashing and hash-match verification across a full package (proof-package
`verify.py` and its attack runner `08-examples/permit-core-l2/attacks.py`);
acts-on target membership and other runtime relationship checks
(`ACTS_ON_TARGET_MEMBERSHIP`); canonicalization interoperability across
implementations (interop vectors are a pre-public-v0.1 gate, see STATUS.md);
or anything about the institutional fidelity of an encoding. A green run means
"the schemas still catch what they caught," nothing more.
