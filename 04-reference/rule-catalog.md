# Rule Catalog

The rule catalog assigns stable identifiers, severities, and minimum conformance classes to validation diagnostics. It complements JSON Schema: schemas enforce local structure, while catalog rules also cover relationships, reference resolution, lifecycle behavior, package consistency, and claims that require more than one object to evaluate.

The machine-readable catalog is [available as JSON](rules/catalog.json).

## Conventions

A rule grounded in a normative `MUST` has severity `error`. A rule grounded in `SHOULD` has severity `warning`. Informative guidance is not represented as a validation rule.

The `scope` field identifies the minimum conformance class at which a rule is evaluated. Higher Core classes inherit lower-class requirements: `Core-L1` is contained by `Core-L2`, which is contained by `Core-L3`. `Extended-L2` adds extension negotiation to `Core-L2`; `Corpus-L3` adds provenance requirements to `Core-L3`.

`scope` is not a complete applicability test. Every rule also carries an
`applicability` object:

- `evaluation_target` identifies the artifact or behavior evaluated;
- `direct_claim_subject_types` lists the subject types to which the rule applies directly;
- `artifact_condition` states whether the target is required or evaluated only when
  present or claimed.

A validator selects a rule only when the claimed class includes the rule's `scope` and
the declaration's `claim_subject_type` appears in
`direct_claim_subject_types`. A package rule therefore does not directly apply to a
parser or renderer claim. An implementation suite may use an artifact-facing rule as the
expected result for a fixture, but that is fixture-oracle use rather than direct
applicability.

## Coverage

The 74-rule catalog currently covers:

- required protocol, institution, governed-context, and CommitmentPoint structure;
- commitment types, extension declarations, and class coupling;
- the six gates and their minimum contents;
- authority, delegation, discretion, AI assistance, and shadow binding;
- binding-effect basis, binding force, outcomes, notice, reasons, and recourse;
- dependencies, triggers, current time, and operation-of-law behavior;
- act relationships, target membership, lifecycle, and derived status;
- ProtocolVersion, GovernedContext, and Receipt identity;
- receipt content, hash chains, and personal-data boundaries;
- canonicalization, hash format, package manifests, and dual hash vectors;
- references, renderings, runtime bindings, and extension behavior;
- encoding provenance, publisher relationships, and governance addenda;
- conformance declarations and encoding-depth consistency.

## Relationship to Implementations

The catalog is normative where the candidate specification explicitly grounds a rule. Implementations may emit additional diagnostics, but they should not reuse an ICSL identifier for different behavior or reduce the severity of a normative error.

The catalog remains candidate-stage. Proposed changes should identify the normative clause, explain the implementation consequence, and include a fixture or mutation where practical.
