# PQMobile - Post-Quantum Cryptography for Mobile Platforms

This directory contains cross-compiled implementations of NIST-selected post-quantum cryptographic algorithms for mobile platforms (phones and tablets).

## Overview

PQMobile provides optimized implementations for:
- **iOS** (iPhone, iPad) - iOS 12.0+
- **Android** (phones, tablets) - API level 21+
- **Cross-platform** frameworks (React Native, Flutter, etc.)

## Supported Algorithms

All NIST Round 3 winners:

### Key Encapsulation Mechanisms (KEM)
- **ML-KEM** (FIPS 203): 512, 768, 1024 bit security
- **HQC-KEM**: 128, 192, 256 bit security

### Digital Signatures
- **ML-DSA** (FIPS 204): 44, 65, 87 bit security
- **FN-DSA** (Falcon): 512, 1024 bit security

*Note: Classic McEliece not included due to size/performance constraints on mobile devices*

## Architecture

### Rust Core
- Cross-platform Rust implementation
- Bindings for iOS and Android
- Optimized for mobile CPU architectures

### Platform Integration
- **iOS**: Swift/Objective-C bindings
- **Android**: JNI (Java Native Interface)
- **Cross-platform**: C FFI bindings

## Build Requirements

### Prerequisites
```bash
# Install Rust targets
rustup target add aarch64-apple-ios x86_64-apple-ios
rustup target add aarch64-linux-android armv7-linux-androideabi i686-linux-android

# Install Android NDK
# Install Xcode for iOS development
```

### Building

```bash
./build.sh
```

This will cross-compile for all supported mobile platforms.

## Directory Structure

```
pqmobile/
├── build.sh              # Cross-compilation script
├── README.md             # This file
├── pqcrypto/             # Rust implementation
├── common/               # Shared C code
├── crypto_kem/           # KEM algorithm implementations
├── crypto_sign/          # Signature algorithm implementations
└── archive/              # Build artifacts (after completion)
```

## Usage

### iOS Integration
```swift
import PQMobile

// Example usage
let kem = MLKEM512()
let (publicKey, secretKey) = try kem.keypair()
let (ciphertext, sharedSecret) = try kem.encapsulate(publicKey)
// ... etc
```

### Android Integration
```java
import com.pqmobile.PQMobile;

// Example usage
MLKEM512 kem = new MLKEM512();
KeyPair keyPair = kem.keypair();
EncapsulatedKey encapsulated = kem.encapsulate(keyPair.publicKey);
// ... etc
```

## Performance Considerations

- **Memory optimized** for mobile constraints
- **Battery aware** implementations
- **Background processing** support
- **Thread-safe** operations

## Security Notes

- All implementations are **constant-time**
- **Memory-safe** operations
- **Platform security** integration (Keychain, Keystore)
- **Certificate pinning** support
