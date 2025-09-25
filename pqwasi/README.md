# PQCWASI - Post-Quantum Cryptography for WebAssembly System Interface

This directory contains WebAssembly System Interface (WASI) implementations of NIST-selected post-quantum cryptographic algorithms.

## Overview

WASI allows WebAssembly modules to run outside web browsers in environments like:
- Serverless functions (AWS Lambda, Cloudflare Workers, etc.)
- Edge computing platforms
- Command-line tools
- Embedded systems with WASI runtimes

## Supported Algorithms

All NIST Round 3 winners and finalists:

### Key Encapsulation Mechanisms (KEM)
- **ML-KEM** (FIPS 203): 512, 768, 1024 bit security
- **HQC-KEM**: 128, 192, 256 bit security
- **Classic McEliece**: 348864, 460896, 6688128, 6960119, 8192128 bit parameters

### Digital Signatures
- **ML-DSA** (FIPS 204): 44, 65, 87 bit security
- **FN-DSA** (Falcon): 512, 1024 bit security

## Build Requirements

### Prerequisites
1. **Rust** with wasm32-wasip1 target:
   ```bash
   rustup target add wasm32-wasip1
   ```

2. **WASI SDK** for C compilation:
   - Download from: https://github.com/WebAssembly/wasi-sdk/releases
   - Set environment variable: `export WASI_SDK_DIR=/path/to/wasi-sdk`

### Building

```bash
./build.sh
```

This will compile the Rust pqcrypto library with WASI support and place the resulting WebAssembly libraries in the appropriate directories.

## Directory Structure

```
pqwasi/
├── build.sh              # Build script
├── README.md             # This file
├── clean/                # Reference implementations
├── avx2/                 # AVX2 optimized versions (when available)
├── refimp/               # Reference implementations
├── optimp/               # Optimized implementations
├── pqclean/              # C implementations from PQClean
├── pqcrypto/             # Rust wrapper library
└── archive/              # Build artifacts (after completion)
```

## Usage

WASI modules can be executed using any WASI-compatible runtime:

```bash
# Example with wasmtime
wasmtime my_pqc_app.wasm

# Example with wasmer
wasmer my_pqc_app.wasm
```

## Security Notes

- All implementations are constant-time where possible
- Memory safety is enforced by WebAssembly
- Cryptographic operations are identical to native implementations

## Testing

Run the build script to compile and test the implementations:

```bash
./build.sh
```

Successful builds will produce `.wasm` files in the respective directories.
