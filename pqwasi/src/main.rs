// PQCWASI Test Implementation
use pqcrypto_mlkem::mlkem768;
use pqcrypto_mldsa::mldsa65;
use pqcrypto_hqc::hqc256;

fn main() {
    println!("Testing PQCWASI implementation...");

    // Test ML-KEM-768
    println!("Testing ML-KEM-768...");
    let (pk, sk) = mlkem768::keypair();
    println!("✓ ML-KEM-768 keypair generated (pk: {} bytes, sk: {} bytes)",
             pk.len(), sk.len());

    let (ct, ss) = mlkem768::encapsulate(&pk);
    println!("✓ ML-KEM-768 encapsulation (ct: {} bytes, ss: {} bytes)",
             ct.len(), ss.len());

    let dec_ss = mlkem768::decapsulate(&ct, &sk);
    println!("✓ ML-KEM-768 decapsulation (ss: {} bytes)", dec_ss.len());

    assert_eq!(ss, dec_ss, "Shared secrets must match");
    println!("✓ ML-KEM-768 encapsulation/decapsulation roundtrip successful");

    // Test ML-DSA-65
    println!("Testing ML-DSA-65...");
    let (pk, sk) = mldsa65::keypair();
    println!("✓ ML-DSA-65 keypair generated (pk: {} bytes, sk: {} bytes)",
             pk.len(), sk.len());

    let message = b"Hello, post-quantum world!";
    let signature = mldsa65::sign(&message, &sk);
    println!("✓ ML-DSA-65 signature generated ({} bytes)", signature.len());

    let is_valid = mldsa65::verify(&signature, &message, &pk);
    assert!(is_valid, "Signature verification must succeed");
    println!("✓ ML-DSA-65 signature verification successful");

    // Test with wrong message
    let wrong_message = b"Different message";
    let is_invalid = mldsa65::verify(&signature, &wrong_message, &pk);
    assert!(!is_invalid, "Wrong message must fail verification");
    println!("✓ ML-DSA-65 correctly rejects wrong message");

    // Test HQC-KEM-256
    println!("Testing HQC-KEM-256...");
    let (pk, sk) = hqc256::keypair();
    println!("✓ HQC-256 keypair generated (pk: {} bytes, sk: {} bytes)",
             pk.len(), sk.len());

    let (ct, ss) = hqc256::encapsulate(&pk);
    println!("✓ HQC-256 encapsulation (ct: {} bytes, ss: {} bytes)",
             ct.len(), ss.len());

    let dec_ss = hqc256::decapsulate(&ct, &sk);
    println!("✓ HQC-256 decapsulation (ss: {} bytes)", dec_ss.len());

    assert_eq!(ss, dec_ss, "Shared secrets must match");
    println!("✓ HQC-256 encapsulation/decapsulation roundtrip successful");

    println!("✓ All PQCWASI tests passed!");
}
