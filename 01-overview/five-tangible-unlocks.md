# Five Practical Applications

> These scenarios explain capabilities the ICSL v0.1 candidate is intended to support. They are not production deployments or claims of demonstrated impact.

The examples below use different domains to show different parts of the model: auditability, protocol adaptation, portable commitments, rights-preserving coordination, and multi-party assurance.

## 1. Permitting: Decisions That Can Be Audited While the Case Is Live

A permitting protocol can identify the points at which an application becomes complete, an inspection finding is accepted, a permit is granted or refused, an appeal changes the effect of a decision, or a permit is revoked. Each point states the authority, evidence, reasoning, dependencies, version, outcomes, and recourse that govern it.

The resulting receipts give applicants, supervisors, auditors, courts, and downstream registries a common record of what the authority says occurred. They can distinguish a workflow event from an institutional act and trace later suspension or revocation without rewriting the earlier decision.

This can make delays, inconsistent practice, missing authority, and unavailable recourse visible earlier. It can also allow an institution to change case-management vendors without leaving the governing logic trapped in proprietary configuration.

**Distinct capability:** live traceability from a consequential action to its protocol version, authority, outcome, and recourse.

## 2. Crisis Response: Shared Protocols That Can Be Adapted Locally

Emergency response requires national authorities, municipalities, humanitarian agencies, funders, payment providers, and community organizations to act quickly under changing conditions. Shared procedures are useful, but a single fixed workflow rarely survives differences in law, geography, evidence availability, or delivery capacity.

ICSL allows a base protocol to be versioned and adapted while preserving the relationship between versions. A local protocol can change eligibility evidence, responsible authorities, delivery commitments, or grievance routes without becoming impossible to compare with the common model. Receipts can record which institution accepted which obligation under which local version.

The result is not centralized control. Each participant retains responsibility for its own protocol and actions, while common semantics support coordination and review.

**Distinct capability:** forkable protocols that preserve local authority and adaptation without losing provenance or comparability.

## 3. Health Referrals: Commitments That Travel With Existing Data

FHIR already provides mature structures for exchanging clinical and administrative information, including referral workflows. A ServiceRequest or Task can show what was requested and how work is progressing. Local institutions must still determine whether the referral creates a duty, who may accept it, how urgency is governed, and what happens if care is delayed or refused.

An ICSL profile can express those institutional semantics around the existing FHIR exchange. FHIR remains the health-data and workflow layer; ICSL states the authority, evidence, binding force, acceptance point, and recourse associated with the referral.

This could let a receiving provider distinguish an advisory recommendation from an accepted transfer of responsibility. It could also give patients and auditors a clearer record of handoffs without creating a parallel clinical-data system.

**Distinct capability:** portable institutional commitments layered onto an established domain standard rather than a replacement for it.

## 4. Education and Social Support: Coordination Without Making the Person a Data Object

A student or family may interact with schools, transport services, disability-support teams, benefits offices, health providers, and child-protection bodies. Better coordination is valuable, but indiscriminate data sharing can weaken consent, obscure responsibility, and make adverse decisions harder to challenge.

Protocols can specify which institution may determine eligibility, what evidence may be accepted, what support obligation follows, which privacy constraints apply, and where a family can seek review. Receipts can communicate accepted obligations and status without requiring every participating institution to merge its systems or authority.

Civic agents could then help a family understand requirements, assemble evidence, or prepare a challenge while remaining outside the authority boundary. The protocol, not the agent, determines when an institutional act occurs.

**Distinct capability:** person-centered coordination that keeps authority, consent, responsibility, and recourse explicit.

## 5. Climate and Infrastructure Finance: Verifiable Conditions Across Many Parties

Climate, nature, energy, and infrastructure programs often connect public authorities, development banks, private implementers, technical verifiers, communities, and oversight bodies. Payments may depend on permits, safeguards, milestones, consultation, evidence of delivery, and grievance mechanisms. Today these conditions are frequently reconciled through reports and bespoke assurance processes.

An ICSL protocol can identify the acts that approve a project, accept evidence, clear a safeguard, create a payment obligation, recognize a community commitment, or open a grievance route. Receipts can allow the parties to verify those acts without requiring a common project-management platform.

This does not validate the truth of an environmental claim by itself. It makes the authority, evidence requirement, acceptance, and downstream consequence of the claim explicit enough to audit and contest.

**Distinct capability:** multi-party assurance built around governed commitments rather than opaque reporting chains.

## What the Examples Establish

The examples do not depend on one sector-specific product. They apply the same architecture to different institutional problems:

- permitting demonstrates traceability and status over time;
- crisis response demonstrates adaptation and federation;
- health demonstrates integration with mature domain standards;
- education demonstrates agency and rights across institutional boundaries;
- climate and infrastructure finance demonstrates assurance across public, private, and multilateral actors.

Together they show the path from local utility to network value. Protocols make governed processes inspectable. CommitmentPoints identify the acts that matter. Gates constrain when those acts may be accepted. Receipts let their meaning travel. At sufficient adoption, those capabilities could support an open governance network without requiring a single platform or uniform substantive policy.
