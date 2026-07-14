# What Is ICSL?

The Institutional Commitment Specification Language (ICSL) is an open specification language for institutional protocols: governed processes composed of commitment-bearing acts. It expresses both the structure of those processes and the actions through which they produce institutional effects in a precise, machine-readable form.

Public institutions already use workflows, registries, rules engines, case systems, and data standards. These systems can move work and information without fully representing the institutional acts that give a process meaning: a determination of eligibility, acceptance of evidence, grant of a permit, disposition of an appeal, delegation of authority, or correction of an earlier decision.

ICSL provides a common way to express the governed process, identify its consequential acts, state the conditions under which they may count, and record their accepted instances without confusing operational activity with institutional authority.

## The Model in Brief

An ICSL **Protocol** is a named governed process. Each immutable **ProtocolVersion** describes the institution responsible for the protocol, the class of matters it governs, and the CommitmentPoints through which institutional action may occur.

A **CommitmentPoint** is the template for one atomic institutional act. It identifies the act type, trigger, permitted outcomes, binding-effect basis, and six gates that govern acceptance:

- Authority
- Evidence
- Reasoning
- Dependency
- Version
- Recourse

When an act is accepted at a CommitmentPoint in a particular case, it becomes a **Commitment**. A **Receipt** records that Commitment and pins it to the exact ProtocolVersion under which it was produced.

The distinction between template, instance, and record is important. A CommitmentPoint does not bind merely because it has been published. A receipt does not prove legality merely because it validates. ICSL makes the institution's claim explicit and testable; the relevant legal and institutional sources remain authoritative.

## What ICSL Adds

A workflow shows how tasks move. A rules engine evaluates conditions. A registry stores records. ICSL describes what the institution is committing itself to do through those systems, under whose authority, on what basis, with what effect, and subject to what challenge.

This creates a stable institutional specification outside any particular implementation. It can support process design, audit, technology procurement, migration between systems, safer automation, and coordination across organizations.

ICSL does not require institutions to use the same laws, policies, or software. It provides common semantics through which different protocols and institutional actions can be interpreted and compared while local authority remains local.

## What ICSL Is Not

ICSL is not a workflow engine, case-management product, legal reasoning system, universal policy model, or execution platform. It does not authenticate evidence, establish legal authority, or make AI-generated outputs binding by default.

It is a specification layer for the commitment-bearing structure that those systems must implement and respect.

## Current Status

ICSL v0.1 is a consultation candidate published for external review. The conceptual model is frozen, but production interoperability has not yet been demonstrated. The current release is intended for review, experimental implementation, conformance development, and carefully scoped pilots.

OpenCommit is the initiative developing and stewarding ICSL. This GitBook documents the standard; references to OpenCommit concern its stewardship, governance, and public development process.
