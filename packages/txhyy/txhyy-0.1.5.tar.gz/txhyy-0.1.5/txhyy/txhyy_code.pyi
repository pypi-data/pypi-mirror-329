import os
import sys
from typing import Any, List


def getcwd() -> str:
    ...

def remove(path: str) -> None:
    ...

def removedir(path: str) -> None:
    ...

def cmd(command: str) -> int:
    ...

def psshell(command: str) -> None:
    ...

def chdir(path: str) -> None:
    ...

def mkdir(path: str) -> None:
    ...

def get_encoding(file_path: str) -> str:
    ...

def moencoding(input_file_path: str, output_file_path: str, new_encoding: str = 'utf-8') -> None:
    ...

def exists(path: str) -> bool:
    ...

def abspath(path: str) -> str:
    ...

def join(*paths: str) -> str:
    ...

def txprint(*objects: Any, sep: str = ' ', end: str = '\n', file = sys.stdout) -> None:
    ...

def cwdbytes() -> bytes:
    ...

def dirlist(path: str) -> List[str]:
    ...

def name(oldpath: str, newpath: str) -> None:
    ...

def file(path: str) -> None:
    ...

def idir(path: str) -> None:
    ...

READ = os.R_OK
WRITE = os.W_OK
RUN = os.X_OK

def pathq(filepath: str, r: int) -> bool:
    ...

def permissions(path: str, r: int) -> None:
    ...

import ctypes

class WinRightCilck:
    def auto_arrange(enable: bool) -> None:
        ...

    def grid(enable: bool) -> None:
        ...

    def icon(enable: bool) -> None:
        ...

    def desktop_icons(show: bool) -> None:
        ...

    def icon_size(size: int) -> None:
        ...

    def defaults() -> None:
        ...

    def sort_order(sort_type: int) -> None:
        ...


def _calculate_hash(data: bytes, algorithm: str) -> str:
    ...

def sha256(data: bytes) -> str:
    ...

def sha384(data: bytes) -> str:
    ...

def sha224(data: bytes) -> str:
    ...

def sha1(data: bytes) -> str:
    ...

def sha512(data: bytes) -> str:
    ...

def md5(data: bytes) -> str:
    ...

def blake2b(data: bytes) -> str:
    ...

def sha3_256(data: bytes) -> str:
    ...

def shake_128(data: bytes) -> str:
    ...

def shake_256(data: bytes) -> str:
    ...

def sha3_384(data: bytes) -> str:
    ...

def sha3_512(data: bytes) -> str:
    ...

def blake2s(data: bytes) -> str:
    ...

user32 = ctypes.windll.user32
shell32 = ctypes.windll.shell32
kernel32 = ctypes.windll.kernel32
ole32 = ctypes.windll.ole32
ws2_32 = ctypes.windll.ws2_32
winmm = ctypes.windll.winmm
gdi32 = ctypes.windll.gdi32
advapi32 = ctypes.windll.advapi32
odbc32 = ctypes.windll.odbc32
msimg32 = ctypes.windll.msimg32
_system32_path = os.path.join(os.environ['SystemRoot'], 'System32')
_winspool_path = os.path.join(_system32_path, 'winspool.drv')

winspool = ctypes.windll.LoadLibrary(_winspool_path)
setupapi = ctypes.windll.setupapi
crypt32 = ctypes.windll.crypt32
netapi32 = ctypes.windll.netapi32

import http.server
import socketserver
import ssl
import subprocess
import threading

class HTTPServer:
    def __init__(self, port: int = 8000, directory: str = '.') -> None:
        ...

    def start(self) -> None:
        ...


class HTTPSServer:
    def __init__(self, port: int = 4433, directory: str = '.', certfile: str = 'cert.pem', keyfile: str = 'key.pem') -> None:
        ...

    def start(self) -> None:
        ...


class BackendPythonServer:
    def __init__(self, python_file_path: str, port: int = None) -> None:
        ...

    def start(self) -> None:
        ...


from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import datetime

class SelfSignedCertificateGenerator:
    def __init__(self, common_name: str, private_key_path: str = 'private_key.pem', certificate_path: str = 'certificate.pem',
                 key_size: int = 2048, validity_days: int = 365) -> None:
        ...

    def generate(self) -> None:
        ...


import wmi
import ctypes
import winreg
import os, sys
import win32con
import win32gui
import win32api
import subprocess
import win32clipboard
from win32com.client import Dispatch

FILE_ATTRIBUTE_HIDDEN = 0x2
FILE_ATTRIBUTE_READONLY = 0x1
FILE_ATTRIBUTE_ARCHIVE = 0x20
FILE_ATTRIBUTE_SYSTEM = 0x4
FILE_ATTRIBUTE_COMPRESSED = 0x800

def exit(code: int) -> None:
    ...

def attributes(file_path: str, hidden: bool = False, readonly: bool = False, archive: bool = False, system: bool = False, compressed: bool = False) -> None:
    ...

installlist = ['https://pypi.tuna.tsinghua.edu.cn/simple - 清华',"https://mirrors.aliyun.com/pypi/simple/ - 阿里云","https://pypi.mirrors.ustc.edu.cn/simple/ - 中国科学技术大学","https://pypi.doubanio.com/simple/ - 豆瓣镜像"]

def install(modules: List[str], mirror_url: str = "https://pypi.tuna.tsinghua.edu.cn/simple") -> str:
    ...

def quit(code: int) -> None:
    ...

def ctrlc(text: str) -> None:
    ...

def curani(cursor_path: str) -> None:
    ...

def size() -> tuple:
    ...

def copy(source_file: str, destination_file: str, TrueorFalse: bool = False) -> None:
    ...

def system(none = None) -> str:
    ...

def shortcut(target_path: str, shortcut_path: str, run_as_admin: bool = False) -> None:
    ...

shell = Dispatch('WScript.Shell')

def brightness(brightness: int) -> None:
    ...

Error = Exception

def desktop() -> str:
    ...

def backend(file: str) -> None:
    ...

def getcwd() -> str:
    ...

def username() -> str:
    ...

def increase(file_extension: str = None, file_type: str = None, icon_path: str = None, associated_program: str = None) -> None:
    ...

def delete(file_extension: str, file_type: str) -> None:
    ...

def modify(old_file_extension: str = None, old_file_type: str = None, new_file_extension: str = None, new_file_type: str = None,
           new_icon_path: str = None, new_associated_program: str = None) -> None:
    ...

def activate_windows(product_key: str) -> None:
    ...

Roaming = os.getenv('APPDATA')

def home() -> str:
    ...

def pi(numbers: int) -> float:
    ...

def factorial(n: int) -> int:
    ...

def sin(x: float, num_terms: int = 10) -> float:
    ...

def cos(x: float, num_terms: int = 10) -> float:
    ...

def tan(x: float, num_terms: int = 10) -> float:
    ...

def cot(x: float, num_terms: int = 10) -> float:
    ...

class ComplexNumber:
    def __init__(self, real: float, imag: float) -> None:
        ...

    def __add__(self, other: 'ComplexNumber') -> 'ComplexNumber':
        ...

    def __sub__(self, other: 'ComplexNumber') -> 'ComplexNumber':
        ...

    def __mul__(self, other: 'ComplexNumber') -> 'ComplexNumber':
        ...

    def __truediv__(self, other: 'ComplexNumber') -> 'ComplexNumber':
        ...

    def __str__(self) -> str:
        ...

def sqrt(a: float, tolerance: float = 1e-6, max_iterations: int = 100) -> float:
    ...

def exp(x: float, num_terms: int = 10) -> float:
    ...

def ln(x: float, tolerance: float = 1e-6, max_iterations: int = 100) -> float:
    ...

def power(x: float, n: int) -> float:
    ...

def combination(n: int, k: int) -> int:
    ...