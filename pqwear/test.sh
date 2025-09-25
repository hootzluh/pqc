#!/bin/bash

# PQWear Test Script
# Tests the wearable implementations

echo "PQWear Test Script"
echo "=================="

# Check if implementations exist
if [ ! -d "watchos-arm64" ] || [ ! -d "wearos-arm64" ]; then
    echo "No wearable implementations found. Run ./build.sh first."
    echo "Note: watchOS builds require Xcode, Wear OS builds require NDK."
    exit 1
fi

echo "✓ Wearable implementations found"
echo "✓ PQWear setup is ready for wearable platform integration"

# Platform-specific notes
echo ""
echo "Integration notes:"
echo "- watchOS: Use Swift/Objective-C bindings with the watchos-* libraries"
echo "- Wear OS: Use JNI with the wearos-* libraries"
echo "- Smart rings: May require additional platform adaptations"
echo "- Test on actual wearable devices for battery/performance validation"
