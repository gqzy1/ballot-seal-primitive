# BallotSeal

**Keep consent attached to the exact proposal terms.**

BallotSeal is a GenLayer governance primitive for recording acknowledgements against a versioned proposal and determining whether a later version remains within the acknowledged context.

## Core rule

Compare proposal versions across five decision dimensions:

1. **Budget**
2. **Beneficiary**
3. **Delivery scope**
4. **Deadline**
5. **Authority**

An unchanged dimension may retain its existing acknowledgement epoch. A material change—or a result that cannot be classified confidently—requires fresh acknowledgement. Earlier acknowledgements remain part of the history and are never silently rewritten.

## Scope and safety

- BallotSeal is **not** a voting or quorum system.
- An acknowledgement record is not legal consent and does not automatically execute a proposal.
- Local preview fixtures are demonstrations only; they do not represent a live AI consensus result or an on-chain transaction.
- Custom proposal workflows require the intended GenLayer contract deployment and wallet interaction.
- No deployment, wallet write, or on-chain transaction is implied by this repository.

## Repository layout

The contract implementation, tests, and supporting documentation will be maintained here as the **Intelligent Contracts** track. The companion Projects application is maintained separately so that the contract primitive and user-facing app can be reviewed independently.

## Development status

This repository has just been initialized. Treat runtime compatibility, full test execution, and live-chain behavior as unverified until their evidence is recorded in the repository.
