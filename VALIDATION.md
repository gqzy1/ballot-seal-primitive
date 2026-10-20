# Current validation — V0.3

This report applies only to `contracts/ballot_seal.py` matching SOURCE_SHA256.txt, not earlier V0.1/V0.2 claims.

| Command | Result |
|---|---|
| PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest -q tests | 29 PASS in SDK Direct Mode, native SDK containers and mocked LLMs |
| genvm-lint setup --version v0.2.16 --contract contracts/ballot_seal.py --json | PASS, pinned artifacts |
| genvm-lint check contracts/ballot_seal.py --json | PASS: 3 AST checks and SDK validation; 3 writes / 4 views |
| genvm-lint schema contracts/ballot_seal.py --output docs/abi.json | PASS |
| genvm-lint typecheck contracts/ballot_seal.py --json | PASS: 0 errors / 0 warnings with configured Pyright |
| sha256sum -c SOURCE_SHA256.txt | Exact canonical source digest, also copied into B |

Raw outputs in evidence/. Commands were run in Python 3.12 with gltest 0.29.2 and genvm-linter 0.11.0. These automated tests do not run a fixed WASM executor or real LLM. Hosted GenVM execution and native semantic consensus were validated separately in the deployed lifecycle. Tests cover invalid and uncertain output, every changed dimension, owner namespace isolation, exact digests, consent continuation/reset/non-resurrection, acknowledgement immutability, duplicate/stale/invalid operations and storage bounds. Independent validator invocation rejects same-final-action results with different changed dimensions and allows reason-text variation.

Hosted target-runtime and native-consensus evidence are recorded in [docs/LIVE_ACCEPTANCE.md](docs/LIVE_ACCEPTANCE.md). Runtime and coverage limits are documented there.
