# Conformance Suite

The ICSL v0.1 candidate includes a seed conformance suite.

The suite is designed to test whether validators, package producers, and related tools can detect valid and invalid protocol structures, commitment points, gates, receipts, package metadata, references, conformance declarations, runtime leakage, and ambiguity traps.

## What The Suite Tests

The current fixture set covers:

- Core structural validity;
- missing gates;
- binding and recourse semantics;
- receipt hash-chain behavior;
- runtime binding smuggling;
- reference version requirements;
- unsupported extensions;
- governance addendum requirements;
- package manifest and hash-vector rules;
- conformance declaration validity;
- AI authority boundaries;
- temporal current-time requirements;
- dependency resolution;
- durable evidence requirements;
- canonicalization edge cases.

## Intended Use

The conformance suite is intended for:

- implementers building validators;
- reviewers stress-testing the candidate spec;
- standards contributors identifying ambiguity;
- public-sector technology teams evaluating implementability;
- AI governance reviewers testing runtime boundaries.

Because ICSL v0.1 is a candidate, passing the suite should be described as candidate conformance testing, not final certification.

