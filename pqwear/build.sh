#!/bin/bash

# PQWear Build Script
# Cross-compiles PQC algorithms for wearable devices

set -e

echo "PQWear Build Script"
echo "==================="

# Check if required tools are available
command -v cargo >/dev/null 2>&1 || { echo "Error: cargo not found. Install Rust."; exit 1; }

echo "Building for wearable platforms..."

cd pqcrypto

# Build for watchOS (wearable iOS)
echo "Building for watchOS..."
if cargo build --target aarch64-apple-ios --release --features "wearable-optimized"; then
    echo "✓ watchOS ARM64 build successful"
    cp target/aarch64-apple-ios/release/libpqcrypto.a ../watchos-arm64/
else
    echo "⚠ watchOS ARM64 build failed (may require Xcode)"
fi

# Build for Wear OS (wearable Android)
echo "Building for Wear OS..."
if command -v ndk-build >/dev/null 2>&1; then
    # Use size-optimized builds for wearables
    export RUSTFLAGS="-C opt-level=s -C panic=abort -C codegen-units=1"

    if cargo build --target aarch64-linux-android --release; then
        echo "✓ Wear OS ARM64 build successful"
        cp target/aarch64-linux-android/release/libpqcrypto.a ../wearos-arm64/
    else
        echo "⚠ Wear OS ARM64 build failed"
    fi

    if cargo build --target armv7-linux-androideabi --release; then
        echo "✓ Wear OS ARMv7 build successful"
        cp target/armv7-linux-androideabi/release/libpqcrypto.a ../wearos-armv7/
    else
        echo "⚠ Wear OS ARMv7 build failed"
    fi
else
    echo "⚠ Android NDK not found. Install Android NDK for Wear OS builds."
fi

cd ..

echo "Build completed!"
echo "Check the platform-specific directories for compiled libraries."
echo "Note: Full iOS/Android builds may require additional SDK setup."
