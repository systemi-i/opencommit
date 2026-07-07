# ICSL Package Format Candidate

Status: candidate draft.  
Date: 2026-07-07.

## 1. Purpose

The ICSL package format gives protocol artifacts, conformance declarations, references,
hash vectors, receipts, renderings, and optional execution bindings a stable envelope.

The package format must preserve the central invariant: canonical protocol truth must be
separable from runtime bindings, credentials, interfaces, and deployment configuration.

## 2. Minimum Package

A minimum package contains:

- `manifest.json`
- `protocol-version.json`
- `conformance.json`
- `hashes.json`

## 3. Recommended Layout

```text
manifest.json
protocol-version.json
conformance.json
hashes.json
references/
receipts/
renderings/
extensions/
bindings/
```

Only `protocol-version.json` is canonical protocol truth in the minimum package.

## 4. Manifest

`manifest.json` MUST identify:

- package id
- ICSL version
- profile or conformance target
- package files and roles

Every file declared in the manifest MUST exist.

Suggested roles:

- `protocol-version`
- `conformance-declaration`
- `hash-vector`
- `reference`
- `receipt`
- `rendering`
- `extension`
- `execution-binding`

## 5. Hashes

`hashes.json` records file hashes.

Seed harness behavior:

- algorithm: SHA-256
- hash input: source file bytes
- hash vector covers every non-hash-vector file declared by the manifest
- `hashes.json` is not required to hash itself

Open publication decision: whether final packages must include both source-byte hashes and
canonical JSON hashes for JSON artifacts.

## 6. Conformance Declaration

`conformance.json` MUST identify:

- claim subject
- conformance class
- ICSL version
- test-suite version
- result

An implementation, protocol package, registry, corpus, or renderer MUST NOT claim unqualified
ICSL compliance.

## 7. References

`references/` MAY include laws, policies, bylaws, service rules, forms, official notices,
delegation documents, or external standards.

References SHOULD declare:

- id
- label
- source type
- locator
- version, date, or stable retrieval basis
- hash where feasible

Normative references SHOULD be versioned.

## 8. Receipts

`receipts/` MAY include examples, test vectors, or actual runtime receipt chains.

Receipt chains SHOULD include:

- receipt id
- receipt hash
- previous hash
- content hash where content is included
- created-at timestamp

## 9. Renderings

`renderings/` MAY include human-facing documentation, HTML, Markdown, PDF, diagrams, or
interface projections.

Renderings MUST NOT introduce semantics absent from canonical protocol truth.

## 10. Bindings

`bindings/` MAY include deployment-specific execution bindings.

Bindings MUST:

- remain outside canonical protocol truth
- be separately declared
- be separately hashed
- be removable without changing the ProtocolVersion hash
- have no authority to change gate outcomes

Bindings MUST NOT contain secrets in publishable packages.

## 11. Extensions

`extensions/` MAY include profile or domain-specific material.

Extensions SHOULD use explicit namespaces. A validator that does not understand an extension
MUST reject, warn, or downgrade according to the declared conformance class.
