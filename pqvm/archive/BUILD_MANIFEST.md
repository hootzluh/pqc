Build Manifest — pqvm (scaffold)

Planned steps (high-level):
1) Record environment versions
2) Create workspace and copy-in sources
3) Implement target-specific wrappers (Substrate/CosmWasm/EVM/Move)
4) Build wasm/native artifacts
5) Run KATs and benchmarks
6) Archive intermediates and logs

Each step will log to archive/logs/<timestamp>-<step>.log

