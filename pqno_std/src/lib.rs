#![no_std]
#![cfg_attr(feature = "alloc", feature(alloc))]

//! # PQNoStd - Post-Quantum Cryptography for Embedded Systems
//!
//! This crate provides `no_std` implementations of NIST-selected post-quantum
//! cryptographic algorithms optimized for resource-constrained embedded devices.
//!
//! ## Features
//!
//! - **no_std compatible** - No standard library dependencies
//! - **Stack-only operations** - Optional heap allocation
//! - **Hardware acceleration** - Support for crypto hardware when available
//! - **Memory constrained** - Optimized for devices with limited RAM/flash
//! - **Constant time** - Protection against timing attacks
//!
//! ## Supported Algorithms
//!
//! ### Key Encapsulation Mechanisms (KEM)
//! - **ML-KEM** (FIPS 203): 512, 768, 1024 bit security
//! - **HQC-KEM**: 128, 192, 256 bit security
//!
//! ### Digital Signatures
//! - **ML-DSA** (FIPS 204): 44, 65, 87 bit security
//! - **FN-DSA** (Falcon): 512, 1024 bit security
//!
//! ## Usage
//!
//! ```rust,ignore
//! use pqno_std::{MlKem512, MlDsa44};
//!
//! // Stack-allocated buffers
//! let mut public_key = [0u8; 800];   // ML-KEM-512 public key
//! let mut secret_key = [0u8; 1632];  // ML-KEM-512 secret key
//! let mut ciphertext = [0u8; 768];   // ML-KEM-512 ciphertext
//! let mut shared_secret = [0u8; 32]; // Shared secret
//!
//! // Generate keypair
//! MlKem512::keypair(&mut public_key, &mut secret_key, rng);
//!
//! // Encapsulate
//! MlKem512::encapsulate(&mut ciphertext, &mut shared_secret, &public_key, rng);
//!
//! // Decapsulate
//! MlKem512::decapsulate(&mut shared_secret, &ciphertext, &secret_key);
//! ```

#[cfg(feature = "alloc")]
extern crate alloc;

// Re-export for convenience
pub use core::{cmp, mem, ptr, slice};

// Error types
pub mod error;
pub use error::Error;

// Random number generation
pub mod rng;
pub use rng::RngCore;

// Algorithm implementations
pub mod kem;
pub mod sign;

// Re-export algorithms
pub use kem::*;
pub use sign::*;

// Memory management utilities
pub mod memory;

// Testing utilities (only when std is available)
#[cfg(feature = "test")]
pub mod test_utils;

/// Initialize the cryptographic library
///
/// This function should be called before using any cryptographic operations
/// to ensure proper initialization of hardware acceleration and random number
/// generation.
pub fn init() -> Result<(), Error> {
    // Initialize hardware acceleration if available
    #[cfg(feature = "hw-accel")]
    {
        // Initialize AES/SHA hardware
        unsafe { memory::init_hardware_accel() };
    }

    // Initialize RNG if hardware RNG is available
    #[cfg(any(feature = "cortex-m33", feature = "esp32"))]
    {
        rng::init_hardware_rng();
    }

    Ok(())
}

/// Get library version information
pub const fn version() -> &'static str {
    env!("CARGO_PKG_VERSION")
}

/// Get supported features at compile time
#[macro_export]
macro_rules! features {
    () => {
        concat!(
            "alloc=", cfg!(feature = "alloc"), ",",
            "hw-accel=", cfg!(feature = "hw-accel"), ",",
            "ultra-constrained=", cfg!(feature = "ultra-constrained"), ",",
            "standard-embedded=", cfg!(feature = "standard-embedded"), ",",
            "high-end-embedded=", cfg!(feature = "high-end-embedded")
        )
    };
}

/// Compile-time memory usage information
#[macro_export]
macro_rules! memory_usage {
    ($algorithm:ident) => {
        concat!(
            stringify!($algorithm),
            " - Stack: ", $algorithm::STACK_USAGE, " bytes",
            ", Flash: ", $algorithm::FLASH_USAGE, " bytes"
        )
    };
}
