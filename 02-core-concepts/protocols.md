# Protocols

An ICSL protocol is a named governed process. A ProtocolVersion is an immutable publication of that process at a particular point in time.

A ProtocolVersion identifies the responsible institution, describes the class of matters governed, and defines the CommitmentPoints at which institutional acts may occur. It does not attempt to reproduce every task, screen, notification, or internal handoff involved in service delivery. Those operational details belong in workflow and case-management systems unless they independently create a reliance-worthy institutional effect.

Examples include permit determination, emergency assistance, health referral, student-support eligibility, inspection and enforcement, grant disbursement, and administrative appeal.

## Why Versioning Matters

Public procedures change. Authority may move to a different office, evidentiary requirements may be amended, a deadline may change, or a new route of recourse may be created. A case must nevertheless remain interpretable under the rules that governed it when the institution acted.

ICSL therefore treats each ProtocolVersion as immutable. A correction or amendment produces a new version rather than changing an old one in place. Runtime contexts and receipts pin the exact version by identifier and canonical hash.

## Relationship to Workflow

ICSL is not a workflow-orchestration language. A conforming protocol provides the institutional information needed to evaluate and record consequential acts, but it does not necessarily specify screen order, queue management, staffing, message transport, retries, scheduling, or user-interface behavior.

Implementations may bind a ProtocolVersion to BPMN, CMMN, case-management configuration, decision engines, registries, or custom software. Those bindings remain outside canonical protocol truth so that replacing the implementation does not silently change the institution's commitments.

## Federation and Autonomy

Protocols do not require all institutions to use the same platform or substantive policy. Each institution may publish and maintain its own versions, cite its own legal sources, and adapt shared patterns to its jurisdiction.

Common structure makes those protocols easier to compare and their Receipts easier to interpret. It can provide semantic inputs to future federation arrangements while leaving authority with the institution legally responsible for the act. ICSL v0.1 does not itself define those arrangements or authorize Receipt exchange.
