# Introducing ICSL

## A Specification Language for Institutional Commitments

## Abstract

Public institutions make consequential commitments every day. They grant permits, recognize entitlements, register claims, certify facts, suspend payments, decide appeals, delegate authority, and close cases. These acts matter because they change what people and organizations may do, what they are owed, what they must provide, and what they can challenge.

The systems used to administer these acts are increasingly digital, but the institutional protocols behind them usually remain implicit. Law, policy, forms, workflow configuration, case records, and professional practice each carry part of the meaning. No single artifact reliably states what the institution is committing itself to do, who may act, what evidence is sufficient, which rules apply, what effect follows, or what recourse remains.

The Institutional Commitment Specification Language (ICSL) is an open specification language for institutional protocols: governed processes composed of commitment-bearing acts. It expresses both the structure of those processes and the actions through which they produce institutional effects. It is intended to make consequential public action more precise, comparable, auditable, and interoperable while preserving legal authority, institutional autonomy, human judgment, and rights of challenge.

ICSL is not a workflow engine or an attempt to turn law into software. It defines the governed institutional structure that workflows, case systems, rules engines, digital public infrastructure, and AI-assisted tools are expected to respect.

## 1. The Missing Institutional Object

Modern public systems are good at handling parts of institutional action. Identity systems authenticate people and organizations. Registries hold records. Payment systems transfer value. Data exchanges move information. Workflow systems route tasks. Rules engines evaluate conditions. Case-management systems preserve operational state.

None of these components, by itself, represents the institutional act as a whole.

An API can transmit a permit outcome without explaining why it has effect. A workflow can mark a case approved without establishing that the approver had authority. A registry can record eligibility without identifying the rule version or evidence on which the determination relied. A notification can report a result without carrying the route by which it may be challenged.

This is not simply missing metadata. The missing object is the institution's own governed protocol: the structured account of how consequential acts may be produced, connected, relied upon, corrected, and changed.

When that protocol remains distributed across prose and software configuration, several problems follow. Institutional knowledge becomes dependent on particular staff and vendors. Similar services cannot be compared without reconstructing local terminology. Oversight begins after the fact and requires substantial manual interpretation. Cross-agency coordination depends on bilateral agreements about meaning. Automation can accelerate a process while making its authority and challenge mechanisms less visible.

ICSL starts from a specific proposition: institutions need a shared way to describe the commitment-bearing structure of their procedures, separate from the software that happens to execute them.

## 2. What ICSL Is

ICSL is a specification language for institutional protocols: governed processes composed of commitment-bearing acts.

A protocol is a named governed process for a class of cases, matters, applications, incidents, decisions, obligations, or remedies. A ProtocolVersion is an immutable publication of that protocol at a particular point in its development. It identifies the responsible institution, the class of matters governed, and the institutional acts that may occur under that version.

The practical distinction between ICSL and adjacent tools is straightforward:

- a workflow describes how work moves;
- a registry describes what records exist;
- a rules engine evaluates specified conditions;
- a case system manages an individual matter;
- an ICSL protocol describes the institutional acts for which the institution becomes answerable, and the conditions under which those acts may count.

These tools are complementary. ICSL can express the commitment-bearing structure across a process lifecycle, but it does not reproduce every operational step or provide end-to-end orchestration. A workflow may implement part of an ICSL protocol, and an ICSL protocol may refer to evidence held in a registry or rules evaluated elsewhere. ICSL does not replace those systems. It gives them a common institutional object around which to align.

## 3. The Core Model

The central semantic primitive in ICSL is the **CommitmentPoint**. A CommitmentPoint is a versioned template for one atomic institutional act. Its accepted instance in a particular case is a **Commitment**.

A practical way to recognize a CommitmentPoint is to ask whether an act creates a reliance-worthy institutional effect. Does it determine a right, obligation, permission, status, or procedural course? Does another institution rely on it? Can it expire, be challenged, be remedied, or be superseded? If so, it is likely part of the commitment-bearing structure of the protocol.

Not every workflow event qualifies. Assigning a task, drafting a letter, moving a record between queues, or producing an AI recommendation is not a CommitmentPoint merely because it appears in the process. The distinction prevents ordinary operational activity from being mistaken for institutional authority.

### Commitment types

Every CommitmentPoint is classified by one of eight core act types:

- **DECIDE** establishes an authoritative disposition among allowed outcomes.
- **ATTEST** formally asserts or accepts a proposition or evidentiary state.
- **APPEAL** disposes of a challenge to a prior Commitment on its merits.
- **REMEDY** commits correction or redress for an identified defect or wrong.
- **OVERRIDE** displaces a valid Commitment under superseding authority or interest.
- **EVOLVE** changes the governing protocol or rules prospectively.
- **CLOSE** moves a governed context to a terminal state.
- **DELEGATE** transfers bounded authority to an identified recipient.

The classification is deliberately narrow. It helps implementations and reviewers distinguish recurring forms of institutional action, but the label does not create authority or binding force. Those properties must be stated elsewhere in the protocol.

### The six gates

Each CommitmentPoint is governed by six gates:

- **Authority** identifies who is empowered to make the act count and on what basis.
- **Evidence** states what information or records may support the act.
- **Reasoning** identifies the evaluative rule or justification connecting evidence to outcome.
- **Dependency** identifies prior Commitments, outcomes, conditions, or timing on which the act relies.
- **Version** ensures that the operative protocol and referenced rules are the ones actually applied.
- **Recourse** states what review, challenge, correction, or appeal remains available.

A CommitmentPoint also declares its trigger, allowed outcomes, and binding-effect basis. Together, these elements answer a concrete question: under this published protocol, what would have to be true for this particular institutional act to be accepted?

### From protocol to receipt

When a CommitmentPoint is validly instantiated in a particular GovernedContext, it produces a Commitment. A **Receipt** records that Commitment. It identifies the protocol version, CommitmentPoint, context, authority, outcome, and relevant relationships to earlier acts.

Receipts preserve institutional claims in a form that other systems can inspect and verify. They pin an act to the exact ProtocolVersion under which it was made, so a later change to the protocol cannot silently change the meaning of an earlier act. Later suspension, remedy, override, appeal, or supersession is recorded as further action rather than by erasing history.

A Receipt records the institution's assertion that an act was accepted under a pinned ProtocolVersion. Its hash chain is tamper-evident only relative to an externally retained chain head; v0.1 does not authenticate the issuer or prove legality, factual truth, or lawful authority. Receipts are also potentially sensitive and linkable. They are not public or safely portable by default.

## 4. A Permit Example

Consider a construction permit. The authority may already have an application portal, a document repository, a case-management workflow, a zoning rules engine, and a registry of issued permits. Those systems can still leave the governed structure of the process difficult to reconstruct.

An ICSL ProtocolVersion could identify the following CommitmentPoints:

```text
CP-01  DECIDE  Determine that the application is procedurally complete
CP-02  ATTEST  Accept the technical compliance finding
CP-03  DECIDE  Grant or refuse the permit
CP-04  DECIDE  Determine whether an appeal is admissible
CP-05  APPEAL  Decide the appeal on its merits
CP-06  CLOSE   Close the matter after the final outcome
```

For the permit decision, the protocol would identify the authorized decision-maker, the evidence that may be considered, the governing rule and reasoning requirements, the prior findings on which the decision depends, the allowed outcomes, and the recourse attached to an adverse result.

When the permit is granted or refused, the resulting receipt pins the decision to that protocol version. An applicant can identify the stated authority and challenge route. A downstream registry can distinguish the formal decision from an internal recommendation. An auditor can reconstruct the relationship between the technical finding, the decision, and any later appeal without relying on the internal configuration of the case system.

The example also shows what ICSL leaves outside its scope. It does not assign inspection tasks, schedule staff, store architectural drawings, calculate zoning compliance, or send the decision notice. Those functions remain with operational and domain systems. ICSL specifies the institutional acts those systems must support and the boundaries they must not silently redefine.

## 5. Why Protocols Matter

Institutions do not act through isolated decisions. They act through protocols in which decisions depend on attestations, delegations establish authority, appeals act on earlier outcomes, remedies correct defects, and protocol changes govern future cases.

Treating the protocol as the first-class artifact creates several possibilities that isolated data schemas do not.

First, a protocol can be inspected before it is implemented. Missing authority, weak evidence requirements, contradictory dependencies, unavailable recourse, and ambiguous outcomes can be found during design rather than after harm occurs.

Second, the protocol can remain stable across technology changes. A new case system or workflow product can implement the same institutional specification instead of forcing the institution to reconstruct its own rules from vendor configuration.

Third, protocol versions can be compared. Offices and jurisdictions may use different substantive rules while still exposing where their authority, evidence, timing, outcomes, and recourse structures differ. Comparability does not require uniform policy.

Fourth, protocols can be adapted without losing lineage. A common emergency or service-delivery protocol may be localized to different laws and capacities while preserving its relationship to a shared model. This could support future federation without requiring one platform or one central authority; v0.1 does not define the composition, trust, or exchange arrangements that federation requires.

## 6. Why This Is Needed Now

Three developments make the problem urgent.

The first is the expansion of digital public infrastructure. Identity, payments, registries, messaging, signatures, and data exchange provide increasingly capable rails for public action. They establish who is interacting, move data and value, and connect institutions. They do not by themselves specify what an institution has committed itself to do through those rails.

The second is the introduction of AI into consequential processes. AI systems can retrieve information, extract facts, prepare applications, classify records, recommend outcomes, and coordinate tools. Without an explicit institutional protocol, a recommendation can become a decision through software design alone, or an inferred fact can become accepted evidence without an authorized act. General AI principles do not resolve these operational boundaries. The protocol must state where assistance ends and institutional authority begins.

The third is the growing need for coordination across institutional boundaries. Public services increasingly involve multiple agencies, levels of government, regulated providers, civil-society organizations, and international partners. Requiring every participant to adopt the same platform is often impractical and can undermine autonomy. Shared protocol semantics offer a different path: participants can retain their own systems and authority while making their commitments interpretable to one another.

The risk is not only that institutions fail to modernize. It is that they become faster and more connected without becoming more governable. ICSL is designed for the harder objective: increasing institutional capability while preserving answerability.

## 7. What ICSL Could Enable

The first value of ICSL is local. An institution can use a protocol specification to examine its own procedures, preserve institutional knowledge, test implementation against policy, make recourse visible, and reduce dependence on undocumented configuration. These benefits do not require a network of adopters.

The next value is operational. Software teams can implement against a published institutional object instead of translating prose independently into each application. Auditors can inspect the intended commitment structure and compare it with runtime receipts. AI-assisted tools can be constrained by explicit authority, evidence, and acceptance boundaries.

The larger value is interoperable. A referral can carry whether responsibility was merely requested or formally accepted. A benefit decision can expose the protocol and recourse that govern it. A funding milestone can identify which authority accepted which evidence and what obligation followed. Institutions can understand each other's actions without pretending that their laws or organizations are identical.

At sufficient adoption, versioned protocols and appropriately authorized exchange of minimized Receipts could contribute to an open governance network: an environment in which public services and institutional actions coordinate across systems and jurisdictions while each institution retains control of its law, operations, and authority. ICSL v0.1 supplies candidate semantic primitives for that future; it does not yet define federation, composition, trust negotiation, or cross-institution execution.

This is a long-term proposition, not a capability demonstrated by v0.1. The immediate task is to establish whether independent institutions and implementers can use the same specification consistently.

## 8. Boundaries and Safeguards

ICSL is intentionally not the whole institutional stack.

It does not create legal authority. The relevant constitution, law, regulation, policy, delegation, or other institutional source remains authoritative. Encoding a process does not make it lawful, and a validator cannot settle a legal dispute.

It does not prove that evidence is true. Domain systems, credentials, signatures, provenance mechanisms, and human review remain necessary to establish authenticity and sufficiency.

It is not a complete workflow or orchestration language. It does not assign work, manage queues, schedule resources, or specify every operational step.

It does not make automation authoritative by default. An AI system or software service may assist, recommend, or act only within authority that the institution has lawfully established and represented.

It is not intended for every low-consequence process. ICSL is most useful where authority, evidence, effect, dependency, version, and challenge materially affect whether an act should count.

These boundaries are part of the design. ICSL is useful only if its institutional claims remain distinguishable from legal truth, operational execution, and technical verification.

## 9. How ICSL Should Be Judged

The standard should not be judged primarily by whether its model is elegant. It should be judged by whether it performs useful work under independent use.

**Representation success** means that different encoders can describe the same real protocol with substantial agreement, using a stable core rather than inventing bespoke categories for every domain.

**Diagnostic success** means that the process of encoding reveals consequential ambiguities, such as unclear authority, missing recourse, hidden dependencies, weak evidence requirements, or unsafe automation boundaries.

**Implementation success** means that teams can build validators and operational systems from the specification without relying on private interpretations from its authors.

**Interoperability success** means that independently produced artifacts can be exchanged, validated, and interpreted consistently across implementations and institutional settings.

**Institutional success** means that a real organization finds the specification useful in redesign, modernization, oversight, coordination, or rights-preserving automation, and can identify an improvement that would have been harder to achieve without it.

These are demanding tests. They are also the tests a serious institutional standard should meet.

## 10. Current Status

ICSL v0.1 is a consultation candidate published for external review. Its conceptual model is frozen, and the current package includes the normative specification, JSON Schemas, diagnostic rules, conformance and packaging profiles, implementation guidance, canonicalization requirements, a worked protocol package, and executable mutation and attack tests.

This establishes internal coherence, not production readiness. The worked package is synthetic. The public fixture set is incomplete. Independent validator implementations and cross-language canonicalization results do not yet exist. Exploratory encodings of public services informed development of the model, but they are research material rather than a validated benchmark.

The next phase must therefore produce external evidence: independent review, multi-encoder studies, publishable positive and negative fixtures, independent implementations, interoperability reports, and carefully selected pilots grounded in authoritative institutional sources.

## 11. Stewardship and Participation

ICSL is being developed through OpenCommit, an initiative intended to support open specification, testing, implementation, and governance of the standard. OpenCommit is the stewarding initiative; ICSL is the standard documented in this book.

No single government, vendor, or implementation should control the language through which institutions represent their commitments. Durable stewardship will require transparent decision records, public issue handling, versioned releases, independent implementation, and participation from public administration, law, service delivery, standards, technology, civil society, and affected communities.

The purpose of consultation is not to ratify a finished idea. It is to determine whether the model is intelligible, implementable, appropriately bounded, and useful across legal and institutional traditions.

## Conclusion

Digital infrastructure gives institutions the means to act across systems. Software and AI give them growing capacity to act at speed and scale. What remains missing is a shared institutional object that states what those systems are authorized to make count.

ICSL proposes that the object should be the institutional protocol: a versioned, inspectable composition of commitment-bearing acts, with explicit authority, evidence, reasoning, dependency, version, outcomes, effects, and recourse.

ICSL is not the whole answer, and v0.1 does not prove the proposition. It does make the proposition precise enough to test.

The question is whether institutions can become more capable, interoperable, and adaptive without becoming less accountable, less contestable, or less legitimate. ICSL is an attempt to make the answer yes.
