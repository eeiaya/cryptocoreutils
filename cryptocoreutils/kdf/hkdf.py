

from ..mac.hmac import HMAC


def derive_key(master_key, context, length=32):

    if length < 1:
        raise ValueError("Key length must be at least 1")

    # Convert context to bytes if string
    if isinstance(context, str):
        context = context.encode('utf-8')

    # Ensure context is bytes
    if not isinstance(context, (bytes, bytearray)):
        raise TypeError("Context must be bytes or string")

    # Convert master_key to bytes if string
    if isinstance(master_key, str):
        # Try to detect if it's a hex string
        if (len(master_key) > 0 and
            len(master_key) % 2 == 0 and
            all(c in '0123456789abcdefABCDEF' for c in master_key)):
            try:
                master_key = bytes.fromhex(master_key)
            except ValueError:
                master_key = master_key.encode('utf-8')
        else:
            master_key = master_key.encode('utf-8')

    # Ensure master_key is bytes
    if not isinstance(master_key, (bytes, bytearray)):
        raise TypeError("Master key must be bytes or string")

    # HMAC-SHA256 produces 32-byte blocks
    hlen = 32

    # Maximum derivable length
    max_length = 255 * hlen  # As per HKDF specification
    if length > max_length:
        raise ValueError(f"Requested length too large (max: {max_length} bytes)")

    derived = b''
    counter = 1

    while len(derived) < length:
        # T_i = HMAC(master_key, context || counter)
        # Counter is encoded as a 4-byte big-endian integer
        block = _hmac_sha256(master_key, context + counter.to_bytes(4, 'big'))
        derived += block
        counter += 1

    # Truncate to exact requested length
    return derived[:length]


def derive_key_with_info(master_key, salt, info, length=32):
    """
    Extended key derivation with salt and info parameters.

    This is a more complete implementation similar to HKDF (RFC 5869).

    Args:
        master_key: Input keying material (IKM)
        salt: Optional salt value (a non-secret random value)
        info: Optional context and application specific information
        length: Length of output keying material in bytes

    Returns:
        Derived key as bytes
    """
    # HKDF-Extract: PRK = HMAC(salt, IKM)
    if salt is None:
        salt = b'\x00' * 32  # Default salt of HashLen zeros

    if isinstance(salt, str):
        salt = salt.encode('utf-8')

    if isinstance(master_key, str):
        if all(c in '0123456789abcdefABCDEF' for c in master_key) and len(master_key) % 2 == 0:
            master_key = bytes.fromhex(master_key)
        else:
            master_key = master_key.encode('utf-8')

    prk = _hmac_sha256(salt, master_key)

    # HKDF-Expand
    return derive_key(prk, info, length)


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


def derive_key_hierarchy(master_key, *contexts, length=32):

    return {ctx: derive_key(master_key, ctx, length) for ctx in contexts}