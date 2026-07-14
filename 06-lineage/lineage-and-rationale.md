# ICSL Lineage and Rationale

## 1. The Design Problem

Public institutions increasingly act through software, but the institutional conditions governing those actions are rarely represented as portable technical objects. Law and policy state the formal rules. Administrative practice supplies interpretation and judgment. Workflow products coordinate tasks. Databases store outcomes. None of those components, by itself, provides a common account of when an institution has created an effect on which another person or system may rely.

ICSL addresses that narrower problem. It represents governed processes as versioned protocols, identifies reliance-worthy institutional acts as CommitmentPoints, specifies the conditions of acceptance through six gates, and records accepted acts through Receipts.

This design draws on several bodies of work. The relationship is one of inheritance and synthesis, not equivalence or endorsement by the scholars and standards named below.

## 2. Institutional Grammar and Polycentric Governance

The most direct conceptual lineage is the Institutional Grammar associated with Sue Crawford and Elinor Ostrom and its later development by institutional-analysis researchers. Institutional Grammar demonstrates that institutional statements can be analyzed through recurring components such as actors, deontic operators, aims, conditions, and consequences.

ICSL adopts the underlying premise that institutions have structure that can be represented more precisely than undifferentiated prose. It does not attempt to replace Institutional Grammar or encode every institutional statement. Instead, it focuses on the operational point at which rules and institutional arrangements produce an accepted act.

Ostrom's work on polycentric governance is equally important to the architecture. Public coordination need not depend on a single center of control. Multiple institutions can retain distinct authority, adapt rules to local conditions, and coordinate through shared arrangements. ICSL's preference for versioned, forkable protocols and federated validation follows that logic: interoperability should not require one platform or one substantive policy.

## 3. Administrative Law and Procedural Justice

Authority, reasons, evidence, notice, review, and remedy are not merely software concerns. They are central to administrative legality and procedural justice. ICSL's six gates reflect the practical need to ask who may act, on what material, under which rule and version, subject to which dependencies, and with what route of challenge.

The specification does not encode a universal theory of lawful administration. Legal traditions differ, and an ICSL artifact cannot certify legality. The model instead makes an institution's operational claim about those matters explicit enough to inspect. This is why adverse outcomes, discretion, recourse, source precedence, and rebuttable receipts occupy central rather than peripheral roles.

## 4. Rules as Code and Computational Law

Rules-as-code initiatives, statutory programming languages, and legal-rule interchange standards show that parts of legislation and policy can be made machine-consumable. Catala, OpenFisca, LegalRuleML, Akoma Ntoso, ELI, and related work address different parts of this landscape: executable calculations, formal norms, document structure, and stable legal identifiers.

ICSL does not compete with those capabilities. A Reasoning gate may reference a decision table, rules engine, formal rule representation, or human-discretion process. References may point into structured legislation. ICSL adds the surrounding institutional act: who was authorized to apply the rule, which evidence was accepted, what outcome became effective, which recourse followed, and which receipt records the act.

This boundary is important. Correct computation does not by itself establish authority, and a formally encoded rule does not determine how an institution accepts its result.

## 5. Workflow, Decisions, and Case Management

BPMN, DMN, and CMMN provide mature ways to orchestrate processes, express decision logic, and manage cases. Public institutions also rely on service-specific workflow standards and commercial case-management platforms.

ICSL distinguishes those operational descriptions from canonical institutional semantics. A BPMN task may implement part of a CommitmentPoint, and a DMN table may supply its Reasoning gate, but neither is automatically the authoritative definition of the act. Deployment bindings remain replaceable; the ProtocolVersion states the conditions that must survive a change of engine or vendor.

The distinction also limits ICSL's scope. A conforming protocol is not necessarily executable end to end without workflow definitions, interfaces, data mappings, identity and access controls, messaging, and operational policy. ICSL specifies the governed acts those systems must respect.

## 6. Records, Events, and Verifiable Data

Receipts draw on event-sourced and append-only approaches to institutional memory. Rather than editing an earlier decision when its effect changes, a later receipt records suspension, revival, variation, revocation, or supersession. Current status is derived from the ordered history.

Hash linking and canonical identity make tampering detectable relative to an independently retained chain head. They do not authenticate the actor or prove legality. Verifiable Credentials and related signature systems may later provide an envelope for authentication and selective disclosure, but v0.1 keeps that problem outside the core receipt model.

This separation allows the standard to define institutional content and lifecycle before committing to one credential or trust infrastructure.

## 7. Digital Public Infrastructure

Digital public infrastructure has established reusable capabilities for identity, payments, registries, credentials, and data exchange. Systems such as X-Road demonstrate that public institutions can coordinate through federated technical infrastructure rather than a single central application.

ICSL proposes a complementary semantic layer. Transport can move a message; a protocol and receipt can state what institutional effect the message represents. Identity can establish a principal; the Authority gate can state why that principal may perform a particular act. A payment rail can transfer value; a Commitment can state which governed decision created the payment obligation.

The proposed contribution is therefore not another delivery rail. It is a common representation of the governed action that travels over existing rails.

## 8. AI Governance

Many AI-governance frameworks identify transparency, accountability, human oversight, contestability, and risk management as important principles. Public administration needs those principles to appear inside operational processes.

ICSL contributes a process-level boundary. It distinguishes candidate facts from accepted evidence, assistance from delegated authority, and recommendations from Commitments. The shadow-binding test brings consequential triage and routing into view when they effectively control access despite being labelled preliminary or advisory.

This does not make an AI system safe merely because it participates in an ICSL process. It makes specific authority, evidence, and recourse failures easier to express and test.

## 9. Relationship to Selected Standards

| Standard or field | Primary concern | Relationship to ICSL |
| --- | --- | --- |
| Institutional Grammar | Structure of institutional statements | Informs rule representation; ICSL focuses on acceptance and institutional effect. |
| Catala and OpenFisca | Executable statutory and tax-benefit logic | May implement deterministic Reasoning; ICSL adds authority, evidence, outcome, and recourse. |
| Akoma Ntoso, ELI, and ECLI | Structured legal documents and stable identifiers | Provide source structure and locators for References. |
| LegalRuleML | Interchange of legal rules, modalities, and temporal validity | May represent rule content used by a Reasoning gate. |
| BPMN, DMN, and CMMN | Workflow, decisions, and case management | Operate in the runtime layer and may implement parts of a protocol. |
| W3C Verifiable Credentials | Authenticated, verifiable claims | A possible future envelope for receipt authenticity; not required by v0.1. |
| ODRL | Permissions, prohibitions, and obligations over assets | Offers relevant vocabulary patterns but does not supply ICSL's public-act and recourse model. |
| X-Road and federated exchange | Secure inter-organizational data transport | Can carry ICSL packages and receipts; ICSL supplies institutional semantics. |
| Open Referral | Service and organization directories | Can identify services to which governed referral protocols point. |
| HL7 FHIR | Clinical and administrative health-data exchange | Remains the health data and workflow layer; ICSL can profile the institutional effect of a referral or acceptance. |

## 10. The Claimed Contribution

ICSL's proposed contribution is not that governance can be fully reduced to code. It is that certain institutional acts can be represented consistently enough for systems to validate their declared conditions, preserve their history, and communicate their meaning without owning the same software.

That proposition remains to be demonstrated through independent implementations and real institutional use. Its importance is likely to grow as public systems exchange more consequential actions and AI systems participate more deeply in administration. Without an explicit act layer, technical interoperability can increase while responsibility, recourse, and institutional meaning become harder to locate.
