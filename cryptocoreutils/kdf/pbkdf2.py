"""
PBKDF2-HMAC-SHA256 implementation following RFC 2898.

Password-Based Key Derivation Function 2 (PBKDF2) is designed to derive
cryptographic keys from passwords. It applies a pseudorandom function
(HMAC-SHA256) to the password along with a salt value and repeats the
process many times to increase the computational cost of attacks.
"""

from ..mac.hmac import HMAC


def pbkdf2_hmac_sha256(password, salt, iterations, dklen):
    """
    PBKDF2-HMAC-SHA256 implementation following RFC 2898.

    Derives a cryptographic key from a password using HMAC-SHA256 as the
    pseudorandom function (PRF).

    Algorithm:
        DK = T1 || T2 || ... || Tdklen/hLen
        where Ti = F(Password, Salt, c, i)

        F(Password, Salt, c, i) = U1 ^ U2 ^ ... ^ Uc
        where:
            U1 = PRF(Password, Salt || INT_32_BE(i))
            Uj = PRF(Password, U_{j-1})

    Args:
        password: Password as bytes or string (will be UTF-8 encoded)
        salt: Salt as bytes or hex string
        iterations: Number of iterations (integer, must be >= 1)
        dklen: Desired key length in bytes

    Returns:
        Derived key as bytes of length dklen

    Raises:
        ValueError: If parameters are invalid
    """
    # Validate iterations
    if iterations < 1:
        raise ValueError("Iterations must be at least 1")

    if dklen < 1:
        raise ValueError("Derived key length must be at least 1")

    # Convert password to bytes if string
    if isinstance(password, str):
        password = password.encode('utf-8')

    # Ensure password is bytes
    if not isinstance(password, (bytes, bytearray)):
        raise TypeError("Password must be bytes or string")

    # Convert salt to bytes if string
    if isinstance(salt, str):
        # Try to detect if it's a hex string
        if (len(salt) > 0 and
            len(salt) % 2 == 0 and
            all(c in '0123456789abcdefABCDEF' for c in salt)):
            try:
                salt = bytes.fromhex(salt)
            except ValueError:
                salt = salt.encode('utf-8')
        else:
            salt = salt.encode('utf-8')

    # Ensure salt is bytes
    if not isinstance(salt, (bytes, bytearray)):
        salt = bytes(salt)

    # HMAC-SHA256 output length (32 bytes = 256 bits)
    hlen = 32

    # Calculate number of blocks needed
    # Each block produces hlen bytes, we need ceil(dklen / hlen) blocks
    blocks_needed = (dklen + hlen - 1) // hlen

    # RFC 2898: Check for maximum derived key length
    # dkLen <= (2^32 - 1) * hLen
    max_dklen = (2**32 - 1) * hlen
    if dklen > max_dklen:
        raise ValueError(f"Derived key too long (max: {max_dklen} bytes)")

    derived_key = b''

    for block_num in range(1, blocks_needed + 1):
        # F(Password, Salt, c, i) = U1 ^ U2 ^ ... ^ Uc

        # U1 = PRF(Password, Salt || INT_32_BE(i))
        # INT_32_BE(i) is i encoded as a 4-byte big-endian integer
        u_prev = _hmac_sha256(password, salt + block_num.to_bytes(4, 'big'))

        # Initialize block with U1
        block = bytearray(u_prev)

        # Compute U2 through Uc and XOR into block
        for _ in range(2, iterations + 1):
            # Uj = PRF(Password, U_{j-1})
            u_curr = _hmac_sha256(password, u_prev)

            # XOR u_curr into block
            for i in range(hlen):
                block[i] ^= u_curr[i]

            u_prev = u_curr

        derived_key += bytes(block)

    # Return exactly dklen bytes (truncate if we generated more)
    return derived_key[:dklen]


def _hmac_sha256(key: bytes, msg: bytes) -> bytes:
    """
    Compute HMAC-SHA256 using our implementation from Sprint 5.

    Args:
        key: HMAC key as bytes
        msg: Message to authenticate as bytes

    Returns:
        HMAC-SHA256 digest as bytes (32 bytes)
    """
    hmac = HMAC(key, 'sha256')
    hmac.update(msg)
    return hmac.digest()


def generate_salt(length: int = 16) -> bytes:
    """
    Generate a cryptographically secure random salt.

    A salt is a random value that is used along with the password to derive
    the key. It ensures that the same password will produce different keys
    when used with different salts.

    Args:
        length: Salt length in bytes (default: 16 bytes = 128 bits)

    Returns:
        Random salt as bytes

    Raises:
        ValueError: If length is less than 1
    """
    if length < 1:
        raise ValueError("Salt length must be at least 1")

    try:
        # Try to use our CSPRNG implementation from previous sprint
        from ..csprng import generate_random_bytes
        return generate_random_bytes(length)
    except ImportError:
        # Fallback to os.urandom if CSPRNG module not available
        import os
        return os.urandom(length)


def pbkdf2_verify(password, salt, iterations, dklen, expected_key):
    """
    Verify a password against a previously derived key.

    Uses constant-time comparison to prevent timing attacks.

    Args:
        password: Password to verify
        salt: Salt used during key derivation
        iterations: Number of iterations used
        dklen: Key length
        expected_key: The expected derived key to compare against

    Returns:
        True if password is correct, False otherwise
    """
    derived = pbkdf2_hmac_sha256(password, salt, iterations, dklen)

    if isinstance(expected_key, str):
        expected_key = bytes.fromhex(expected_key)

    # Constant-time comparison
    if len(derived) != len(expected_key):
        return False

    result = 0
    for a, b in zip(derived, expected_key):
        result |= a ^ b

    return result == 0