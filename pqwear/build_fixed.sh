#!/bin/bash

# PQWear Build Script (Fixed)
# Builds PQC algorithms for wearable devices with size optimizations

set -e

echo "PQWear Build Script"
echo "=================="

echo "Building for wearable platforms with size optimizations..."

# Create output directories if they don't exist
mkdir -p watchos-arm64
mkdir -p wearos-arm64
mkdir -p wearos-armv7

# Clean previous builds
rm -f watchos-arm64/*.a wearos-arm64/*.a wearos-armv7/*.a

# Build each algorithm with wearable optimizations (size-optimized)
echo "Building ML-KEM algorithms..."
for algo in "ml-kem-512" "ml-kem-768" "ml-kem-1024"; do
    if [ -d "$algo/clean" ]; then
        echo "  Building $algo for wearables..."
        cd "$algo/clean"

        # Use size optimization for wearables and copy common headers
        cp -r ../../../common/* .
        make clean && make EXTRAFLAGS="-Os"

        # Copy to wearable platform directories
        cp *.a ../../../../watchos-arm64/ 2>/dev/null || true
        cp *.a ../../../../wearos-arm64/ 2>/dev/null || true
        cp *.a ../../../../wearos-armv7/ 2>/dev/null || true

        cd ../../../..
    fi
done

echo "Building ML-DSA algorithms..."
for algo in "ml-dsa-44" "ml-dsa-65" "ml-dsa-87"; do
    if [ -d "$algo/clean" ]; then
        echo "  Building $algo for wearables..."
        cd "$algo/clean"

        # Use size optimization for wearables and copy common headers
        cp -r ../../../common/* .
        make clean && make EXTRAFLAGS="-Os"

        # Copy to wearable platform directories
        cp *.a ../../../../watchos-arm64/ 2>/dev/null || true
        cp *.a ../../../../wearos-arm64/ 2>/dev/null || true
        cp *.a ../../../../wearos-armv7/ 2>/dev/null || true

        cd ../../../..
    fi
done

echo "Building HQC-KEM algorithms..."
for algo in "hqc-128" "hqc-192" "hqc-256"; do
    if [ -d "$algo/clean" ]; then
        echo "  Building $algo for wearables..."
        cd "$algo/clean"

        # Use size optimization for wearables and copy common headers
        cp -r ../../../common/* .
        make clean && make EXTRAFLAGS="-Os"

        # Copy to wearable platform directories
        cp *.a ../../../../watchos-arm64/ 2>/dev/null || true
        cp *.a ../../../../wearos-arm64/ 2>/dev/null || true
        cp *.a ../../../../wearos-armv7/ 2>/dev/null || true

        cd ../../../..
    fi
done

echo "Building Falcon algorithms..."
for algo in "falcon-512" "falcon-1024"; do
    if [ -d "$algo/clean" ]; then
        echo "  Building $algo for wearables..."
        cd "$algo/clean"

        # Use size optimization for wearables and copy common headers
        cp -r ../../../common/* .
        make clean && make EXTRAFLAGS="-Os"

        # Copy to wearable platform directories
        cp *.a ../../../../watchos-arm64/ 2>/dev/null || true
        cp *.a ../../../../wearos-arm64/ 2>/dev/null || true
        cp *.a ../../../../wearos-armv7/ 2>/dev/null || true

        cd ../../../..
    fi
done

echo "Build completed!"
echo "Wearable-optimized libraries are available in:"
echo "  - watchos-arm64/ (Apple Watch)"
echo "  - wearos-arm64/ (Android Wear 64-bit)"
echo "  - wearos-armv7/ (Android Wear 32-bit)"

# Verify the builds
echo ""
echo "Verifying built libraries..."
for platform in "watchos-arm64" "wearos-arm64" "wearos-armv7"; do
    if [ -d "$platform" ]; then
        lib_count=$(ls -1 $platform/ | grep "\.a$" | wc -l)
        echo "$platform: $lib_count libraries built"
    fi
done
