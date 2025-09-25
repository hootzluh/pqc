# PQMobile - Cross-compilation Makefile for Mobile Platforms
# Supports iOS (ARM64, x86_64) and Android (ARM64, ARMv7)

# Default target
.PHONY: all ios android clean test benchmark help

# Architectures to build
IOS_ARCHS := arm64 x86_64
ANDROID_ARCHS := arm64 armv7

# Build all platforms
all: ios android

# iOS builds
ios: ios-arm64 ios-x86_64

ios-arm64:
	@echo "Building for iOS ARM64..."
	@mkdir -p ios-arm64
	@make -f Makefile.ios TARGET=arm64 SYSROOT=iphoneos
	@mv *.a ios-arm64/ 2>/dev/null || true

ios-x86_64:
	@echo "Building for iOS x86_64..."
	@mkdir -p ios-x86_64
	@make -f Makefile.ios TARGET=x86_64 SYSROOT=iphonesimulator
	@mv *.a ios-x86_64/ 2>/dev/null || true

# Android builds
android: android-arm64 android-armv7

android-arm64:
	@echo "Building for Android ARM64..."
	@mkdir -p android-arm64
	@if command -v ndk-build >/dev/null 2>&1; then \
		make -f Makefile.android TARGET=arm64-v8a; \
		mv *.a android-arm64/ 2>/dev/null || true; \
	else \
		echo "Android NDK not found - skipping Android ARM64 build"; \
	fi

android-armv7:
	@echo "Building for Android ARMv7..."
	@mkdir -p android-armv7
	@if command -v ndk-build >/dev/null 2>&1; then \
		make -f Makefile.android TARGET=armeabi-v7a; \
		mv *.a android-armv7/ 2>/dev/null || true; \
	else \
		echo "Android NDK not found - skipping Android ARMv7 build"; \
	fi

# Test all implementations
test:
	@echo "Running KAT tests..."
	@./test_kat.sh

# Benchmark all implementations
benchmark:
	@echo "Running benchmarks..."
	@./benchmark.sh

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	@rm -rf ios-arm64 ios-x86_64 android-arm64 android-armv7
	@make -f Makefile.ios clean 2>/dev/null || true
	@make -f Makefile.android clean 2>/dev/null || true
	@find . -name "*.a" -delete
	@find . -name "*.o" -delete

# Show help
help:
	@echo "PQMobile Build System"
	@echo ""
	@echo "Targets:"
	@echo "  all        - Build for all platforms"
	@echo "  ios        - Build for iOS (ARM64 + x86_64)"
	@echo "  android    - Build for Android (ARM64 + ARMv7)"
	@echo "  test       - Run KAT validation tests"
	@echo "  benchmark  - Run performance benchmarks"
	@echo "  clean      - Clean all build artifacts"
	@echo ""
	@echo "Requirements:"
	@echo "  - Xcode (for iOS builds)"
	@echo "  - Android NDK (for Android builds)"
	@echo "  - iOS/Android SDKs"
	@echo ""
	@echo "Supported Algorithms:"
	@echo "  - ML-KEM (512, 768, 1024)"
	@echo "  - ML-DSA (44, 65, 87)"
	@echo "  - FN-DSA (512, 1024)"
	@echo "  - HQC-KEM (128, 192, 256)"
