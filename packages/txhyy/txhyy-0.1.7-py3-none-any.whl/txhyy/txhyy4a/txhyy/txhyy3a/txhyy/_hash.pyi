#Txhyy - hash.pyi

import winreg
import ctypes

class WinRightCilck:
    @staticmethod
    def auto_arrange(enable: bool) -> None: ...

    @staticmethod
    def grid(enable: bool) -> None: ...

    @staticmethod
    def icon(enable: bool) -> None: ...

    @staticmethod
    def desktop_icons(show: bool) -> None: ...

    @staticmethod
    def icon_size(size: int) -> None: ...

    @staticmethod
    def defaults() -> None: ...

    @staticmethod
    def sort_order(sort_type: str) -> None: ...


def _calculate_hash(data: str | bytes, algorithm) -> str: ...

def sha256(data: str | bytes) -> str:
    """
    计算输入数据的 SHA-256 哈希值。

    参数:
    data (str | bytes): 要进行哈希计算的数据，可以是字符串或字节类型。
        若为字符串，内部会先将其编码为 UTF-8 字节类型。

    返回:
    str: 输入数据的 SHA-256 哈希值的十六进制字符串表示。
    """
    ...

def sha384(data: str | bytes) -> str:
    """
    计算输入数据的 SHA-384 哈希值。

    参数:
    data (str | bytes): 要进行哈希计算的数据，可以是字符串或字节类型。
        若为字符串，内部会先将其编码为 UTF-8 字节类型。

    返回:
    str: 输入数据的 SHA-384 哈希值的十六进制字符串表示。
    """
    ...

def sha224(data: str | bytes) -> str:
    """
    计算输入数据的 SHA-224 哈希值。

    参数:
    data (str | bytes): 要进行哈希计算的数据，可以是字符串或字节类型。
        若为字符串，内部会先将其编码为 UTF-8 字节类型。

    返回:
    str: 输入数据的 SHA-224 哈希值的十六进制字符串表示。
    """
    ...

def sha1(data: str | bytes) -> str:
    """
    计算输入数据的 SHA-1 哈希值。

    参数:
    data (str | bytes): 要进行哈希计算的数据，可以是字符串或字节类型。
        若为字符串，内部会先将其编码为 UTF-8 字节类型。

    返回:
    str: 输入数据的 SHA-1 哈希值的十六进制字符串表示。
    """
    ...

def sha512(data: str | bytes) -> str:
    """
    计算输入数据的 SHA-512 哈希值。

    参数:
    data (str | bytes): 要进行哈希计算的数据，可以是字符串或字节类型。
        若为字符串，内部会先将其编码为 UTF-8 字节类型。

    返回:
    str: 输入数据的 SHA-512 哈希值的十六进制字符串表示。
    """
    ...

def md5(data: str | bytes) -> str:
    """
    计算输入数据的 MD5 哈希值。

    参数:
    data (str | bytes): 要进行哈希计算的数据，可以是字符串或字节类型。
        若为字符串，内部会先将其编码为 UTF-8 字节类型。

    返回:
    str: 输入数据的 MD5 哈希值的十六进制字符串表示。
    """
    ...

def blake2b(data: str | bytes) -> str:
    """
    计算输入数据的 BLAKE2b 哈希值。

    参数:
    data (str | bytes): 要进行哈希计算的数据，可以是字符串或字节类型。
        若为字符串，内部会先将其编码为 UTF-8 字节类型。

    返回:
    str: 输入数据的 BLAKE2b 哈希值的十六进制字符串表示。
    """
    ...

def sha3_256(data: str | bytes) -> str:
    """
    计算输入数据的 SHA3-256 哈希值。

    参数:
    data (str | bytes): 要进行哈希计算的数据，可以是字符串或字节类型。
        若为字符串，内部会先将其编码为 UTF-8 字节类型。

    返回:
    str: 输入数据的 SHA3-256 哈希值的十六进制字符串表示。
    """
    ...

def shake_128(data: str | bytes) -> str:
    """
    计算输入数据的 SHAKE-128 哈希值。

    参数:
    data (str | bytes): 要进行哈希计算的数据，可以是字符串或字节类型。
        若为字符串，内部会先将其编码为 UTF-8 字节类型。

    返回:
    str: 输入数据的 SHAKE-128 哈希值的十六进制字符串表示。
    """
    ...

def shake_256(data: str | bytes) -> str:
    """
    计算输入数据的 SHAKE-256 哈希值。

    参数:
    data (str | bytes): 要进行哈希计算的数据，可以是字符串或字节类型。
        若为字符串，内部会先将其编码为 UTF-8 字节类型。

    返回:
    str: 输入数据的 SHAKE-256 哈希值的十六进制字符串表示。
    """
    ...

def sha3_384(data: str | bytes) -> str:
    """
    计算输入数据的 SHA3-384 哈希值。

    参数:
    data (str | bytes): 要进行哈希计算的数据，可以是字符串或字节类型。
        若为字符串，内部会先将其编码为 UTF-8 字节类型。

    返回:
    str: 输入数据的 SHA3-384 哈希值的十六进制字符串表示。
    """
    ...

def sha3_512(data: str | bytes) -> str:
    """
    计算输入数据的 SHA3-512 哈希值。

    参数:
    data (str | bytes): 要进行哈希计算的数据，可以是字符串或字节类型。
        若为字符串，内部会先将其编码为 UTF-8 字节类型。

    返回:
    str: 输入数据的 SHA3-512 哈希值的十六进制字符串表示。
    """
    ...

def blake2s(data: str | bytes) -> str:
    """
    计算输入数据的 BLAKE2s 哈希值。

    参数:
    data (str | bytes): 要进行哈希计算的数据，可以是字符串或字节类型。
        若为字符串，内部会先将其编码为 UTF-8 字节类型。

    返回:
    str: 输入数据的 BLAKE2s 哈希值的十六进制字符串表示。
    """
    ...