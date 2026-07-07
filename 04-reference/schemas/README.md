# Schema Skeletons

The schemas in this directory are seed schemas for standards-harness work. They are not
yet a complete formal specification. Their purpose is to name the objects that survived
conceptual freeze and provide a place for validation rules, fixtures, and package examples
to converge.

All schemas use JSON Schema draft 2020-12 and a provisional `$id` under
`https://igsl.dev/icsl/schemas/0.1-freeze/`.

`ICSLCommon.schema.json` contains shared candidate definitions for conformance classes,
binding force, recourse states, authority gates, recourse gates, binding-effect basis, and
diagnostics. Object schemas should reuse these definitions rather than restating enums.

The schemas are now stricter than the original seed skeletons, but they remain candidate
schemas. Final publication still needs a full JSON Schema validation path in the CLI or a
separate reference validator.
