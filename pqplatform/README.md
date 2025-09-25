# PQPlatform - Post-Quantum Cryptography for Smart TV & Smart Home Platforms

This directory contains implementations of NIST-selected post-quantum cryptographic algorithms optimized for smart TV and smart home platforms.

## Overview

PQPlatform provides optimized implementations for:
- **tvOS** (Apple TV) - tvOS 13.0+
- **Android TV** (smart TVs, streaming devices) - API level 21+
- **Smart Home Platforms**:
  - **Google Home/Assistant** - Cast-enabled devices
  - **Apple HomePod/HomeOS** - HomePod and HomePod mini
  - **Amazon Echo** - Alexa-enabled devices
  - **Smart displays** and **voice assistants**

## Supported Algorithms

All NIST Round 3 winners:

### Key Encapsulation Mechanisms (KEM)
- **ML-KEM** (FIPS 203): 512, 768, 1024 bit security
- **HQC-KEM**: 128, 192, 256 bit security

### Digital Signatures
- **ML-DSA** (FIPS 204): 44, 65, 87 bit security
- **FN-DSA** (Falcon): 512, 1024 bit security

*Note: Classic McEliece not included due to size/performance constraints on consumer devices*

## Architecture

### Rust Core
- Cross-platform Rust implementation
- Optimized for smart home networking
- Voice assistant and remote control integration

### Platform Integration
- **tvOS**: Swift/Objective-C bindings for Apple TV apps
- **Android TV**: JNI bindings for Android TV applications
- **Smart Home**: Platform-specific SDK integration for voice assistants
- **Cross-platform**: C FFI bindings for framework development

## Smart Home Integration

### Voice Assistant Security
- **Secure voice command processing**
- **Privacy-preserving audio analysis**
- **Trusted execution environments**
- **Device-to-device authentication**

### Network Security
- **Home network encryption**
- **IoT device authentication**
- **Secure firmware updates**
- **Remote access security**

### Smart TV Features
- **Content protection** (DRM integration)
- **Streaming security** (secure video delivery)
- **Remote control authentication**
- **Multi-user household security**

## Build Requirements

### Prerequisites
```bash
# Install Rust targets
rustup target add aarch64-apple-ios x86_64-apple-ios
rustup target add aarch64-linux-android armv7-linux-androideabi i686-linux-android

# Install platform SDKs
# - Xcode for tvOS development
# - Android SDK for Android TV
# - Platform-specific SDKs for smart home integration
```

### Building

```bash
./build.sh
```

This will cross-compile for all supported smart TV and smart home platforms.

## Directory Structure

```
pqplatform/
├── build.sh              # Cross-compilation script
├── README.md             # This file
├── pqcrypto/             # Rust implementation
├── common/               # Shared C code
├── crypto_kem/           # KEM algorithm implementations
├── crypto_sign/          # Signature algorithm implementations
└── archive/              # Build artifacts (after completion)
```

## Usage Examples

### tvOS Integration
```swift
import PQPlatform

// Secure streaming content
let kem = MLKEM512()
let (publicKey, secretKey) = try kem.keypair()
// ... DRM content protection ...

// Voice assistant authentication
let dsa = MLDSA65()
let (pubKey, privKey) = try dsa.keypair()
// ... secure voice command verification ...
```

### Android TV Integration
```java
import com.pqplatform.PQPlatform;

// Secure casting
MLKEM512 kem = new MLKEM512();
KeyPair keyPair = kem.keypair();
// ... secure content casting ...

// Multi-user authentication
MLDSA65 dsa = new MLDSA65();
KeyPair signKeys = dsa.keypair();
// ... household user verification ...
```

### Smart Home Integration
```javascript
// Google Home/Assistant
const pqPlatform = require('pqplatform');

// Secure device pairing
const kem = pqPlatform.MLKEM512();
const keys = kem.keypair();
// ... secure IoT device authentication ...

// Voice command security
const dsa = pqPlatform.MLDSA65();
const signKeys = dsa.keypair();
// ... privacy-preserving voice processing ...
```

## Performance Considerations

- **Network-optimized** for home connectivity
- **Multi-device coordination** support
- **Background processing** for always-on devices
- **Memory efficient** for consumer electronics
- **Power-aware** for always-listening devices

## Security Considerations

- **Home network security** (secure device mesh)
- **Privacy protection** (voice data security)
- **Multi-user isolation** (household security)
- **Remote access protection** (secure cloud integration)
- **Firmware security** (secure updates)

## Integration Patterns

### Smart Home Hub
- Central security coordinator for IoT devices
- Secure device discovery and pairing
- Network-wide key management

### Voice Assistant
- Privacy-preserving voice processing
- Secure command authentication
- Trusted execution for sensitive operations

### Smart TV/Entertainment
- Content protection and DRM
- Secure streaming protocols
- Multi-user content access control
