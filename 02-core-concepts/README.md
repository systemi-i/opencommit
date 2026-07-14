# Core Concepts

ICSL is a specification language for institutional protocols: governed processes composed of commitment-bearing acts. It expresses the structure of a process, identifies the points at which that process can produce an institutional effect, and records each accepted act in a form another system can inspect.

- A **ProtocolVersion** is an immutable publication of a governed process.
- A **CommitmentPoint** defines one kind of reliance-worthy institutional act within that process.
- The **six gates** define the conditions under which the act may be accepted.
- A **Commitment** is the act accepted at a CommitmentPoint in a particular governed context.
- A **Receipt** is the durable record of that Commitment and its place in the protocol's history.
- **Conformance classes** state which parts of the candidate standard an artifact or implementation supports.

These distinctions prevent several common errors. A workflow step is not automatically an institutional act. A completed software task is not evidence that the actor had authority. A receipt is not proof of legality. An AI recommendation is not a decision unless an institution has lawfully made it one.

The following pages explain the concepts informatively. The [candidate specification](../03-specification/icsl-v0.1-candidate-spec.md) remains authoritative where the two differ.
