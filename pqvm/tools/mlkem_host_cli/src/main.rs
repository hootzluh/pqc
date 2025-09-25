use anyhow::{anyhow, Result};
use clap::Parser;
use serde::Serialize;
use std::fs::File;
use std::io::{BufRead, BufReader};
// Bring trait methods into scope for from_bytes/as_bytes
use pqcrypto_traits::kem::{Ciphertext as _, SecretKey as _, SharedSecret as _};

#[derive(Parser, Debug)]
#[command(author, version, about = "ML-KEM KAT verifier (decap check from .rsp)", long_about=None)]
struct Args {
    /// Variant: mlkem512 | mlkem768 | mlkem1024
    #[arg(long)]
    variant: String,
    /// Path to .rsp file
    #[arg(long)]
    rsp: String,
}

#[derive(Serialize)]
struct KatSummary {
    variant: String,
    cases_total: usize,
    cases_passed: usize,
}

fn parse_hex(s: &str) -> Result<Vec<u8>> {
    let s = s.trim();
    let s = s.strip_prefix("0x").unwrap_or(s);
    Ok(hex::decode(s)?)
}

fn run_rsp(variant: &str, path: &str) -> Result<KatSummary> {
    let f = File::open(path)?;
    let r = BufReader::new(f);
    let mut cases_total = 0usize;
    let mut cases_passed = 0usize;

    let mut cur_ct: Option<Vec<u8>> = None;
    let mut cur_sk: Option<Vec<u8>> = None;
    let mut cur_ss: Option<Vec<u8>> = None;

    for line in r.lines() {
        let line = line?;
        let l = line.trim();
        if l.is_empty() || l.starts_with('#') { continue; }
        if let Some(rest) = l.strip_prefix("ct =") { cur_ct = Some(parse_hex(rest)?); }
        if let Some(rest) = l.strip_prefix("sk =") { cur_sk = Some(parse_hex(rest)?); }
        if let Some(rest) = l.strip_prefix("ss =") { cur_ss = Some(parse_hex(rest)?); }
        if l.starts_with("count =") {
            // on new count boundary, if we have a complete prior tuple, evaluate it
            if let (Some(ct), Some(sk), Some(ss)) = (cur_ct.take(), cur_sk.take(), cur_ss.take()) {
                cases_total += 1;
                let ok = verify_case(variant, &ct, &sk, &ss)?;
                if ok { cases_passed += 1; }
            }
        }
    }
    // tail case
    if let (Some(ct), Some(sk), Some(ss)) = (cur_ct.take(), cur_sk.take(), cur_ss.take()) {
        cases_total += 1;
        let ok = verify_case(variant, &ct, &sk, &ss)?;
        if ok { cases_passed += 1; }
    }

    Ok(KatSummary { variant: variant.to_string(), cases_total, cases_passed })
}

fn verify_case(variant: &str, ct: &[u8], sk: &[u8], ss_exp: &[u8]) -> Result<bool> {
    match variant {
        "mlkem512" => {
            use pqcrypto_mlkem::mlkem512 as v;
            let ct = v::Ciphertext::from_bytes(ct).map_err(|e| anyhow!("ct: {e:?}"))?;
            let sk = v::SecretKey::from_bytes(sk).map_err(|e| anyhow!("sk: {e:?}"))?;
            let ss = v::decapsulate(&ct, &sk);
            Ok(ss.as_bytes() == ss_exp)
        }
        "mlkem768" => {
            use pqcrypto_mlkem::mlkem768 as v;
            let ct = v::Ciphertext::from_bytes(ct).map_err(|e| anyhow!("ct: {e:?}"))?;
            let sk = v::SecretKey::from_bytes(sk).map_err(|e| anyhow!("sk: {e:?}"))?;
            let ss = v::decapsulate(&ct, &sk);
            Ok(ss.as_bytes() == ss_exp)
        }
        "mlkem1024" => {
            use pqcrypto_mlkem::mlkem1024 as v;
            let ct = v::Ciphertext::from_bytes(ct).map_err(|e| anyhow!("ct: {e:?}"))?;
            let sk = v::SecretKey::from_bytes(sk).map_err(|e| anyhow!("sk: {e:?}"))?;
            let ss = v::decapsulate(&ct, &sk);
            Ok(ss.as_bytes() == ss_exp)
        }
        _ => Err(anyhow!("unknown variant: {variant}")),
    }
}

fn main() -> Result<()> {
    let args = Args::parse();
    let summary = run_rsp(&args.variant, &args.rsp)?;
    println!("{}", serde_json::to_string(&summary)?);
    if summary.cases_total == summary.cases_passed { Ok(()) } else { std::process::exit(1) }
}

