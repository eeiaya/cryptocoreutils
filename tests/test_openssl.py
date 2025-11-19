"""OpenSSL interoperability tests for all modes"""
import subprocess
import os
import tempfile

def run_command(cmd, capture_output=True):
    """Executes command and returns error details"""
    try:
        result = subprocess.run(cmd, capture_output=capture_output, text=True, check=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, f"Exit code: {e.returncode}, Error: {e.stderr}"


def run_openssl_test(mode):
    """Tests one mode with OpenSSL"""
    print(f"Testing {mode.upper()} mode...")

    # Create temporary file with data aligned to block size (16 bytes)
    test_data = "Test data 16 bytes"  # Exactly 16 bytes
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write(test_data)
        test_file = f.name

    try:
        # Test 1: Our utility -> OpenSSL
        print("  Our -> OpenSSL...", end="")

        # Encrypt with our utility
        success, error = run_command([
            'python3', 'main.py', '-alg', 'aes', '-m', mode, '-enc',
            '-k', '00112233445566778899aabbccddeeff',
            '-i', test_file, '-o', test_file + '.our.enc'
        ])

        if not success:
            print(f" FAIL - Our encryption failed: {error}")
            return False

        # For modes that require different OpenSSL handling
        if mode in ['cfb', 'ofb', 'ctr']:
            # Stream modes - use -nopad
            return test_stream_mode(mode, test_file)
        else:
            # Block modes (ECB, CBC) - handle padding
            return test_block_mode(mode, test_file)

    except Exception as e:
        print(f" FAIL - Unexpected error: {e}")
        return False
    finally:
        # Cleanup temporary files
        for ext in ['.our.enc', '.ciphertext_only.bin', '.openssl.dec', '.openssl.enc', '.our.dec']:
            temp_path = test_file + ext
            if os.path.exists(temp_path):
                os.remove(temp_path)
        if os.path.exists(test_file):
            os.remove(test_file)


def test_stream_mode(mode, test_file):
    """Test stream modes (CFB, OFB, CTR) with -nopad"""
    # Extract IV from our file
    with open(test_file + '.our.enc', 'rb') as f:
        iv_data = f.read(16)
        iv_hex = iv_data.hex()

    # Extract ciphertext only (skip IV)
    ciphertext_file = test_file + '.ciphertext_only.bin'
    with open(test_file + '.our.enc', 'rb') as fin:
        with open(ciphertext_file, 'wb') as fout:
            fin.seek(16)  # Skip IV
            fout.write(fin.read())

    # Decrypt with OpenSSL
    success, error = run_command([
        'openssl', 'enc', f'-aes-128-{mode}', '-d',
        '-K', '00112233445566778899aabbccddeeff',
        '-iv', iv_hex,
        '-in', ciphertext_file,
        '-out', test_file + '.openssl.dec',
        '-nopad'
    ])

    if not success:
        print(f" FAIL - OpenSSL decryption failed: {error}")
        return False

    # Check
    with open(test_file, 'rb') as f1, open(test_file + '.openssl.dec', 'rb') as f2:
        test1_pass = f1.read() == f2.read()

    print(" PASS" if test1_pass else " FAIL")

    # Test 2: OpenSSL -> Our utility
    print("  OpenSSL -> Our...", end="")

    # Generate IV for OpenSSL encryption
    success, iv_result = run_command(['openssl', 'rand', '-hex', '16'])
    if not success:
        print(f" FAIL - IV generation failed: {iv_result}")
        return False
    new_iv = iv_result.strip()

    # Encrypt with OpenSSL
    success, error = run_command([
        'openssl', 'enc', f'-aes-128-{mode}',
        '-K', '00112233445566778899aabbccddeeff',
        '-iv', new_iv,
        '-in', test_file, '-out', test_file + '.openssl.enc',
        '-nosalt', '-nopad'
    ])

    if not success:
        print(f" FAIL - OpenSSL encryption failed: {error}")
        return False

    # Decrypt with our utility
    success, error = run_command([
        'python3', 'main.py', '-alg', 'aes', '-m', mode, '-dec',
        '-k', '00112233445566778899aabbccddeeff',
        '-iv', new_iv,
        '-i', test_file + '.openssl.enc',
        '-o', test_file + '.our.dec'
    ])

    if not success:
        print(f" FAIL - Our decryption failed: {error}")
        return False

    # Check
    with open(test_file, 'rb') as f1, open(test_file + '.our.dec', 'rb') as f2:
        test2_pass = f1.read() == f2.read()

    print(" PASS" if test2_pass else " FAIL")

    return test1_pass and test2_pass


def test_block_mode(mode, test_file):
    """Test block modes (ECB, CBC) with padding"""
    # Test 1: Our utility -> OpenSSL
    print("  Our -> OpenSSL...", end="")

    # For ECB, no IV handling needed
    if mode == 'ecb':
        # Use our encrypted file directly with OpenSSL
        success, error = run_command([
            'openssl', 'enc', '-aes-128-ecb', '-d',
            '-K', '00112233445566778899aabbccddeeff',
            '-in', test_file + '.our.enc',
            '-out', test_file + '.openssl.dec'
        ])
        # В функции test_block_mode, для CBC режима:
    else:
        # CBC - extract IV and use only ciphertext
        with open(test_file + '.our.enc', 'rb') as f:
            iv_data = f.read(16)
            iv_hex = iv_data.hex()

        # Create file with ciphertext only (skip IV)
        ciphertext_file = test_file + '.ciphertext_only.bin'
        with open(test_file + '.our.enc', 'rb') as fin:
            with open(ciphertext_file, 'wb') as fout:
                fin.seek(16)  # Skip IV
                fout.write(fin.read())

        success, error = run_command([
            'openssl', 'enc', f'-aes-128-{mode}', '-d',
            '-K', '00112233445566778899aabbccddeeff',
            '-iv', iv_hex,
            '-in', ciphertext_file,  # ← Use ciphertext only, no IV!
            '-out', test_file + '.openssl.dec'
        ])
    if not success:
        print(f" FAIL - OpenSSL decryption failed: {error}")
        return False

    # Check
    with open(test_file, 'rb') as f1, open(test_file + '.openssl.dec', 'rb') as f2:
        test1_pass = f1.read() == f2.read()

    print(" PASS" if test1_pass else " FAIL")

    # Test 2: OpenSSL -> Our utility
    print("  OpenSSL -> Our...", end="")

    if mode == 'ecb':
        # Encrypt with OpenSSL
        success, error = run_command([
            'openssl', 'enc', '-aes-128-ecb',
            '-K', '00112233445566778899aabbccddeeff',
            '-in', test_file, '-out', test_file + '.openssl.enc'
        ])

        # Decrypt with our utility
        success, error = run_command([
            'python3', 'main.py', '-alg', 'aes', '-m', mode, '-dec',
            '-k', '00112233445566778899aabbccddeeff',
            '-i', test_file + '.openssl.enc',
            '-o', test_file + '.our.dec'
        ])
    else:
        # Generate IV for OpenSSL encryption
        success, iv_result = run_command(['openssl', 'rand', '-hex', '16'])
        if not success:
            print(f" FAIL - IV generation failed: {iv_result}")
            return False
        new_iv = iv_result.strip()

        # Encrypt with OpenSSL
        success, error = run_command([
            'openssl', 'enc', f'-aes-128-{mode}',
            '-K', '00112233445566778899aabbccddeeff',
            '-iv', new_iv,
            '-in', test_file, '-out', test_file + '.openssl.enc'
        ])

        # Decrypt with our utility
        success, error = run_command([
            'python3', 'main.py', '-alg', 'aes', '-m', mode, '-dec',
            '-k', '00112233445566778899aabbccddeeff',
            '-iv', new_iv,
            '-i', test_file + '.openssl.enc',
            '-o', test_file + '.our.dec'
        ])

    if not success:
        print(f" FAIL - Our decryption failed: {error}")
        return False

    # Check
    with open(test_file, 'rb') as f1, open(test_file + '.our.dec', 'rb') as f2:
        test2_pass = f1.read() == f2.read()

    print(" PASS" if test2_pass else " FAIL")

    return test1_pass and test2_pass

def main():
    print("OpenSSL Interoperability Tests")
    print("=" * 50)

    # Test all modes
    modes = ['ecb', 'cbc', 'cfb', 'ofb', 'ctr']
    results = []

    for mode in modes:
        success = run_openssl_test(mode)
        results.append((mode, success))
        print()

    # Results
    print("Final Results:")
    print("=" * 50)
    all_passed = True
    for mode, success in results:
        status = "PASS" if success else "FAIL"
        print(f"  {mode.upper()}: {status}")
        if not success:
            all_passed = False

    print(f"\nOverall: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")

if __name__ == "__main__":
    main()