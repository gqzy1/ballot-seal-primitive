# Intelligent Contracts — submission draft

**Title:** BallotSeal — Version-bound Governance Acknowledgements

**Category:** Governance (secondary: Developer Tools)

**Repository:** https://github.com/gqzy1/ballot-seal-primitive

**Description:** BallotSeal is a reusable GenLayer Intelligent Contract that keeps acknowledgements bound to the exact governance proposal terms a participant reviewed. The leader and validators independently compare revisions across budget, beneficiary, delivery scope, deadline and authority. All five unchanged labels preserve the consent epoch; a material or uncertain result opens a new epoch. Immutable proposal versions and per-version acknowledgement records prevent later cosmetic edits from silently resurrecting older consent. The primitive includes per-dimension rationale, source-excerpt grounding, owner namespaces, stale-version guards, bounded storage, JSON views and offline tests.

**GenLayer contribution:** Native LLM nondeterminism with a custom equivalence rule on every independently classified dimension, followed by deterministic history and epoch transitions. Explanations are annotations, not exact prose consensus.

**Reuse:** A governance tool can call create/revise/acknowledge and query version history and acknowledgement applicability without controlling treasury execution or implementing a second classifier.

**Evidence:** See VALIDATION.md, evidence/, canonical full source and docs/abi.json. SDK Direct Mode and static checks are explicitly separated from fixed GenVM and real onchain execution.

**Current disclosure:** Undeployed candidate. Live model accuracy and network consensus are not established. Do not claim a contract address or real transaction. Runtime/deployment evidence gate remains open. Not a voting, quorum or legal-consent protocol.

**Finalization before Portal:** replace this draft's deployment disclosure only with actual verified evidence, where required by the task. Do not remove limitations to make it appear complete. Portal has not been submitted.
