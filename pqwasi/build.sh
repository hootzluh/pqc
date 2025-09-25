#!/bin/bash

# PQCWASI Build Script
# Builds WebAssembly System Interface (WASI) versions of PQC algorithms

set -e

echo "PQCWASI Build Script"
echo "===================="

# Check if WASI SDK is available
# Set WASI_SDK_DIR if not already set
if [ -z "$WASI_SDK_DIR" ]; then
    if [ -d "$HOME/wasi-sysroot" ]; then
        export WASI_SDK_DIR="$HOME/wasi-sysroot/share/wasi-sysroot"
        echo "Auto-detected WASI_SDK_DIR: $WASI_SDK_DIR"
    else
        echo "Warning: WASI_SDK_DIR environment variable not set"
        echo "Please install WASI SDK and set WASI_SDK_DIR"
        echo ""
        echo "Installation instructions:"
        echo "1. Download WASI SDK from: https://github.com/WebAssembly/wasi-sdk/releases"
        echo "2. Extract to a directory (e.g., /opt/wasi or ~/wasi)"
        echo "3. Set WASI_SDK_DIR environment variable"
        echo "4. Ensure wasm32-wasip1 target is installed: rustup target add wasm32-wasip1"
        echo ""
        echo "Example:"
        echo "export WASI_SDK_DIR=/opt/wasi/wasi-sysroot"
        echo ""
        exit 1
    fi
fi

echo "Building PQC algorithms for WASI..."

# Build the Rust pqcrypto library for WASI
cd pqcrypto
echo "Building Rust pqcrypto library for wasm32-wasip1..."

# Try to build with all features
if cargo build --target wasm32-wasip1 --release --features serialization; then
    echo "✓ Successfully built pqcrypto with all features"
    cp target/wasm32-wasip1/release/*.rlib ../clean/
    echo "✓ Copied WASI libraries to clean/ directory"
else
    echo "✗ Failed to build with all features, trying minimal build..."

    # Try minimal build
    if cargo build --target wasm32-wasip1 --release --no-default-features --features pqcrypto-mlkem; then
        echo "✓ Successfully built minimal pqcrypto"
        cp target/wasm32-wasip1/release/*.rlib ../clean/
        echo "✓ Copied WASI libraries to clean/ directory"
    else
        echo "✗ Build failed. Check WASI SDK installation."
        exit 1
    fi
fi

cd ..

echo "Build completed successfully!"
echo "WASI-compatible libraries are in the clean/ directory."
