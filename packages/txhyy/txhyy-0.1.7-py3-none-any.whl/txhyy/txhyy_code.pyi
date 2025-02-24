# Txhyy Code .pyi

import os
import sys
import ctypes
from win32com.client import Dispatch
from decimal import Decimal


def getcwd() -> str:
    """获取当前工作目录"""


def remove(path: str) -> None:
    """删除指定路径的文件"""


def removedir(path: str) -> None:
    """删除指定路径的目录（函数体省略）"""


def cmd(command: str) -> int:
    """执行系统命令，返回命令执行的返回值"""


def powershell(command: str) -> None:
    """执行 PowerShell 命令（函数体省略）"""


def chdir(path: str) -> None:
    """改变当前工作目录"""


def mkdir(path: str) -> None:
    """创建指定路径的目录"""


def get_encoding(file_path: str) -> str:
    """获取文件的编码（函数体省略）"""


def moencoding(input_file_path: str, output_file_path: str, new_encoding: str = 'utf-8') -> None:
    """修改文件编码（函数体省略）"""


def exists(path: str) -> bool:
    """检查指定路径是否存在（函数体省略）"""


def abspath(path: str) -> str:
    """获取指定路径的绝对路径（函数体省略）"""


def join(*paths: str) -> str:
    """连接多个路径（函数体省略）"""


def txprint(*objects, sep: str = ' ', end: str = '\n', file = sys.stdout) -> None:
    """类似 print 功能的函数"""


def cwdbytes() -> bytes:
    """获取当前工作目录的字节表示（函数体省略）"""


def dirlist(path: str) -> list[str]:
    """获取指定路径下的文件和目录列表"""


def name(oldpath: str, newpath: str) -> None:
    """重命名文件或目录（函数体省略）"""


def file(path: str) -> None:
    """处理文件相关操作（函数体省略）"""


def idir(path: str) -> None:
    """处理目录相关操作（函数体省略）"""


READ = os.R_OK
WRITE = os.W_OK
RUN = os.X_OK


def pathq(filepath: str, r: int) -> bool:
    """检查文件是否具有指定权限"""


def permissions(path: str, r: int) -> None:
    """设置文件权限（函数体省略）"""


class WinRightCilck:
    @staticmethod
    def auto_arrange(enable: bool) -> None:
        """自动排列桌面图标（函数体省略）"""

    @staticmethod
    def grid(enable: bool) -> None:
        """设置桌面网格显示（函数体省略）"""

    @staticmethod
    def icon(enable: bool) -> None:
        """设置桌面图标显示（函数体省略）"""

    @staticmethod
    def desktop_icons(show: bool) -> None:
        """显示或隐藏桌面图标（函数体省略）"""

    @staticmethod
    def icon_size(size: int) -> None:
        """设置桌面图标大小（函数体省略）"""

    @staticmethod
    def defaults() -> None:
        """恢复桌面默认设置（函数体省略）"""

    @staticmethod
    def sort_order(sort_type: int) -> None:
        """设置桌面图标排序方式（函数体省略）"""


def _calculate_hash(data: bytes, algorithm: str) -> str:
    """计算数据的哈希值（函数体省略）"""


def sha256(data: bytes) -> str:
    """计算数据的 SHA-256 哈希值（函数体省略）"""


def sha384(data: bytes) -> str:
    """计算数据的 SHA-384 哈希值（函数体省略）"""


def sha224(data: bytes) -> str:
    """计算数据的 SHA-224 哈希值（函数体省略）"""


def sha1(data: bytes) -> str:
    """计算数据的 SHA-1 哈希值（函数体省略）"""


def sha512(data: bytes) -> str:
    """计算数据的 SHA-512 哈希值（函数体省略）"""


def md5(data: bytes) -> str:
    """计算数据的 MD5 哈希值（函数体省略）"""


def blake2b(data: bytes) -> str:
    """计算数据的 Blake2b 哈希值（函数体省略）"""


def sha3_256(data: bytes) -> str:
    """计算数据的 SHA3-256 哈希值（函数体省略）"""


def shake_128(data: bytes) -> str:
    """计算数据的 SHAKE-128 哈希值（函数体省略）"""


def shake_256(data: bytes) -> str:
    """计算数据的 SHAKE-256 哈希值（函数体省略）"""


def sha3_384(data: bytes) -> str:
    """计算数据的 SHA3-384 哈希值（函数体省略）"""


def sha3_512(data: bytes) -> str:
    """计算数据的 SHA3-512 哈希值（函数体省略）"""


def blake2s(data: bytes) -> str:
    """计算数据的 Blake2s 哈希值（函数体省略）"""


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


class HTTPServer:
    """创建 HTTP 服务器"""
    def __init__(self, port: int = 8000, directory: str = '.') -> None:
        """初始化 HTTP 服务器"""

    def start(self) -> None:
        """启动 HTTP 服务器（函数体省略）"""


class HTTPSServer:
    """创建 HTTPS 服务器,需要证书(测试情况下只用使用自签名证书就行了)"""
    def __init__(self, port: int = 4433, directory: str = '.', certfile: str = 'cert.pem', keyfile: str = 'key.pem') -> None:
        """初始化 HTTPS 服务器"""

    def start(self) -> None:
        """启动 HTTPS 服务器（函数体省略）"""


class BackendPythonServer:
    """停止 Python 服务器"""
    def __init__(self, python_file_path: str, port: int | None = None) -> None:
        """初始化后端 Python 服务器"""

    def start(self) -> None:
        """启动后端 Python 服务器（函数体省略）"""


class SelfSignedCertificateGenerator:
    """生成自签名证书"""
    def __init__(self, common_name: str, private_key_path: str = 'private_key.pem', certificate_path: str = 'certificate.pem',
                 key_size: int = 2048, validity_days: int = 365) -> None:
        """初始化生成器"""

    def generate(self) -> None:
        """生成自签名证书（函数体省略）"""


FILE_ATTRIBUTE_HIDDEN = 0x2
FILE_ATTRIBUTE_READONLY = 0x1
FILE_ATTRIBUTE_ARCHIVE = 0x20
FILE_ATTRIBUTE_SYSTEM = 0x4
FILE_ATTRIBUTE_COMPRESSED = 0x800


def exit(code: int) -> None:
    """退出程序"""


def attributes(file_path: str, hidden: bool = False, readonly: bool = False, archive: bool = False, system: bool = False, compressed: bool = False) -> None:
    """设置指定文件的属性为隐藏、只读、存档、系统或压缩"""


installlist: list[str] = [
    "https://pypi.tuna.tsinghua.edu.cn/simple - 清华",
    "https://mirrors.aliyun.com/pypi/simple/ - 阿里云",
    "https://pypi.mirrors.ustc.edu.cn/simple/ - 中国科学技术大学",
    "https://pypi.doubanio.com/simple/ - 豆瓣镜像"
]


def install(modules: list[str], mirror_url: str = "https://pypi.tuna.tsinghua.edu.cn/simple") -> str:
    """依次安装指定的多个模块，可以指定镜像源，并返回安装输出"""


def quit(code: int) -> None:
    """退出程序"""


def ctrlc(text: str) -> None:
    """复制指定的内容"""


def curani(cursor_path: str) -> None:
    """设置鼠标指针(.cur,.ani)"""


def size() -> tuple[int, int]:
    """获取屏幕分辨率"""


def copy(source_file: str, destination_file: str, TrueorFalse: bool = False) -> None:
    """复制文件,且不用管理员权限(如果文件是管理员权限或更高权限复制需要管理员权限)"""


def system(none = None) -> str:
    """通过调用系统命令识别操作系统"""


def shortcut(target_path: str, shortcut_path: str, run_as_admin: bool = False) -> None:
    """创建指定文件的快捷方式"""


shell = Dispatch('WScript.Shell')


def brightness(brightness: int) -> None:
    """设置笔记本屏幕亮度"""


Error = Exception


def desktop() -> str:
    """获取桌面位置(Desktop)"""


def backend(file: str) -> None:
    """将指定的文件在后台运行"""


def username() -> str:
    """获取用户名"""


def increase(file_extension: str | None = None, file_type: str | None = None, icon_path: str | None = None, associated_program: str | None = None) -> None:
    """自定义文件后缀名、文件类型、图标和关联程序"""


def delete(file_extension: str, file_type: str) -> None:
    """删除文件扩展名关联的函数"""


def modify(old_file_extension: str | None = None, old_file_type: str | None = None, new_file_extension: str | None = None, new_file_type: str | None = None,
           new_icon_path: str | None = None, new_associated_program: str | None = None) -> None:
    """修改文件后缀名的关联"""


def activate_windows(product_key: str) -> None:
    """激活 Windows 系统"""


Roaming: str = os.getenv('APPDATA')


def home() -> str:
    """获取用户文件夹路径"""


def pi(numbers: int) -> Decimal:
    """计算指定精度的圆周率（函数体省略）"""


def factorial(n: int) -> int:
    """计算阶乘"""


def sin(x: float, num_terms: int = 10) -> float:
    """使用泰勒级数展开计算正弦函数"""


def cos(x: float, num_terms: int = 10) -> float:
    """使用泰勒级数展开计算余弦函数"""


def tan(x: float, num_terms: int = 10) -> float:
    """计算正切函数"""


def cot(x: float, num_terms: int = 10) -> float:
    """计算余切函数"""


class ComplexNumber:
    def __init__(self, real: float, imag: float) -> None:
        """初始化复数（函数体省略）"""

    def __add__(self, other: 'ComplexNumber') -> 'ComplexNumber':
        """复数加法（函数体省略）"""

    def __sub__(self, other: 'ComplexNumber') -> 'ComplexNumber':
        """复数减法（函数体省略）"""

    def __mul__(self, other: 'ComplexNumber') -> 'ComplexNumber':
        """复数乘法（函数体省略）"""

    def __truediv__(self, other: 'ComplexNumber') -> 'ComplexNumber':
        """复数除法（函数体省略）"""

    def __str__(self) -> str:
        """返回复数的字符串表示（函数体省略）"""


def sqrt(a: float, tolerance: float = 1e-6, max_iterations: int = 100) -> float:
    """计算平方根（函数体省略）"""


def exp(x: float, num_terms: int = 10) -> float:
    """计算指数函数（函数体省略）"""


def ln(x: float, tolerance: float = 1e-6, max_iterations: int = 100) -> float:
    """计算自然对数（函数体省略）"""


def power(x: float, n: int) -> float:
    """计算幂次方（函数体省略）"""


def combination(n: int, k: int) -> int:
    """计算组合数（函数体省略）"""

import os
import ssl
import wmi

def getcwdb() -> bytes:
    """获取当前工作目录的字节表示"""

def sslver() -> str:
    """获取当前 SSL 上下文使用的协议名称"""

def is_module_installed(module_name: str) -> bool:
    """
    检查指定模块是否已安装
    :param module_name: 要检查的模块名称
    :return: 如果模块已安装返回 True，否则返回 False
    """

def notify(title: str | None, message: str | None, app_name: str | None = None, timeout: int = 5, icon: str | None = None) -> None:
    """发送通知"""

class CPUInfo:
    def __init__(self) -> None:
        """初始化 CPU 信息类"""

    def get_physical_core_count(self) -> int:
        """获取物理核心数"""

    def get_logical_core_count(self) -> int:
        """获取逻辑核心数"""

    def get_cpu_percent(self, interval: int = 1) -> float:
        """获取 CPU 使用率"""

class MemoryInfo:
    def __init__(self) -> None:
        """初始化内存信息类"""

    def get_total_memory(self) -> float:
        """获取总内存（GB）"""

    def get_used_memory(self) -> float:
        """获取已使用内存（GB）"""

    def get_memory_percent(self) -> float:
        """获取内存使用率"""

class DiskInfo:
    def __init__(self, path: str = '/') -> None:
        """初始化磁盘信息类"""

    def get_total_disk_space(self) -> float:
        """获取总磁盘空间（GB）"""

    def get_used_disk_space(self) -> float:
        """获取已使用磁盘空间（GB）"""

    def get_disk_percent(self) -> float:
        """获取磁盘使用率"""

class GPUInfo:
    def __init__(self) -> None:
        """初始化 GPU 信息类"""

    def get_gpu_names(self) -> list[str]:
        """获取显卡名称列表"""

    def get_nvidia_gpu_memory_info(self) -> list[dict[str, float]]:
        """获取 NVIDIA GPU 显存信息列表"""

    def __del__(self) -> None:
        """销毁 GPU 信息类实例"""

class MotherboardInfo:
    def __init__(self) -> None:
        """初始化主板信息类"""

    def get_motherboard_manufacturer(self) -> str | None:
        """获取主板制造商信息"""

    def get_motherboard_product(self) -> str | None:
        """获取主板产品型号信息"""

    def get_motherboard_serial_number(self) -> str | None:
        """获取主板序列号信息"""

class NetworkAdapterInfo:
    def __init__(self) -> None:
        """初始化网络适配器信息类"""

    def get_network_adapter_names(self) -> list[str]:
        """获取网卡名称列表"""

    def get_network_adapter_mac_addresses(self) -> list[str] | dict[str, str]:
        """获取网卡 MAC 地址列表或字典"""

class ScreenInfo:
    def __init__(self) -> None:
        """初始化屏幕信息类"""

    def get_screen_count(self) -> int:
        """获取屏幕数量"""

    def get_screen_resolutions(self) -> list[tuple[int, int]]:
        """获取屏幕分辨率列表"""

class HardwareInfo:
    def __init__(self) -> None:
        """初始化硬件信息类"""

    def get_sound_card_info(self) -> list[dict[str, str]]:
        """获取声卡信息列表"""

    def get_camera_info(self) -> list[int] | list[str]:
        """获取摄像头信息列表"""

class System:
    def __init__(self) -> None:
        """初始化系统信息类"""

    def get_os_info(self) -> dict[str, str]:
        """获取操作系统信息"""

    def get_cpu_info(self) -> dict[str, int | float]:
        """获取 CPU 信息"""

    def get_memory_info(self) -> dict[str, float]:
        """获取内存信息"""

    def get_disk_info(self, path: str = '/') -> dict[str, float]:
        """获取磁盘信息"""

    def get_network_info(self) -> dict[str, list[dict[str, dict[str, str]]] | int]:
        """获取网络信息"""

    def get_motherboard_info(self) -> dict[str, str]:
        """获取主板信息"""

    def get_gpu_info(self) -> dict[str, list[str]]:
        """获取显卡信息"""

demoy1 = ... #演示获取系统信息的代码

def demoy() -> None:
    """演示获取系统信息"""

class SystemInfo:
    def __init__(self) -> None:
        """初始化详细系统信息类"""

    def get_detailed_system_name(self) -> str | None:
        """获取详细系统名称"""

    def __str__(self) -> str:
        """返回详细系统名称字符串表示"""