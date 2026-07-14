# The Six Gates

Every CommitmentPoint declares six gates. Together they state the conditions that must be satisfied before an attempted act can be accepted as a Commitment.

1. **Authority** identifies the legal or institutional basis on which the actor may act. Task ownership alone is insufficient.
2. **Evidence** identifies the durable facts, records, or inputs required for the act.
3. **Reasoning** states how the institution applies rules, calculations, professional judgment, or discretion to the evidence.
4. **Dependency** identifies earlier commitments, external conditions, or temporal requirements that must hold.
5. **Version** pins the ProtocolVersion governing the act.
6. **Recourse** states the available route of review, appeal, grievance, correction, or challenge, including an explicit basis where recourse does not apply.

## Gates Are Institutional Claims

The gates do not prove that an institution acted lawfully. They make the institution's claim about validity explicit and testable. A validator can determine that a required authority field is missing or that an adverse outcome lacks a recourse declaration; it cannot determine that the cited official truly held authority under all applicable law.

The model also does not require every rule to be deterministic. Where law or policy confers discretion, the Reasoning gate must represent discretion rather than disguise it as a mechanical rule. ICSL aims to make the location and exercise of judgment visible, not eliminate it.

## Attempted and Accepted Acts

An implementation evaluates an attempted act against all six gates and the allowed outcomes declared by the CommitmentPoint. If the requirements are satisfied and the responsible authority accepts the act, the runtime produces a Receipt. If the attempt is blocked or rejected, it produces an EvaluationRecord rather than a Receipt.

This distinction prevents software completion from being mistaken for institutional acceptance.

## AI and Gate Truth

AI may help collect evidence, explain requirements, summarize material, draft reasons, or recommend routing. Its output does not become authoritative merely because a system generated it. Candidate facts must be accepted through the relevant institutional process, and any delegated automated authority must have an explicit basis and recourse.

The normative requirements are in [Section 8 of the candidate specification](../03-specification/icsl-v0.1-candidate-spec.md#8-ai-boundary).
