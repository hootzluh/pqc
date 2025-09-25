#!/bin/bash

# Build all PQMobile algorithms for host system testing
# This allows us to validate functionality before cross-compilation

set -e

echo "Building PQMobile algorithms for host system..."
echo "==============================================="

cd Reference_Implementation/crypto_kem

# Build ML-KEM variants
echo "Building ML-KEM algorithms..."
for variant in kyber512 kyber768 kyber1024; do
    echo "  Building $variant..."
    cd $variant
    gcc -O3 -Wall -Wextra -std=c99 -I../../../common -c cbd.c fips202.c indcpa.c kem.c ntt.c poly.c polyvec.c reduce.c rng.c verify.c symmetric-shake.c
    ar -r ../../../../lib${variant//kyber/ml-kem}.a *.o
    rm *.o
    cd ..
done

cd ../..

cd Reference_Implementation/crypto_sign

# Build ML-DSA variants
echo "Building ML-DSA algorithms..."
for variant in dilithium2 dilithium3 dilithium5; do
    echo "  Building $variant..."
    cd $variant
    gcc -O3 -Wall -Wextra -std=c99 -I../../../common -c fips202.c ntt.c packing.c poly.c polyvec.c reduce.c rounding.c sign.c symmetric-shake.c
    ar -r ../../../../lib${variant//dilithium/ml-dsa}.a *.o
    rm *.o
    cd ..
done

cd ../..

cd Reference_Implementation

# Build HQC variants
echo "Building HQC algorithms..."
for variant in hqc-128 hqc-192 hqc-256; do
    echo "  Building $variant..."
    cd $variant
    gcc -O3 -Wall -Wextra -std=c99 -I../../common -c code.c fft.c gf.c gf2x.c hqc.c kem.c parsing.c reed_muller.c reed_solomon.c shake_ds.c shake_prng.c vector.c
    ar -r ../../../lib${variant}.a *.o
    rm *.o
    cd ..
done

cd ..

echo "All algorithms built successfully!"
echo "Libraries created:"
ls -la lib*.a
