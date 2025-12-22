import os
from pathlib import Path
from ..crypto.aes import AES128
from ..exceptions import AuthenticationError, CryptoOperationError
from ..csprng import generate_random_bytes


class GCMMode:
    NONCE_SIZE = 12
    TAG_SIZE = 16
    BLOCK_SIZE = 16
    GF_REDUCTION = 0xE1 << 120



    def __init__(self, key: bytes, nonce: bytes = None):
        # Если ключ строка hex, преобразуем в байты
        if isinstance(key, str):
            try:
                key = bytes.fromhex(key)
            except ValueError:
                raise ValueError("Ключ должен быть hex-строкой или байтами")

        # Проверяем допустимые размеры ключа
        if len(key) not in (16, 24, 32):
            raise ValueError(f"Неверный размер ключа: {len(key)} байт (допустимо: 16, 24, 32)")

        self.key = key
        # Используем первые 16 байт для AES128
        aes_key = key[:16] if len(key) > 16 else key
        self.cipher = AES128(aes_key)

        self.nonce = nonce if nonce else generate_random_bytes(self.NONCE_SIZE)

        if len(self.nonce) != self.NONCE_SIZE:
            raise ValueError(f"Nonce должен быть {self.NONCE_SIZE} байт")

        zero_block = bytes(self.BLOCK_SIZE)
        self._H = self._bytes_to_int(
            self.cipher.encrypt_block(zero_block)
        )

    @staticmethod
    def _bytes_to_int(b: bytes) -> int:
        return int.from_bytes(b, 'big')

    @staticmethod
    def _int_to_bytes(n: int, length: int = 16) -> bytes:
        return n.to_bytes(length, 'big')

    def _gf_mult(self, x: int, y: int) -> int:
        z = 0
        v = y
        for i in range(127, -1, -1):
            if (x >> i) & 1:
                z ^= v
            if v & 1:
                v = (v >> 1) ^ self.GF_REDUCTION
            else:
                v >>= 1
        return z

    def _ghash(self, aad: bytes, ciphertext: bytes) -> bytes:
        aad_padded = aad + bytes((self.BLOCK_SIZE - len(aad) % self.BLOCK_SIZE) % self.BLOCK_SIZE)
        ct_padded = ciphertext + bytes((self.BLOCK_SIZE - len(ciphertext) % self.BLOCK_SIZE) % self.BLOCK_SIZE)
        len_block = (len(aad) * 8).to_bytes(8, 'big') + (len(ciphertext) * 8).to_bytes(8, 'big')

        data = aad_padded + ct_padded + len_block
        y = 0

        for i in range(0, len(data), self.BLOCK_SIZE):
            block = self._bytes_to_int(data[i:i + self.BLOCK_SIZE])
            y = self._gf_mult(y ^ block, self._H)

        return self._int_to_bytes(y)

    def _inc32(self, counter: bytes) -> bytes:
        nonce_part = counter[:12]
        counter_val = int.from_bytes(counter[12:], 'big')
        counter_val = (counter_val + 1) & 0xFFFFFFFF
        return nonce_part + counter_val.to_bytes(4, 'big')

    def _ctr_encrypt(self, data: bytes, initial_counter: bytes) -> bytes:
        result = bytearray()
        counter = initial_counter

        for i in range(0, len(data), self.BLOCK_SIZE):
            block = data[i:i + self.BLOCK_SIZE]
            # Используй encrypt_block для каждого счетчика
            keystream = self.cipher.encrypt_block(counter)  # encrypt_block

            for j, byte in enumerate(block):
                result.append(byte ^ keystream[j])

            counter = self._inc32(counter)

        return bytes(result)

    def encrypt(self, plaintext: bytes, aad: bytes = b"") -> bytes:
        j0 = self.nonce + b'\x00\x00\x00\x01'
        counter = self._inc32(j0)
        ciphertext = self._ctr_encrypt(plaintext, counter)

        ghash_result = self._ghash(aad, ciphertext)
        e_j0 = self.cipher.encrypt_block(j0)
        tag = bytes(a ^ b for a, b in zip(ghash_result, e_j0))

        return self.nonce + ciphertext + tag

    def decrypt(self, data: bytes, aad: bytes = b"", external_nonce: bytes = None) -> bytes:
        if external_nonce is not None:
            if len(external_nonce) != self.NONCE_SIZE:
                raise ValueError(f"Nonce должен быть {self.NONCE_SIZE} байт")
            nonce = external_nonce

            if len(data) < self.TAG_SIZE:
                raise ValueError(f"Данные слишком маленькие: {len(data)} байт")

            tag = data[-self.TAG_SIZE:]
            ciphertext = data[:-self.TAG_SIZE]
        else:
            min_size = self.NONCE_SIZE + self.TAG_SIZE
            if len(data) < min_size:
                raise ValueError(f"Данные слишком маленькие: {len(data)} байт")

            nonce = data[:self.NONCE_SIZE]
            tag = data[-self.TAG_SIZE:]
            ciphertext = data[self.NONCE_SIZE:-self.TAG_SIZE]

        self.nonce = nonce


        self.cipher = AES128(self.key)
        zero_block = bytes(self.BLOCK_SIZE)
        self._H = self._bytes_to_int(self.cipher.encrypt_block(zero_block))

        j0 = nonce + b'\x00\x00\x00\x01'
        ghash_result = self._ghash(aad, ciphertext)
        e_j0 = self.cipher.encrypt_block(j0)  # encrypt_block
        expected_tag = bytes(a ^ b for a, b in zip(ghash_result, e_j0))

        if not self._constant_time_compare(tag, expected_tag):
            raise AuthenticationError("Authentication failed: AAD mismatch or ciphertext tampered")

        counter = self._inc32(j0)
        plaintext = self._ctr_encrypt(ciphertext, counter)
        return plaintext

    @staticmethod
    def _constant_time_compare(a: bytes, b: bytes) -> bool:
        if len(a) != len(b):
            return False
        result = 0
        for x, y in zip(a, b):
            result |= x ^ y
        return result == 0

    def encrypt_file(self, input_path, output_path, aad: bytes = b""):
        try:
            with open(input_path, 'rb') as f:
                plaintext = f.read()

            result = self.encrypt(plaintext, aad)

            with open(output_path, 'wb') as f:
                f.write(result)

        except (IOError, OSError) as e:
            raise CryptoOperationError(f"File I/O error: {e}")

    def decrypt_file(self, input_path, output_path, aad: bytes = b"", nonce: bytes = None):
        try:
            with open(input_path, 'rb') as f:
                data = f.read()

            try:
                plaintext = self.decrypt(data, aad, external_nonce=nonce)
            except AuthenticationError:
                output_file = Path(output_path)
                if output_file.exists():
                    output_file.unlink()
                raise

            with open(output_path, 'wb') as f:
                f.write(plaintext)

        except (IOError, OSError) as e:
            raise CryptoOperationError(f"File I/O error: {e}")