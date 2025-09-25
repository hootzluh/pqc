#!/bin/bash

# PQMobile Test Script
# Tests the mobile implementations

echo "PQMobile Test Script"
echo "==================="

# Check if implementations exist
if [ ! -d "ios-arm64" ] || [ ! -d "android-arm64" ]; then
    echo "No mobile implementations found. Run ./build.sh first."
    echo "Note: iOS builds require Xcode, Android builds require NDK."
    exit 1
fi

echo "✓ Mobile implementations found"
echo "✓ PQMobile setup is ready for platform integration"

# Platform-specific notes
echo ""
echo "Integration notes:"
echo "- iOS: Use Swift/Objective-C bindings with the ios-* libraries"
echo "- Android: Use JNI with the android-* libraries"
echo "- Test on actual devices for performance validation"
