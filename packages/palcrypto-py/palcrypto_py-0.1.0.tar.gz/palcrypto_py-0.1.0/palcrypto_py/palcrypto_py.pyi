from typing import Optional


def generate_aes_key() -> bytes: ...

def aes_encrypt(pal_aes_key_bytes: bytes, plain_bytes: bytes) -> bytes: ...

def aes_decrypt(
        pal_aes_key_bytes: bytes,
        encrypted_bytes: bytes,
        nonce_len: Optional[int]) -> bytes: ...


class CbKeyPair:
    public_key_bytes: bytes
    private_key_bytes: bytes

    def __str__(self) -> str: ...

def generate_cb_key_pair() -> CbKeyPair: ...


def cb_encrypt(
    peer_pal_crypto_public_key_bytes: bytes,
    my_pal_crypto_secret_key_bytes: bytes,
    plain_bytes: bytes
) -> bytes: ...

def cb_decrypt(
        peer_pal_crypto_public_key_bytes: bytes,
        my_pal_crypto_secret_key_bytes: bytes,
        encrypted_bytes: bytes,
        nonce_len: Optional[int]) -> bytes: ...