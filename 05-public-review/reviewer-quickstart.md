# Reviewer Quickstart

This page is for reviewing the ICSL candidate itself. To assess whether a real institutional protocol or existing encoding aligns with ICSL, use the [Protocol Assessment Guide](../04-reference/protocol-assessment-guide.md) and [Agent Protocol-Alignment Brief](../04-reference/agent-protocol-alignment-brief.md).

## Reading Path

1. Read the repository [README](../README.md) and [scope statement](v0.1-scope-contract.md).
2. Read the [candidate specification](../03-specification/icsl-v0.1-candidate-spec.md), followed by the [conformance profile](../03-specification/conformance-profile.md).
3. Inspect the [reference schemas](../04-reference/schemas/README.md) and [rule catalog](../04-reference/rule-catalog.md).
4. Review the [worked permit package](../08-examples/permit-core-l2/README.md).
5. Compare unresolved questions against [Open Issues](open-issues.md).

## Run the Published Checks

From the repository root:

```sh
python3 04-reference/mutations/run_mutations.py
python3 08-examples/permit-core-l2/verify.py
python3 08-examples/permit-core-l2/attacks.py
```

The mutation runner evaluates 28 declared expectations against known-valid protocol,
receipt, governed-context, and conformance-declaration baselines. The package verifier
checks the synthetic Core-L2 example's schemas, identities, relationships, receipt chain,
and hash vector. The attack runner confirms that the control package passes and five
specified adversarial changes fail for their intended reasons.

These checks are deliberately narrower than the planned conformance suite. A green run establishes only the behavior stated by each harness.

## Reference Surface

- `04-reference/schemas/` contains twelve Draft 2020-12 schemas.
- `04-reference/rules/catalog.json` contains 74 diagnostic definitions.
- `04-reference/mutations/` contains mutation baselines, expectations, and runner.
- `08-examples/permit-core-l2/` contains the synthetic package, verifier, and attacks.
- `conformance.json` in the worked package declares `not_run` because the full suite is not yet published.

## Questions for Technical Review

- Can the existence of a CommitmentPoint be determined consistently?
- Are the eight act types and their boundary tests sufficient?
- Can another implementation reproduce ProtocolVersion and receipt hashes?
- Do target relationships prevent an appeal or remedy from acting on an unrelated receipt?
- Can extensions be processed without silent semantic loss?
- Are class and encoding-depth claims enforceable?
- Are runtime and deployment details prevented from changing canonical truth?
- Do diagnostics correspond clearly to normative requirements?
