import unittest
import os
from cryptocoreutils.modes.etm import ETMMode


class TestETMMode(unittest.TestCase):
    """Tests for Encrypt-then-MAC mode."""

    def test_etm_basic_encrypt_decrypt(self):
        """Basic ETM encryption/decryption."""
        key = os.urandom(16)
        plaintext = b"Test ETM mode"

        etm = ETMMode(key, mode='cbc')
        ciphertext = etm.encrypt(plaintext)

        # Verify structure: IV(16) + ciphertext + tag(32)
        self.assertGreaterEqual(len(ciphertext), 48)

        # Decrypt
        decrypted = etm.decrypt(ciphertext)
        self.assertEqual(plaintext, decrypted)

    def test_etm_with_aad(self):
        """ETM with additional authenticated data."""
        key = os.urandom(16)
        plaintext = b"Secret data"
        aad = b"metadata: important"

        etm = ETMMode(key, mode='cbc')
        ciphertext = etm.encrypt(plaintext, aad)

        # Correct AAD
        decrypted = etm.decrypt(ciphertext, aad)
        self.assertEqual(plaintext, decrypted)

        # Wrong AAD should fail
        with self.assertRaises(Exception) as e:
            etm.decrypt(ciphertext, b"wrong metadata")
        self.assertIn("Authentication", str(e.exception))

    def test_etm_ciphertext_tampering(self):
        """ETM should detect ciphertext tampering."""
        key = os.urandom(16)
        plaintext = b"Don't tamper with me!"

        etm = ETMMode(key, mode='cbc')
        ciphertext = etm.encrypt(plaintext)

        # Tamper with ciphertext (not IV or tag)
        tampered = bytearray(ciphertext)
        tampered[20] ^= 0x01  # Change a byte in the ciphertext part

        with self.assertRaises(Exception):
            etm.decrypt(bytes(tampered))

    def test_etm_tag_tampering(self):
        """ETM should detect tag tampering."""
        key = os.urandom(16)
        plaintext = b"Test tag security"

        etm = ETMMode(key, mode='cbc')
        ciphertext = etm.encrypt(plaintext)

        # Tamper with tag (last 32 bytes)
        tampered = bytearray(ciphertext)
        tampered[-1] ^= 0xFF

        with self.assertRaises(Exception):
            etm.decrypt(bytes(tampered))

    def test_etm_file_operations(self):
        """ETM file encryption/decryption."""
        import tempfile

        key = os.urandom(16)
        plaintext = b"File operation test content"
        aad = b"file metadata"

        with tempfile.NamedTemporaryFile(delete=False) as f_input:
            f_input.write(plaintext)
            input_path = f_input.name

        encrypted_path = input_path + '.etm'
        decrypted_path = input_path + '.dec'

        try:
            # Encrypt file
            etm = ETMMode(key, mode='cbc')
            etm.encrypt_file(input_path, encrypted_path, aad)

            # Decrypt file
            etm2 = ETMMode(key, mode='cbc')
            etm2.decrypt_file(encrypted_path, decrypted_path, aad)

            # Verify
            with open(decrypted_path, 'rb') as f:
                decrypted = f.read()
            self.assertEqual(plaintext, decrypted)

            # Test catastrophic failure
            wrong_key = os.urandom(16)
            etm_wrong = ETMMode(wrong_key, mode='cbc')

            with self.assertRaises(Exception):
                etm_wrong.decrypt_file(encrypted_path, decrypted_path + '.wrong', aad)

        finally:
            # Cleanup
            import os
            for path in [input_path, encrypted_path, decrypted_path]:
                if os.path.exists(path):
                    os.remove(path)


if __name__ == '__main__':
    unittest.main()