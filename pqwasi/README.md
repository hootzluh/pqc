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

### Pre-built Libraries

The WASI-compatible Rust libraries are pre-built and available in the `clean/` directory:

- `libpqcrypto_mlkem.rlib` - ML-KEM (512, 768, 1024) implementations
- `libpqcrypto_mldsa.rlib` - ML-DSA (44, 65, 87) implementations
- `libpqcrypto_hqc.rlib` - HQC-KEM (128, 192, 256) implementations
- `libpqcrypto_falcon.rlib` - Falcon signature algorithms
- `libpqcrypto_classicmceliece.rlib` - Classic McEliece KEM algorithms
- `libpqcrypto_sphincsplus.rlib` - SPHINCS+ signature algorithms

### Testing with WASI Runtimes

To test the compiled WASI modules:

1. **Install a WASI runtime** (e.g., wasmtime):
   ```bash
   curl -sSfL https://github.com/bytecodealliance/wasmtime/releases/latest/download/wasmtime-x86_64-macos.tar.xz | tar xJf -
   sudo mv wasmtime-x86_64-macos/wasmtime /usr/local/bin/
   ```

2. **Create a test application** using the pqcrypto library:
   ```rust
   use pqcrypto_mlkem::mlkem768;
   use pqcrypto_mldsa::mldsa65;

   fn main() {
       // Test ML-KEM-768
       let (pk, sk) = mlkem768::keypair();
       let (ct, ss) = mlkem768::encapsulate(&pk);
       let dec_ss = mlkem768::decapsulate(&ct, &sk);
       assert_eq!(ss, dec_ss);

       // Test ML-DSA-65
       let (pk, sk) = mldsa65::keypair();
       let message = b"Hello, post-quantum world!";
       let signature = mldsa65::sign(&message, &sk);
       let is_valid = mldsa65::verify(&signature, &message, &pk);
       assert!(is_valid);

       println!("✓ All PQCWASI tests passed!");
   }
   ```

3. **Compile for WASI**:
   ```bash
   cargo build --target wasm32-wasip1 --release
   ```

4. **Run with wasmtime**:
   ```bash
   wasmtime target/wasm32-wasip1/release/your-app.wasm
   ```

### Verification

The implementation has been verified to:
- ✅ Compile successfully for wasm32-wasip1 target
- ✅ Include all required NIST PQC algorithms
- ✅ Support all security levels (ML-KEM 512/768/1024, ML-DSA 44/65/87, HQC 128/192/256)
- ✅ Be compatible with standard WASI runtimes
- ✅ Ready for serverless and edge deployment environments
