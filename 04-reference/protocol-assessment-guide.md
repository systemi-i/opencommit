# ICSL Protocol Assessment Guide

## Purpose

This guide defines a repeatable method for assessing a real institutional protocol against the ICSL v0.1 candidate. It is intended for human reviewers, protocol encoders, corpus teams, and AI-assisted review systems.

An assessment must answer three different questions:

1. **Source fidelity:** Does the assessment or encoding accurately reflect the authoritative institutional sources?
2. **ICSL representability:** Can the governed process and its commitment-bearing acts be expressed faithfully using the ICSL model?
3. **Candidate conformance:** If an ICSL artifact exists, does it satisfy the requirements of its declared conformance class?

These questions must not be collapsed into a single intuitive judgment. A schema-valid artifact may misrepresent its source. A well-understood procedure may not yet have an ICSL encoding. A source may expose a genuine limitation in the candidate model.

This guide supports structured candidate assessment. It does not provide legal certification, determine that an institutional act is lawful, or replace review by people competent in the relevant jurisdiction and domain.

## 1. Required Inputs

An assessment should begin only when the following inputs have been identified:

- the protocol, procedure, or governed process to be assessed;
- the institution or institutional boundary responsible for it;
- its jurisdiction and relevant dates;
- authoritative sources and their versions;
- the intended ICSL version, normally `0.1`;
- the target encoding depth and conformance class, normally `Core-L2` for a substantive protocol review;
- any existing ICSL ProtocolVersion, package, receipts, or related artifacts;
- the assessment date, assessor identity, and tools used.

If no encoded artifact exists, the work is a **source and representability assessment**, not a conformance test. The assessor may prepare a proposed encoding, but must label it as a derived artifact rather than an official institutional publication.

## 2. Authority and Reference Order

Two different authority hierarchies apply.

### Institutional source authority

For claims about the real protocol, prefer sources in this order unless the jurisdiction establishes a different hierarchy:

1. constitutions, statutes, regulations, court orders, and other binding legal instruments;
2. formally adopted administrative rules, delegations, and official procedure instruments;
3. official service manuals, forms, registers, notices, and published guidance;
4. authoritative system specifications and operating procedures;
5. documented institutional practice and interviews;
6. secondary descriptions.

Every material claim should cite a source location. Search results, snippets, summaries, and model-generated text are discovery aids, not authoritative sources.

When sources conflict, the assessor must record the conflict. It must not silently choose the interpretation that makes the encoding easier.

### ICSL authority

For claims about ICSL, use:

1. the [ICSL v0.1 Candidate Specification](../03-specification/icsl-v0.1-candidate-spec.md);
2. the [Conformance Profile](../03-specification/conformance-profile.md);
3. the [reference schemas](schemas/README.md) and [machine-readable rule catalog](rules/catalog.json);
4. the [Package Format](../03-specification/package-format.md), where a package is assessed;
5. the [Implementation Guide](../03-specification/implementation-guide.md);
6. worked examples and explanatory pages.

The specification and conformance profile state normative requirements. Schemas and catalog rules make many of those requirements testable. Guides and examples are informative. If these materials disagree, report a standards inconsistency rather than resolving it silently.

## 3. Assessment Modes

### Mode A: Source protocol assessment

Use this mode when the input is legislation, policy, manuals, forms, diagrams, service descriptions, or operational documentation, but no ICSL artifact exists.

The output states whether the process is sufficiently documented for ICSL encoding, proposes its commitment-bearing structure, and identifies source gaps or model pressure. It cannot make a conformance claim.

### Mode B: Encoding fidelity review

Use this mode when both authoritative sources and an ICSL encoding exist.

The output compares every material encoded claim with its source, identifies omitted or invented semantics, and states whether the encoding represents the protocol faithfully.

### Mode C: Candidate conformance review

Use this mode when an ICSL artifact or package exists.

The output validates structure, class requirements, cross-object semantics, references, canonicalization, identities, and package integrity. A conformance review does not establish source fidelity unless Mode B is also performed.

A complete protocol assessment normally combines all three modes.

## 4. Ordered Assessment Procedure

### Step 1: Establish scope and provenance

Identify the named protocol, responsible institution, governed-context class, jurisdiction, temporal scope, source versions, and intended assessment boundary. Record excluded subprocesses and explain why they are outside scope.

Create a source register containing, at minimum:

- source identifier and title;
- issuing authority;
- publication and effective dates, where known;
- source type and authority level;
- stable location or file reference;
- sections relevant to the protocol;
- access date;
- known supersession, amendment, or authenticity concerns.

Do not begin detailed encoding from a single service-summary page when more authoritative sources govern the procedure.

### Step 2: Reconstruct the governed process

Describe the process in institutional terms before translating it into ICSL. Identify:

- the matter or case being governed;
- entry and terminal conditions;
- responsible and participating institutions;
- consequential determinations, attestations, delegations, remedies, overrides, appeals, protocol changes, and closure acts;
- dependencies among those acts;
- deadlines, lapse rules, and operation-of-law effects;
- adverse outcomes and available recourse;
- external standards, systems, and evidence sources.

Keep ordinary workflow activity visible during analysis, but do not assume every activity is a CommitmentPoint.

### Step 3: Identify CommitmentPoints

Apply the inclusion rule in specification section 3.5. A stage is a CommitmentPoint only when it records an institutional act that creates, denies, certifies, modifies, delegates, remedies, appeals, supersedes, or closes a reliance-worthy institutional effect.

For every candidate stage, record:

- inclusion decision: include, exclude, or uncertain;
- institutional effect, if included;
- who or what may rely on that effect;
- source citation;
- reason for exclusion, if excluded;
- uncertainty or missing evidence.

Do not promote submissions, assignments, drafts, queue changes, notifications, recommendations, or internal reasoning into CommitmentPoints unless they independently satisfy the inclusion rule.

Perform a coverage check after identification: every consequential effect found in Step 2 must be represented by a CommitmentPoint or explicitly recorded as an unresolved omission.

### Step 4: Apply atomicity and classify each act

Split a stage when it performs more than one institutional act. Where a legally indivisible instrument has multiple effects, apply the specification's atomicity rule and explain the primary classification from the recourse perspective.

Classify each CommitmentPoint using the ordered procedure in specification section 3.5a, not keyword matching or intuition:

1. `EVOLVE`
2. `DELEGATE`
3. `APPEAL`
4. `REMEDY`
5. `OVERRIDE`
6. `CLOSE`
7. `DECIDE`
8. `ATTEST`
9. `EXTENSION`, only where the Extended-L2 requirements are satisfied

Apply the APPEAL/DECIDE, REMEDY/OVERRIDE, and DECIDE/ATTEST boundary tests explicitly. A request for appeal is not automatically an `APPEAL`; the core type applies to disposition of the challenge on its merits.

The type is classificatory. Never derive authority, binding force, outcomes, recourse, or automation permissions from it.

### Step 5: Specify each CommitmentPoint

For every included CommitmentPoint, assess or encode:

- stable identifier and name;
- `commitment_type` and any permitted subtype or extension declaration;
- trigger and trigger condition;
- allowed outcomes, including `effect_class`;
- `adverse_outcome_possible` consistency;
- binding-effect basis and binding force;
- Authority gate;
- Evidence gate;
- Reasoning gate;
- Dependency gate;
- Version gate;
- Recourse gate;
- notice and reason-giving expectations for adverse or mixed outcomes;
- legal basis for unavailable or inapplicable recourse where required;
- relevant normative references.

For each populated field, identify its source. Use an explicit gap or uncertainty marker where the source is silent. Do not invent a deadline, authority, evidentiary rule, legal basis, or recourse path to make the artifact validate.

### Step 6: Assess protocol composition

Check the protocol as a system rather than as a list of isolated CommitmentPoints:

- all dependencies resolve;
- temporal and external triggers are evaluable;
- allowed outcomes connect coherently to later dependencies;
- appeal, remedy, and override targets are explicit and permitted;
- delegation names its recipient and bounded scope;
- evolution identifies the protocol or version being changed;
- closure corresponds to a terminal transition;
- later acts can resolve the status of earlier Commitments without rewriting history;
- the protocol covers meaningful entry, progression, recourse, and termination conditions.

ICSL may express the process end to end in institutional terms without reproducing every task or system operation.

### Step 7: Check layer boundaries

Separate canonical institutional truth from runtime and deployment concerns.

The canonical ProtocolVersion must not depend on workflow routing, database identifiers, UI state, vendor configuration, prompt text, model choice, or other deployment bindings. Those elements may implement or support the protocol, but they must not silently alter gate outcomes or institutional semantics.

Check that:

- the ProtocolVersion contains a GovernedContextDescriptor, not runtime case data;
- runtime GovernedContexts pin the exact ProtocolVersion;
- personal data is not embedded in canonical receipt content;
- renderings add no semantics;
- AI assistance does not become accepted evidence or authority without the required institutional act and delegation basis;
- unknown required semantics fail closed at the claimed class.

### Step 8: Validate structure and rules

Validate each artifact against the applicable Draft 2020-12 schema. Resolve schema references correctly and use format checking. Schema success is necessary but not sufficient.

Then evaluate every rule in `04-reference/rules/catalog.json` for which both the declared
class includes `scope` and the declaration's `claim_subject_type` appears in
`applicability.direct_claim_subject_types`. Check the stated `evaluation_target` and
`artifact_condition`. Record each diagnostic with:

- rule identifier;
- severity;
- artifact and JSON Pointer path;
- observed condition;
- normative basis;
- source citation, where relevant;
- proposed correction or required decision.

Do not reduce an `error` to a warning. Do not present authoring heuristics as conformance
rules. Record a rule as `not_applicable` when the subject-type or artifact condition does
not select it. Use `not_assessed` only when an applicable requirement could not be
evaluated, and explain why.

### Step 9: Validate package and identity, where applicable

For a package, additionally check:

- manifest completeness and path safety;
- conformance declaration completeness;
- immutable ProtocolVersion identity;
- RFC 8785 canonicalization requirements;
- source and canonical hashes;
- hash-vector completeness;
- receipt content and hash chains;
- receipt-to-ProtocolVersion hash matches;
- governed-context version pinning;
- `acts_on` target resolution and target membership;
- extension negotiation and fallback behavior.

The worked permit verifier validates only its own synthetic package. Passing that verifier does not validate another protocol.

### Step 10: Run an adversarial review

Attempt to falsify the encoding and assessment. At minimum, ask:

- Was a consequential act omitted because it looked like a workflow step?
- Was a multi-act instrument forced into one CommitmentPoint?
- Was authority confused with task ownership or software permission?
- Was an adverse outcome encoded without real recourse, notice, or reasons?
- Was missing source information converted into a confident value?
- Could a receipt be retargeted to an unrelated prior act?
- Could runtime configuration change canonical meaning?
- Could a protocol or version be swapped without invalidating its receipts?
- Does an AI-produced fact or recommendation cross the commitment boundary silently?
- Does the encoding describe published rules while ignoring contradictory institutional practice?

Record attacks attempted and their results. An untested assumption must not be described as verified.

## 5. Finding Categories

Use the following categories consistently:

- `SOURCE_GAP`: an authoritative source does not provide information required for faithful encoding.
- `SOURCE_CONFLICT`: relevant sources give materially inconsistent instructions.
- `SCOPE_ERROR`: the protocol or governed-context boundary is incorrect or unexplained.
- `OMITTED_COMMITMENT`: a consequential institutional act is absent.
- `ATOMICITY_ERROR`: multiple institutional acts are improperly combined.
- `CLASSIFICATION_ERROR`: a CommitmentPoint does not follow the ordered taxonomy or boundary tests.
- `ENCODING_DEFECT`: the ICSL artifact misstates or invents source semantics.
- `CONFORMANCE_ERROR`: a normative candidate requirement is violated.
- `CONFORMANCE_WARNING`: a normative recommendation is not satisfied.
- `MODEL_PRESSURE`: the source cannot be represented faithfully without an extension or candidate-model change.
- `IMPLEMENTATION_LEAKAGE`: runtime or deployment details alter canonical institutional truth.
- `LEGAL_REVIEW_REQUIRED`: resolving the issue requires competent legal interpretation.
- `NOT_ASSESSED`: evidence, tooling, or scope was insufficient to perform the check.

`MODEL_PRESSURE` must be supported by a concrete source-grounded counterexample. Difficulty or inconvenience alone does not establish a defect in ICSL.

## 6. Assessment Results

Report each axis independently.

### Source fidelity result

- `supported`: all material encoded claims are source-supported and no consequential source rule is knowingly omitted;
- `supported_with_gaps`: the encoding is substantially supported but named source gaps or unresolved interpretations remain;
- `not_supported`: material claims are invented, contradicted, or omitted;
- `not_assessable`: authoritative sources were unavailable or insufficient.

### Representability result

- `represented`: the governed process and identified consequential acts are expressible in the selected ICSL class;
- `partially_represented`: material parts remain unresolved or unencoded;
- `model_pressure`: at least one source-grounded requirement cannot be represented faithfully within the selected class;
- `not_assessable`: process reconstruction is insufficient.

### Candidate conformance result

- `pass`: every applicable requirement was assessed, no error diagnostic remains, and all package checks in scope passed; warning diagnostics, if any, are reported separately;
- `fail`: at least one error diagnostic remains;
- `not_run`: no encoded artifact was supplied or validation was not performed;
- `partial`: validation was performed, but one or more required checks could not be completed.

Any result must identify the claim subject identity, claim subject type, ICSL version,
conformance class, encoding depth where applicable, assessment method or tool version,
date, and limitations. Do not use an unqualified phrase such as “ICSL compliant.”
Candidate assessment is not certification.

## 7. Required Report Structure

Every assessment report should contain:

1. executive determination;
2. protocol identity and scope;
3. assessment modes and target class;
4. source register and source-quality assessment;
5. reconstructed process summary;
6. CommitmentPoint inventory and coverage matrix;
7. per-CommitmentPoint assessment;
8. protocol-level composition and lifecycle assessment;
9. schema and rule diagnostics;
10. adversarial checks;
11. separate source-fidelity, representability, and candidate-conformance results;
12. unresolved questions and required reviewers;
13. proposed corrections, clearly separated from the assessed artifact;
14. machine-readable summary where required.

The report must make it possible for another reviewer to reproduce the reasoning from source to finding. A conclusion without citations, field-level evidence, and applied rule identifiers is not a completed assessment.

## 8. Minimum Quality Bar

An assessment is complete only when:

- every source is registered and cited;
- every consequential process act is included or explicitly dispositioned;
- every CommitmentPoint passes the inclusion, atomicity, and classification checks;
- every required field is source-supported or marked as a gap;
- every applicable schema and catalog rule is evaluated;
- source fidelity and candidate conformance are reported separately;
- material uncertainties are visible;
- proposed repairs do not overwrite the original artifact;
- the final claim is qualified by version, class, method, and limitations.

This quality bar is intentionally higher than producing valid JSON. The objective is a faithful, reviewable representation of governed institutional action, not merely an artifact that passes structural checks.
