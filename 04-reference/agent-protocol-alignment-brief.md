# Agent Brief: Validate a Protocol Against ICSL v0.1

Use this document as the operating brief for an AI agent assessing a real institutional protocol or an existing ICSL encoding. Provide the agent with repository access, the protocol sources, any candidate encoding, and the requested target class.

## Assignment

Assess the supplied institutional protocol against the ICSL v0.1 candidate. Produce a source-grounded, reproducible report that separately determines:

1. whether the protocol has been understood and represented faithfully;
2. whether its governed process and commitment-bearing acts are representable in ICSL;
3. whether any supplied ICSL artifact satisfies the requirements of its declared candidate conformance class.

Do not treat these as one question. Do not describe an artifact as aligned merely because it parses or passes JSON Schema.

## Inputs

You must receive or identify:

- protocol name and responsible institution;
- jurisdiction and relevant effective date;
- authoritative source files or stable source locations;
- existing ICSL artifacts, if any;
- target ICSL version;
- claim subject identity and claim subject type;
- target conformance class and encoding depth;
- output location or delivery format.

Default to claim subject type `protocol_package`, `Core-L2`, and encoding depth `L2`
when a substantive assessment of an encoding is requested but no target is stated. State
that this is an assessment assumption. Encoding depth applies to encoded ProtocolVersions,
not to implementation subjects.

If authoritative sources are unavailable, do not infer the missing procedure from general knowledge. Return `not_assessable` for source fidelity and list the material needed to continue.

## Required ICSL Materials

Read these files before assessing the protocol:

1. `03-specification/icsl-v0.1-candidate-spec.md`
2. `03-specification/conformance-profile.md`
3. `04-reference/protocol-assessment-guide.md`
4. `04-reference/schemas/README.md` and the applicable schemas in that directory
5. `04-reference/rules/catalog.json`
6. `03-specification/package-format.md`, if a package is supplied or proposed
7. `03-specification/implementation-guide.md`

Use `08-examples/permit-core-l2/` only as an informative worked example. Do not copy its institutional content into another protocol and do not treat its verifier as a general validator.

If the specification, conformance profile, schemas, and rule catalog disagree, report a candidate-standard inconsistency. Do not silently choose one interpretation.

## Non-Negotiable Rules

- Cite an authoritative source for every material institutional claim.
- Distinguish source text, your interpretation, and encoded value.
- Never invent authority, evidence, deadlines, dependencies, legal basis, binding force, allowed outcomes, or recourse.
- Never infer semantics from a field name, workflow label, or commitment type alone.
- Never classify by keyword matching. Apply the ordered procedure and boundary tests in specification section 3.5a.
- Never treat task ownership, system permissions, or AI capability as institutional authority.
- Never treat a recommendation, draft, notification, submission, or queue transition as a CommitmentPoint unless it independently creates a reliance-worthy institutional effect.
- Never alter the assessed source or artifact silently. Put proposed corrections in a separate file or clearly marked section.
- Never claim legal validity, certification, or unqualified “ICSL compliance.”
- Never use search snippets, generated summaries, or the worked example as authority for the real protocol.
- Mark uncertainty explicitly. Unknown required semantics must not pass silently.

## Procedure

### 1. Register and rank sources

Create a source register recording title, issuer, date, authority level, version, relevant sections, location, access date, and known amendments. Prefer primary and formally adopted sources. Record conflicts and missing instruments.

### 2. Define the protocol boundary

State the responsible institution, governed-context class, entry and terminal conditions, jurisdictions, participating bodies, and exclusions. Explain whether the material describes one protocol, a family of protocols, or only public-facing service information.

### 3. Reconstruct the process before encoding

Produce a concise process map covering consequential acts, dependencies, timing, lapse, operation-of-law effects, adverse outcomes, recourse, external evidence, and institutional handoffs. Preserve operational steps for context but distinguish them from institutional acts.

### 4. Build a CommitmentPoint candidate table

For every candidate stage, report:

| Field | Required content |
| --- | --- |
| Stage | Source label or event |
| Inclusion | include / exclude / uncertain |
| Effect | Reliance-worthy institutional effect, if any |
| Reliance | Who or what may rely on it |
| Source | Precise citation |
| Rationale | Inclusion or exclusion reasoning |
| Confidence | high / medium / low |

After completing the table, verify that every consequential effect in the process map is represented or reported as an omission.

### 5. Apply atomicity and classification

Split stages containing multiple institutional acts. Then apply the ordered first-match procedure:

`EVOLVE -> DELEGATE -> APPEAL -> REMEDY -> OVERRIDE -> CLOSE -> DECIDE -> ATTEST -> EXTENSION`

Document the matched test and any relevant boundary test. In particular:

- an appeal filing is not the same as the merits disposition of an appeal;
- correction of a defect is not the same as displacement of a valid act under superseding authority;
- characterization of a proposition is not the same as determination of a right, obligation, permission, procedural course, or status.

### 6. Review every CommitmentPoint

For each CommitmentPoint, report source support and assessment for:

- identifier and atomic act;
- commitment type;
- trigger and trigger condition;
- allowed outcomes and effect classes;
- adverse-outcome flag;
- binding-effect basis and binding force;
- Authority, Evidence, Reasoning, Dependency, Version, and Recourse gates;
- notice and reason-giving requirements;
- normative references;
- permitted target relationships, evolution target, or delegation scope where relevant;
- unresolved source gaps.

Use a field-level matrix. A value is `supported` only when a citation directly supports it. Mark `interpreted`, `conflicted`, `missing`, or `not_applicable` where appropriate.

### 7. Review protocol composition and lifecycle

Check entry, progression, dependencies, temporal behavior, allowed-outcome transitions, recourse, act-on relationships, delegation, evolution, and closure. Confirm that the protocol expresses the governed process end to end in institutional terms even when ordinary workflow steps remain outside ICSL.

### 8. Review boundaries

Check canonical/runtime separation, ProtocolVersion and GovernedContext separation, version pinning, personal-data boundaries, rendering behavior, AI assistance, delegated authority, and external evidence. Report any runtime configuration that changes canonical meaning as `IMPLEMENTATION_LEAKAGE`.

### 9. Run structural and semantic validation

If an encoding exists:

1. validate each artifact against its applicable Draft 2020-12 schema with reference resolution and format checking;
2. evaluate catalog rules only when the declared class includes the rule's `scope` and
   the declared `claim_subject_type` is listed in
   `applicability.direct_claim_subject_types`;
3. validate all references and dependencies;
4. for packages, validate manifest safety and completeness, conformance declaration, RFC 8785 canonicalization, dual hashes, hash vector, ProtocolVersion identity, receipts, chains, version matches, and target membership;
5. record rules outside the selected subject or artifact condition as `NOT_APPLICABLE`,
   and applicable checks that could not be performed as `NOT_ASSESSED`.

Schema success alone must never produce a passing overall result.

### 10. Attack the result

Try to disprove the assessment by testing for omitted consequential acts, false authority, invented source semantics, missing adverse recourse, incorrect act classification, combined acts, unrelated receipt targets, protocol substitution, runtime leakage, and silent AI elevation.

List each attack, expected protection, observed result, and finding raised.

## Finding Format

Use one record per finding:

```markdown
### [P1] Short finding title

- Category: SOURCE_GAP | SOURCE_CONFLICT | SCOPE_ERROR | OMITTED_COMMITMENT |
  ATOMICITY_ERROR | CLASSIFICATION_ERROR | ENCODING_DEFECT |
  CONFORMANCE_ERROR | CONFORMANCE_WARNING | MODEL_PRESSURE |
  IMPLEMENTATION_LEAKAGE | LEGAL_REVIEW_REQUIRED | NOT_ASSESSED
- ICSL rule: rule id or specification section
- Artifact path: file and JSON Pointer, if applicable
- Source: precise citation
- Observation: what was found
- Consequence: why it matters
- Required action: correction, source request, institutional decision, or model issue
- Confidence: high | medium | low
```

Use priorities as follows:

- `P0`: the assessment or artifact could authorize or represent materially harmful action incorrectly;
- `P1`: a required institutional semantic or candidate-conformance requirement is missing or wrong;
- `P2`: a material recommendation, ambiguity, or review gap remains;
- `P3`: editorial or non-substantive improvement.

## Required Final Report

Produce the report in this order:

### 1. Executive determination

State the three results separately:

| Axis | Allowed result |
| --- | --- |
| Source fidelity | supported / supported_with_gaps / not_supported / not_assessable |
| ICSL representability | represented / partially_represented / model_pressure / not_assessable |
| Candidate conformance | pass / fail / not_run / partial |

Identify the claim subject, claim subject type, ICSL version, target class, encoding depth
where applicable, assessment date, assessor or agent version, and principal limitations.

### 2. Findings

List findings first, ordered by priority and then by protocol sequence. Do not bury an error in narrative summary.

### 3. Source register

Include source authority, versions, citations, conflicts, and missing materials.

### 4. Process and CommitmentPoint coverage

Include the process map, candidate table, final CommitmentPoint inventory, exclusions, atomicity decisions, classifications, and coverage gaps.

### 5. Field-level fidelity matrix

Show whether each material ICSL field is supported, interpreted, conflicted, missing, or not applicable, with citations.

### 6. Conformance results

List schema results, all applicable catalog diagnostics, package checks, tests not run, and tool versions.

### 7. Adversarial review

List the attempted attacks and whether the expected protections held.

### 8. Required decisions and repairs

Separate source requests, institutional decisions, encoding repairs, implementation changes, and proposed ICSL changes. Do not modify the original artifact as part of the assessment.

### 9. Machine-readable summary

End with:

```json
{
  "assessment_subject": "",
  "claim_subject_type": "protocol_package",
  "institution": "",
  "jurisdiction": "",
  "icsl_version": "0.1",
  "target_class": "Core-L2",
  "encoding_depth": "L2",
  "source_fidelity": "",
  "representability": "",
  "candidate_conformance": "",
  "errors": 0,
  "warnings": 0,
  "not_assessed": 0,
  "model_pressure_findings": 0,
  "assessment_date": "",
  "assessor": "",
  "limitations": []
}
```

## Completion Test

Before reporting completion, confirm that:

- every consequential act was included or explicitly dispositioned;
- every encoded institutional claim has a source citation;
- all six gates and required CommitmentPoint semantics were reviewed;
- the ordered taxonomy and boundary tests were applied;
- every applicable schema and catalog rule was assessed;
- source fidelity was not inferred from conformance;
- missing information was not invented;
- proposed repairs are separate from the assessed artifact;
- the final result is qualified by version, class, method, and limitations.

If any item is false, the candidate conformance result is `partial` and must say why.
