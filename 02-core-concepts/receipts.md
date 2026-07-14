# Receipts

A Receipt is the durable record of an accepted Commitment. It identifies the exact ProtocolVersion, CommitmentPoint, governed context, outcome, acting authority, and time involved. Its hash binds those fields into an append-only chain.

Where relevant, a Receipt may also record AI assistance and an `acts_on` relationship to an earlier receipt. That relationship allows later acts to suspend, revive, vary, revoke, quash, supersede, or expire an earlier Commitment without altering the original record.

## What a Receipt Establishes

A valid receipt establishes that a particular data object conforms to the receipt structure, names a specific protocol version, and fits a verifiable hash chain. Subject to the applicable conformance checks, another system can determine which act and outcome the issuing institution recorded.

A receipt does not establish that the cited evidence was true, that the signer controlled the stated authority, or that the act was substantively lawful. ICSL v0.1 receipts are unsigned; their hashes provide tamper evidence relative to an independently retained chain head, not authentication or non-repudiation.

This limitation is intentional. A structured institutional record is useful only if its technical integrity and its legal significance are not confused.

## Portability and Current Status

Because the receipt pins the protocol by canonical hash, a consumer does not have to infer meaning from a vendor-specific event name. It can resolve the CommitmentPoint, inspect its allowed outcomes and gates, and determine whether later receipts changed the act's status.

That capability supports handoffs between agencies, registries, auditors, service providers, and civic agents. Each consumer still applies its own trust and legal rules, but the object being evaluated has a common structure.

Receipts are therefore an interoperability mechanism, not a universal source of trust. They make claims precise enough to verify, compare, and contest.
