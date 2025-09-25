// Test HQC-KEM implementation
use pqcrypto_hqc::hqc256;

fn main() {
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

    println!("✓ HQC-KEM-256 test passed!");
}
