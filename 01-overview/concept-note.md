# Concept Note: ICSL

## Institutional Coordination and Service Language

Digital public infrastructure is entering a new phase. Governments, public agencies, civic institutions, development partners, and AI systems are increasingly expected to coordinate across programs, jurisdictions, platforms, and legal mandates. But the institutional layer underneath public service delivery remains largely informal, fragmented, and non-machine-readable.

Today, public systems can exchange data, authenticate people, process payments, and automate workflows. What they cannot reliably exchange is the institutional meaning of an action: who had authority, what rule applied, what evidence was used, what obligation was created, what recourse was available, what version of the procedure governed the decision, and whether the action was legitimate within its institutional context.

This is the gap ICSL is designed to address.

ICSL, the Institutional Coordination and Service Language, is an open standards effort for representing public-service rules, commitments, decisions, and institutional actions in a structured, interoperable, auditable form. It provides a common language for describing how governance becomes execution.

Rather than treating governance as documentation, compliance, or after-the-fact oversight, ICSL treats governance as an operational layer: a way to make institutional commitments explicit before systems act, portable across systems, and reviewable after action occurs.

## The Problem

Most public-sector digital transformation has focused on technical interoperability: APIs, data schemas, identity systems, registries, payment rails, and workflow platforms. These are essential, but they do not solve the deeper coordination problem.

Public services are not merely data transactions. They are institutional actions. A benefit approval, permit denial, referral, inspection, enforcement notice, appeal window, eligibility determination, or service obligation is not just an event in software. It is an action governed by authority, evidence, procedure, rights, duties, and recourse.

When these institutional dimensions are not explicit, several problems follow:

- Systems automate decisions without preserving the rules that made them legitimate.
- Agencies cannot compare procedures across programs or jurisdictions.
- AI tools can assist workflows but cannot reliably know where authority begins or ends.
- Public service delivery becomes difficult to audit, contest, improve, or coordinate.
- Interoperability stops at data exchange, rather than extending to institutional meaning.
- Governance remains trapped in PDFs, policy manuals, legal text, and tacit administrative practice.

The result is a missing layer in digital public infrastructure: an institutional protocol layer.

## What ICSL Is

ICSL is a proposed open standard for making institutional rules and public-service commitments computable without making them opaque or unaccountable.

It defines a structured way to represent:

- institutions and governed contexts;
- protocols and protocol versions;
- commitment points where institutional action occurs;
- authority, evidence, reasoning, dependency, version, and recourse gates;
- receipts that record what happened and under which rules;
- conformance classes for validators, registries, runtime systems, and AI-assisted tools.

In plain terms, ICSL allows a public system to say:

> This action was taken by this institution, under this protocol version, with this authority, based on this evidence, producing this commitment, with these rights of review or recourse.

That sentence is currently scattered across laws, regulations, forms, workflow tools, case notes, databases, and human memory. ICSL makes it explicit, structured, portable, and verifiable.

## How It Works

ICSL separates three layers that are often collapsed in current systems.

First, there is the canonical institutional layer: the protocol, commitment points, gates, and rules that define whether an action is valid within a governed context.

Second, there is the runtime layer: the software, AI assistants, workflow engines, registries, and service platforms that help execute or support institutional action.

Third, there is the evidence and receipt layer: the durable record of what rule version was used, what evidence was considered, what decision or commitment was made, and what recourse was available.

This separation matters. It ensures that a vendor platform, AI model, or local workflow tool cannot silently redefine the institutional meaning of an action. Runtime systems may assist execution, but canonical authority remains in the governed protocol.

ICSL uses a gate model to determine whether a commitment point is institutionally valid. A commitment is not treated as valid merely because software produced it. It must satisfy required checks such as authority, evidence, reasoning, dependencies, version control, and recourse.

This allows different systems to interoperate not just around data, but around governed action.

## Why Now

Several trends make this urgent.

AI is entering public administration faster than institutional safeguards can be operationalized. Governments need ways to let AI assist service delivery without allowing AI systems to silently become decision-makers, authorities, or sources of unchallengeable procedural logic.

Digital public infrastructure is scaling across countries and sectors. Identity, payments, registries, data exchange, and service portals are becoming foundational. But without a shared institutional coordination layer, these systems risk becoming technically integrated but procedurally incoherent.

Public trust in digital governance depends on explainability, contestability, and accountability. Citizens and institutions need to know not only what decision was made, but under what authority, according to what rule, using what evidence, and with what right to challenge.

Development partners and governments are increasingly investing in DPI, AI governance, public-sector modernization, and service delivery reform. ICSL offers a way to connect those investments into a common institutional grammar rather than a patchwork of isolated tools.

The timing is therefore critical. The world is building digital rails for public action. ICSL helps ensure those rails carry legitimate, accountable, interoperable governance.

## Why This Is Transformational

ICSL could become a key component in an internet of interoperable public services and institutional actions.

Just as the web made documents linkable, and APIs made data and services composable, ICSL aims to make institutional commitments interoperable. It gives public systems a way to recognize, compare, verify, and coordinate actions across institutional boundaries.

This could unlock:

- cross-agency service coordination;
- portable eligibility and entitlement logic;
- auditable AI-assisted public administration;
- comparable service-delivery performance across jurisdictions;
- reusable public-service protocols;
- safer automation of high-stakes decisions;
- clearer recourse and appeal pathways;
- institutional memory that survives staff turnover and vendor changes;
- governance systems that can be tested before deployment and audited after execution.

For donors and funders, the opportunity is not simply to support another technical standard. It is to help define the missing governance layer of digital public infrastructure.

## Development Plan

The project is currently moving from conceptual review into a v0.1 standards candidate.

The next phase will produce:

- an ICSL v0.1 candidate specification;
- enforceable schemas for protocols, commitment points, gates, receipts, and packages;
- a conformance suite with test fixtures;
- a reference package format;
- implementation guidance for validators, registries, service platforms, and AI systems;
- governance and lineage documentation connecting ICSL to institutional grammar, Ostrom's work, public administration, digital public infrastructure, and AI governance;
- a public review process with experts in standards, civic technology, public-sector delivery, legal and institutional design, and AI governance.

The goal is not to prematurely declare a finished standard. The goal is to create a rigorous, reviewable, testable v0.1 candidate that can attract implementation partners and serious institutional critique.

## What Funding Would Support

Funding would support the transition from promising standards concept to credible public infrastructure candidate.

Priority activities include:

- standards editing and formal specification work;
- schema hardening and validator development;
- conformance test-suite expansion;
- reference implementation and package tooling;
- applied pilots with public-service workflows;
- expert review from legal, governance, DPI, and AI safety communities;
- documentation and public review materials;
- institutional partnership development;
- open-source governance and stewardship planning.

## The Core Claim

The future of public-sector digital transformation will not be defined only by better software, better data exchange, or more powerful AI. It will depend on whether institutional action itself can become explicit, interoperable, accountable, and governable at scale.

ICSL is an attempt to build that layer.

It turns governance from static compliance into operational infrastructure.

It gives AI systems boundaries they can respect.

It gives public institutions a way to coordinate without losing accountability.

And it gives digital public infrastructure a missing protocol for legitimate public action.

## Invitation

We are seeking partners who believe that the next generation of digital public infrastructure must be institutionally intelligent, not merely technically integrated.

ICSL is early enough to shape, but mature enough to review, test, and pilot.

The opportunity now is to help develop an open standard that could become foundational to public-service delivery, AI governance, and institutional interoperability in the years ahead.
