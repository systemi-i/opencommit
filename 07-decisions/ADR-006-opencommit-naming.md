# ADR-006: OpenCommit Initiative Naming

Status: Accepted

Date: 2026-07-14

## Context

The initiative name "OpenCommit" is already used by an open-source AI commit-message tool. The overlap creates practical concerns:

- the npm and GitHub namespaces are effectively unownable;
- search results for "opencommit" resolve overwhelmingly to the CLI, creating a permanent SEO conflict;
- the two projects may be confused by users, contributors, or partners.

The standard itself is named ICSL and is unaffected by this collision; the question concerns only the umbrella initiative name.

## Decision

The public identity of the standard, documentation, and external consultation is
**ICSL**. OpenCommit remains a non-normative working name for the project and stewarding
initiative. It is not part of the ICSL data model, canonical artifacts, schema
namespaces, conformance claims, or version identifiers.

The initiative name may therefore be changed later without renaming the standard or
invalidating any ICSL artifact. Public-facing documentation should lead with ICSL and
use OpenCommit only where the stewardship or project context needs to be identified.

## Consequences

- Public-facing materials lead with ICSL rather than OpenCommit.
- The project avoids treating OpenCommit as a protocol, namespace, certification, or product identity.
- A later initiative rename is editorial and organizational, not a change to the ICSL conceptual model.
- The version-token ladder and ICSL identifiers do not depend on this decision.

## References

- di-sukharev/opencommit (existing CLI project on npm and GitHub)
- Status and Roadmap
