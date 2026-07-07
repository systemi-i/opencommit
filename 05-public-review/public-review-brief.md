# ICSL Public Review Brief

Status: candidate draft.  
Date: 2026-07-07.

## What Is ICSL?

ICSL is a candidate standard for representing institutional protocols as explicit,
versioned, auditable, interoperable commitment systems.

It is designed for public services, governance systems, regulated institutional processes,
service delivery networks, registries, and AI-assisted administrative systems.

## Core Idea

ICSL does not start with tasks or forms. It starts with institutional commitments.

The atomic unit is the CommitmentPoint: the moment an institution accepts, denies, certifies,
modifies, delegates, remedies, supersedes, or closes a reliance-worthy institutional effect.

Every CommitmentPoint has six gates:

- Authority
- Evidence
- Reasoning
- Dependency
- Version
- Recourse

## Why It Matters

ICSL can help create an interoperable public-service layer where institutions can exchange
not only data, but governed actions with explicit authority, evidence, versioning, recourse,
and receipts.

This could improve:

- public-service delivery
- cross-agency coordination
- governance transparency
- interoperability
- auditability
- comparability
- AI safety in institutional contexts
- accountability at scale

## Current Status

The conceptual model is frozen for v0.1 candidate work.

The review package includes:

- conceptual freeze decision
- hardening patch
- standards-readiness review
- seed schemas
- seed conformance harness
- initial fixtures
- package example

ICSL is not yet a final public standard.

## Review Questions

Reviewers should ask:

- Is CommitmentPoint the right primitive?
- Are the six gates sufficient and necessary?
- Does the recourse model handle adverse outcomes clearly?
- Does the model protect canonical governance semantics from runtime/vendor bindings?
- Are conformance claims specific enough?
- Can independent implementers produce the same validation results?
- Does this support public-service interoperability without erasing local legal variation?

## Desired Feedback

The project needs feedback from:

- public-service operators
- standards experts
- legal-informatics researchers
- institutional economists
- digital public infrastructure teams
- civic technology builders
- administrative-law experts
- AI governance researchers
- validator and registry implementers
