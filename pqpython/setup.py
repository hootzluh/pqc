#!/usr/bin/env python3
"""
Setup script for pqpython - Python bindings for NIST Post-Quantum Cryptography algorithms
"""

import os
from setuptools import setup, Extension


def get_pqclean_sources():
    """Get C source files for core working algorithms."""
    sources = []

    # Add common files
    common_dir = os.path.join('pqclean', 'common')
    if os.path.exists(common_dir):
        for file in os.listdir(common_dir):
            if file.endswith('.c') and not file.startswith('keccak2x'):  # Skip NEON files
                sources.append(os.path.join(common_dir, file))

    # Include all ML-KEM variants and ML-DSA-44
    sources.extend([
        # ML-KEM-512
        "pqclean/crypto_kem/ml-kem-512/clean/cbd.c",
        "pqclean/crypto_kem/ml-kem-512/clean/indcpa.c",
        "pqclean/crypto_kem/ml-kem-512/clean/kem.c",
        "pqclean/crypto_kem/ml-kem-512/clean/ntt.c",
        "pqclean/crypto_kem/ml-kem-512/clean/poly.c",
        "pqclean/crypto_kem/ml-kem-512/clean/polyvec.c",
        "pqclean/crypto_kem/ml-kem-512/clean/reduce.c",
        "pqclean/crypto_kem/ml-kem-512/clean/symmetric-shake.c",
        "pqclean/crypto_kem/ml-kem-512/clean/verify.c",

        # ML-KEM-768
        "pqclean/crypto_kem/ml-kem-768/clean/cbd.c",
        "pqclean/crypto_kem/ml-kem-768/clean/indcpa.c",
        "pqclean/crypto_kem/ml-kem-768/clean/kem.c",
        "pqclean/crypto_kem/ml-kem-768/clean/ntt.c",
        "pqclean/crypto_kem/ml-kem-768/clean/poly.c",
        "pqclean/crypto_kem/ml-kem-768/clean/polyvec.c",
        "pqclean/crypto_kem/ml-kem-768/clean/reduce.c",
        "pqclean/crypto_kem/ml-kem-768/clean/symmetric-shake.c",
        "pqclean/crypto_kem/ml-kem-768/clean/verify.c",

        # ML-KEM-1024
        "pqclean/crypto_kem/ml-kem-1024/clean/cbd.c",
        "pqclean/crypto_kem/ml-kem-1024/clean/indcpa.c",
        "pqclean/crypto_kem/ml-kem-1024/clean/kem.c",
        "pqclean/crypto_kem/ml-kem-1024/clean/ntt.c",
        "pqclean/crypto_kem/ml-kem-1024/clean/poly.c",
        "pqclean/crypto_kem/ml-kem-1024/clean/polyvec.c",
        "pqclean/crypto_kem/ml-kem-1024/clean/reduce.c",
        "pqclean/crypto_kem/ml-kem-1024/clean/symmetric-shake.c",
        "pqclean/crypto_kem/ml-kem-1024/clean/verify.c",

        # ML-DSA-44
        "pqclean/crypto_sign/ml-dsa-44/clean/ntt.c",
        "pqclean/crypto_sign/ml-dsa-44/clean/packing.c",
        "pqclean/crypto_sign/ml-dsa-44/clean/poly.c",
        "pqclean/crypto_sign/ml-dsa-44/clean/polyvec.c",
        "pqclean/crypto_sign/ml-dsa-44/clean/reduce.c",
        "pqclean/crypto_sign/ml-dsa-44/clean/rounding.c",
        "pqclean/crypto_sign/ml-dsa-44/clean/sign.c",
        "pqclean/crypto_sign/ml-dsa-44/clean/symmetric-shake.c",

        # ML-DSA-65
        "pqclean/crypto_sign/ml-dsa-65/clean/ntt.c",
        "pqclean/crypto_sign/ml-dsa-65/clean/packing.c",
        "pqclean/crypto_sign/ml-dsa-65/clean/poly.c",
        "pqclean/crypto_sign/ml-dsa-65/clean/polyvec.c",
        "pqclean/crypto_sign/ml-dsa-65/clean/reduce.c",
        "pqclean/crypto_sign/ml-dsa-65/clean/rounding.c",
        "pqclean/crypto_sign/ml-dsa-65/clean/sign.c",
        "pqclean/crypto_sign/ml-dsa-65/clean/symmetric-shake.c",

        # ML-DSA-87
        "pqclean/crypto_sign/ml-dsa-87/clean/ntt.c",
        "pqclean/crypto_sign/ml-dsa-87/clean/packing.c",
        "pqclean/crypto_sign/ml-dsa-87/clean/poly.c",
        "pqclean/crypto_sign/ml-dsa-87/clean/polyvec.c",
        "pqclean/crypto_sign/ml-dsa-87/clean/reduce.c",
        "pqclean/crypto_sign/ml-dsa-87/clean/rounding.c",
        "pqclean/crypto_sign/ml-dsa-87/clean/sign.c",
        "pqclean/crypto_sign/ml-dsa-87/clean/symmetric-shake.c",

        # FN-DSA-512 (falcon-512)
        "pqclean/crypto_sign/falcon-512/clean/codec.c",
        "pqclean/crypto_sign/falcon-512/clean/common.c",
        "pqclean/crypto_sign/falcon-512/clean/fft.c",
        "pqclean/crypto_sign/falcon-512/clean/fpr.c",
        "pqclean/crypto_sign/falcon-512/clean/keygen.c",
        "pqclean/crypto_sign/falcon-512/clean/pqclean.c",
        "pqclean/crypto_sign/falcon-512/clean/rng.c",
        "pqclean/crypto_sign/falcon-512/clean/sign.c",
        "pqclean/crypto_sign/falcon-512/clean/vrfy.c",

        # FN-DSA-1024 (falcon-1024)
        "pqclean/crypto_sign/falcon-1024/clean/codec.c",
        "pqclean/crypto_sign/falcon-1024/clean/common.c",
        "pqclean/crypto_sign/falcon-1024/clean/fft.c",
        "pqclean/crypto_sign/falcon-1024/clean/fpr.c",
        "pqclean/crypto_sign/falcon-1024/clean/keygen.c",
        "pqclean/crypto_sign/falcon-1024/clean/pqclean.c",
        "pqclean/crypto_sign/falcon-1024/clean/rng.c",
        "pqclean/crypto_sign/falcon-1024/clean/sign.c",
        "pqclean/crypto_sign/falcon-1024/clean/vrfy.c",

        # HQC-KEM-128
        "pqclean/crypto_kem/hqc-128/clean/code.c",
        "pqclean/crypto_kem/hqc-128/clean/fft.c",
        "pqclean/crypto_kem/hqc-128/clean/gf.c",
        "pqclean/crypto_kem/hqc-128/clean/gf2x.c",
        "pqclean/crypto_kem/hqc-128/clean/hqc.c",
        "pqclean/crypto_kem/hqc-128/clean/kem.c",
        "pqclean/crypto_kem/hqc-128/clean/parsing.c",
        "pqclean/crypto_kem/hqc-128/clean/reed_muller.c",
        "pqclean/crypto_kem/hqc-128/clean/reed_solomon.c",
        "pqclean/crypto_kem/hqc-128/clean/shake_ds.c",
        "pqclean/crypto_kem/hqc-128/clean/shake_prng.c",
        "pqclean/crypto_kem/hqc-128/clean/vector.c",

        # HQC-KEM-192
        "pqclean/crypto_kem/hqc-192/clean/code.c",
        "pqclean/crypto_kem/hqc-192/clean/fft.c",
        "pqclean/crypto_kem/hqc-192/clean/gf.c",
        "pqclean/crypto_kem/hqc-192/clean/gf2x.c",
        "pqclean/crypto_kem/hqc-192/clean/hqc.c",
        "pqclean/crypto_kem/hqc-192/clean/kem.c",
        "pqclean/crypto_kem/hqc-192/clean/parsing.c",
        "pqclean/crypto_kem/hqc-192/clean/reed_muller.c",
        "pqclean/crypto_kem/hqc-192/clean/reed_solomon.c",
        "pqclean/crypto_kem/hqc-192/clean/shake_ds.c",
        "pqclean/crypto_kem/hqc-192/clean/shake_prng.c",
        "pqclean/crypto_kem/hqc-192/clean/vector.c",

                # HQC-KEM-256
                "pqclean/crypto_kem/hqc-256/clean/code.c",
                "pqclean/crypto_kem/hqc-256/clean/fft.c",
                "pqclean/crypto_kem/hqc-256/clean/gf.c",
                "pqclean/crypto_kem/hqc-256/clean/gf2x.c",
                "pqclean/crypto_kem/hqc-256/clean/hqc.c",
                "pqclean/crypto_kem/hqc-256/clean/kem.c",
                "pqclean/crypto_kem/hqc-256/clean/parsing.c",
                "pqclean/crypto_kem/hqc-256/clean/reed_muller.c",
                "pqclean/crypto_kem/hqc-256/clean/reed_solomon.c",
                "pqclean/crypto_kem/hqc-256/clean/shake_ds.c",
                "pqclean/crypto_kem/hqc-256/clean/shake_prng.c",
                "pqclean/crypto_kem/hqc-256/clean/vector.c",

                # Classic McEliece-348864
                "pqclean/crypto_kem/mceliece348864/clean/aes256ctr.c",
                "pqclean/crypto_kem/mceliece348864/clean/benes.c",
                "pqclean/crypto_kem/mceliece348864/clean/bm.c",
                "pqclean/crypto_kem/mceliece348864/clean/controlbits.c",
                "pqclean/crypto_kem/mceliece348864/clean/crypto_int16.c",
                "pqclean/crypto_kem/mceliece348864/clean/crypto_int32.c",
                "pqclean/crypto_kem/mceliece348864/clean/crypto_uint16.c",
                "pqclean/crypto_kem/mceliece348864/clean/crypto_uint32.c",
                "pqclean/crypto_kem/mceliece348864/clean/crypto_uint64.c",
                "pqclean/crypto_kem/mceliece348864/clean/decrypt.c",
                "pqclean/crypto_kem/mceliece348864/clean/encrypt.c",
                "pqclean/crypto_kem/mceliece348864/clean/gf.c",
                "pqclean/crypto_kem/mceliece348864/clean/operations.c",
                "pqclean/crypto_kem/mceliece348864/clean/pk_gen.c",
                "pqclean/crypto_kem/mceliece348864/clean/root.c",
                "pqclean/crypto_kem/mceliece348864/clean/sk_gen.c",
                "pqclean/crypto_kem/mceliece348864/clean/synd.c",
                "pqclean/crypto_kem/mceliece348864/clean/transpose.c",
                "pqclean/crypto_kem/mceliece348864/clean/util.c",

                # Classic McEliece-460896
                "pqclean/crypto_kem/mceliece460896/clean/aes256ctr.c",
                "pqclean/crypto_kem/mceliece460896/clean/benes.c",
                "pqclean/crypto_kem/mceliece460896/clean/bm.c",
                "pqclean/crypto_kem/mceliece460896/clean/controlbits.c",
                "pqclean/crypto_kem/mceliece460896/clean/crypto_int16.c",
                "pqclean/crypto_kem/mceliece460896/clean/crypto_int32.c",
                "pqclean/crypto_kem/mceliece460896/clean/crypto_uint16.c",
                "pqclean/crypto_kem/mceliece460896/clean/crypto_uint32.c",
                "pqclean/crypto_kem/mceliece460896/clean/crypto_uint64.c",
                "pqclean/crypto_kem/mceliece460896/clean/decrypt.c",
                "pqclean/crypto_kem/mceliece460896/clean/encrypt.c",
                "pqclean/crypto_kem/mceliece460896/clean/gf.c",
                "pqclean/crypto_kem/mceliece460896/clean/operations.c",
                "pqclean/crypto_kem/mceliece460896/clean/pk_gen.c",
                "pqclean/crypto_kem/mceliece460896/clean/root.c",
                "pqclean/crypto_kem/mceliece460896/clean/sk_gen.c",
                "pqclean/crypto_kem/mceliece460896/clean/synd.c",
                "pqclean/crypto_kem/mceliece460896/clean/transpose.c",
                "pqclean/crypto_kem/mceliece460896/clean/util.c",

                # Classic McEliece-6688128
                "pqclean/crypto_kem/mceliece6688128/clean/aes256ctr.c",
                "pqclean/crypto_kem/mceliece6688128/clean/benes.c",
                "pqclean/crypto_kem/mceliece6688128/clean/bm.c",
                "pqclean/crypto_kem/mceliece6688128/clean/controlbits.c",
                "pqclean/crypto_kem/mceliece6688128/clean/crypto_int16.c",
                "pqclean/crypto_kem/mceliece6688128/clean/crypto_int32.c",
                "pqclean/crypto_kem/mceliece6688128/clean/crypto_uint16.c",
                "pqclean/crypto_kem/mceliece6688128/clean/crypto_uint32.c",
                "pqclean/crypto_kem/mceliece6688128/clean/crypto_uint64.c",
                "pqclean/crypto_kem/mceliece6688128/clean/decrypt.c",
                "pqclean/crypto_kem/mceliece6688128/clean/encrypt.c",
                "pqclean/crypto_kem/mceliece6688128/clean/gf.c",
                "pqclean/crypto_kem/mceliece6688128/clean/operations.c",
                "pqclean/crypto_kem/mceliece6688128/clean/pk_gen.c",
                "pqclean/crypto_kem/mceliece6688128/clean/root.c",
                "pqclean/crypto_kem/mceliece6688128/clean/sk_gen.c",
                "pqclean/crypto_kem/mceliece6688128/clean/synd.c",
                "pqclean/crypto_kem/mceliece6688128/clean/transpose.c",
                "pqclean/crypto_kem/mceliece6688128/clean/util.c",

                # Classic McEliece-6960119
                "pqclean/crypto_kem/mceliece6960119/clean/aes256ctr.c",
                "pqclean/crypto_kem/mceliece6960119/clean/benes.c",
                "pqclean/crypto_kem/mceliece6960119/clean/bm.c",
                "pqclean/crypto_kem/mceliece6960119/clean/controlbits.c",
                "pqclean/crypto_kem/mceliece6960119/clean/crypto_int16.c",
                "pqclean/crypto_kem/mceliece6960119/clean/crypto_int32.c",
                "pqclean/crypto_kem/mceliece6960119/clean/crypto_uint16.c",
                "pqclean/crypto_kem/mceliece6960119/clean/crypto_uint32.c",
                "pqclean/crypto_kem/mceliece6960119/clean/crypto_uint64.c",
                "pqclean/crypto_kem/mceliece6960119/clean/decrypt.c",
                "pqclean/crypto_kem/mceliece6960119/clean/encrypt.c",
                "pqclean/crypto_kem/mceliece6960119/clean/gf.c",
                "pqclean/crypto_kem/mceliece6960119/clean/operations.c",
                "pqclean/crypto_kem/mceliece6960119/clean/pk_gen.c",
                "pqclean/crypto_kem/mceliece6960119/clean/root.c",
                "pqclean/crypto_kem/mceliece6960119/clean/sk_gen.c",
                "pqclean/crypto_kem/mceliece6960119/clean/synd.c",
                "pqclean/crypto_kem/mceliece6960119/clean/transpose.c",
                "pqclean/crypto_kem/mceliece6960119/clean/util.c",

                # Classic McEliece-8192128
                "pqclean/crypto_kem/mceliece8192128/clean/aes256ctr.c",
                "pqclean/crypto_kem/mceliece8192128/clean/benes.c",
                "pqclean/crypto_kem/mceliece8192128/clean/bm.c",
                "pqclean/crypto_kem/mceliece8192128/clean/controlbits.c",
                "pqclean/crypto_kem/mceliece8192128/clean/crypto_int16.c",
                "pqclean/crypto_kem/mceliece8192128/clean/crypto_int32.c",
                "pqclean/crypto_kem/mceliece8192128/clean/crypto_uint16.c",
                "pqclean/crypto_kem/mceliece8192128/clean/crypto_uint32.c",
                "pqclean/crypto_kem/mceliece8192128/clean/crypto_uint64.c",
                "pqclean/crypto_kem/mceliece8192128/clean/decrypt.c",
                "pqclean/crypto_kem/mceliece8192128/clean/encrypt.c",
                "pqclean/crypto_kem/mceliece8192128/clean/gf.c",
                "pqclean/crypto_kem/mceliece8192128/clean/operations.c",
                "pqclean/crypto_kem/mceliece8192128/clean/pk_gen.c",
                "pqclean/crypto_kem/mceliece8192128/clean/root.c",
                "pqclean/crypto_kem/mceliece8192128/clean/sk_gen.c",
                "pqclean/crypto_kem/mceliece8192128/clean/synd.c",
                "pqclean/crypto_kem/mceliece8192128/clean/transpose.c",
                "pqclean/crypto_kem/mceliece8192128/clean/util.c",
            ])

    return sources


def get_include_dirs():
    """Get include directories for compilation."""
    includes = [
        'pqclean/common',
        'pqclean/crypto_kem/ml-kem-512/clean',
        'pqclean/crypto_kem/ml-kem-768/clean',
        'pqclean/crypto_kem/ml-kem-1024/clean',
        'pqclean/crypto_kem/hqc-128/clean',
        'pqclean/crypto_kem/hqc-192/clean',
        'pqclean/crypto_kem/hqc-256/clean',
        'pqclean/crypto_kem/mceliece348864/clean',
        'pqclean/crypto_kem/mceliece460896/clean',
        'pqclean/crypto_kem/mceliece6688128/clean',
        'pqclean/crypto_kem/mceliece6960119/clean',
        'pqclean/crypto_kem/mceliece8192128/clean',
        'pqclean/crypto_sign/ml-dsa-44/clean',
        'pqclean/crypto_sign/ml-dsa-65/clean',
        'pqclean/crypto_sign/ml-dsa-87/clean',
        'pqclean/crypto_sign/falcon-512/clean',
        'pqclean/crypto_sign/falcon-1024/clean',
    ]

    return includes


# Get the long description from README
with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pqpython',
    version='0.1.0',
    description='Python bindings for NIST Post-Quantum Cryptography algorithms',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='PQC Team',
    author_email='pqc@example.com',
    url='https://github.com/pqc/pqpython',
    packages=['pqpython'],
    package_dir={'pqpython': 'pqpython'},
    ext_modules=[
        Extension(
            'pqpython._pqpython',
            sources=get_pqclean_sources(),
            include_dirs=get_include_dirs(),
            extra_compile_args=['-O3', '-std=c99'],
        )
    ],
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Security :: Cryptography',
    ],
    keywords='cryptography post-quantum pqc nist',
)
