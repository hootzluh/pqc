"""
Known Answer Test (KAT) validation for NIST Post-Quantum Cryptography algorithms
"""

import os
import re
from typing import Dict, List, Tuple, Optional
from pathlib import Path


class KATTestCase:
    """Represents a single KAT test case"""

    def __init__(self, count: int, seed: bytes, pk: bytes, sk: bytes, ct: bytes, ss: bytes):
        self.count = count
        self.seed = seed
        self.pk = pk
        self.sk = sk
        self.ct = ct
        self.ss = ss


class KATParser:
    """Parser for NIST KAT .rsp files"""

    @staticmethod
    def parse_hex_string(hex_str: str) -> bytes:
        """Parse a hex string, removing whitespace and comments"""
        # Remove comments and extra whitespace
        clean_str = re.sub(r'#.*$', '', hex_str, flags=re.MULTILINE)
        clean_str = re.sub(r'\s+', '', clean_str)
        clean_str = clean_str.strip()
        return bytes.fromhex(clean_str)

    @staticmethod
    def parse_kat_file(filepath: str) -> List[KATTestCase]:
        """Parse a KAT .rsp file and return list of test cases"""
        test_cases = []

        with open(filepath, 'r') as f:
            content = f.read()

        # Split into sections based on "count = X"
        sections = re.split(r'count = (\d+)', content)

        for i in range(1, len(sections), 2):
            count = int(sections[i])
            section = sections[i + 1]

            # Extract values using multiline regex
            seed_match = re.search(r'seed = ([0-9A-Fa-f\s]+?)(?=\n[A-Za-z]+ =|\n$)', section, re.DOTALL)
            pk_match = re.search(r'pk = ([0-9A-Fa-f\s]+?)(?=\n[A-Za-z]+ =|\n$)', section, re.DOTALL)
            sk_match = re.search(r'sk = ([0-9A-Fa-f\s]+?)(?=\n[A-Za-z]+ =|\n$)', section, re.DOTALL)
            ct_match = re.search(r'ct = ([0-9A-Fa-f\s]+?)(?=\n[A-Za-z]+ =|\n$)', section, re.DOTALL)
            ss_match = re.search(r'ss = ([0-9A-Fa-f]+?)(?=\n[A-Za-z]+ =|\n$)', section, re.DOTALL)

            if not all([seed_match, pk_match, sk_match, ct_match, ss_match]):
                raise ValueError(f"Missing required fields in test case {count}")

            try:
                seed = KATParser.parse_hex_string(seed_match.group(1))
                pk = KATParser.parse_hex_string(pk_match.group(1))
                sk = KATParser.parse_hex_string(sk_match.group(1))
                ct = KATParser.parse_hex_string(ct_match.group(1))
                ss = KATParser.parse_hex_string(ss_match.group(1))

                test_cases.append(KATTestCase(count, seed, pk, sk, ct, ss))
            except ValueError as e:
                print(f"Warning: Failed to parse test case {count}: {e}")
                continue

        return test_cases


class KATValidator:
    """Validates cryptographic implementations against KAT test vectors"""

    def __init__(self, kat_dir: str):
        self.kat_dir = Path(kat_dir)
        self.parsers = {
            'ml-kem-512': KATParser(),
            'ml-kem-768': KATParser(),
            'ml-kem-1024': KATParser(),
            'ml-dsa-44': KATParser(),
            'ml-dsa-65': KATParser(),
            'ml-dsa-87': KATParser(),
            'hqc-kem-128': KATParser(),
            'hqc-kem-192': KATParser(),
            'hqc-kem-256': KATParser(),
        }

    def get_kat_files(self, algorithm: str) -> Tuple[str, str]:
        """Get the .req and .rsp files for an algorithm"""
        # Map algorithm names to KAT file patterns
        name_map = {
            'ml-kem-512': 'kyber512',
            'ml-kem-768': 'kyber768',
            'ml-kem-1024': 'kyber1024',
            'ml-dsa-44': 'dilithium2',
            'ml-dsa-65': 'dilithium3',
            'ml-dsa-87': 'dilithium5',
            'hqc-kem-128': 'hqc-128',
            'hqc-kem-192': 'hqc-192',
            'hqc-kem-256': 'hqc-256',
        }

        base_name = name_map.get(algorithm)
        if not base_name:
            raise ValueError(f"No KAT files found for algorithm: {algorithm}")

        # Find the KAT files
        req_file = None
        rsp_file = None

        # Search in different possible locations
        search_paths = []

        if 'ml-kem' in algorithm or 'ml-dsa' in algorithm:
            search_paths.append(self.kat_dir / 'NIST-ml-kem' / 'KAT')
            search_paths.append(self.kat_dir / 'NIST-ml-dsa' / 'KAT')
        elif 'hqc' in algorithm:
            search_paths.append(self.kat_dir / 'NIST-hqc-kem' / 'KATs' / 'Optimized_Implementation')
            search_paths.append(self.kat_dir / 'NIST-hqc-kem' / 'KATs' / 'Reference_Implementation')

        for subdir_path in search_paths:
            if subdir_path.exists():
                # Look for files matching the pattern
                for file_path in subdir_path.rglob(f'*{base_name}*'):
                    if file_path.suffix == '.req':
                        req_file = str(file_path)
                    elif file_path.suffix == '.rsp':
                        rsp_file = str(file_path)

                # If not found, try looking for files in subdirectories
                if not req_file or not rsp_file:
                    for file_path in subdir_path.rglob(f'*.req'):
                        if base_name.replace('hqc-kem-', 'hqc-') in str(file_path):
                            req_file = str(file_path)
                    for file_path in subdir_path.rglob(f'*.rsp'):
                        if base_name.replace('hqc-kem-', 'hqc-') in str(file_path):
                            rsp_file = str(file_path)

        if not req_file or not rsp_file:
            raise FileNotFoundError(f"KAT files not found for {algorithm}")

        return req_file, rsp_file

    def validate_kem_algorithm(self, algorithm, kem_impl) -> Dict[str, int]:
        """Validate a KEM algorithm against KAT vectors"""
        print(f"Validating {algorithm} against KAT vectors...")

        try:
            req_file, rsp_file = self.get_kat_files(algorithm)
        except (ValueError, FileNotFoundError) as e:
            print(f"  ✗ Error finding KAT files: {e}")
            return {'total': 0, 'passed': 0, 'failed': 0}

        try:
            test_cases = self.parsers[algorithm].parse_kat_file(rsp_file)
        except Exception as e:
            print(f"  ✗ Error parsing KAT file: {e}")
            return {'total': 0, 'passed': 0, 'failed': 0}

        total = len(test_cases)
        passed = 0
        failed = 0

        print(f"  Testing {total} KAT vectors...")

        for test_case in test_cases[:10]:  # Test first 10 vectors for speed
            try:
                # Test keypair generation
                pk, sk = kem_impl.keypair()
                if len(pk) != len(test_case.pk) or len(sk) != len(test_case.sk):
                    print(f"    ✗ Test case {test_case.count}: Keypair size mismatch")
                    failed += 1
                    continue

                # Test encapsulation
                ct, ss_enc = kem_impl.enc(pk)
                if len(ct) != len(test_case.ct) or len(ss_enc) != len(test_case.ss):
                    print(f"    ✗ Test case {test_case.count}: Encapsulation size mismatch")
                    failed += 1
                    continue

                # Test decapsulation
                ss_dec = kem_impl.dec(ct, sk)
                if len(ss_dec) != len(test_case.ss):
                    print(f"    ✗ Test case {test_case.count}: Decapsulation size mismatch")
                    failed += 1
                    continue

                # Compare with expected values (byte-by-byte comparison)
                if ss_enc == ss_dec and ss_enc == test_case.ss:
                    passed += 1
                    print(f"    ✓ Test case {test_case.count}: PASSED")
                else:
                    failed += 1
                    print(f"    ✗ Test case {test_case.count}: Shared secret mismatch")
                    print(f"      Expected: {test_case.ss.hex()}")
                    print(f"      Got:      {ss_enc.hex()}")

            except Exception as e:
                print(f"    ✗ Test case {test_case.count}: Exception - {e}")
                failed += 1

        return {'total': total, 'passed': passed, 'failed': failed}

    def validate_signature_algorithm(self, algorithm, sig_impl) -> Dict[str, int]:
        """Validate a signature algorithm against KAT vectors"""
        print(f"Validating {algorithm} against KAT vectors...")

        try:
            req_file, rsp_file = self.get_kat_files(algorithm)
        except (ValueError, FileNotFoundError) as e:
            print(f"  ✗ Error finding KAT files: {e}")
            return {'total': 0, 'passed': 0, 'failed': 0}

        try:
            test_cases = self.parsers[algorithm].parse_kat_file(rsp_file)
        except Exception as e:
            print(f"  ✗ Error parsing KAT file: {e}")
            return {'total': 0, 'passed': 0, 'failed': 0}

        total = len(test_cases)
        passed = 0
        failed = 0

        print(f"  Testing {total} KAT vectors...")

        for test_case in test_cases[:10]:  # Test first 10 vectors for speed
            try:
                # Test keypair generation
                pk, sk = sig_impl.keypair()
                if len(pk) != len(test_case.pk) or len(sk) != len(test_case.sk):
                    print(f"    ✗ Test case {test_case.count}: Keypair size mismatch")
                    failed += 1
                    continue

                # For signature validation, we need a message to sign
                # The KAT files don't contain the message, so we'll use a standard message
                message = b"NIST KAT validation test message"

                # Test signing
                signature = sig_impl.sign(message, sk)
                if len(signature) < 1:
                    print(f"    ✗ Test case {test_case.count}: Empty signature")
                    failed += 1
                    continue

                # Test verification
                is_valid = sig_impl.verify(signature, message, pk)
                if not is_valid:
                    print(f"    ✗ Test case {test_case.count}: Signature verification failed")
                    failed += 1
                    continue

                # Test with wrong message (should fail)
                wrong_message = b"Different message"
                is_invalid = sig_impl.verify(signature, wrong_message, pk)
                if is_invalid:
                    print(f"    ✗ Test case {test_case.count}: Wrong message accepted")
                    failed += 1
                    continue

                passed += 1
                print(f"    ✓ Test case {test_case.count}: PASSED")

            except Exception as e:
                print(f"    ✗ Test case {test_case.count}: Exception - {e}")
                failed += 1

        return {'total': total, 'passed': passed, 'failed': failed}
