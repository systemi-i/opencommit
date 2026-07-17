#!/usr/bin/env python3
"""Verifier for the ICSL Core-L2 proof exemplar (08-examples/permit-core-l2).

Checks, against the repository's frozen schemas and canonicalization profile
(RFC 8785 JCS under I-JSON constraints; see 04-reference/canonicalization/ and
ADR-002/ADR-003):

  1. every JSON artifact validates against its schema
     (JSON Schema draft 2020-12, local $ref registry -- no network;
     format assertions such as date-time are enforced via FormatChecker);
  2. the receipt chain recomputes: receipt_hash over the JCS canonical bytes of
     each receipt with the receipt_hash member removed, previous_hash linkage
     (genesis null), content_hash over the JCS canonical bytes of content,
     outcome tokens and acts_on effects allowed by the ProtocolVersion;
  2a. commitment_type:
     every CommitmentPoint carries a valid core commitment_type (this canonical
     Core-L2 package admits no EXTENSION marker and GENERIC is forbidden);
     every receipt's derived commitment_type copy equals its CommitmentPoint's
     type (RECEIPT_COMMITMENT_TYPE_MATCH); relational types identify their
     targets (APPEAL_TARGET_REQUIRED, REMEDY_TARGET_IDENTIFIED,
     OVERRIDE_TARGET_AND_BASIS_REQUIRED via acts_on_allowed);
  2b. version identity:
     every receipt's protocol_version_hash equals the recomputed canonical
     (JCS + sha256) hash of protocol-version.json
     (RECEIPT_PROTOCOL_VERSION_HASH_MATCH). The ProtocolVersion object contains
     no hash of itself, so the hash preimage is non-self-referential; its
     embedded governed_context is a GovernedContextDescriptor -- descriptive
     only, no runtime members (protocol_version_id, protocol_version_hash,
     governed_context_id, current_time), so no zero-hash convention exists
     anywhere;
  2c. typed act relationships: acts_on_allowed.targets reference existing CommitmentPoint
     ids, and every receipt's acts_on.target_receipt_id resolves to a receipt
     whose commitment_point_id is in the acting CP's acts_on_allowed.targets
     (ACTS_ON_TARGET_MEMBERSHIP -- an appeal cannot act on an unrelated receipt);
  3. the hash vector recomputes: source-byte sha256 for every declared file,
     canonical-JSON sha256 for JSON artifacts, coverage of every manifest file
     except the self-exempt hashes.json;
  4. the manifest is complete and safe: it declares itself, every declared file
     exists, every file in the package is declared, and no declared path is
     absolute or contains '..' segments.

This script is schema validation plus hash recomputation. It is NOT the ICSL
conformance suite; exiting 0 supports no conformance claim (see conformance.json).

Canonicalization discipline (see ADR-002 and the canonicalization profile):
RFC 8785 sorts object members by UTF-16 code units while Python's sort_keys
sorts by code points; the orderings diverge for non-BMP member names. Canonical
ICSL artifacts therefore require ASCII member names (values may be any
Unicode), and conforming artifacts encode all quantities as strings. This
verifier uses a real RFC 8785 implementation when one is installed
(pip install rfc8785); otherwise it asserts BOTH preconditions -- no non-string
JSON numbers anywhere AND all member names ASCII -- before every hash and fails
closed if either is violated (under those preconditions sorted compact
json.dumps is byte-identical to RFC 8785; the guarded fallback is NOT a general
JCS implementation). The ASCII-member-name rule is also an artifact conformance
constraint, so it is asserted even when rfc8785 is installed (2026-07 repair
sprint -- see 07-decisions/).

Usage: python3 verify.py        (requires: pip install jsonschema)
"""

import hashlib
import json
import posixpath
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator, FormatChecker
    from referencing import Registry, Resource
except ImportError:  # pragma: no cover
    sys.stderr.write("verify.py requires the 'jsonschema' package (pip install jsonschema)\n")
    sys.exit(2)

try:  # real RFC 8785 implementation, preferred when available
    import rfc8785  # type: ignore
except ImportError:  # pragma: no cover
    rfc8785 = None

PKG = Path(__file__).resolve().parent
SCHEMAS = PKG.parent.parent / "04-reference" / "schemas"

CORE_COMMITMENT_TYPES = {
    "DECIDE", "ATTEST", "APPEAL", "REMEDY", "OVERRIDE", "EVOLVE", "CLOSE", "DELEGATE",
}

FAILURES = []


def check(ok, label):
    print(("PASS  " if ok else "FAIL  ") + label)
    if not ok:
        FAILURES.append(label)
    return ok


def _reject_float(_s):
    raise ValueError(
        "JSON number with fraction/exponent found; the ICSL string-encoding rule "
        "(legal quantities as strings) is violated and json.dumps is no longer "
        "JCS-equivalent for this document"
    )


def _reject_int_out_of_ijson(s):
    v = int(s)
    if abs(v) > 2**53 - 1:
        raise ValueError("integer outside I-JSON exact range")
    return v


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f, parse_float=_reject_float, parse_int=_reject_int_out_of_ijson)


def assert_canonicalizable(obj, path="$"):
    """Fail closed unless the object satisfies BOTH JCS-guard preconditions.

    (1) No non-string JSON number anywhere: conforming ICSL artifacts encode
        all quantities as strings (ADR-002).
    (2) All member names (object keys) are ASCII: RFC 8785 sorts members by
        UTF-16 code units while Python's sort_keys sorts by code points, and
        the orderings diverge for non-BMP member names, so canonical ICSL
        artifacts require ASCII member names (values may be any Unicode).

    Under these two preconditions sorted compact json.dumps is byte-identical
    to RFC 8785, which is what makes the guarded fallback sound; the ASCII
    member-name rule is additionally an artifact conformance constraint and is
    asserted even when rfc8785 is installed (extended in the 2026-07 repair
    sprint -- see 07-decisions/).
    """
    if isinstance(obj, bool) or obj is None or isinstance(obj, str):
        return
    if isinstance(obj, (int, float)):
        raise ValueError(
            "non-string JSON number at " + path + ": " + repr(obj)
            + " -- ICSL artifacts must encode quantities as strings (ADR-002); "
            "refusing to hash"
        )
    if isinstance(obj, list):
        for i, v in enumerate(obj):
            assert_canonicalizable(v, path + "[" + str(i) + "]")
        return
    if isinstance(obj, dict):
        for k, v in obj.items():
            if not isinstance(k, str) or not k.isascii():
                raise ValueError(
                    "non-ASCII member name at " + path + ": " + repr(k)
                    + " -- canonical ICSL artifacts require ASCII member names "
                    "(UTF-16 vs code-point sort divergence); refusing to hash"
                )
            assert_canonicalizable(v, path + "." + str(k))
        return
    raise ValueError("unhashable JSON value at " + path + ": " + repr(type(obj)))


def jcs_bytes(obj):
    assert_canonicalizable(obj)
    if rfc8785 is not None:
        return rfc8785.dumps(obj)
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def tagged_sha256(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def safe_manifest_path(path):
    """A declared package path must be relative and free of '..' segments."""
    if not isinstance(path, str) or path == "":
        return False
    if path.startswith("/") or path.startswith("\\") or (len(path) > 1 and path[1] == ":"):
        return False
    if posixpath.isabs(path):
        return False
    segments = path.replace("\\", "/").split("/")
    return ".." not in segments


def build_registry():
    resources = []
    for p in sorted(SCHEMAS.glob("*.schema.json")):
        s = load_json(p)
        resources.append((s["$id"], Resource.from_contents(s)))
    return Registry().with_resources(resources)


def validator_for(registry, schema_name):
    schema = load_json(SCHEMAS / schema_name)
    return Draft202012Validator(schema, registry=registry, format_checker=FormatChecker())


def validate(validator, instance, label):
    errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.absolute_path))
    ok = not errors
    check(ok, "schema: " + label)
    for e in errors[:10]:
        print("        at /" + "/".join(str(x) for x in e.absolute_path) + ": " + e.message[:200])
    return ok


def main():
    if rfc8785 is None:
        print("NOTE  rfc8785 not installed; using the guarded JCS approximation "
              "(sound because BOTH preconditions -- no non-string JSON numbers AND "
              "ASCII member names -- are asserted before every hash, failing closed)")
    else:
        print("NOTE  using the installed rfc8785 implementation for canonical bytes")

    registry = build_registry()
    v_protocol = validator_for(registry, "ProtocolVersion.schema.json")
    v_receipt = validator_for(registry, "Receipt.schema.json")
    v_reference = validator_for(registry, "Reference.schema.json")
    v_conformance = validator_for(registry, "ConformanceDeclaration.schema.json")
    v_manifest = validator_for(registry, "PackageManifest.schema.json")
    v_hashvector = validator_for(registry, "HashVector.schema.json")

    # --- manifest ---------------------------------------------------------
    manifest = load_json(PKG / "manifest.json")
    validate(v_manifest, manifest, "manifest.json (PackageManifest)")
    declared = {f["path"]: f["role"] for f in manifest["files"]}
    check("manifest.json" in declared and declared["manifest.json"] == "manifest",
          "manifest declares itself with role manifest")
    for path in declared:
        check(safe_manifest_path(path),
              "declared path is relative and contains no '..' segments: " + repr(path))
    for path in declared:
        if not safe_manifest_path(path):
            continue  # already failed above; do not touch the filesystem with it
        check((PKG / path).is_file(), "declared file exists: " + path)
    on_disk = {
        str(p.relative_to(PKG))
        for p in PKG.rglob("*")
        if p.is_file() and "__pycache__" not in p.parts and not p.name.startswith(".")
    }
    undeclared = sorted(on_disk - set(declared))
    check(not undeclared, "every package file is declared in the manifest"
          + ("" if not undeclared else " (undeclared: " + ", ".join(undeclared) + ")"))

    # --- protocol version -------------------------------------------------
    protocol = load_json(PKG / "protocol-version.json")
    validate(v_protocol, protocol, "protocol-version.json (ProtocolVersion)")
    cps = {cp["id"]: cp for cp in protocol["commitment_points"]}
    check(protocol["conformance_class"] == manifest["profile"],
          "protocol conformance_class matches manifest profile")

    # embedded governed_context is a GovernedContextDescriptor: descriptive only,
    # no runtime members, so no zero-hash convention exists anywhere.
    gcd = protocol.get("governed_context")
    check(isinstance(gcd, dict) and "description" in gcd,
          "governed_context is a descriptor object with a description")
    if isinstance(gcd, dict):
        allowed_members = {"description", "subject_class", "scope", "jurisdiction_note"}
        runtime_members = {"protocol_version_id", "protocol_version_hash",
                           "governed_context_id", "current_time"}
        present_runtime = sorted(set(gcd) & runtime_members)
        check(not present_runtime,
              "governed_context descriptor carries no runtime members"
              + ("" if not present_runtime else " (found: " + ", ".join(present_runtime) + ")"))
        extra = sorted(set(gcd) - allowed_members)
        check(not extra,
              "governed_context descriptor has only descriptor members "
              "(description, subject_class?, scope?, jurisdiction_note?)"
              + ("" if not extra else " (unexpected: " + ", ".join(extra) + ")"))

    # Canonical version-identity hash: JCS + sha256 over the complete
    # ProtocolVersion object.
    # The object contains no hash of itself, so the preimage is
    # non-self-referential and this recomputation is well-defined.
    check("protocol_version_hash" not in protocol,
          "ProtocolVersion carries no hash of itself (non-self-referential preimage)")
    protocol_version_hash = tagged_sha256(jcs_bytes(protocol))
    print("NOTE  protocol_version_hash (recomputed) = " + protocol_version_hash)

    # adverse-flag consistency (ADVERSE_FLAG_OUTCOME_CONSISTENCY)
    for cp in protocol["commitment_points"]:
        outcomes = cp.get("allowed_outcomes", [])
        has_adverse = any(o["effect_class"] in ("adverse", "mixed") for o in outcomes)
        check(cp["binding_effect_basis"]["adverse_outcome_possible"] == has_adverse,
              "adverse_outcome_possible consistent with outcome effect classes: " + cp["id"])

    # commitment_type checks (CP_COMMITMENT_TYPE_REQUIRED / _INVALID,
    # CP_GENERIC_TYPE_FORBIDDEN, APPEAL_TARGET_REQUIRED, REMEDY_TARGET_IDENTIFIED,
    # OVERRIDE_TARGET_AND_BASIS_REQUIRED)
    reference_ids = {r["id"] for r in protocol.get("references", [])}
    for cp in protocol["commitment_points"]:
        ct = cp.get("commitment_type")
        check(ct is not None, "commitment_type present: " + cp["id"])
        check(ct in CORE_COMMITMENT_TYPES,
              "commitment_type is a core type (no EXTENSION/GENERIC in this canonical Core-L2 package): "
              + cp["id"] + " = " + repr(ct))
        aoa = cp.get("acts_on_allowed")
        if aoa is not None:
            check(bool(aoa.get("allowed_effects")),
                  "acts_on_allowed declares allowed_effects: " + cp["id"])
            targets = aoa.get("targets", [])
            check(bool(targets), "acts_on_allowed declares targets: " + cp["id"])
            for t in targets:
                check(t in cps,
                      "acts_on_allowed target is an existing CommitmentPoint id: "
                      + cp["id"] + " -> " + repr(t))
            if "basis_reference" in aoa:
                check(aoa["basis_reference"] in reference_ids,
                      "acts_on_allowed basis_reference resolves to a declared reference: " + cp["id"])
        if ct in ("APPEAL", "REMEDY", "OVERRIDE"):
            check(aoa is not None and bool(aoa.get("allowed_effects")) and bool(aoa.get("targets")),
                  ct + " CP identifies its targets via acts_on_allowed (effects + targets): " + cp["id"])
        if ct == "OVERRIDE":
            check(aoa is not None and "basis_reference" in aoa,
                  "OVERRIDE CP declares basis_reference: " + cp["id"])

    # --- reference --------------------------------------------------------
    reference = load_json(PKG / "references" / "building-act.json")
    validate(v_reference, reference, "references/building-act.json (Reference)")

    # --- conformance declaration -------------------------------------------
    conformance = load_json(PKG / "conformance.json")
    validate(v_conformance, conformance, "conformance.json (ConformanceDeclaration)")
    check(conformance["result"] == "not_run",
          "conformance result stays honest (not_run: the suite is unpublished)")

    # --- receipt chain ------------------------------------------------------
    def verify_receipt_hashes(receipt, label):
        body = {k: v for k, v in receipt.items() if k != "receipt_hash"}
        ok = receipt["receipt_hash"] == tagged_sha256(jcs_bytes(body))
        check(ok, "receipt_hash recomputes: " + label)
        if "content" in receipt:
            check(receipt["content_hash"] == tagged_sha256(jcs_bytes(receipt["content"])),
                  "content_hash recomputes: " + label)
        cp = cps.get(receipt["commitment_point_id"])
        check(cp is not None, "commitment_point_id resolves: " + label)
        if cp is not None:
            tokens = [o["token"] for o in cp.get("allowed_outcomes", [])]
            check(receipt["outcome"] in tokens, "outcome token allowed by CP: " + label)
        check(receipt["protocol_version_id"] == protocol["protocol_version_id"],
              "receipt pins this ProtocolVersion: " + label)
        # Version-identity binding (RECEIPT_PROTOCOL_VERSION_HASH_MATCH).
        check("protocol_version_hash" in receipt,
              "receipt carries protocol_version_hash: " + label)
        if "protocol_version_hash" in receipt:
            check(receipt["protocol_version_hash"] == protocol_version_hash,
                  "receipt protocol_version_hash matches recomputed canonical hash: " + label)
        # derived commitment_type copy (RECEIPT_COMMITMENT_TYPE_MATCH; SHOULD at
        # Core-L2, and every receipt in this package carries it)
        check("commitment_type" in receipt, "receipt carries commitment_type copy: " + label)
        if cp is not None and "commitment_type" in receipt:
            check(receipt["commitment_type"] == cp.get("commitment_type"),
                  "receipt commitment_type matches its CommitmentPoint: " + label)
        return cp

    chain = load_json(PKG / "receipts" / "chain-01.json")
    check(isinstance(chain, list) and len(chain) >= 2, "chain-01.json is a receipt chain")
    by_id = {}
    prev_hash = None
    context_ids = set()
    for i, receipt in enumerate(chain):
        label = "chain-01[" + str(i) + "] " + receipt.get("receipt_id", "?")
        validate(v_receipt, receipt, label + " (Receipt)")
        cp = verify_receipt_hashes(receipt, label)
        if i == 0:
            check(receipt["previous_hash"] is None, "genesis previous_hash is null: " + label)
        else:
            check(receipt["previous_hash"] == prev_hash, "previous_hash links to prior receipt: " + label)
        if "acts_on" in receipt:
            target = receipt["acts_on"]["target_receipt_id"]
            effect = receipt["acts_on"]["effect"]
            check(target in by_id, "acts_on target is an earlier receipt in the chain: " + label)
            allowed = (cp or {}).get("acts_on_allowed", {}).get("allowed_effects", [])
            check(effect in allowed, "acts_on effect allowed by CP acts_on_allowed: " + label)
            # Runtime target membership (ACTS_ON_TARGET_MEMBERSHIP): the acted-on receipt's
            # CommitmentPoint must be among the acting CP's declared targets, so
            # an appeal (or remedy/override) cannot act on an unrelated receipt.
            if target in by_id:
                target_cp_id = by_id[target]["commitment_point_id"]
                allowed_targets = (cp or {}).get("acts_on_allowed", {}).get("targets", [])
                check(target_cp_id in allowed_targets,
                      "acts_on target's CommitmentPoint is in the acting CP's acts_on_allowed.targets: "
                      + label + " (target CP " + target_cp_id + ")")
        prev_hash = receipt["receipt_hash"]
        by_id[receipt["receipt_id"]] = receipt
        context_ids.add(receipt["governed_context_id"])
    check(len(context_ids) == 1, "chain-01 receipts share one governed_context_id")

    # --- deemed receipt -----------------------------------------------------
    deemed = load_json(PKG / "receipts" / "deemed-example.json")
    validate(v_receipt, deemed, "receipts/deemed-example.json (Receipt)")
    verify_receipt_hashes(deemed, "deemed-example")
    check(deemed.get("deemed") is True, "deemed receipt carries deemed: true")
    check(deemed["authority"].startswith("operation_of_law:"),
          "deemed receipt authority is operation_of_law:<legal_source>")
    # Its previous_hash points at a predecessor in its own (unshipped) context
    # chain; linkage is verifiable only against that chain, not this package.
    print("NOTE  deemed-example previous_hash targets a receipt outside this package (documented in README)")

    # --- hash vector ----------------------------------------------------------
    hashes = load_json(PKG / "hashes.json")
    validate(v_hashvector, hashes, "hashes.json (HashVector)")
    entries = {e["path"]: e for e in hashes["entries"]}
    for path in entries:
        check(safe_manifest_path(path),
              "hash-vector path is relative and contains no '..' segments: " + repr(path))
    expected_cover = set(declared) - {"hashes.json"}
    check(set(entries) == expected_cover,
          "hash vector covers every manifest file except self-exempt hashes.json")
    for path, entry in sorted(entries.items()):
        if not safe_manifest_path(path):
            continue  # already failed above; do not touch the filesystem with it
        raw = (PKG / path).read_bytes()
        check(entry["source_hash"] == tagged_sha256(raw), "source_hash recomputes: " + path)
        if path.endswith(".json"):
            check("canonical_hash" in entry, "canonical_hash present for JSON artifact: " + path)
            if "canonical_hash" in entry:
                check(entry["canonical_hash"] == tagged_sha256(jcs_bytes(load_json(PKG / path))),
                      "canonical_hash recomputes: " + path)
        else:
            check("canonical_hash" not in entry, "no canonical_hash for non-JSON file: " + path)

    print()
    if FAILURES:
        print("RESULT: FAIL (" + str(len(FAILURES)) + " failed checks)")
        return 1
    print("RESULT: PASS (all checks green; this is schema + hash verification, not a conformance-suite pass)")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except ValueError as e:
        # JCS-guard trip (non-string number or non-ASCII member name): fail
        # closed with a clear verdict instead of a bare traceback.
        print("GUARD " + str(e))
        print()
        print("RESULT: FAIL (canonicalization guard tripped; failing closed)")
        sys.exit(1)
