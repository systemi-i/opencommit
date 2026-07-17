#!/usr/bin/env python3
"""Persisted attack runner for the ICSL Core-L2 proof exemplar.

Demonstrates that verify.py catches semantic tampering, not just byte
corruption. For each attack the runner copies the repo subtree into a fresh
temp tree PRESERVING the repo-relative layout (verify.py resolves the schemas
at ../../04-reference/schemas relative to itself; a flat copy crashes -- this
was demonstrated during the audit), applies exactly one semantic violation,
then LEGITIMATELY recomputes every hash the attacker could recompute
(content_hash, receipt_hash, previous_hash linkage, the whole hash vector) so
that only the semantic violation remains, and requires verify.py to fail with
the expected diagnostic.

Control: an unmodified copy must verify (exit 0).

Attacks (each must be caught -- verify.py exit != 0 AND expected marker seen):
  A1  retarget the appeal-disposition receipt's acts_on at the intake receipt
      (ACTS_ON_TARGET_MEMBERSHIP: cp-01-intake is not among the acting CP's
      acts_on_allowed.targets);
  A2  corrupt one chain receipt's protocol_version_hash
      (RECEIPT_PROTOCOL_VERSION_HASH_MATCH);
  A3  mutate the runtime deemed-example receipt's pinned hash --
      context/receipt version mismatch (same rule, deemed receipt);
  A4  declare a manifest path containing a '..' segment (path safety);
  A5  JCS guard vector: inject a non-ASCII member name into a canonical
      artifact copy (the ASCII-member-name guard must trip, failing closed).

Exit status: 0 iff the control passes AND every attack is caught.

Usage: python3 attacks.py        (requires: pip install jsonschema)
"""

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PKG = Path(__file__).resolve().parent          # .../08-examples/permit-core-l2
REPO = PKG.parent.parent                        # repo root
REL_PKG = PKG.relative_to(REPO)                 # 08-examples/permit-core-l2

RESULTS = []


def jcs_bytes(obj):
    """Attacker-side canonical bytes (sorted compact json.dumps).

    Sound for these artifacts: the package contains no JSON numbers and only
    ASCII member names, so this equals RFC 8785 byte-for-byte. A5 deliberately
    breaks the ASCII precondition in the artifact under attack; for that file
    the runner forges hashes with this same non-guarded serializer, exactly as
    an attacker would -- the point is that verify.py refuses to accept it.
    """
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def tagged_sha256(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def dump(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write("\n")


def make_tree():
    """Copy 04-reference/ and 08-examples/ into a temp tree, preserving the
    repo-relative layout so verify.py's ../../04-reference/schemas resolves."""
    root = Path(tempfile.mkdtemp(prefix="icsl-attack-"))
    for sub in ("04-reference", "08-examples"):
        shutil.copytree(REPO / sub, root / sub,
                        ignore=shutil.ignore_patterns("__pycache__", ".*"))
    return root


def rehash_receipts(pkg):
    """Legitimately recompute content_hash, receipt_hash and previous_hash
    linkage for chain-01, and self-hashes for the deemed receipt, so only the
    injected semantic violation remains detectable."""
    chain_path = pkg / "receipts" / "chain-01.json"
    chain = load(chain_path)
    prev = None
    for receipt in chain:
        receipt["previous_hash"] = prev
        if "content" in receipt:
            receipt["content_hash"] = tagged_sha256(jcs_bytes(receipt["content"]))
        body = {k: v for k, v in receipt.items() if k != "receipt_hash"}
        receipt["receipt_hash"] = tagged_sha256(jcs_bytes(body))
        prev = receipt["receipt_hash"]
    dump(chain_path, chain)

    deemed_path = pkg / "receipts" / "deemed-example.json"
    deemed = load(deemed_path)
    # its previous_hash targets a receipt outside the package; keep it
    if "content" in deemed:
        deemed["content_hash"] = tagged_sha256(jcs_bytes(deemed["content"]))
    body = {k: v for k, v in deemed.items() if k != "receipt_hash"}
    deemed["receipt_hash"] = tagged_sha256(jcs_bytes(body))
    dump(deemed_path, deemed)


def rehash_vector(pkg):
    """Regenerate hashes.json over the (possibly tampered) tree, exactly as an
    attacker with write access would, so byte-level hash checks all pass."""
    manifest = load(pkg / "manifest.json")
    entries = []
    for f in manifest["files"]:
        path = f["path"]
        if path == "hashes.json":
            continue
        fs_path = pkg / path
        if not fs_path.is_file():
            continue  # unsafe/phantom declared path (A4): nothing to hash
        entry = {"path": path, "source_hash": tagged_sha256(fs_path.read_bytes())}
        if path.endswith(".json"):
            entry["canonical_hash"] = tagged_sha256(jcs_bytes(load(fs_path)))
        entries.append(entry)
    dump(pkg / "hashes.json", {"kind": "HashVector", "algorithm": "sha256", "entries": entries})


def run_verify(pkg):
    proc = subprocess.run([sys.executable, str(pkg / "verify.py")],
                          capture_output=True, text=True)
    return proc.returncode, proc.stdout + proc.stderr


def record(name, ok, detail):
    RESULTS.append((name, ok))
    print(("PASS  " if ok else "FAIL  ") + name + " -- " + detail)


def run_attack(name, description, mutate, marker, rehash=True):
    root = make_tree()
    try:
        pkg = root / REL_PKG
        mutate(pkg)
        if rehash:
            rehash_receipts(pkg)
        rehash_vector(pkg)
        code, out = run_verify(pkg)
        caught = code != 0
        marker_seen = marker in out
        record(name, caught and marker_seen,
               description
               + " | verify exit=" + str(code)
               + (", expected diagnostic seen" if marker_seen
                  else ", EXPECTED DIAGNOSTIC MISSING (" + marker + ")"))
    finally:
        shutil.rmtree(root, ignore_errors=True)


# --- attack mutations -------------------------------------------------------

def a1_retarget_acts_on(pkg):
    """Retarget the appeal-disposition receipt's acts_on at the intake receipt."""
    chain_path = pkg / "receipts" / "chain-01.json"
    chain = load(chain_path)
    disposition = next(r for r in chain if r["commitment_point_id"] == "cp-10-appeal-disposition")
    intake = next(r for r in chain if r["commitment_point_id"] == "cp-01-intake")
    disposition["acts_on"]["target_receipt_id"] = intake["receipt_id"]
    dump(chain_path, chain)


def a2_corrupt_chain_pv_hash(pkg):
    """Corrupt one chain receipt's protocol_version_hash."""
    chain_path = pkg / "receipts" / "chain-01.json"
    chain = load(chain_path)
    chain[0]["protocol_version_hash"] = "sha256:" + "ab" * 32
    dump(chain_path, chain)


def a3_mutate_deemed_pinned_hash(pkg):
    """Mutate the runtime deemed receipt's pinned hash (version mismatch)."""
    deemed_path = pkg / "receipts" / "deemed-example.json"
    deemed = load(deemed_path)
    h = deemed["protocol_version_hash"]
    flipped = h[:-1] + ("0" if h[-1] != "0" else "1")
    deemed["protocol_version_hash"] = flipped
    dump(deemed_path, deemed)


def a4_manifest_dotdot_path(pkg):
    """Declare a manifest path that escapes the package via '..'."""
    manifest_path = pkg / "manifest.json"
    manifest = load(manifest_path)
    manifest["files"].append({"path": "../evil.json", "role": "reference"})
    dump(manifest_path, manifest)


def a5_non_ascii_member_name(pkg):
    """Inject a non-ASCII member name into a canonical artifact copy."""
    ref_path = pkg / "references" / "building-act.json"
    ref = load(ref_path)
    ref["locatör_note"] = "smuggled member with a non-ASCII name"
    dump(ref_path, ref)


def main():
    print("attack runner: temp tree preserves repo-relative layout "
          "(04-reference/ + 08-examples/), verify.py run per copy\n")

    # --- control ------------------------------------------------------------
    root = make_tree()
    try:
        code, out = run_verify(root / REL_PKG)
        record("CONTROL unmodified package verifies", code == 0,
               "verify exit=" + str(code))
        if code != 0:
            print(out)
    finally:
        shutil.rmtree(root, ignore_errors=True)

    # --- attacks --------------------------------------------------------------
    # markers are anchored to verify.py's "FAIL  " prefix so a PASS line
    # carrying the same label text can never satisfy the expectation
    run_attack(
        "A1 acts_on retargeted at the intake receipt is caught",
        "disposition receipt's acts_on now targets cp-01-intake; hashes recomputed",
        a1_retarget_acts_on,
        "FAIL  acts_on target's CommitmentPoint is in the acting CP's acts_on_allowed.targets")
    run_attack(
        "A2 corrupted chain protocol_version_hash is caught",
        "chain-01[0] pins a bogus ProtocolVersion hash; receipt hashes recomputed",
        a2_corrupt_chain_pv_hash,
        "FAIL  receipt protocol_version_hash matches recomputed canonical hash")
    run_attack(
        "A3 mutated deemed-receipt pinned hash is caught",
        "deemed-example pins a flipped hash (context/receipt version mismatch)",
        a3_mutate_deemed_pinned_hash,
        "FAIL  receipt protocol_version_hash matches recomputed canonical hash")
    run_attack(
        "A4 manifest path with '..' segment is caught",
        "manifest declares ../evil.json; hash vector regenerated",
        a4_manifest_dotdot_path,
        "FAIL  declared path is relative and contains no '..' segments: '../evil.json'",
        rehash=False)
    run_attack(
        "A5 non-ASCII member name trips the JCS guard (fail closed)",
        "references/building-act.json gains member 'locatör_note'; "
        "attacker-forged hashes recorded",
        a5_non_ascii_member_name,
        "non-ASCII member name",
        rehash=False)

    print()
    failed = [name for name, ok in RESULTS if not ok]
    if failed:
        print("RESULT: FAIL (" + str(len(failed)) + " unmet expectations: "
              + "; ".join(failed) + ")")
        return 1
    print("RESULT: PASS (control verified; all 5 attacks caught with the expected diagnostics)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
