"""Authentication utilities for Great Clips API."""

import hashlib
import hmac
import base64
from typing import Optional

from .config import get_config


def _hmac_sha256(key: bytes, message: bytes) -> bytes:
    """Calculate HMAC-SHA256 hash."""
    return hmac.new(key, message, hashlib.sha256).digest()


def _parse_secret_key_csv(csv: str) -> bytes:
    """
    Parse CSV string into bytes with Uint8Array semantics.

    JS used: new Uint8Array(secret.split(',').map(parseInt))
    Negative ints wrap into 0..255 in Uint8Array, so mask with 0xFF.
    """
    return bytes((int(tok.strip(), 10) & 0xFF) for tok in csv.split(","))


def _encrypt_with_xo(array_xor_with_h: bytes, encrypt_seven_c: str) -> bytes:
    """
    XOR encryption with HMAC-SHA256.

    JS: bitwiseXorMap = s(TextEncoder().encode(encryptSevenC), "")
        _xorResult = arrayXorWithH[i] ^ bitwiseXorMap[i] for i in 0..31
    Where s(key, msg) = HMAC-SHA256(key, msg)
    """
    text_bytes = encrypt_seven_c.encode("utf-8")
    bitwise_xor_map = _hmac_sha256(text_bytes, b"")  # 32 bytes
    # XOR first 32 bytes (arrayLength = 32 in JS)
    return bytes(a ^ b for a, b in zip(array_xor_with_h[:32], bitwise_xor_map[:32]))


def get_encrypted_token(payload: str, config: Optional['Config'] = None) -> str:
    """
    Generate authentication token for stylewaretouch.net API.

    This function reproduces the JavaScript token generation logic from Great Clips'
    embedded authentication. It uses HMAC-SHA256 with a secret key and encryption key
    loaded from configuration.

    Args:
        payload: The timestamp + JSON payload as a string
        config: Optional Config instance. If None, loads from environment.

    Returns:
        Base64url-encoded HMAC-SHA256 token

    Raises:
        ValueError: If configuration is missing required values
    """
    if config is None:
        config = get_config()

    # Validate configuration
    if not config.secret_key_csv:
        raise ValueError("SECRET_KEY_CSV is required in configuration")
    if not config.encryption_key:
        raise ValueError("ENCRYPTION_KEY is required in configuration")

    # Parse the CSV into bytes with Uint8Array semantics
    key_bucket = _parse_secret_key_csv(config.secret_key_csv)  # 32 bytes

    # JS: generateHash = await encryptWithXO(keyBucket, encryptionKey)
    generate_hash = _encrypt_with_xo(key_bucket, config.encryption_key)  # 32 bytes

    # JS: s(generateHash, keyString)  => HMAC-SHA256(key=generate_hash, msg=keyString)
    final_digest = _hmac_sha256(generate_hash, payload.encode("utf-8"))

    # JS hexToBase64(...) then replace +/ with -_ (i.e., base64url) and KEEP padding
    return base64.urlsafe_b64encode(final_digest).decode("utf-8")
