#!/bin/bash

# PQWear Build Script
# Builds PQC algorithms for wearable devices with size optimizations

set -e

echo "PQWear Build Script"
echo "==================="

echo "Building for wearable platforms with size optimizations..."

# Build all algorithms with wearable optimizations (size-optimized)
for algo_dir in ml-kem-*/clean ml-dsa-*/clean falcon-*/clean hqc-*/clean; do
    if [ -d "$algo_dir" ]; then
        echo "Building $algo_dir for wearables..."
        cd "$algo_dir"

        # Use size optimization for wearables
        make clean && make EXTRAFLAGS="-Os"

        # Copy to wearable platform directories
        cp *.a ../../../watchos-arm64/ 2>/dev/null || true
        cp *.a ../../../wearos-arm64/ 2>/dev/null || true
        cp *.a ../../../wearos-armv7/ 2>/dev/null || true

        cd ../../..
    fi
done

echo "Build completed!"
echo "Wearable-optimized libraries are available in:"
echo "  - watchos-arm64/ (Apple Watch)"
echo "  - wearos-arm64/ (Android Wear 64-bit)"
echo "  - wearos-armv7/ (Android Wear 32-bit)"
