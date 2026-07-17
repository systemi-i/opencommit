# Claims and Maturity

ICSL is a candidate standard. Public claims should describe the evidence that exists without implying certification, legal authority, or demonstrated production interoperability.

## Supported Claims

The project can state that:

- the ICSL v0.1 conceptual model is frozen for external consultation;
- a candidate specification, package format, conformance profile, and implementation guide are published;
- the reference layer contains twelve JSON Schemas and 74 diagnostic rules;
- one synthetic Core-L2 package passes the included schema and hash verifier;
- the published mutation suite meets 28 declared expectations;
- the package attack runner rejects five specified adversarial changes;
- exploratory service encodings informed the model but are not a validated benchmark;
- broader fixtures, interoperability vectors, and independent implementation reports remain outstanding.

Each statement is deliberately bounded by its subject and evidence.

## Claims Not Yet Supported

The project and implementers should not claim that:

- ICSL is a final or formally adopted public standard;
- a product or institution is unqualifiedly “ICSL compliant”;
- production interoperability has been demonstrated;
- the candidate model is legally correct across jurisdictions;
- an encoding establishes legal authority or overrides its source;
- a receipt proves the substantive legality or authenticity of an act;
- a valid receipt is safe or lawful to publish, index, or exchange without further access,
  privacy, retention, and purpose controls;
- the current verifier is a complete reference implementation;
- AI systems acquire authority by implementing ICSL;
- exploratory corpus results demonstrate empirical validation or universal coverage;
- v0.1 already provides cross-protocol composition, an execution-binding standard, or a
  functioning open governance network.

## Conformance Statements

A conformance statement must identify the claim subject identity, claim subject type, ICSL version, conformance class, test-suite version, result, and validating implementation or report. A `pass` also requires a published suite profile for that subject type.

For example:

```text
Validator X reports that package Y passes ICSL 0.1-freeze Core-L2
as claim subject type protocol_package against suite Z, version 0.3,
using Validator X version 0.4.1.
```

“Validator X is ICSL compliant” is not an adequate claim because it omits the tested subject, class, suite, and result.

## Legal and Institutional Effect

ICSL represents an institution's account of governed action. It does not create authority, certify a source encoding, or determine which legal instrument prevails. Those questions remain governed by applicable law and institutional arrangements.
