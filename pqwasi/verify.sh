#!/bin/bash

# PQCWASI Verification Script
# Verifies that the WASI implementation is properly built

echo "PQCWASI Verification"
echo "===================="

# Check if libraries exist
echo "Checking for built WASI libraries..."

REQUIRED_LIBS=(
    "libpqcrypto_mlkem.rlib"
    "libpqcrypto_mldsa.rlib"
    "libpqcrypto_hqc.rlib"
    "libpqcrypto_falcon.rlib"
    "libpqcrypto_classicmceliece.rlib"
    "libpqcrypto_sphincsplus.rlib"
    "libpqcrypto_traits.rlib"
    "libpqcrypto_internals.rlib"
    "libpqcrypto.rlib"
)

MISSING_LIBS=()
for lib in "${REQUIRED_LIBS[@]}"; do
    if [ -f "clean/$lib" ]; then
        size=$(stat -f%z "clean/$lib" 2>/dev/null || stat -c%s "clean/$lib" 2>/dev/null || echo "unknown")
        echo "✓ $lib ($size bytes)"
    else
        echo "✗ $lib (missing)"
        MISSING_LIBS+=("$lib")
    fi
done

if [ ${#MISSING_LIBS[@]} -eq 0 ]; then
    echo ""
    echo "✓ All required WASI libraries are present"
else
    echo ""
    echo "✗ Missing libraries: ${MISSING_LIBS[*]}"
    exit 1
fi

# Check library sizes are reasonable
echo ""
echo "Verifying library sizes..."

MIN_SIZES=(
    "libpqcrypto_mlkem.rlib:400000"
    "libpqcrypto_mldsa.rlib:400000"
    "libpqcrypto_hqc.rlib:400000"
    "libpqcrypto_falcon.rlib:800000"
    "libpqcrypto_classicmceliece.rlib:1500000"
    "libpqcrypto_sphincsplus.rlib:1500000"
    "libpqcrypto_traits.rlib:15000"
    "libpqcrypto_internals.rlib:50000"
    "libpqcrypto.rlib:7000"
)

SIZE_ISSUES=()
for size_check in "${MIN_SIZES[@]}"; do
    lib_name="${size_check%:*}"
    min_size="${size_check#*:}"

    if [ -f "clean/$lib_name" ]; then
        actual_size=$(stat -f%z "clean/$lib_name" 2>/dev/null || stat -c%s "clean/$lib_name" 2>/dev/null || echo "0")

        if [ "$actual_size" -lt "$min_size" ]; then
            echo "⚠ $lib_name is smaller than expected ($actual_size < $min_size bytes)"
            SIZE_ISSUES+=("$lib_name")
        fi
    fi
done

if [ ${#SIZE_ISSUES[@]} -eq 0 ]; then
    echo "✓ All library sizes are within expected ranges"
else
    echo "⚠ Some libraries may be smaller than expected: ${SIZE_ISSUES[*]}"
fi

# Check for source implementations
echo ""
echo "Checking for implementation sources..."

IMPLEMENTATION_DIRS=(
    "mlkem:pqcrypto-mlkem"
    "mldsa:pqcrypto-mldsa"
    "hqc:pqcrypto-hqc"
    "falcon:pqcrypto-falcon"
    "classicmceliece:pqcrypto-classicmceliece"
    "sphincsplus:pqcrypto-sphincsplus"
)

MISSING_DIRS=()
for dir_info in "${IMPLEMENTATION_DIRS[@]}"; do
    dir_name="${dir_info%:*}"
    expected_dir="${dir_info#*:}"

    if [ -d "archive/pqcrypto/$expected_dir" ]; then
        echo "✓ $dir_name implementation available ($expected_dir)"
    else
        echo "✗ $dir_name implementation missing ($expected_dir)"
        MISSING_DIRS+=("$dir_name")
    fi
done

if [ ${#MISSING_DIRS[@]} -eq 0 ]; then
    echo ""
    echo "✓ All required algorithm implementations are available"
else
    echo ""
    echo "✗ Missing implementations: ${MISSING_DIRS[*]}"
    exit 1
fi

echo ""
echo "Verification completed successfully!"
echo "PQCWASI implementation is ready for use with:"
echo "- Serverless functions (AWS Lambda, Cloudflare Workers)"
echo "- Edge computing platforms"
echo "- Embedded systems with WASI runtimes"
echo "- Any environment supporting WebAssembly"

echo ""
echo "To test with a WASI runtime:"
echo "1. Install wasmtime: curl -sSfL https://github.com/bytecodealliance/wasmtime/releases/latest/download/wasmtime-x86_64-macos.tar.xz | tar xJf - && sudo mv wasmtime-x86_64-macos/wasmtime /usr/local/bin/"
echo "2. Create a Rust application using the pqcrypto crates"
echo "3. Build with: cargo build --target wasm32-wasip1 --release"
echo "4. Run with: wasmtime target/wasm32-wasip1/release/your-app.wasm"
