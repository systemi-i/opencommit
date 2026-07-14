# Conformance Testing

The final ICSL v0.1 conformance suite has not yet been published. The release target is at least 25 public fixtures covering valid artifacts, invalid structures, semantic contradictions, canonicalization, package behavior, extensions, and adversarial cases. Until that suite and independent validator reports exist, the project makes no claim of complete conformance or production interoperability.

Three narrower, reviewer-runnable checks are included today.

## Schema-Mutation Suite

The [mutation suite](mutations/) applies declared changes to known-valid ProtocolVersion, Receipt, and GovernedContext baselines. Its 26 expectations test selected schema protections, rule coverage, canonicalization guards, extension boundaries, version identity, and class-depth consistency.

Run it from the repository root:

```sh
python3 04-reference/mutations/run_mutations.py
```

A successful run means that each published expectation produced its declared result. It does not mean that catalog rules were fully executed or that an arbitrary package conforms.

## Worked-Package Verifier

The synthetic permit package includes a verifier for its schemas, manifest, hash vector, ProtocolVersion identity, receipt chain, outcomes, act relationships, and selected semantic rules.

```sh
python3 08-examples/permit-core-l2/verify.py
```

The verifier is tied to the worked package and should not be described as a complete reference implementation.

## Package Attack Runner

The package also includes five persisted attacks covering target substitution, version-hash corruption, manifest path traversal, and canonicalization guards.

```sh
python3 08-examples/permit-core-l2/attacks.py
```

The runner first verifies an unchanged control package and then confirms that each mutation fails for its intended reason.

## Planned Fixture Families

The public conformance suite is expected to include:

- Core-L1 structural fixtures;
- Core-L2 authority, outcome, binding, recourse, lifecycle, and receipt fixtures;
- Core-L3 governance and provenance fixtures;
- canonicalization and cross-language hash vectors;
- package, manifest, reference, and rendering fixtures;
- extension negotiation and fallback fixtures;
- runtime-smuggling and semantic-ambiguity attacks;
- implementation reports showing how independent validators interpret diagnostics.

Passing a future suite will still require a qualified claim naming the tested subject, class, ICSL version, suite version, validator, and result.
