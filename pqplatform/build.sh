#!/bin/bash

# PQPlatform Build Script
# Cross-compiles PQC algorithms for smart TV and smart home platforms

set -e

echo "PQPlatform Build Script"
echo "======================="

# Check if required tools are available
command -v cargo >/dev/null 2>&1 || { echo "Error: cargo not found. Install Rust."; exit 1; }

echo "Building for smart TV and smart home platforms..."

cd pqcrypto

# Build for tvOS (Apple TV)
echo "Building for tvOS..."
if cargo build --target aarch64-apple-ios --release --features "smart-home-optimized"; then
    echo "✓ tvOS ARM64 build successful"
    cp target/aarch64-apple-ios/release/libpqcrypto.a ../tvos-arm64/
else
    echo "⚠ tvOS ARM64 build failed (may require Xcode)"
fi

if cargo build --target x86_64-apple-ios --release --features "smart-home-optimized"; then
    echo "✓ tvOS x86_64 build successful"
    cp target/x86_64-apple-ios/release/libpqcrypto.a ../tvos-x86_64/
else
    echo "⚠ tvOS x86_64 build failed (may require Xcode)"
fi

# Build for Android TV
echo "Building for Android TV..."
if command -v ndk-build >/dev/null 2>&1; then
    # Use network-optimized builds for smart home devices
    export RUSTFLAGS="-C opt-level=3 -C codegen-units=4"

    if cargo build --target aarch64-linux-android --release --features "smart-home-optimized"; then
        echo "✓ Android TV ARM64 build successful"
        cp target/aarch64-linux-android/release/libpqcrypto.a ../androidtv-arm64/
    else
        echo "⚠ Android TV ARM64 build failed"
    fi

    if cargo build --target armv7-linux-androideabi --release --features "smart-home-optimized"; then
        echo "✓ Android TV ARMv7 build successful"
        cp target/armv7-linux-androideabi/release/libpqcrypto.a ../androidtv-armv7/
    else
        echo "⚠ Android TV ARMv7 build failed"
    fi
else
    echo "⚠ Android NDK not found. Install Android NDK for Android TV builds."
fi

# Build for smart home platforms (generic ARM)
echo "Building for smart home platforms..."
if cargo build --target aarch64-unknown-linux-gnu --release --features "smart-home-optimized"; then
    echo "✓ Smart Home ARM64 build successful"
    cp target/aarch64-unknown-linux-gnu/release/libpqcrypto.a ../smarthome-arm64/
else
    echo "⚠ Smart Home ARM64 build failed"
fi

cd ..

echo "Build completed!"
echo "Check the platform-specific directories for compiled libraries."
echo "Note: Full platform builds may require additional SDK setup."
echo ""
echo "Supported platforms:"
echo "- tvOS: Apple TV and tvOS applications"
echo "- Android TV: Smart TVs and streaming devices"
echo "- Smart Home: Google Home, Apple HomePod, Amazon Echo, etc."
