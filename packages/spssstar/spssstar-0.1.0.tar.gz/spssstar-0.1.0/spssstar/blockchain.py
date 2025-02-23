import hashlib


def generate_blockchain_hash(data: str) -> str:
    """
    Generate a blockchain hash for the given data.
    :param data: Input data to hash.
    :return: Blockchain hash as a string.
    """
    return hashlib.sha256(data.encode()).hexdigest()