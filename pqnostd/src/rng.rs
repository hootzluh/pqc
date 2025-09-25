//! Random number generation for no_std environments

use crate::Error;

/// Random number generator core trait
pub trait RngCore {
    /// Fill the buffer with random bytes
    fn fill_bytes(&mut self, buffer: &mut [u8]) -> Result<(), Error>;

    /// Generate a single random u32
    fn next_u32(&mut self) -> Result<u32, Error> {
        let mut buf = [0u8; 4];
        self.fill_bytes(&mut buf)?;
        Ok(u32::from_le_bytes(buf))
    }

    /// Generate a single random u64
    fn next_u64(&mut self) -> Result<u64, Error> {
        let mut buf = [0u8; 8];
        self.fill_bytes(&mut buf)?;
        Ok(u64::from_le_bytes(buf))
    }
}

/// Software-based ChaCha RNG (when hardware RNG not available)
#[cfg(feature = "test")]
pub struct ChaChaRng {
    // Implementation would use rand_chacha crate
}

#[cfg(feature = "test")]
impl RngCore for ChaChaRng {
    fn fill_bytes(&mut self, buffer: &mut [u8]) -> Result<(), Error> {
        // Use rand_chacha to fill buffer
        // This would require std, so only available in test mode
        todo!("Implement ChaCha RNG")
    }
}

/// Hardware RNG for Cortex-M devices with TRNG
#[cfg(any(feature = "cortex-m33", feature = "cortex-m4", feature = "cortex-m7"))]
pub struct HardwareRng;

#[cfg(any(feature = "cortex-m33", feature = "cortex-m4", feature = "cortex-m7"))]
impl HardwareRng {
    /// Create a new hardware RNG instance
    pub fn new() -> Self {
        Self
    }

    /// Check if hardware RNG is available
    pub fn is_available() -> bool {
        // Check if RNG peripheral is available and enabled
        // Implementation depends on specific MCU
        true // Placeholder
    }
}

#[cfg(any(feature = "cortex-m33", feature = "cortex-m4", feature = "cortex-m7"))]
impl RngCore for HardwareRng {
    fn fill_bytes(&mut self, buffer: &mut [u8]) -> Result<(), Error> {
        // Use MCU-specific RNG peripheral
        // This would use PAC (Peripheral Access Crate) for the specific MCU
        Err(Error::HardwareAccelUnavailable) // Placeholder
    }
}

/// Hardware RNG for ESP32
#[cfg(feature = "esp32")]
pub struct Esp32Rng;

#[cfg(feature = "esp32")]
impl Esp32Rng {
    /// Create a new ESP32 RNG instance
    pub fn new() -> Self {
        Self
    }
}

#[cfg(feature = "esp32")]
impl RngCore for Esp32Rng {
    fn fill_bytes(&mut self, buffer: &mut [u8]) -> Result<(), Error> {
        // Use ESP32 RNG peripheral
        Err(Error::HardwareAccelUnavailable) // Placeholder
    }
}

/// Initialize hardware RNG if available
pub fn init_hardware_rng() {
    #[cfg(any(feature = "cortex-m33", feature = "cortex-m4", feature = "cortex-m7"))]
    {
        // Initialize Cortex-M RNG peripheral
        unsafe {
            // RNG initialization code would go here
        }
    }

    #[cfg(feature = "esp32")]
    {
        // Initialize ESP32 RNG
        unsafe {
            // ESP32 RNG initialization code would go here
        }
    }
}

/// Get the best available RNG for the current platform
pub fn get_rng() -> Result<&'static mut dyn RngCore, Error> {
    #[cfg(any(feature = "cortex-m33", feature = "cortex-m4", feature = "cortex-m7"))]
    {
        static mut HW_RNG: Option<HardwareRng> = None;
        unsafe {
            if HW_RNG.is_none() {
                HW_RNG = Some(HardwareRng::new());
            }
            if let Some(rng) = &mut HW_RNG {
                return Ok(rng);
            }
        }
    }

    #[cfg(feature = "esp32")]
    {
        static mut ESP_RNG: Option<Esp32Rng> = None;
        unsafe {
            if ESP_RNG.is_none() {
                ESP_RNG = Some(Esp32Rng::new());
            }
            if let Some(rng) = &mut ESP_RNG {
                return Ok(rng);
            }
        }
    }

    Err(Error::RngFailure)
}
