"""
RFC 4231 HMAC-SHA256 test vectors.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from cryptocoreutils.mac.hmac import HMAC


class TestHMACRFC4231Vectors(unittest.TestCase):
    """RFC 4231 HMAC-SHA256 Known Answer Tests."""

    def test_case_1(self):
        """
        RFC 4231 Test Case 1.
        Key:  0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b (20 bytes)
        Data: "Hi There"
        HMAC-SHA-256: b0344c61d8db38535ca8afceaf0bf12b881dc200c9833da726e9376c2e32cff7
        """
        key = bytes.fromhex('0b' * 20)
        data = b'Hi There'
        expected = 'b0344c61d8db38535ca8afceaf0bf12b881dc200c9833da726e9376c2e32cff7'

        hmac = HMAC(key, 'sha256')
        hmac.update(data)

        self.assertEqual(hmac.hexdigest(), expected)
        print("✓ RFC 4231 Test Case 1 passed")

    def test_case_2(self):
        """
        RFC 4231 Test Case 2.
        Key:  "Jefe"
        Data: "what do ya want for nothing?"
        HMAC-SHA-256: 5bdcc146bf60754e6a042426089575c75a003f089d2739839dec58b964ec3843
        """
        key = b'Jefe'
        data = b'what do ya want for nothing?'
        expected = '5bdcc146bf60754e6a042426089575c75a003f089d2739839dec58b964ec3843'

        hmac = HMAC(key, 'sha256')
        hmac.update(data)

        self.assertEqual(hmac.hexdigest(), expected)
        print("✓ RFC 4231 Test Case 2 passed")

    def test_case_3(self):
        """
        RFC 4231 Test Case 3.
        Key:  0xaa repeated 20 times
        Data: 0xdd repeated 50 times
        HMAC-SHA-256: 773ea91e36800e46854db8ebd09181a72959098b3ef8c122d9635514ced565fe
        """
        key = bytes.fromhex('aa' * 20)
        data = bytes.fromhex('dd' * 50)
        expected = '773ea91e36800e46854db8ebd09181a72959098b3ef8c122d9635514ced565fe'

        hmac = HMAC(key, 'sha256')
        hmac.update(data)

        self.assertEqual(hmac.hexdigest(), expected)
        print("✓ RFC 4231 Test Case 3 passed")

    def test_case_4(self):
        """
        RFC 4231 Test Case 4.
        Key:  0x0102030405060708090a0b0c0d0e0f10111213141516171819 (25 bytes)
        Data: 0xcd repeated 50 times
        HMAC-SHA-256: 82558a389a443c0ea4cc819899f2083a85f0faa3e578f8077a2e3ff46729665b
        """
        key = bytes.fromhex('0102030405060708090a0b0c0d0e0f10111213141516171819')
        data = bytes.fromhex('cd' * 50)
        expected = '82558a389a443c0ea4cc819899f2083a85f0faa3e578f8077a2e3ff46729665b'

        hmac = HMAC(key, 'sha256')
        hmac.update(data)

        self.assertEqual(hmac.hexdigest(), expected)
        print("✓ RFC 4231 Test Case 4 passed")

    def test_case_6(self):
        """
        RFC 4231 Test Case 6 - Long key (131 bytes).
        Key:  0xaa repeated 131 times
        Data: "Test Using Larger Than Block-Size Key - Hash Key First"
        HMAC-SHA-256: 60e431591ee0b67f0d8a26aacbf5b77f8e0bc6213728c5140546040f0ee37f54
        """
        key = bytes.fromhex('aa' * 131)
        data = b'Test Using Larger Than Block-Size Key - Hash Key First'
        expected = '60e431591ee0b67f0d8a26aacbf5b77f8e0bc6213728c5140546040f0ee37f54'

        hmac = HMAC(key, 'sha256')
        hmac.update(data)

        self.assertEqual(hmac.hexdigest(), expected)
        print("✓ RFC 4231 Test Case 6 passed")

    def test_case_7(self):
        """
        RFC 4231 Test Case 7 - Long key and long data.
        Key:  0xaa repeated 131 times
        Data: "This is a test using a larger than block-size key and a
               larger than block-size data..."
        """
        key = bytes.fromhex('aa' * 131)
        data = (b'This is a test using a larger than block-size key and a '
                b'larger than block-size data. The key needs to be hashed '
                b'before being used by the HMAC algorithm.')
        expected = '9b09ffa71b942fcb27635fbcd5b0e944bfdc63644f0713938a7f51535c3a35e2'

        hmac = HMAC(key, 'sha256')
        hmac.update(data)

        self.assertEqual(hmac.hexdigest(), expected)
        print("✓ RFC 4231 Test Case 7 passed")


if __name__ == '__main__':
    unittest.main(verbosity=2)