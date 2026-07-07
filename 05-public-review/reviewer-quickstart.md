# Reviewer Quickstart

Date: 2026-07-07.

## Read First

1. `11-v0.1-candidate-spec/README.md`
2. `11-v0.1-candidate-spec/ICSL-v0.1-candidate-spec.md`
3. `11-v0.1-candidate-spec/ICSL-conformance-profile.md`
4. `10-standards-harness/README.md`
5. `12-release-candidate/CLAIM-GUARDRAILS.md`

## Run The Harness

From the review project root:

```bash
cd 10-standards-harness
node bin/icsl-harness.mjs fixtures run fixtures
node bin/icsl-harness.mjs package verify packages/minimal-core
node bin/icsl-harness.mjs conformance report fixtures
```

Expected result:

- 40 fixtures pass
- minimal package verifies
- conformance report lists fixture summary

## Inspect The Fixtures

Useful starting fixtures:

- `F01-minimal-valid-core`
- `F04-advisory-false-positive`
- `F12-runtime-binding-smuggling`
- `F17-governance-addendum-required`
- `F28-valid-extended-package`
- `F33-valid-core-l3-governance`
- `F36-ai-gate-authority-invalid`
- `F43-canonical-array-order`

## Review Questions

- Can an independent implementer understand when a CommitmentPoint exists?
- Are the six gates universal without being too blunt?
- Are authority, task ownership, and delegation clearly separated?
- Does the recourse model make adverse outcomes inspectable?
- Is the canonical/runtime/package boundary implementable?
- Are conformance claims specific enough to prevent overclaiming?
- Are the open issues acceptable for release-candidate status?
