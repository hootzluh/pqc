#!/usr/bin/env python3
import sys, os, time, pathlib, json, subprocess

"""
KAT runner for pqvm
- For ML-KEM: verify decapsulation against .rsp vectors using host CLI (native)
- Logs results to archive/logs and writes summary to KAT_RESULTS.md
"""

ROOT = pathlib.Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "archive"
LOGS = ARCHIVE / "logs"
LOGS.mkdir(parents=True, exist_ok=True)

ts = time.strftime("%Y%m%d-%H%M%S")
log_path = LOGS / f"{ts}-run_kats_mlkem.log"

RESULTS_MD = ROOT / "KAT_RESULTS.md"

def log(msg: str):
    with open(log_path, 'a') as f:
        f.write(msg + "\n")
    print(msg)

def run_mlkem():
    kat_root = ROOT.parent / "pqkat" / "NIST-ml-kem-fips203" / "KAT"
    variants = {
        "mlkem512": kat_root / "mlkem512" / "PQCkemKAT_1632.rsp",
        "mlkem768": kat_root / "mlkem768" / "PQCkemKAT_2400.rsp",
        "mlkem1024": kat_root / "mlkem1024" / "PQCkemKAT_3168.rsp",
    }
    results = {}
    for variant, rsp in variants.items():
        if not rsp.exists():
            log(f"SKIP {variant}: {rsp} not found")
            continue
        cmd = ["cargo", "run", "-q", "-p", "mlkem_host_cli", "--", "--variant", variant, "--rsp", str(rsp)]
        log(f"running: {' '.join(cmd)} (cwd={ROOT})")
        cp = subprocess.run(cmd, cwd=str(ROOT))
        results[variant] = cp.returncode
        log(f"{variant}: exit_code={cp.returncode}")
    return results

if __name__ == "__main__":
    log("pqvm KAT runner starting (ML-KEM only)...")
    res = run_mlkem()
    passed = [k for k,v in res.items() if v == 0]
    failed = [k for k,v in res.items() if v != 0]
    summary = {
        "mlkem_passed": passed,
        "mlkem_failed": failed,
        "timestamp": ts,
    }
    log(json.dumps(summary, indent=2))
    with open(RESULTS_MD, 'a') as f:
        f.write(f"\n[ML-KEM] {ts} summary: {json.dumps(summary)}\n")
    sys.exit(0 if not failed else 1)
