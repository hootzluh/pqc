#![cfg_attr(not(test), no_std)]

// Scaffold pallet: Minimal types and placeholders; real FRAME wiring added later.

pub mod api {
    // Host-call like interface placeholders for PQC operations.
    // Final pallet will expose dispatchables and runtime APIs.
    pub fn mlkem_keygen(_param: &str) -> Result<(), u8> { Err(1) }
    pub fn mlkem_encap(_param: &str, _pk: &[u8], _ct: &mut [u8], _ss: &mut [u8]) -> Result<(), u8> { Err(1) }
    pub fn mlkem_decap(_param: &str, _sk: &[u8], _ct: &[u8], _ss: &mut [u8]) -> Result<(), u8> { Err(1) }

    pub fn mldsa_keygen(_param: &str) -> Result<(), u8> { Err(1) }
    pub fn mldsa_sign(_param: &str, _sk: &[u8], _m: &[u8], _sig: &mut [u8]) -> Result<(), u8> { Err(1) }
    pub fn mldsa_verify(_param: &str, _pk: &[u8], _m: &[u8], _sig: &[u8]) -> bool { false }
}

