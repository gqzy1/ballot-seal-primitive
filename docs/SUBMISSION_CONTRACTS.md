# Intelligent Contracts — submission material

**Title:** BallotSeal — Version-bound Governance Acknowledgements

**Category:** Governance; secondary Developer Tools.

**Repository:** https://github.com/gqzy1/ballot-seal-primitive

**Network:** Stable GenLayer Studionet, chain ID 61999.

**Contract address:** `0x01Da0016b86dA8DD85721A502Cb88B5dfb462d4c`

**Deployment transaction:** `0xd6a6c8a748dbe0ea31f31db1542f4f5026192ad3a5194d3ed8b2c67d53589def`

**Explorer:** https://explorer-studio.genlayer.com/address/0x01Da0016b86dA8DD85721A502Cb88B5dfb462d4c

**Description:** BallotSeal is a reusable GenLayer Intelligent Contract that keeps acknowledgements attached to the exact governance proposal terms a participant reviewed. Each revision is independently assessed across budget, beneficiary, delivery scope, deadline and authority using native GenLayer LLM nondeterminism and an equivalence rule on every dimension. All five SAME labels preserve the consent epoch; material or uncertain terms require a new epoch. Exact text, SHA-256 fingerprints, parent links, immutable versions and per-version acknowledgements make the full history inspectable. Owner namespaces, expected-version checks, grounded quotes and bounded input/output/storage protect state transitions. It is not a vote, quorum mechanism, legal-consent instrument or treasury executor.

**Why GenLayer:** Byte-level diffs cannot determine changes in natural-language obligations. The contract obtains independently computed semantic labels through native GenLayer consensus, then applies deterministic version/epoch rules. Accepted leader explanations are annotations; validators are not claimed to agree on prose word for word.

**Actual evidence:** Seven transactions finalized successfully: deploy; create V1; acknowledge V1; cosmetic V2 with five SAME labels and epoch 1; doubled-budget V3 with CHANGED budget and epoch 2; cosmetic V4 retaining epoch 2 without reviving V1 acknowledgement; acknowledge V4 with both V1/V4 records preserved. Deployed full-source bytes match the A/B canonical SHA-256 `08deb1ff3faf647a239ae99d362894ab57e4a478d5f2c00b19e0f1585e7f39af`. Receipts, model reasons, quotes, quorum information and Finalized reads are in docs/LIVE_ACCEPTANCE.md and evidence/studionet/. Earlier 29 Direct Mode tests use mocked LLM output and are identified separately.

**Reuse:** Integrators can create/revise/acknowledge and query proposal, version and acknowledgement history without fund custody or automatic execution. Interface: docs/abi.json and docs/PROTOCOL.md.

**Current limitations and release gate:** Final dual-track status remains BLOCKED. A missing-terms non-persistent Studio simulation returned null without observable labels, so live UNCERTAIN-label behavior is not claimed as verified. Real change cases outside budget and cosmetic revisions were not repeated. Narrow-screen browser acceptance and external EIP-1193 public-app wallet writes remain unverified. Some validators were cancelled after quorum; preserved receipts must not be described as five unanimous completed executions. No Portal submission has been made. Use only accurate verified fields when the remaining acceptance gates are resolved.

