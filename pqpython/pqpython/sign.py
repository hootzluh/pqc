"""
Digital Signature algorithms for pqpython
"""

import os
import ctypes
from typing import Tuple, Optional
from pathlib import Path


class SignatureAlgorithm:
    """Base class for signature algorithms"""

    def __init__(self, name: str, public_key_bytes: int, secret_key_bytes: int, signature_bytes: int):
        self.name = name
        self.public_key_bytes = public_key_bytes
        self.secret_key_bytes = secret_key_bytes
        self.signature_bytes = signature_bytes

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
        # Handle FN-DSA naming convention (FALCON512 instead of FNDSA512)
        if self.name.startswith('fn-dsa-'):
            num = self.name.split('-')[2]  # Extract 512 or 1024
            func_prefix = f"PQCLEAN_FALCON{num}_CLEAN"
        else:
            func_prefix = f"PQCLEAN_{self.name.upper().replace('-', '')}_CLEAN"

        func_name = f"{func_prefix}_crypto_sign_keypair"
        keypair_func = getattr(self.lib, func_name)
        keypair_func.argtypes = [ctypes.POINTER(ctypes.c_uint8), ctypes.POINTER(ctypes.c_uint8)]
        keypair_func.restype = ctypes.c_int

        func_name = f"{func_prefix}_crypto_sign_signature"
        sign_func = getattr(self.lib, func_name)
        sign_func.argtypes = [ctypes.POINTER(ctypes.c_uint8), ctypes.POINTER(ctypes.c_size_t),
                             ctypes.POINTER(ctypes.c_uint8), ctypes.c_size_t,
                             ctypes.POINTER(ctypes.c_uint8)]
        sign_func.restype = ctypes.c_int

        func_name = f"{func_prefix}_crypto_sign_verify"
        verify_func = getattr(self.lib, func_name)
        verify_func.argtypes = [ctypes.POINTER(ctypes.c_uint8), ctypes.c_size_t,
                               ctypes.POINTER(ctypes.c_uint8), ctypes.c_size_t,
                               ctypes.POINTER(ctypes.c_uint8)]
        verify_func.restype = ctypes.c_int

    def keypair(self) -> Tuple[bytes, bytes]:
        """Generate a public/private keypair"""
        pk = (ctypes.c_uint8 * self.public_key_bytes)()
        sk = (ctypes.c_uint8 * self.secret_key_bytes)()

        if self.name.startswith('fn-dsa-'):
            num = self.name.split('-')[2]
            func_name = f"PQCLEAN_FALCON{num}_CLEAN_crypto_sign_keypair"
        else:
            func_name = f"PQCLEAN_{self.name.upper().replace('-', '')}_CLEAN_crypto_sign_keypair"
        func = getattr(self.lib, func_name)
        result = func(pk, sk)

        if result != 0:
            raise RuntimeError(f"Keypair generation failed for {self.name}")

        return bytes(pk), bytes(sk)

    def sign(self, message: bytes, secret_key: bytes, context: Optional[bytes] = None) -> bytes:
        """Sign a message"""
        if len(secret_key) != self.secret_key_bytes:
            raise ValueError(f"Secret key must be {self.secret_key_bytes} bytes")

        # For now, we'll only implement basic signing without context
        # Context-aware signing would require additional PQClean functions
        if context is not None:
            raise NotImplementedError("Context-aware signing not yet implemented")

        sig = (ctypes.c_uint8 * self.signature_bytes)()
        siglen = ctypes.c_size_t(self.signature_bytes)
        msg = (ctypes.c_uint8 * len(message))(*message)
        sk = (ctypes.c_uint8 * self.secret_key_bytes)(*secret_key)

        if self.name.startswith('fn-dsa-'):
            num = self.name.split('-')[2]
            func_name = f"PQCLEAN_FALCON{num}_CLEAN_crypto_sign_signature"
        else:
            func_name = f"PQCLEAN_{self.name.upper().replace('-', '')}_CLEAN_crypto_sign_signature"
        func = getattr(self.lib, func_name)
        result = func(sig, ctypes.byref(siglen), msg, len(message), sk)

        if result != 0:
            raise RuntimeError(f"Signing failed for {self.name}")

        return bytes(sig)[:siglen.value]

    def verify(self, signature: bytes, message: bytes, public_key: bytes, context: Optional[bytes] = None) -> bool:
        """Verify a signature"""
        if len(public_key) != self.public_key_bytes:
            raise ValueError(f"Public key must be {self.public_key_bytes} bytes")

        if context is not None:
            raise NotImplementedError("Context-aware verification not yet implemented")

        sig = (ctypes.c_uint8 * len(signature))(*signature)
        msg = (ctypes.c_uint8 * len(message))(*message)
        pk = (ctypes.c_uint8 * self.public_key_bytes)(*public_key)

        if self.name.startswith('fn-dsa-'):
            num = self.name.split('-')[2]
            func_name = f"PQCLEAN_FALCON{num}_CLEAN_crypto_sign_verify"
        else:
            func_name = f"PQCLEAN_{self.name.upper().replace('-', '')}_CLEAN_crypto_sign_verify"
        func = getattr(self.lib, func_name)
        result = func(sig, len(signature), msg, len(message), pk)

        return result == 0


# ML-DSA algorithms
MLDSA44 = SignatureAlgorithm(
    name="ml-dsa-44",
    public_key_bytes=1312,
    secret_key_bytes=2560,
    signature_bytes=2420
)

MLDSA65 = SignatureAlgorithm(
    name="ml-dsa-65",
    public_key_bytes=1952,
    secret_key_bytes=4032,
    signature_bytes=3309
)

MLDSA87 = SignatureAlgorithm(
    name="ml-dsa-87",
    public_key_bytes=2592,
    secret_key_bytes=4896,
    signature_bytes=4627
)

# FN-DSA algorithms (Falcon)
FNDSA512 = SignatureAlgorithm(
    name="falcon-512",
    public_key_bytes=897,
    secret_key_bytes=1281,
    signature_bytes=752
)

FNDSA1024 = SignatureAlgorithm(
    name="falcon-1024",
    public_key_bytes=1793,
    secret_key_bytes=2305,
    signature_bytes=1462
)
