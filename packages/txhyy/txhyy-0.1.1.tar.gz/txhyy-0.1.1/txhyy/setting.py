import ctypes
import os

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

try:
    winspool = ctypes.windll.LoadLibrary(_winspool_path)
except Exception as e:
    print(f"Error loading winspool.drv: {e}")

setupapi = ctypes.windll.setupapi
crypt32 = ctypes.windll.crypt32
netapi32 = ctypes.windll.netapi32

"""HTTP server and HTTPS server"""
import http.server
import socketserver
import ssl
import subprocess
import threading

class HTTPServer:
    """创建HTTP服务器"""
    def __init__(self, port=8000, directory='.'):
        self.port = port
        self.directory = directory

    def start(self):
        os.chdir(self.directory)
        Handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", self.port), Handler) as httpd:
            print(f"HTTP server is listening on port {self.port}, serving directory {self.directory}")
            httpd.serve_forever()


class HTTPSServer:
    """创建HTTPS服务器,需要证书(测试情况下只用使用自签名证书就行了)"""
    def __init__(self, port=4433, directory='.', certfile='cert.pem', keyfile='key.pem'):
        self.port = port
        self.directory = directory
        self.certfile = certfile
        self.keyfile = keyfile

    def start(self):
        os.chdir(self.directory)
        Handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", self.port), Handler) as httpd:
            print(f"HTTPS server is listening on port {self.port}, serving directory {self.directory}")
            httpd.socket = ssl.wrap_socket(
                httpd.socket,
                keyfile=self.keyfile,
                certfile=self.certfile,
                server_side=True
            )
            httpd.serve_forever()


class BackendPythonServer:
    """停止Python服务器"""
    def __init__(self, python_file_path, port=None):
        self.python_file_path = python_file_path
        self.port = port

    def start(self):
        command = ['python', self.python_file_path]
        if self.port:
            command.extend(['--port', str(self.port)])
        try:
            process = subprocess.Popen(command)
            print(f"The backend Python server ({self.python_file_path}) has been started")
            # To avoid blocking the main thread, use a thread to wait for the process to end
            def monitor_process():
                process.wait()
                print(f"The backend Python server ({self.python_file_path}) has stopped")
            threading.Thread(target=monitor_process).start()
        except Exception as e:
            print(f"An error occurred while starting the backend Python server: {e}")


from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import datetime


class SelfSignedCertificateGenerator:
    """生成自签名证书"""
    def __init__(self, common_name, private_key_path='private_key.pem', certificate_path='certificate.pem',
                 key_size=2048, validity_days=365):
        """
        初始化生成器

        :param common_name: 证书的通用名称（CN），通常是域名或服务器名称
        :param private_key_path: 私钥文件的保存路径
        :param certificate_path: 证书文件的保存路径
        :param key_size: 私钥的位数，默认为 2048
        :param validity_days: 证书的有效期（天），默认为 365 天
        """
        self.common_name = common_name
        self.private_key_path = private_key_path
        self.certificate_path = certificate_path
        self.key_size = key_size
        self.validity_days = validity_days


    def generate(self):
        """
        生成自签名证书
        """
        # 生成私钥
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=self.key_size
        )

        # 保存私钥到文件
        with open(self.private_key_path, 'wb') as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))

        # 构建证书主题
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, self.common_name)
        ])

        # 生成证书
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            datetime.datetime.utcnow() + datetime.timedelta(days=self.validity_days)
        ).add_extension(
            x509.SubjectAlternativeName([x509.DNSName(self.common_name)]),
            critical=False,
        ).sign(private_key, hashes.SHA256())

        # 保存证书到文件
        with open(self.certificate_path, 'wb') as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))

        print(f"The self-signed certificate is generated, the private key is stored in {self.private_key_path}, and the certificate is stored in {self.certificate_path} .")
