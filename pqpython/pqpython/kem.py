"""
Key Encapsulation Mechanism (KEM) algorithms for pqpython
"""

import os
import ctypes
from typing import Tuple
from pathlib import Path


class KEMAlgorithm:
    """Base class for KEM algorithms"""

    def __init__(self, name: str, public_key_bytes: int, secret_key_bytes: int,
                 ciphertext_bytes: int, shared_secret_bytes: int):
        self.name = name
        self.public_key_bytes = public_key_bytes
        self.secret_key_bytes = secret_key_bytes
        self.ciphertext_bytes = ciphertext_bytes
        self.shared_secret_bytes = shared_secret_bytes

        # Load the shared library
        lib_dir = Path(__file__).parent
        lib_names = ["_pqpython.so", "_pqpython.cpython-39-darwin.so", "_pqpython.dylib"]

        lib_path = None
        for name in lib_names:
            candidate = lib_dir / name
            if candidate.exists():
                lib_path = candidate
                break

        if lib_path is None:
            # Try build directory
            build_dir = Path(__file__).parent.parent / "build"
            for name in lib_names:
                candidate = build_dir / f"lib.macosx-10.9-universal2-3.9" / "pqpython" / name
                if candidate.exists():
                    lib_path = candidate
                    break

        if lib_path is None:
            raise RuntimeError(f"Could not find pqpython library in {lib_dir} or build directory")

        try:
            self.lib = ctypes.CDLL(str(lib_path))
        except OSError as e:
            raise RuntimeError(f"Could not load pqpython library from {lib_path}: {e}")

        # Set up function signatures
        self._setup_functions()

    def _setup_functions(self):
        """Set up ctypes function signatures"""
        # Handle HQC naming convention (HQC128 instead of HQCKEM128)
        if self.name.startswith('hqc-kem-'):
            hqc_num = self.name.split('-')[2]  # Extract 128, 192, or 256
            func_prefix = f"PQCLEAN_HQC{hqc_num}_CLEAN"
        else:
            func_prefix = f"PQCLEAN_{self.name.upper().replace('-', '')}_CLEAN"

        func_name = f"{func_prefix}_crypto_kem_keypair"
        keypair_func = getattr(self.lib, func_name)
        keypair_func.argtypes = [ctypes.POINTER(ctypes.c_uint8), ctypes.POINTER(ctypes.c_uint8)]
        keypair_func.restype = ctypes.c_int

        func_name = f"{func_prefix}_crypto_kem_enc"
        enc_func = getattr(self.lib, func_name)
        enc_func.argtypes = [ctypes.POINTER(ctypes.c_uint8), ctypes.POINTER(ctypes.c_uint8), ctypes.POINTER(ctypes.c_uint8)]
        enc_func.restype = ctypes.c_int

        func_name = f"{func_prefix}_crypto_kem_dec"
        dec_func = getattr(self.lib, func_name)
        dec_func.argtypes = [ctypes.POINTER(ctypes.c_uint8), ctypes.POINTER(ctypes.c_uint8), ctypes.POINTER(ctypes.c_uint8)]
        dec_func.restype = ctypes.c_int

    def keypair(self) -> Tuple[bytes, bytes]:
        """Generate a public/private keypair"""
        pk = (ctypes.c_uint8 * self.public_key_bytes)()
        sk = (ctypes.c_uint8 * self.secret_key_bytes)()

        if self.name.startswith('hqc-kem-'):
            hqc_num = self.name.split('-')[2]
            func_name = f"PQCLEAN_HQC{hqc_num}_CLEAN_crypto_kem_keypair"
        else:
            func_name = f"PQCLEAN_{self.name.upper().replace('-', '')}_CLEAN_crypto_kem_keypair"
        func = getattr(self.lib, func_name)
        result = func(pk, sk)

        if result != 0:
            raise RuntimeError(f"Keypair generation failed for {self.name}")

        return bytes(pk), bytes(sk)

    def enc(self, public_key: bytes) -> Tuple[bytes, bytes]:
        """Encapsulate a shared secret using the public key"""
        if len(public_key) != self.public_key_bytes:
            raise ValueError(f"Public key must be {self.public_key_bytes} bytes")

        ct = (ctypes.c_uint8 * self.ciphertext_bytes)()
        ss = (ctypes.c_uint8 * self.shared_secret_bytes)()
        pk = (ctypes.c_uint8 * self.public_key_bytes)(*public_key)

        if self.name.startswith('hqc-kem-'):
            hqc_num = self.name.split('-')[2]
            func_name = f"PQCLEAN_HQC{hqc_num}_CLEAN_crypto_kem_enc"
        else:
            func_name = f"PQCLEAN_{self.name.upper().replace('-', '')}_CLEAN_crypto_kem_enc"
        func = getattr(self.lib, func_name)
        result = func(ct, ss, pk)

        if result != 0:
            raise RuntimeError(f"Encapsulation failed for {self.name}")

        return bytes(ct), bytes(ss)

    def dec(self, ciphertext: bytes, secret_key: bytes) -> bytes:
        """Decapsulate a shared secret using the secret key"""
        if len(ciphertext) != self.ciphertext_bytes:
            raise ValueError(f"Ciphertext must be {self.ciphertext_bytes} bytes")
        if len(secret_key) != self.secret_key_bytes:
            raise ValueError(f"Secret key must be {self.secret_key_bytes} bytes")

        ss = (ctypes.c_uint8 * self.shared_secret_bytes)()
        ct = (ctypes.c_uint8 * self.ciphertext_bytes)(*ciphertext)
        sk = (ctypes.c_uint8 * self.secret_key_bytes)(*secret_key)

        if self.name.startswith('hqc-kem-'):
            hqc_num = self.name.split('-')[2]
            func_name = f"PQCLEAN_HQC{hqc_num}_CLEAN_crypto_kem_dec"
        else:
            func_name = f"PQCLEAN_{self.name.upper().replace('-', '')}_CLEAN_crypto_kem_dec"
        func = getattr(self.lib, func_name)
        result = func(ss, ct, sk)

        if result != 0:
            raise RuntimeError(f"Decapsulation failed for {self.name}")

        return bytes(ss)


# ML-KEM algorithms
MLKEM512 = KEMAlgorithm(
    name="ml-kem-512",
    public_key_bytes=800,
    secret_key_bytes=1632,
    ciphertext_bytes=768,
    shared_secret_bytes=32
)

MLKEM768 = KEMAlgorithm(
    name="ml-kem-768",
    public_key_bytes=1184,
    secret_key_bytes=2400,
    ciphertext_bytes=1088,
    shared_secret_bytes=32
)

MLKEM1024 = KEMAlgorithm(
    name="ml-kem-1024",
    public_key_bytes=1568,
    secret_key_bytes=3168,
    ciphertext_bytes=1568,
    shared_secret_bytes=32
)

# HQC-KEM algorithms
HQCKEM128 = KEMAlgorithm(
    name="hqc-kem-128",
    public_key_bytes=2249,
    secret_key_bytes=2305,
    ciphertext_bytes=4433,
    shared_secret_bytes=64
)

HQCKEM192 = KEMAlgorithm(
    name="hqc-kem-192",
    public_key_bytes=4522,
    secret_key_bytes=4586,
    ciphertext_bytes=8978,
    shared_secret_bytes=64
)

HQCKEM256 = KEMAlgorithm(
    name="hqc-kem-256",
    public_key_bytes=7245,
    secret_key_bytes=7317,
    ciphertext_bytes=14421,
    shared_secret_bytes=64
)

# Classic McEliece algorithms
ClassicMcEliece348864 = KEMAlgorithm(
    name="mceliece348864",
    public_key_bytes=261120,
    secret_key_bytes=6492,
    ciphertext_bytes=96,
    shared_secret_bytes=32
)

ClassicMcEliece460896 = KEMAlgorithm(
    name="mceliece460896",
    public_key_bytes=524160,
    secret_key_bytes=13608,
    ciphertext_bytes=156,
    shared_secret_bytes=32
)

ClassicMcEliece6688128 = KEMAlgorithm(
    name="mceliece6688128",
    public_key_bytes=1044992,
    secret_key_bytes=13932,
    ciphertext_bytes=208,
    shared_secret_bytes=32
)

ClassicMcEliece6960119 = KEMAlgorithm(
    name="mceliece6960119",
    public_key_bytes=1047319,
    secret_key_bytes=13948,
    ciphertext_bytes=194,
    shared_secret_bytes=32
)

ClassicMcEliece8192128 = KEMAlgorithm(
    name="mceliece8192128",
    public_key_bytes=1357824,
    secret_key_bytes=14120,
    ciphertext_bytes=208,
    shared_secret_bytes=32
)
