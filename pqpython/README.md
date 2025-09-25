# pqpython

Python bindings for NIST Post-Quantum Cryptography algorithms.

This package provides Python bindings to the PQClean implementations of NIST-selected post-quantum cryptographic algorithms, including:

## Key Encapsulation Mechanisms (KEM)
- **ML-KEM** (formerly Kyber): ML-KEM-512, ML-KEM-768, ML-KEM-1024
- **HQC**: HQC-128, HQC-192, HQC-256
- **Classic McEliece**: Multiple parameter sets

## Digital Signature Algorithms
- **ML-DSA** (formerly Dilithium): ML-DSA-44, ML-DSA-65, ML-DSA-87
- **Falcon**: Falcon-512, Falcon-1024
- **SPHINCS+**: Multiple SHA-256 and SHAKE-256 variants

## Installation

```bash
pip install .
```

## Usage

### Key Encapsulation

```python
import pqpython

# Generate keypair
public_key, secret_key = pqpython.MLKEM768.keypair()

# Encapsulate shared secret
ciphertext, shared_secret = pqpython.MLKEM768.enc(public_key)

# Decapsulate shared secret
decapsulated_secret = pqpython.MLKEM768.dec(ciphertext, secret_key)

assert shared_secret == decapsulated_secret
```

### Digital Signatures

```python
import pqpython

# Generate keypair
public_key, secret_key = pqpython.MLDSA65.keypair()

# Sign message
message = b"Hello, post-quantum world!"
signature = pqpython.MLDSA65.sign(message, secret_key)

# Verify signature
is_valid = pqpython.MLDSA65.verify(signature, message, public_key)
assert is_valid
```

### SPHINCS+ Signatures

```python
import pqpython

# Create SPHINCS+ instance
sphincs = pqpython.SPHINCS_SHA256_128F

# Generate keypair
public_key, secret_key = sphincs.keypair()

# Sign and verify
signature = sphincs.sign(message, secret_key)
is_valid = sphincs.verify(signature, message, public_key)
```

## Security

This package binds to the PQClean reference implementations of post-quantum cryptographic algorithms. These implementations are designed for correctness and clarity rather than optimized performance.

## Testing

The package includes comprehensive tests including Known Answer Tests (KAT) validation using the official NIST test vectors.

## License

This project uses the same license as PQClean.
