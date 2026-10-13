# JobSeal

**Local-first job evidence logger and QuantumGuard pack generator for field operators.**

Offline. Deterministic. Pay once. Compatible with QuantumGuard CONTRACT-v1, VeriQuote, and Evidence-Core.

## Why JobSeal?

Field operators lose money when clients dispute completed work. JobSeal captures the job details, notes, and media hashes, then seals them into a client-verifiable QuantumGuard evidence bundle.

- No SaaS. No subscription. Runs completely offline after key setup.
- Clients verify the pack with the free QuantumGuard verifier.
- Pairs with FieldQuote / VeriQuote for quoting and LedgerLite / Chaser for invoicing.

## Quick Start

```bash
pip install cryptography   # optional but recommended for real signatures
python3 src/jobseal.py --demo
python3 src/jobseal.py --job samples/job-001.json --out sealed.json
```

Verify the output with the QuantumGuard CLI:

```bash
qg verify sealed.json
```

## What you can sell

| SKU       | Price | Includes                                      |
|-----------|-------|-----------------------------------------------|
| Operator  | $49   | CLI + key setup guide + 1-year email support  |
| Command   | $149  | + templates + batch mode + reseller rights    |
| Agency    | $399  | + white-label + onboarding call               |

Purchase / access: danpennic@gmail.com

Source remains free under Apache-2.0 OR MIT. Commercial Operator Pack sold separately.

## Stack Fit

- Python CLI (same family as VeriQuote, LedgerLite, PlanClose)
- Emits QuantumGuard CONTRACT-v1 bundles (Ed25519)
- Deterministic payload hashing
- Local key storage

## License

Apache-2.0 OR MIT
