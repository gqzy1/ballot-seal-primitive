# BallotSeal Primitive

**Keep acknowledgement attached to the exact proposal terms.**

BallotSeal is a reusable GenLayer Intelligent Contract for governance proposal amendments. It seals exact version text, independently classifies five dimensions of change and preserves acknowledgements in immutable history. A meaningful or uncertain change starts a new consent epoch. Later cosmetic revisions cannot revive an older epoch's acknowledgement.

**Release: 0.3 · Target: Stable Studionet / 61999 · Status: UNDEPLOYED.** No real transaction, live model accuracy or onchain consensus is claimed. This release is an offline-validated candidate; see [validation](VALIDATION.md) and [runtime boundaries](docs/RUNTIME.md).

## Why it needs GenLayer

The same budget or delivery obligation can be rephrased; a small edit can also replace a recipient or grant treasury access. A byte diff cannot decide whether the underlying obligation changed. Leader and validators independently interpret the same sealed inputs through GenLayer's native nondeterministic boundary. They must agree on **every dimension's label**, rather than merely agree on a final pass/fail result. Only accepted decisions reach deterministic storage.

Budget, beneficiary, delivery scope, deadline and authority are assessed as `SAME`, `CHANGED` or `UNCERTAIN`. Each result includes a bounded explanation and exact source excerpts. Explanations are the accepted leader's text, not verbatim prose agreed by validators. Quote grounding and schema validation supplement independent label agreement; they do not prove a model cannot be manipulated.

| Result | Deterministic effect |
|---|---|
| All five SAME | CARRY: keep current epoch |
| Any CHANGED | RECONFIRM: increment epoch |
| Otherwise any UNCERTAIN | REVIEW: increment epoch |

Acknowledgement is an explicit acceptance of the exact current text within this registry. REVIEW permits acknowledgement after a person reviews the text; it is not a governance veto or a claim that uncertainty was resolved.

## Use and test

Python **3.12**:

```bash
pip install -r requirements-dev.txt
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest -q tests
# genvm-lint must be on PATH
 genvm-lint setup --version v0.2.16 --contract contracts/ballot_seal.py --json
 genvm-lint check contracts/ballot_seal.py --json
sha256sum -c SOURCE_SHA256.txt
```

Canonical full source: [contracts/ballot_seal.py](contracts/ballot_seal.py). Explicit SDK hash in its first line; v0.2.16 artifact in direct tests. The app holds a byte-identical full copy. [Application](https://github.com/gqzy1/ballotseal-genlayer) · [public walkthrough](https://ballotseal-gqzy1.zsf197176.chatgpt.site/).

[API and architecture](docs/PROTOCOL.md) · [Consensus and threats](docs/SECURITY.md) · [deployment gate](docs/DEPLOYMENT.md) · [Intelligent Contracts submission draft](docs/SUBMISSION_CONTRACTS.md).

## Bounds

16 proposals per address; 32 versions per proposal; 20–6,000 Unicode code points in exact text; 100-character title. Per-address bounds do not prevent Sybil activity. Acknowledgements are unique per address and version, with at most 32 historical records per address per proposal. Public reads return JSON and do not enumerate all users.

No votes, quorum, membership, signatures over external documents, source authenticity, legal consent, fund custody or automatic execution. MIT licensed.

GitHub Pages is configured for Actions but its hosted workflow is still queued; no Pages deployment success is claimed. Intended Pages URL: https://gqzy1.github.io/ballotseal-genlayer/ . The live walkthrough above uses the existing public Site.
