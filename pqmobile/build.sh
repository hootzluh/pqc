#!/bin/bash

# PQMobile Build Script
# Cross-compiles PQC algorithms for iOS and Android platforms

set -e

echo "PQMobile Build Script"
echo "====================="

# Check if required tools are available
command -v cargo >/dev/null 2>&1 || { echo "Error: cargo not found. Install Rust."; exit 1; }

echo "Building for mobile platforms..."

cd pqcrypto

# Build for iOS
echo "Building for iOS..."
if cargo build --target aarch64-apple-ios --release; then
    echo "✓ iOS ARM64 build successful"
    cp target/aarch64-apple-ios/release/libpqcrypto.a ../ios-arm64/
else
    echo "⚠ iOS ARM64 build failed (may require Xcode)"
fi

if cargo build --target x86_64-apple-ios --release; then
    echo "✓ iOS x86_64 build successful"
    cp target/x86_64-apple-ios/release/libpqcrypto.a ../ios-x86_64/
else
    echo "⚠ iOS x86_64 build failed (may require Xcode)"
fi

# Build for Android (requires Android NDK)
echo "Building for Android..."
if command -v ndk-build >/dev/null 2>&1; then
    if cargo build --target aarch64-linux-android --release; then
        echo "✓ Android ARM64 build successful"
        cp target/aarch64-linux-android/release/libpqcrypto.a ../android-arm64/
    else
        echo "⚠ Android ARM64 build failed"
    fi

    if cargo build --target armv7-linux-androideabi --release; then
        echo "✓ Android ARMv7 build successful"
        cp target/armv7-linux-androideabi/release/libpqcrypto.a ../android-armv7/
    else
        echo "⚠ Android ARMv7 build failed"
    fi
else
    echo "⚠ Android NDK not found. Install Android NDK for Android builds."
fi

cd ..

echo "Build completed!"
echo "Check the platform-specific directories for compiled libraries."
echo "Note: Full iOS/Android builds may require additional SDK setup."
