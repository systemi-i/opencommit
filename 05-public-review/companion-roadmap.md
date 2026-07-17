# Companion Specifications and Research Roadmap

ICSL v0.1 defines the canonical semantics of governed processes and the institutional acts accepted under them. It deliberately does not absorb every concern required to operate a public service. This roadmap identifies the adjacent contracts needed to connect ICSL to execution, federation, registries, privacy controls, and institutional learning while preserving that boundary.

Placement on this roadmap is not a promise of inclusion in the core standard. A companion becomes normative only after its problem is demonstrated, its relationship to the core is explicit, and at least one independent implementation and conformance test exercise the proposed contract.

## Before Final v0.1

The following are release evidence for the existing core, not extensions to it:

- at least 25 public positive, negative, adversarial, and package-level fixtures;
- cross-language canonicalization vectors covering ProtocolVersions, Receipts, Unicode values, nested objects, control characters, empty structures, and package dual hashes;
- at least one independent validator and implementation report;
- a claim-subject applicability profile that distinguishes protocol-package validation from parser, validator, composer, registry, runtime, renderer, and corpus claims;
- explicit resolution or deferral of every open issue that could affect v0.1 interoperability.

## Priority Companion Workstreams

### Capability Binding

Define a typed, non-canonical interface between a CommitmentPoint and an operational capability. Candidate concepts include the input supplied, output contract, acceptance path, binding status, failure semantics, and the effect obligation created after acceptance. Bindings must be replaceable without changing ProtocolVersion identity and must never acquire authority to set gate truth.

### Effects and Reconciliation

Define records for external effects such as payments, notifications, registry writes, credential issuance, or capacity changes. A Commitment and an applied rail effect are not the same event. The companion should make `pending`, `applied`, `failed`, and `compensated` states observable and preserve the institutional basis for retry, compensation, or escalation.

### Cross-Protocol Composition

Define how one protocol refers to another ProtocolVersion, depends on a Commitment or Receipt issued elsewhere, verifies the other institution's claim, and handles version or availability failure. The first objective is bounded composition between two independently governed protocols, not distributed transactions across arbitrary institutions.

### References and Source Resolution

Define typed references, version resolution, content addressing where lawful and practical, source precedence, supersession, and behavior when a cited source is unavailable. The work must distinguish a resolvable technical reference from an assertion that the referenced source is authoritative or correctly interpreted.

### Semantic Authoring and Publication

Define the handoff from interpretive human or agent-assisted authoring to deterministic publication. The companion should preserve source citations, alternatives, uncertainty, review decisions, and approval provenance while ensuring that canonicalization and hashing are performed by reproducible non-probabilistic tooling.

### Protocol Amendment Evidence

Define optional amendment rationale, proposal, review, and shadow-evaluation records that connect evidence from prior operation to a new ProtocolVersion. These records must never change the terms applied to a GovernedContext already pinned to an earlier version.

### Privacy, Disclosure, and Retention

Define detachable personal-data payloads, selective disclosure, linkability analysis, residency controls, retention, rectification, erasure, and verification after erasure. Profiles should assume that receipts and protocol instances are not public by default. They must address the fact that metadata and resolvable links can disclose sensitive posture even when direct personal data is excluded from canonical content.

### Registry, Discovery, and Conformance Governance

Define immutable publication, discovery, supersession, implementation reports, test-suite governance, and the conditions for qualified conformance or certification claims. The governance model should permit multiple registries and validators while preserving reproducible identity and diagnostic behavior.

## Optional Projections

These projections may improve implementation without becoming protocol-conformance requirements:

- workflow and delivery projections for task order, queues, staffing, retries, and interfaces;
- typed preconditions and postconditions over domain state;
- scheduling and recovery profiles for temporal lapse and operation-of-law effects;
- domain and DPI rail profiles for identity, payments, registries, data exchange, credentials, health, and other established standards;
- agent-authoring records for provenance, confidence, explanation, review, and uncertainty.

## Research Questions

The following remain open until stronger institutional evidence exists:

- whether any recurrent institutional act requires an addition to the eight commitment types or the closed lifecycle-effect algebra;
- whether `commitment_subtype` needs interoperable semantics or should remain profile-defined;
- whether generalized value states for unknown, unavailable, contested, or not-yet-determined information are needed across gates and outcomes;
- whether the class and encoding-depth taxonomies should be simplified after implementation experience;
- how evidence from prior cases should support shadow evaluation and amendment proposals without changing the ProtocolVersion pinned to an existing case;
- how append-only act records interact with erasure rights when the existence or linkage of the record is itself personal data;
- how inter-encoder reliability and cross-jurisdiction comparability should be measured for a public corpus.

## Evidence Required to Advance a Workstream

A proposal should identify a real institutional failure or implementation need, show why existing ICSL objects and profiles cannot represent it adequately, define its effect on canonical identity and conformance, provide at least one working implementation, and include positive and adversarial fixtures. Proposals that introduce fields without a consuming runtime or testable behavior remain research drafts.
