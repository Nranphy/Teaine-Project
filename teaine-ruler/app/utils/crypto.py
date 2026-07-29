import base64
import hashlib

from cryptography.fernet import Fernet, InvalidToken


def _build_fernet(salt: str) -> Fernet:
    """
    根据配置盐生成 Fernet 对称加密器。

    :param salt: KMS 加密盐。
    :return: Fernet 对称加密器。
    :raises ValueError: 当加密盐为空时抛出。
    """

    if not salt.strip():
        raise ValueError('kms salt must not be blank')
    digest = hashlib.sha256(salt.encode('utf-8')).digest()
    key = base64.urlsafe_b64encode(digest)
    return Fernet(key)


def encrypt_text(value: str, salt: str) -> str:
    """
    加密文本并返回可存储的 ASCII 密文。

    :param value: 明文文本。
    :param salt: KMS 加密盐。
    :return: Fernet 密文。
    """

    return _build_fernet(salt).encrypt(value.encode('utf-8')).decode('ascii')


def decrypt_text(value: str, salt: str) -> str:
    """
    解密数据库中的密文文本。

    :param value: Fernet 密文。
    :param salt: KMS 加密盐。
    :return: 明文文本。
    :raises ValueError: 当密文无法通过当前盐解密时抛出。
    """

    try:
        return _build_fernet(salt).decrypt(value.encode('ascii')).decode('utf-8')
    except InvalidToken as exc:
        raise ValueError('failed to decrypt KMS value') from exc


__all__ = ['decrypt_text', 'encrypt_text']
