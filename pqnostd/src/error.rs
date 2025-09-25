//! Error types for PQNoStd operations

/// Result type alias for PQNoStd operations
pub type Result<T> = core::result::Result<T, Error>;

/// Error types that can occur during cryptographic operations
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[repr(u8)]
pub enum Error {
    /// Invalid input parameters
    InvalidInput = 1,

    /// Insufficient buffer size
    BufferTooSmall = 2,

    /// Random number generation failed
    RngFailure = 3,

    /// Verification failed (signatures, etc.)
    VerificationFailed = 4,

    /// Hardware acceleration not available
    HardwareAccelUnavailable = 5,

    /// Memory allocation failed
    MemoryAllocationFailed = 6,

    /// Operation not supported on this platform
    UnsupportedOperation = 7,

    /// Internal error (should not occur)
    InternalError = 8,
}

impl Error {
    /// Get a human-readable description of the error
    pub const fn description(&self) -> &'static str {
        match self {
            Error::InvalidInput => "Invalid input parameters",
            Error::BufferTooSmall => "Buffer too small for operation",
            Error::RngFailure => "Random number generation failed",
            Error::VerificationFailed => "Verification failed",
            Error::HardwareAccelUnavailable => "Hardware acceleration not available",
            Error::MemoryAllocationFailed => "Memory allocation failed",
            Error::UnsupportedOperation => "Operation not supported on this platform",
            Error::InternalError => "Internal error",
        }
    }

    /// Get the error code as a u8
    pub const fn code(&self) -> u8 {
        *self as u8
    }
}

/// Convert from a raw error code to Error enum
impl TryFrom<u8> for Error {
    type Error = ();

    fn try_from(value: u8) -> core::result::Result<Self, Self::Error> {
        match value {
            1 => Ok(Error::InvalidInput),
            2 => Ok(Error::BufferTooSmall),
            3 => Ok(Error::RngFailure),
            4 => Ok(Error::VerificationFailed),
            5 => Ok(Error::HardwareAccelUnavailable),
            6 => Ok(Error::MemoryAllocationFailed),
            7 => Ok(Error::UnsupportedOperation),
            8 => Ok(Error::InternalError),
            _ => Err(()),
        }
    }
}

#[cfg(feature = "alloc")]
use alloc::string::ToString;

#[cfg(feature = "alloc")]
impl alloc::fmt::Display for Error {
    fn fmt(&self, f: &mut alloc::fmt::Formatter<'_>) -> alloc::fmt::Result {
        write!(f, "{}", self.description())
    }
}
