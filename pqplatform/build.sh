#!/bin/bash

# PQPlatform Build Script
# Builds PQC algorithms for smart TV and smart home platforms

set -e

echo "PQPlatform Build Script"
echo "======================="

echo "Building for smart TV and smart home platforms..."

# Build all algorithms with smart home optimizations
for algo_dir in ml-kem-*/clean ml-dsa-*/clean falcon-*/clean hqc-*/clean; do
    if [ -d "$algo_dir" ]; then
        echo "Building $algo_dir for smart platforms..."
        cd "$algo_dir"

        # Use performance optimizations for smart home devices
        make clean && make EXTRAFLAGS="-O3"

        # Copy to smart platform directories
        cp *.a ../../../tvos-arm64/ 2>/dev/null || true
        cp *.a ../../../tvos-x86_64/ 2>/dev/null || true
        cp *.a ../../../androidtv-arm64/ 2>/dev/null || true
        cp *.a ../../../androidtv-armv7/ 2>/dev/null || true
        cp *.a ../../../smarthome-arm64/ 2>/dev/null || true

        cd ../../..
    fi
done

echo "Build completed!"
echo "Smart platform libraries are available in:"
echo "  - tvos-arm64/ (Apple TV)"
echo "  - tvos-x86_64/ (Apple TV Simulator)"
echo "  - androidtv-arm64/ (Android TV 64-bit)"
echo "  - androidtv-armv7/ (Android TV 32-bit)"
echo "  - smarthome-arm64/ (Smart Home devices)"
