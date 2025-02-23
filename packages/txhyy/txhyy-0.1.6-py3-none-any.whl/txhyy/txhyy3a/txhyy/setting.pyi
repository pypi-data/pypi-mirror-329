#Setting

import ctypes
import os
from typing import Optional
from cryptography.x509 import NameOID
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.x509 import CertificateBuilder, random_serial_number
from cryptography.x509.oid import NameOID
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from subprocess import Popen
from threading import Thread
from datetime import datetime, timedelta


user32: ctypes.WinDLL
shell32: ctypes.WinDLL
kernel32: ctypes.WinDLL
ole32: ctypes.WinDLL
ws2_32: ctypes.WinDLL
winmm: ctypes.WinDLL
gdi32: ctypes.WinDLL
advapi32: ctypes.WinDLL
odbc32: ctypes.WinDLL
msimg32: ctypes.WinDLL
_system32_path: str
_winspool_path: str
winspool: Optional[ctypes.WinDLL]
setupapi: ctypes.WinDLL
crypt32: ctypes.WinDLL
netapi32: ctypes.WinDLL


class HTTPServer:
    def __init__(self, port: int = 8000, directory: str = '.') -> None: ...
    def start(self) -> None: ...


class HTTPSServer:
    def __init__(self, port: int = 4433, directory: str = '.', certfile: str = 'cert.pem', keyfile: str = 'key.pem') -> None: ...
    def start(self) -> None: ...


class BackendPythonServer:
    def __init__(self, python_file_path: str, port: Optional[int] = None) -> None: ...
    def start(self) -> None: ...


class SelfSignedCertificateGenerator:
    def __init__(self, common_name: str, private_key_path: str = 'private_key.pem', certificate_path: str = 'certificate.pem',
                 key_size: int = 2048, validity_days: int = 365) -> None: ...
    def generate(self) -> None: ...