# Conformance Testing

The final ICSL v0.1 conformance suite has not yet been published. The release target is at least 25 public fixtures covering valid artifacts, invalid structures, semantic contradictions, canonicalization, package behavior, extensions, and adversarial cases. Until that suite and independent validator reports exist, the project makes no claim of complete conformance or production interoperability.

Three narrower, reviewer-runnable checks are included today.

## Claim-Subject Profiles

Conformance is tested against both a class and a claim-subject type. The current checks
exercise ProtocolVersion, Receipt, GovernedContext, and package invariants. They do not
constitute complete parser, validator, composer, registry, runtime, renderer, or corpus
profiles.

Until a suite publishes requirements and fixtures for one of those implementation
subjects, it cannot receive a `pass` result. Package rules are `not_applicable` as direct
requirements of an implementation claim, even when the implementation is tested using
packages. Artifact rules may still define the expected result of those fixtures.

## Schema-Mutation Suite

The [mutation suite](mutations/) applies declared changes to known-valid ProtocolVersion,
Receipt, GovernedContext, and ConformanceDeclaration baselines. Its 28 expectations test
selected schema protections, rule coverage, canonicalization guards, extension boundaries,
version identity, class-depth consistency, and claim-subject discrimination.

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

Passing a future suite will still require a qualified claim naming the tested subject,
subject type, class, ICSL version, suite version, validator, and result.
