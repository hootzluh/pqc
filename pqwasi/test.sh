#!/bin/bash

# PQCWASI Test Script
# Tests the WASI implementations

echo "PQCWASI Test Script"
echo "==================="

# Check if WASI runtime is available
if ! command -v wasmtime &> /dev/null && ! command -v wasmer &> /dev/null; then
    echo "Warning: No WASI runtime found (wasmtime or wasmer)"
    echo "Install a WASI runtime to test the compiled modules:"
    echo "  brew install wasmtime  # or"
    echo "  curl https://get.wasmer.io -sSfL | sh"
    echo ""
fi

# Check if implementations exist
if [ ! -d "clean" ] || [ ! -f "clean/libpqcrypto.a" ]; then
    echo "No WASI implementations found. Run ./build.sh first."
    exit 1
fi

echo "✓ WASI implementations found"
echo "✓ PQCWASI setup is ready for testing"

# Note: Actual cryptographic testing would require WASI-compatible test binaries
# For now, we verify the build artifacts exist
