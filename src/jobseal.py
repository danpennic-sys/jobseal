#!/usr/bin/env python3
"""
JobSeal — local-first job evidence logger and QuantumGuard pack generator.
Offline. Deterministic. Compatible with QuantumGuard CONTRACT-v1.
"""

import argparse
import base64
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    from cryptography.hazmat.primitives import serialization
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def load_or_generate_key(key_path: Path):
    if key_path.exists():
        with open(key_path, "rb") as f:
            private_key = Ed25519PrivateKey.from_private_bytes(f.read())
        return private_key
    if not CRYPTO_AVAILABLE:
        print("Warning: cryptography not installed. Using demo key (not for production).", file=sys.stderr)
        return None
    private_key = Ed25519PrivateKey.generate()
    with open(key_path, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption()
        ))
    return private_key

def build_payload(job: dict) -> bytes:
    # Deterministic canonical JSON
    canonical = json.dumps(job, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return canonical

def seal_bundle(payload: bytes, private_key) -> dict:
    payload_hash = sha256_hex(payload)
    if private_key is None or not CRYPTO_AVAILABLE:
        # Demo placeholder for testing structure
        signature = "0" * 128
        public_key_hex = "0" * 64
    else:
        signature_bytes = private_key.sign(bytes.fromhex(payload_hash))
        signature = signature_bytes.hex()
        public_key = private_key.public_key()
        public_key_hex = public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        ).hex()
    return {
        "version": "1",
        "payload": base64.b64encode(payload).decode("ascii"),
        "payload_hash": payload_hash,
        "signature": signature,
        "public_key": public_key_hex,
        "alg": "ed25519"
    }

def main():
    parser = argparse.ArgumentParser(description="JobSeal — seal job evidence into QuantumGuard packs")
    parser.add_argument("--job", type=Path, help="Path to job JSON")
    parser.add_argument("--demo", action="store_true", help="Run with built-in demo job")
    parser.add_argument("--out", type=Path, default=Path("sealed-pack.json"), help="Output bundle path")
    parser.add_argument("--key", type=Path, default=Path.home() / ".jobseal" / "key.bin", help="Ed25519 private key path")
    args = parser.parse_args()

    if args.demo:
        job = {
            "operator": "Field Operator",
            "client": "Demo Client LLC",
            "job_id": "JOB-2026-001",
            "description": "HVAC filter replacement and system check",
            "notes": "Completed on-site. All systems nominal. Photos hashed.",
            "media_hashes": ["a1b2c3d4e5f6...", "f6e5d4c3b2a1..."],
            "completed_at": datetime.now(timezone.utc).isoformat(),
            "total": 185.00
        }
    elif args.job:
        with open(args.job) as f:
            job = json.load(f)
    else:
        parser.print_help()
        sys.exit(1)

    payload = build_payload(job)
    key_dir = args.key.parent
    key_dir.mkdir(parents=True, exist_ok=True)
    private_key = load_or_generate_key(args.key)
    bundle = seal_bundle(payload, private_key)

    with open(args.out, "w") as f:
        json.dump(bundle, f, indent=2)
    print(f"Sealed pack written to {args.out}")
    print(f"Verify with: qg verify {args.out}  (or QuantumGuard CLI)")
    print(f"Payload hash: {bundle['payload_hash']}")

if __name__ == "__main__":
    main()
