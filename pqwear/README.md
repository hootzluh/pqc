# PQWear - Post-Quantum Cryptography for Wearable Devices

This directory contains lightweight implementations of NIST-selected post-quantum cryptographic algorithms optimized for wearable devices.

## Overview

PQWear provides resource-optimized implementations for:
- **watchOS** (Apple Watch) - watchOS 6.0+
- **Wear OS** (Android Wear) - API level 25+
- **Smart rings** and **fitness trackers**
- **Resource-constrained** wearable devices

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

- **Ultra-memory optimized** for wearable constraints (< 50MB RAM)
- **Battery-aware** implementations (low power consumption)
- **Fast operations** (sub-second key generation)
- **Background processing** with minimal CPU usage
- **Thread-safe** operations for companion app integration

## Security Notes

- All implementations are **constant-time**
- **Memory-safe** operations
- **Platform security** integration (Keychain, Keystore)
- **Certificate pinning** support
