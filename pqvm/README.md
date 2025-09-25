pqvm — Post-Quantum Cryptography for Blockchain/VM Targets

Overview
- Targets: Substrate (WASM runtime pallet and host functions), CosmWasm contracts, EVM precompiles, Move bindings.
- Algorithms: ML-KEM (Kyber), ML-DSA (Dilithium), FN-DSA (Falcon), HQC-KEM — NIST parameter variants. (Classic McEliece omitted due to memory constraints in blockchain environments)
- Isolation: All sources copied-in under pqvm/; no runtime dependency on paths outside pqvm/.

Build order
- Per user request: pqvm first, then pqnostd.

Structure
- substrate/pallet: FRAME pallet and wasm blob(s)
- cosmwasm/contracts/pqc_contract: CosmWasm contract example using PQC host bindings or static include
- evm/precompiles: Native precompile library + emulator tests
- move/move_bindings: Move VM native bindings or examples
- tools/: KAT runner and benchmark scripts
- benchmarks/: gas/runtime metrics
- archive/: logs, env snapshots, and build intermediates

Status
- Initial scaffolding only. Implementations and KAT runners will be added incrementally.

Notes
- Record environment versions to archive/env-versions.txt
- All commands must log to archive/logs/<timestamp>-<step>.log
- On any failure, create archive/ERROR_REPORT.md as specified.

