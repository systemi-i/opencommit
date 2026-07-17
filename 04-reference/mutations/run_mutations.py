#!/usr/bin/env python3
"""ICSL schema-mutation regression suite runner.

Added in the 2026-07 repair sprint (see 07-decisions/). Loads the schemas from
../schemas into an $id-keyed registry, validates the baseline artifacts
(including the hash bindings between them), then applies each mutation case
from mutations.json to a deep copy of its baseline and checks the declared
expectation:

  schema_reject             -> Draft 2020-12 validation (with format checking)
                               MUST produce at least one error.
  schema_accept_rule_covers -> validation MUST be clean AND the named covering
                               rule MUST exist in ../rules/catalog.json (the
                               catalog rule, not the schema, is the protection).
  guard_trip                -> the runner's own JCS guard MUST reject the
                               case's probe object (runner self-test; no
                               schema involved).

Exit status 0 if and only if every expectation (including baseline validity
and the baseline hash bindings) is met.

Canonicalization discipline (ADR-002 and the canonicalization profile):
sort_keys/compact json.dumps is byte-identical to RFC 8785 (JCS) ONLY under
TWO preconditions, both of which this runner asserts before hashing anything
and fails closed on violation:

  1. no non-string JSON numbers anywhere (booleans excluded) — RFC 8785
     number serialization otherwise diverges from repr()-style output; and
  2. every member name (object key) is ASCII — RFC 8785 sorts members by
     UTF-16 code units while Python sorts by code points, and the orderings
     diverge for member names containing non-BMP characters.

Conforming ICSL artifacts satisfy both by construction (all quantities are
strings; canonical member names MUST be ASCII). When the `rfc8785` package is
available it is used instead of the guarded approximation; the preconditions
are asserted regardless, because conforming artifacts must satisfy them either
way. This guarded approximation is NOT a general JCS implementation.

Baseline hash bindings (no placeholder-hash convention anywhere): the
ProtocolVersion baseline embeds only a GovernedContextDescriptor (no runtime
members, so it contains no hash of anything). The runtime GovernedContext
sample and the baseline receipt each carry the REAL canonical hash of the
baseline ProtocolVersion, and the receipt carries its REAL receipt_hash
(sha256 over the canonical receipt bytes minus the receipt_hash member). The
runner recomputes and verifies all three bindings as positive controls
(rules RECEIPT_PROTOCOL_VERSION_HASH_MATCH and
GOVERNED_CONTEXT_PROTOCOL_VERSION_HASH_MATCH, plus the ADR-003 receipt
preimage); if baseline.json is ever edited, the suite fails until the pinned
hashes are recomputed.
"""

import copy
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCHEMAS_DIR = (HERE / ".." / "schemas").resolve()
CATALOG_PATH = (HERE / ".." / "rules" / "catalog.json").resolve()
MANIFEST_PATH = HERE / "mutations.json"


# --------------------------------------------------------------------------
# Number discipline + canonicalization (ADR-002 / RFC 8785)
# --------------------------------------------------------------------------

def assert_jcs_preconditions(node, path="$"):
    """Fail loudly unless BOTH JCS-equivalence preconditions hold.

    1. No non-string JSON numbers anywhere (booleans excluded).
    2. All member names (object keys) are ASCII — RFC 8785 sorts members by
       UTF-16 code units, Python by code points; the orderings diverge for
       member names containing non-BMP characters (member-name ordering is
       the only divergence risk once numbers are excluded).

    Under both preconditions, compact sorted json.dumps output is
    byte-identical to RFC 8785 (JCS) canonical form. Conforming ICSL
    artifacts satisfy both by construction.
    """
    if isinstance(node, bool):
        return
    if isinstance(node, (int, float)):
        raise ValueError(
            "JCS precondition violated: non-string JSON number at %s "
            "(value %r). ICSL artifacts encode all quantities as strings "
            "(ADR-002)." % (path, node)
        )
    if isinstance(node, dict):
        for key, value in node.items():
            if not key.isascii():
                raise ValueError(
                    "JCS precondition violated: non-ASCII member name %r "
                    "under %s. Canonical ICSL artifacts restrict member "
                    "names to ASCII (canonicalization profile rule 7; "
                    "UTF-16 vs code-point sort-order divergence)."
                    % (key, path)
                )
            assert_jcs_preconditions(value, "%s.%s" % (path, key))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            assert_jcs_preconditions(value, "%s[%d]" % (path, index))


try:
    import rfc8785  # type: ignore

    CANON_BACKEND = "rfc8785 (real RFC 8785 implementation)"

    def canonical_bytes(obj):
        assert_jcs_preconditions(obj)  # ICSL artifacts must hold regardless
        return rfc8785.dumps(obj)

except ImportError:
    CANON_BACKEND = (
        "guarded json.dumps approximation (JCS-equivalent only because the "
        "no-number and ASCII-member-name preconditions are asserted)"
    )

    def canonical_bytes(obj):
        assert_jcs_preconditions(obj)
        return json.dumps(
            obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode("utf-8")


def tagged_hash(obj):
    return "sha256:" + hashlib.sha256(canonical_bytes(obj)).hexdigest()


# --------------------------------------------------------------------------
# Manifest path safety
# --------------------------------------------------------------------------

def safe_manifest_path(name):
    """Reject absolute paths and any '..' segment in manifest file references."""
    p = Path(name)
    if p.is_absolute() or name.startswith(("/", "\\")):
        raise ValueError("manifest path must be relative: %r" % name)
    if ".." in p.parts:
        raise ValueError("manifest path must not contain '..' segments: %r" % name)
    return HERE / p


# --------------------------------------------------------------------------
# Schema registry (Draft 2020-12, $id-keyed, format-checked)
# --------------------------------------------------------------------------

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

FORMAT_CHECKER = FormatChecker()

if "date-time" not in FORMAT_CHECKER.checkers:
    # jsonschema only enforces date-time when rfc3339-validator is installed;
    # formats MUST be enforced, so register a fallback checker.
    from datetime import datetime

    @FORMAT_CHECKER.checks("date-time")
    def _check_date_time(value):  # noqa: ANN001
        if not isinstance(value, str):
            return True
        try:
            datetime.fromisoformat(value.replace("Z", "+00:00"))
            return True
        except ValueError:
            return False


def load_schemas():
    schemas_by_name = {}
    resources = []
    for path in sorted(SCHEMAS_DIR.glob("*.schema.json")):
        schema = json.loads(path.read_text(encoding="utf-8"))
        schemas_by_name[path.name] = schema
        resources.append(
            (schema["$id"], Resource.from_contents(schema, default_specification=DRAFT202012))
        )
    registry = Registry().with_resources(resources)
    return schemas_by_name, registry


def make_validator(schemas_by_name, registry, schema_file):
    if schema_file not in schemas_by_name:
        raise ValueError("unknown schema file referenced by manifest: %r" % schema_file)
    return Draft202012Validator(
        schemas_by_name[schema_file],
        registry=registry,
        format_checker=FORMAT_CHECKER,
    )


def validation_errors(validator, instance):
    return sorted(validator.iter_errors(instance), key=lambda e: list(e.absolute_path))


# --------------------------------------------------------------------------
# JSON-pointer mutation operations
# --------------------------------------------------------------------------

def _pointer_tokens(pointer):
    if pointer == "":
        raise ValueError("root-document operations are not supported")
    if not pointer.startswith("/"):
        raise ValueError("invalid JSON pointer: %r" % pointer)
    return [t.replace("~1", "/").replace("~0", "~") for t in pointer[1:].split("/")]


def apply_op(doc, op):
    kind = op["op"]
    tokens = _pointer_tokens(op["path"])
    parent = doc
    for token in tokens[:-1]:
        parent = parent[int(token)] if isinstance(parent, list) else parent[token]
    last = tokens[-1]
    if isinstance(parent, list):
        if kind == "add" and last == "-":
            parent.append(op["value"])
            return
        index = int(last)
        if kind == "replace":
            parent[index] = op["value"]
        elif kind == "remove":
            del parent[index]
        elif kind == "add":
            parent.insert(index, op["value"])
        else:
            raise ValueError("unsupported op: %r" % kind)
    else:
        if kind == "remove":
            del parent[last]
        elif kind in ("replace", "add"):
            parent[last] = op["value"]
        else:
            raise ValueError("unsupported op: %r" % kind)


def mutate(baseline, ops):
    mutant = copy.deepcopy(baseline)
    for op in ops:
        apply_op(mutant, op)
    if mutant == baseline:
        raise ValueError("mutation is a no-op; check its JSON pointers")
    return mutant


# --------------------------------------------------------------------------
# Runner
# --------------------------------------------------------------------------

def main():
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    schemas_by_name, registry = load_schemas()
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    catalog_rule_ids = {rule["id"] for rule in catalog["rules"]}

    baseline_pv = json.loads(
        safe_manifest_path(manifest["baseline"]).read_text(encoding="utf-8")
    )
    baseline_receipt = json.loads(
        safe_manifest_path(manifest["baseline_receipt"]).read_text(encoding="utf-8")
    )
    baseline_gc = json.loads(
        safe_manifest_path(manifest["baseline_governed_context"]).read_text(
            encoding="utf-8"
        )
    )
    baseline_conformance = json.loads(
        safe_manifest_path(manifest["baseline_conformance"]).read_text(encoding="utf-8")
    )

    # Both JCS preconditions hold for the baselines before anything is hashed.
    assert_jcs_preconditions(baseline_pv, "$(baseline)")
    assert_jcs_preconditions(baseline_receipt, "$(baseline_receipt)")
    assert_jcs_preconditions(baseline_gc, "$(baseline_governed_context)")
    assert_jcs_preconditions(baseline_conformance, "$(baseline_conformance)")

    # Version identity (shared design fact A): protocol_version_hash is the
    # canonical hash over the complete ProtocolVersion object. The object
    # contains no hash of itself (its embedded governed_context is a
    # descriptor with no runtime members), so the preimage is
    # non-self-referential and no placeholder-hash convention is needed.
    pv_hash = tagged_hash(baseline_pv)

    pv_validator = make_validator(schemas_by_name, registry, manifest["baseline_schema"])
    receipt_validator = make_validator(
        schemas_by_name, registry, manifest["baseline_receipt_schema"]
    )
    gc_validator = make_validator(
        schemas_by_name, registry, manifest["baseline_governed_context_schema"]
    )
    conformance_validator = make_validator(
        schemas_by_name, registry, manifest["baseline_conformance_schema"]
    )
    validators = {
        "protocol_version": pv_validator,
        "receipt": receipt_validator,
        "governed_context": gc_validator,
        "conformance_declaration": conformance_validator,
    }
    baselines = {
        "protocol_version": baseline_pv,
        "receipt": baseline_receipt,
        "governed_context": baseline_gc,
        "conformance_declaration": baseline_conformance,
    }

    print("ICSL schema-mutation suite")
    print("  schemas:            %s" % SCHEMAS_DIR)
    print("  canonicalization:   %s" % CANON_BACKEND)
    print("  protocol_version_hash(baseline) = %s" % pv_hash)
    print("    (pinned verbatim in the baseline receipt and the baseline")
    print("     runtime GovernedContext; recompute both if baseline.json changes)")
    print()

    rows = []
    all_ok = True

    def record(case_id, expected, observed, ok, detail):
        nonlocal all_ok
        all_ok = all_ok and ok
        rows.append((case_id, expected, observed, "PASS" if ok else "FAIL", detail))

    # Baseline preconditions (positive controls).
    for case_id, target in (
        ("B00", "protocol_version"),
        ("R00", "receipt"),
        ("C00", "governed_context"),
        ("D00", "conformance_declaration"),
    ):
        errors = validation_errors(validators[target], baselines[target])
        problems = [_summarize(errors)] if errors else []
        if not errors:
            # Hash-binding controls (mirror the catalog match rules).
            if target == "receipt":
                if baseline_receipt.get("protocol_version_hash") != pv_hash:
                    problems.append(
                        "protocol_version_hash mismatch "
                        "(RECEIPT_PROTOCOL_VERSION_HASH_MATCH): expected %s"
                        % pv_hash
                    )
                preimage = {
                    k: v for k, v in baseline_receipt.items() if k != "receipt_hash"
                }
                if baseline_receipt.get("receipt_hash") != tagged_hash(preimage):
                    problems.append(
                        "receipt_hash does not match the ADR-003 preimage "
                        "(canonical receipt bytes minus receipt_hash): "
                        "expected %s" % tagged_hash(preimage)
                    )
            elif target == "governed_context":
                if baseline_gc.get("protocol_version_hash") != pv_hash:
                    problems.append(
                        "protocol_version_hash mismatch "
                        "(GOVERNED_CONTEXT_PROTOCOL_VERSION_HASH_MATCH): "
                        "expected %s" % pv_hash
                    )
        ok = not problems
        observed = "hash_mismatch" if (not errors and problems) else _observed(errors)
        detail = "" if ok else " ".join(problems)
        record(case_id, "schema_accept (baseline %s)" % target, observed, ok, detail)

    # Mutation cases.
    for case in manifest["cases"]:
        case_id = case["id"]
        target = case["target"]
        expected = case["expected"]
        if expected == "guard_trip":
            # Runner self-test: the JCS guard itself MUST reject the probe.
            try:
                canonical_bytes(case["probe"])
            except ValueError as exc:
                record(case_id, expected, "guard_trip", True, str(exc)[:110])
            else:
                record(
                    case_id,
                    expected,
                    "guard_silent",
                    False,
                    "JCS guard accepted a probe it must reject",
                )
            continue
        try:
            mutant = mutate(baselines[target], case["ops"])
        except Exception as exc:  # noqa: BLE001 — surface as a failed row
            record(case_id, expected, "mutation_error", False, str(exc))
            continue
        errors = validation_errors(validators[target], mutant)
        if expected == "schema_reject":
            ok = bool(errors)
            detail = _summarize(errors) if errors else "mutant validated cleanly"
        elif expected == "schema_accept_rule_covers":
            rule_id = case.get("covering_rule", "")
            rule_known = rule_id in catalog_rule_ids
            ok = (not errors) and rule_known
            if errors:
                detail = "unexpected schema errors: %s" % _summarize(errors)
            elif not rule_known:
                detail = "covering rule %r not found in catalog" % rule_id
            else:
                detail = "covered by catalog rule %s" % rule_id
        else:
            ok = False
            detail = "unknown expectation %r" % expected
        record(case_id, expected, _observed(errors), ok, detail)

    _print_table(rows)
    met = sum(1 for row in rows if row[3] == "PASS")
    print()
    print("%d/%d expectations met." % (met, len(rows)))
    if not all_ok:
        print("FAILURE: at least one expectation was not met.")
        return 1
    print("SUCCESS: all expectations met.")
    return 0


def _observed(errors):
    return "schema_reject (%d error%s)" % (len(errors), "" if len(errors) == 1 else "s") \
        if errors else "schema_accept"


def _summarize(errors, limit=1):
    parts = []
    for error in errors[:limit]:
        path = "/" + "/".join(str(p) for p in error.absolute_path)
        message = error.message
        if len(message) > 90:
            message = message[:87] + "..."
        parts.append("%s: %s" % (path, message))
    if len(errors) > limit:
        parts.append("(+%d more)" % (len(errors) - limit))
    return " ".join(parts)


def _print_table(rows):
    header = ("CASE", "EXPECTED", "OBSERVED", "VERDICT", "DETAIL")
    widths = [
        max(len(header[i]), max(len(str(row[i])) for row in rows))
        for i in range(4)
    ]
    fmt = "  ".join("%%-%ds" % w for w in widths) + "  %s"
    print(fmt % header)
    print(fmt % tuple("-" * w for w in widths + [len(header[4])]))
    for row in rows:
        print(fmt % row)


if __name__ == "__main__":
    sys.exit(main())
