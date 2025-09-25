# PQNoStd - Post-Quantum Cryptography for Embedded Systems (no_std)

This directory contains `no_std` implementations of NIST-selected post-quantum cryptographic algorithms for resource-constrained embedded devices.

## Overview

PQNoStd provides `no_std` Rust implementations for:
- **ARM Cortex-M** microcontrollers (M0, M3, M4, M7, M33)
- **ESP32** and **ESP8266** microcontrollers
- **RISC-V** based embedded systems
- **Bare-metal** and **RTOS** environments
- **IoT devices** with severe memory constraints

## Supported Algorithms

All NIST Round 3 winners (optimized for embedded):

### Key Encapsulation Mechanisms (KEM)
- **ML-KEM** (FIPS 203): 512, 768, 1024 bit security
- **HQC-KEM**: 128, 192, 256 bit security

### Digital Signatures
- **ML-DSA** (FIPS 204): 44, 65, 87 bit security
- **FN-DSA** (Falcon): 512, 1024 bit security

*Note: Classic McEliece not included due to memory requirements*

## Architecture

### no_std Rust Core
- **No standard library dependencies**
- **Heap allocation optional** (stack-only implementations available)
- **Static memory allocation** for predictable resource usage
- **Interrupt-safe** operations for RTOS integration

### Hardware Acceleration Support
- **ARM CryptoCell** (when available)
- **AES hardware acceleration**
- **SHA hardware acceleration**
- **True random number generation**

### Memory Profiles

#### Ultra-Constrained (ARM Cortex-M0/M0+)
- **RAM**: < 2KB stack usage
- **Flash**: < 10KB code size
- **Algorithms**: ML-KEM-512, ML-DSA-44 only

#### Standard Embedded (ARM Cortex-M3/M4)
- **RAM**: < 8KB stack usage
- **Flash**: < 50KB code size
- **Algorithms**: All variants supported

#### High-End Embedded (ARM Cortex-M7/M33, ESP32)
- **RAM**: < 32KB stack usage
- **Flash**: < 200KB code size
- **Algorithms**: All variants with optimizations

## Build Requirements

### Prerequisites
```bash
# Install Rust targets for embedded
rustup target add thumbv6m-none-eabi    # Cortex-M0/M0+
rustup target add thumbv7m-none-eabi    # Cortex-M3
rustup target add thumbv7em-none-eabi   # Cortex-M4/M7
rustup target add thumbv8m.main-none-eabi  # Cortex-M33
rustup target add riscv32imac-unknown-none-elf  # RISC-V

# For ESP32
rustup target add xtensa-esp32-none-elf

# Install cargo tools
cargo install cargo-binutils
cargo install probe-run  # For debugging
```

### Building

```bash
# Build for specific target
cargo build --target thumbv7m-none-eabi --release

# Build with specific memory constraints
cargo build --target thumbv6m-none-eabi --release --features "ultra-constrained"

# Build for ESP32
cargo build --target xtensa-esp32-none-elf --release
```

## Directory Structure

```
pqno_std/
├── Cargo.toml            # no_std Rust project configuration
├── build.rs              # Build script for C components
├── src/                  # no_std Rust source code
├── common/               # Shared C code (optimized for embedded)
├── crypto_kem/           # KEM algorithm implementations
├── crypto_sign/          # Signature algorithm implementations
├── examples/             # Embedded examples and demos
└── archive/              # Build artifacts (after completion)
```

## Usage Examples

### Basic no_std Usage
```rust
#![no_std]

use pqno_std::{MlKem512, MlDsa44};

fn main() {
    // Stack-allocated key buffers
    let mut public_key = [0u8; 800];  // ML-KEM-512 public key size
    let mut secret_key = [0u8; 1632]; // ML-KEM-512 secret key size
    let mut ciphertext = [0u8; 768];  // ML-KEM-512 ciphertext size
    let mut shared_secret = [0u8; 32]; // Shared secret size

    // Generate keypair
    MlKem512::keypair(&mut public_key, &mut secret_key);

    // Encapsulate
    MlKem512::encapsulate(&mut ciphertext, &mut shared_secret, &public_key);

    // Decapsulate
    let mut shared_secret2 = [0u8; 32];
    MlKem512::decapsulate(&mut shared_secret2, &ciphertext, &secret_key);
}
```

### RTOS Integration
```rust
use pqno_std::{MlKem512, MlDsa44};
use cortex_m_rt::entry;
use cortex_m_semihosting::hprintln;

#[entry]
fn main() -> ! {
    // Initialize RNG (hardware or software)
    let mut rng = // ... hardware RNG setup

    // Secure key exchange in IoT network
    let mut device_keys = MlKem512::new();
    device_keys.keypair(&mut rng);

    // Sign firmware updates
    let mut signature_keys = MlDsa44::new();
    signature_keys.keypair(&mut rng);

    loop {
        // Main RTOS loop
        // ... secure communication with gateway
    }
}
```

### ESP32 Usage
```rust
use pqno_std::{MlKem512, MlDsa44};
use esp_idf_hal::delay::Delay;

fn main() {
    let delay = Delay::new_default();

    // Use ESP32 hardware RNG
    let mut rng = esp_idf_hal::rng::Rng::new();

    // Secure IoT communication
    let mut kem = MlKem512::new();
    let (public_key, secret_key) = kem.keypair(&mut rng);

    // Send public key to server
    // ... secure channel establishment
}
```

## Memory Management

### Stack-Only Operations
```rust
use pqno_std::stack_only::*;

fn secure_boot() {
    // All operations use only stack memory
    let mut boot_keys = StackMlKem512::new();
    let verification_result = boot_keys.verify_firmware_signature(firmware_data, signature);
}
```

### Static Allocation
```rust
use pqno_std::static_alloc::*;

// Pre-allocated buffers at compile time
static mut KEY_BUFFER: [u8; 1632] = [0; 1632];
static mut SIGNATURE_BUFFER: [u8; 3300] = [0; 3300];

fn secure_communication() {
    let keys = unsafe { StaticMlKem512::from_buffer(&mut KEY_BUFFER) };
    // ... secure operations
}
```

## Performance Optimizations

### Algorithm Selection Guide

| Device Class | RAM Available | Recommended Algorithms |
|-------------|---------------|------------------------|
| Cortex-M0/M0+ | < 2KB | ML-KEM-512, ML-DSA-44 |
| Cortex-M3 | 8-16KB | ML-KEM-512/768, ML-DSA-44/65 |
| Cortex-M4/M7 | 32-128KB | All algorithms |
| ESP32 | 320KB | All algorithms + hardware accel |
| ESP8266 | 80KB | ML-KEM-512/768, ML-DSA-44 |

### Optimization Features

- **Constant-time** implementations (timing attack protection)
- **Memory-safe** operations (no heap allocation by default)
- **Interrupt-safe** for RTOS environments
- **Hardware acceleration** when available
- **Reduced code size** variants for ultra-constrained devices

## Security Considerations

### Embedded-Specific Threats
- **Physical attacks** (side-channel analysis)
- **Power analysis** (SPA/DPA attacks)
- **Fault injection** attacks
- **Memory dumping** attacks

### Countermeasures
- **Constant-time** implementations
- **Memory protection** (when available)
- **Secure boot** integration
- **Key derivation** from hardware RNG
- **Secure element** integration (when available)

## Testing

### Unit Tests
```bash
# Run tests on host (with std)
cargo test

# Run tests on embedded target
cargo test --target thumbv7m-none-eabi
```

### Integration Testing
```bash
# Flash to device
cargo run --bin example --target thumbv7m-none-eabi

# Debug with probe-run
cargo run --bin example --target thumbv7m-none-eabi --features "probe-run"
```

## Supported Boards

### STMicroelectronics
- **STM32F0** series (Cortex-M0)
- **STM32F1/F3** series (Cortex-M3/M4)
- **STM32F4/F7** series (Cortex-M4/M7)

### Nordic Semiconductor
- **nRF52832/52840** (Cortex-M4)
- **nRF9160** (Cortex-M33)

### Espressif
- **ESP32** (Xtensa LX6)
- **ESP8266** (Xtensa LX106)

### Raspberry Pi
- **RP2040** (Dual Cortex-M0+)

## Contributing

When adding new algorithms or optimizations:

1. **Maintain no_std compatibility**
2. **Test on actual hardware** (not just QEMU)
3. **Document memory usage** and performance
4. **Consider hardware acceleration** opportunities
5. **Ensure constant-time operations**
