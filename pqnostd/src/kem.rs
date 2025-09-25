//! Key Encapsulation Mechanism (KEM) implementations
//!
//! This module provides no_std compatible KEM implementations optimized
//! for embedded systems.

use core::result::Result;
use super::Error;
use pqcrypto_traits::kem::{
    Ciphertext as KemCiphertext, PublicKey as KemPublicKey, SecretKey as KemSecretKey,
    SharedSecret as KemSharedSecret,
};

/// ML-KEM-512 implementation
pub struct MlKem512;

impl MlKem512 {
    /// Public key length in bytes
    pub const PUBLIC_KEY_LEN: usize = 800;
    /// Secret key length in bytes
    pub const SECRET_KEY_LEN: usize = 1632;
    /// Ciphertext length in bytes
    pub const CIPHERTEXT_LEN: usize = 768;
    /// Shared secret length in bytes
    pub const SHARED_SECRET_LEN: usize = 32;

    /// Generate ML-KEM-512 keypair
    pub fn keypair(pk: &mut [u8], sk: &mut [u8]) -> Result<(), Error> {
        if pk.len() < Self::PUBLIC_KEY_LEN || sk.len() < Self::SECRET_KEY_LEN {
            return Err(Error::InvalidInput);
        }

        let (pqc_pk, pqc_sk) = pqcrypto_mlkem::mlkem512_keypair();
        pk[..Self::PUBLIC_KEY_LEN].copy_from_slice(pqc_pk.as_bytes());
        sk[..Self::SECRET_KEY_LEN].copy_from_slice(pqc_sk.as_bytes());
        Ok(())
    }

    /// Encapsulate a shared secret
    pub fn encapsulate(
        ct: &mut [u8],
        ss: &mut [u8],
        pk: &[u8]
    ) -> Result<(), Error> {
        if ct.len() < Self::CIPHERTEXT_LEN || ss.len() < Self::SHARED_SECRET_LEN || pk.len() < Self::PUBLIC_KEY_LEN {
            return Err(Error::InvalidInput);
        }

        let pqc_pk = pqcrypto_mlkem::mlkem512::PublicKey::from_bytes(pk)
            .map_err(|_| Error::InvalidInput)?;
        let (pqc_ct, pqc_ss) = pqcrypto_mlkem::mlkem512_encapsulate(&pqc_pk);
        let ct_bytes = pqc_ct.as_bytes();
        let ss_bytes = pqc_ss.as_bytes();
        assert!(ct_bytes.len() <= ct.len(), "Ciphertext buffer too small");
        assert!(ss_bytes.len() <= ss.len(), "Shared secret buffer too small");
        ct[..ct_bytes.len()].copy_from_slice(ct_bytes);
        ss[..ss_bytes.len()].copy_from_slice(ss_bytes);
        Ok(())
    }

    /// Decapsulate a shared secret
    pub fn decapsulate(
        ss: &mut [u8],
        ct: &[u8],
        sk: &[u8]
    ) -> Result<(), Error> {
        if ss.len() < Self::SHARED_SECRET_LEN || ct.len() < Self::CIPHERTEXT_LEN || sk.len() < Self::SECRET_KEY_LEN {
            return Err(Error::InvalidInput);
        }

        let pqc_sk = pqcrypto_mlkem::mlkem512::SecretKey::from_bytes(sk)
            .map_err(|_| Error::InvalidInput)?;
        let pqc_ct = pqcrypto_mlkem::mlkem512::Ciphertext::from_bytes(ct)
            .map_err(|_| Error::InvalidInput)?;
        let pqc_ss = pqcrypto_mlkem::mlkem512_decapsulate(&pqc_ct, &pqc_sk);
        let ss_bytes = pqc_ss.as_bytes();
        assert!(ss_bytes.len() <= ss.len(), "Shared secret buffer too small");
        ss[..ss_bytes.len()].copy_from_slice(ss_bytes);
        Ok(())
    }
}

/// ML-KEM-768 implementation
pub struct MlKem768;

impl MlKem768 {
    /// Public key length in bytes
    pub const PUBLIC_KEY_LEN: usize = 1184;
    /// Secret key length in bytes
    pub const SECRET_KEY_LEN: usize = 2400;
    /// Ciphertext length in bytes
    pub const CIPHERTEXT_LEN: usize = 1088;
    /// Shared secret length in bytes
    pub const SHARED_SECRET_LEN: usize = 32;

    /// Generate ML-KEM-768 keypair
    pub fn keypair(pk: &mut [u8], sk: &mut [u8]) -> Result<(), Error> {
        if pk.len() < Self::PUBLIC_KEY_LEN || sk.len() < Self::SECRET_KEY_LEN {
            return Err(Error::InvalidInput);
        }

        let (pqc_pk, pqc_sk) = pqcrypto_mlkem::mlkem768_keypair();
        pk[..Self::PUBLIC_KEY_LEN].copy_from_slice(pqc_pk.as_bytes());
        sk[..Self::SECRET_KEY_LEN].copy_from_slice(pqc_sk.as_bytes());
        Ok(())
    }

    /// Encapsulate a shared secret
    pub fn encapsulate(
        ct: &mut [u8],
        ss: &mut [u8],
        pk: &[u8]
    ) -> Result<(), Error> {
        if ct.len() < Self::CIPHERTEXT_LEN || ss.len() < Self::SHARED_SECRET_LEN || pk.len() < Self::PUBLIC_KEY_LEN {
            return Err(Error::InvalidInput);
        }

        let pqc_pk = pqcrypto_mlkem::mlkem768::PublicKey::from_bytes(pk)
            .map_err(|_| Error::InvalidInput)?;
        let (pqc_ct, pqc_ss) = pqcrypto_mlkem::mlkem768_encapsulate(&pqc_pk);
        ct[..Self::CIPHERTEXT_LEN].copy_from_slice(pqc_ct.as_bytes());
        ss[..Self::SHARED_SECRET_LEN].copy_from_slice(pqc_ss.as_bytes());
        Ok(())
    }

    /// Decapsulate a shared secret
    pub fn decapsulate(
        ss: &mut [u8],
        ct: &[u8],
        sk: &[u8]
    ) -> Result<(), Error> {
        if ss.len() < Self::SHARED_SECRET_LEN || ct.len() < Self::CIPHERTEXT_LEN || sk.len() < Self::SECRET_KEY_LEN {
            return Err(Error::InvalidInput);
        }

        let pqc_sk = pqcrypto_mlkem::mlkem768::SecretKey::from_bytes(sk)
            .map_err(|_| Error::InvalidInput)?;
        let pqc_ct = pqcrypto_mlkem::mlkem768::Ciphertext::from_bytes(ct)
            .map_err(|_| Error::InvalidInput)?;
        let pqc_ss = pqcrypto_mlkem::mlkem768_decapsulate(&pqc_ct, &pqc_sk);
        ss[..Self::SHARED_SECRET_LEN].copy_from_slice(pqc_ss.as_bytes());
        Ok(())
    }
}

/// ML-KEM-1024 implementation
pub struct MlKem1024;

impl MlKem1024 {
    /// Public key length in bytes
    pub const PUBLIC_KEY_LEN: usize = 1568;
    /// Secret key length in bytes
    pub const SECRET_KEY_LEN: usize = 3168;
    /// Ciphertext length in bytes
    pub const CIPHERTEXT_LEN: usize = 1568;
    /// Shared secret length in bytes
    pub const SHARED_SECRET_LEN: usize = 32;

    /// Generate ML-KEM-1024 keypair
    pub fn keypair(pk: &mut [u8], sk: &mut [u8]) -> Result<(), Error> {
        if pk.len() < Self::PUBLIC_KEY_LEN || sk.len() < Self::SECRET_KEY_LEN {
            return Err(Error::InvalidInput);
        }

        let (pqc_pk, pqc_sk) = pqcrypto_mlkem::mlkem1024_keypair();
        pk[..Self::PUBLIC_KEY_LEN].copy_from_slice(pqc_pk.as_bytes());
        sk[..Self::SECRET_KEY_LEN].copy_from_slice(pqc_sk.as_bytes());
        Ok(())
    }

    /// Encapsulate a shared secret
    pub fn encapsulate(
        ct: &mut [u8],
        ss: &mut [u8],
        pk: &[u8]
    ) -> Result<(), Error> {
        if ct.len() < Self::CIPHERTEXT_LEN || ss.len() < Self::SHARED_SECRET_LEN || pk.len() < Self::PUBLIC_KEY_LEN {
            return Err(Error::InvalidInput);
        }

        let pqc_pk = pqcrypto_mlkem::mlkem1024::PublicKey::from_bytes(pk)
            .map_err(|_| Error::InvalidInput)?;
        let (pqc_ct, pqc_ss) = pqcrypto_mlkem::mlkem1024_encapsulate(&pqc_pk);
        ct[..Self::CIPHERTEXT_LEN].copy_from_slice(pqc_ct.as_bytes());
        ss[..Self::SHARED_SECRET_LEN].copy_from_slice(pqc_ss.as_bytes());
        Ok(())
    }

    /// Decapsulate a shared secret
    pub fn decapsulate(
        ss: &mut [u8],
        ct: &[u8],
        sk: &[u8]
    ) -> Result<(), Error> {
        if ss.len() < Self::SHARED_SECRET_LEN || ct.len() < Self::CIPHERTEXT_LEN || sk.len() < Self::SECRET_KEY_LEN {
            return Err(Error::InvalidInput);
        }

        let pqc_sk = pqcrypto_mlkem::mlkem1024::SecretKey::from_bytes(sk)
            .map_err(|_| Error::InvalidInput)?;
        let pqc_ct = pqcrypto_mlkem::mlkem1024::Ciphertext::from_bytes(ct)
            .map_err(|_| Error::InvalidInput)?;
        let pqc_ss = pqcrypto_mlkem::mlkem1024_decapsulate(&pqc_ct, &pqc_sk);
        ss[..Self::SHARED_SECRET_LEN].copy_from_slice(pqc_ss.as_bytes());
        Ok(())
    }
}

/// HQC-KEM-128 implementation
pub struct Hqc128;

impl Hqc128 {
    /// Public key length in bytes
    pub const PUBLIC_KEY_LEN: usize = 2249;
    /// Secret key length in bytes
    pub const SECRET_KEY_LEN: usize = 57;
    /// Ciphertext length in bytes
    pub const CIPHERTEXT_LEN: usize = 4481;
    /// Shared secret length in bytes
    pub const SHARED_SECRET_LEN: usize = 32;

    /// Generate HQC-KEM-128 keypair
    pub fn keypair(pk: &mut [u8], sk: &mut [u8]) -> Result<(), Error> {
        if pk.len() < Self::PUBLIC_KEY_LEN || sk.len() < Self::SECRET_KEY_LEN {
            return Err(Error::InvalidInput);
        }

        let (pqc_pk, pqc_sk) = pqcrypto_hqc::hqc128::keypair();
        let pk_bytes = pqc_pk.as_bytes();
        let sk_bytes = pqc_sk.as_bytes();
        assert!(pk_bytes.len() <= pk.len(), "Public key buffer too small");
        assert!(sk_bytes.len() <= sk.len(), "Secret key buffer too small");
        pk[..pk_bytes.len()].copy_from_slice(pk_bytes);
        sk[..sk_bytes.len()].copy_from_slice(sk_bytes);
        Ok(())
    }

    /// Encapsulate a shared secret
    pub fn encapsulate(
        ct: &mut [u8],
        ss: &mut [u8],
        pk: &[u8]
    ) -> Result<(), Error> {
        if ct.len() < Self::CIPHERTEXT_LEN || ss.len() < Self::SHARED_SECRET_LEN || pk.len() < Self::PUBLIC_KEY_LEN {
            return Err(Error::InvalidInput);
        }

        let pqc_pk = pqcrypto_hqc::hqc128::PublicKey::from_bytes(pk)
            .map_err(|_| Error::InvalidInput)?;
        let (pqc_ct, pqc_ss) = pqcrypto_hqc::hqc128_encapsulate(&pqc_pk);
        ct[..Self::CIPHERTEXT_LEN].copy_from_slice(pqc_ct.as_bytes());
        ss[..Self::SHARED_SECRET_LEN].copy_from_slice(pqc_ss.as_bytes());
        Ok(())
    }

    /// Decapsulate a shared secret
    pub fn decapsulate(
        ss: &mut [u8],
        ct: &[u8],
        sk: &[u8]
    ) -> Result<(), Error> {
        if ss.len() < Self::SHARED_SECRET_LEN || ct.len() < Self::CIPHERTEXT_LEN || sk.len() < Self::SECRET_KEY_LEN {
            return Err(Error::InvalidInput);
        }

        let pqc_sk = pqcrypto_hqc::hqc128::SecretKey::from_bytes(sk)
            .map_err(|_| Error::InvalidInput)?;
        let pqc_ct = pqcrypto_hqc::hqc128::Ciphertext::from_bytes(ct)
            .map_err(|_| Error::InvalidInput)?;
        let pqc_ss = pqcrypto_hqc::hqc128_decapsulate(&pqc_ct, &pqc_sk);
        ss[..Self::SHARED_SECRET_LEN].copy_from_slice(pqc_ss.as_bytes());
        Ok(())
    }
}

/// HQC-KEM-192 implementation
pub struct Hqc192;

impl Hqc192 {
    /// Public key length in bytes
    pub const PUBLIC_KEY_LEN: usize = 4522;
    /// Secret key length in bytes
    pub const SECRET_KEY_LEN: usize = 57;
    /// Ciphertext length in bytes
    pub const CIPHERTEXT_LEN: usize = 9026;
    /// Shared secret length in bytes
    pub const SHARED_SECRET_LEN: usize = 32;

    /// Generate HQC-KEM-192 keypair
    pub fn keypair(pk: &mut [u8], sk: &mut [u8]) -> Result<(), Error> {
        if pk.len() < Self::PUBLIC_KEY_LEN || sk.len() < Self::SECRET_KEY_LEN {
            return Err(Error::InvalidInput);
        }

        let (pqc_pk, pqc_sk) = pqcrypto_hqc::hqc192::keypair();
        let pk_bytes = pqc_pk.as_bytes();
        let sk_bytes = pqc_sk.as_bytes();
        assert!(pk_bytes.len() <= pk.len(), "Public key buffer too small");
        assert!(sk_bytes.len() <= sk.len(), "Secret key buffer too small");
        pk[..pk_bytes.len()].copy_from_slice(pk_bytes);
        sk[..sk_bytes.len()].copy_from_slice(sk_bytes);
        Ok(())
    }

    /// Encapsulate a shared secret
    pub fn encapsulate(
        ct: &mut [u8],
        ss: &mut [u8],
        pk: &[u8]
    ) -> Result<(), Error> {
        if ct.len() < Self::CIPHERTEXT_LEN || ss.len() < Self::SHARED_SECRET_LEN || pk.len() < Self::PUBLIC_KEY_LEN {
            return Err(Error::InvalidInput);
        }

        let pqc_pk = pqcrypto_hqc::hqc192::PublicKey::from_bytes(pk)
            .map_err(|_| Error::InvalidInput)?;
        let (pqc_ct, pqc_ss) = pqcrypto_hqc::hqc192_encapsulate(&pqc_pk);
        ct[..Self::CIPHERTEXT_LEN].copy_from_slice(pqc_ct.as_bytes());
        ss[..Self::SHARED_SECRET_LEN].copy_from_slice(pqc_ss.as_bytes());
        Ok(())
    }

    /// Decapsulate a shared secret
    pub fn decapsulate(
        ss: &mut [u8],
        ct: &[u8],
        sk: &[u8]
    ) -> Result<(), Error> {
        if ss.len() < Self::SHARED_SECRET_LEN || ct.len() < Self::CIPHERTEXT_LEN || sk.len() < Self::SECRET_KEY_LEN {
            return Err(Error::InvalidInput);
        }

        let pqc_sk = pqcrypto_hqc::hqc192::SecretKey::from_bytes(sk)
            .map_err(|_| Error::InvalidInput)?;
        let pqc_ct = pqcrypto_hqc::hqc192::Ciphertext::from_bytes(ct)
            .map_err(|_| Error::InvalidInput)?;
        let pqc_ss = pqcrypto_hqc::hqc192_decapsulate(&pqc_ct, &pqc_sk);
        ss[..Self::SHARED_SECRET_LEN].copy_from_slice(pqc_ss.as_bytes());
        Ok(())
    }
}

/// HQC-KEM-256 implementation
pub struct Hqc256;

impl Hqc256 {
    /// Public key length in bytes
    pub const PUBLIC_KEY_LEN: usize = 7245;
    /// Secret key length in bytes
    pub const SECRET_KEY_LEN: usize = 57;
    /// Ciphertext length in bytes
    pub const CIPHERTEXT_LEN: usize = 14469;
    /// Shared secret length in bytes
    pub const SHARED_SECRET_LEN: usize = 32;

    /// Generate HQC-KEM-256 keypair
    pub fn keypair(pk: &mut [u8], sk: &mut [u8]) -> Result<(), Error> {
        if pk.len() < Self::PUBLIC_KEY_LEN || sk.len() < Self::SECRET_KEY_LEN {
            return Err(Error::InvalidInput);
        }

        let (pqc_pk, pqc_sk) = pqcrypto_hqc::hqc256::keypair();
        let pk_bytes = pqc_pk.as_bytes();
        let sk_bytes = pqc_sk.as_bytes();
        assert!(pk_bytes.len() <= pk.len(), "Public key buffer too small");
        assert!(sk_bytes.len() <= sk.len(), "Secret key buffer too small");
        pk[..pk_bytes.len()].copy_from_slice(pk_bytes);
        sk[..sk_bytes.len()].copy_from_slice(sk_bytes);
        Ok(())
    }

    /// Encapsulate a shared secret
    pub fn encapsulate(
        ct: &mut [u8],
        ss: &mut [u8],
        pk: &[u8]
    ) -> Result<(), Error> {
        if ct.len() < Self::CIPHERTEXT_LEN || ss.len() < Self::SHARED_SECRET_LEN || pk.len() < Self::PUBLIC_KEY_LEN {
            return Err(Error::InvalidInput);
        }

        let pqc_pk = pqcrypto_hqc::hqc256::PublicKey::from_bytes(pk)
            .map_err(|_| Error::InvalidInput)?;
        let (pqc_ct, pqc_ss) = pqcrypto_hqc::hqc256_encapsulate(&pqc_pk);
        ct[..Self::CIPHERTEXT_LEN].copy_from_slice(pqc_ct.as_bytes());
        ss[..Self::SHARED_SECRET_LEN].copy_from_slice(pqc_ss.as_bytes());
        Ok(())
    }

    /// Decapsulate a shared secret
    pub fn decapsulate(
        ss: &mut [u8],
        ct: &[u8],
        sk: &[u8]
    ) -> Result<(), Error> {
        if ss.len() < Self::SHARED_SECRET_LEN || ct.len() < Self::CIPHERTEXT_LEN || sk.len() < Self::SECRET_KEY_LEN {
            return Err(Error::InvalidInput);
        }

        let pqc_sk = pqcrypto_hqc::hqc256::SecretKey::from_bytes(sk)
            .map_err(|_| Error::InvalidInput)?;
        let pqc_ct = pqcrypto_hqc::hqc256::Ciphertext::from_bytes(ct)
            .map_err(|_| Error::InvalidInput)?;
        let pqc_ss = pqcrypto_hqc::hqc256_decapsulate(&pqc_ct, &pqc_sk);
        ss[..Self::SHARED_SECRET_LEN].copy_from_slice(pqc_ss.as_bytes());
        Ok(())
    }
}
