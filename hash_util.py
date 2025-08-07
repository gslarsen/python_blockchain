import json
import hashlib


def hash_string_sha256(string):
    """Hashes a string using SHA-256 and returns the hexadecimal digest.
    Args:
        string: The string to be hashed.
    Returns:
        The SHA-256 hash of the string in hexadecimal format."""
    return hashlib.sha256(string).hexdigest()


def hash_block(block):
    """Hashes a block and returns the hash value.
    Args:
        block: The block to be hashed.
    """
    return hash_string_sha256(json.dumps(block, sort_keys=True).encode())
