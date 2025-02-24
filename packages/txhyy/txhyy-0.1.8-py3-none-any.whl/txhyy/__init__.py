"""
Author: Huang Yiyi
=========================================================
Txhyy version: 0.1.8
Txhyy title: txhyy
"""

__version__ = "0.1.8"
name = "txhyy"
title = name

import subprocess
import os, ctypes,platform
from . import reg, dialog, pyc
from . import Video, Image
from .txhyy_code import *
from . import zhushi as zhushi
from typing import Callable as Callable


class _Setting:
    user32 = txhyy_code.user32
    shell32 = txhyy_code.shell32
    kernel32 = txhyy_code.kernel32
    ole32 = txhyy_code.ole32
    ws2_32 = txhyy_code.ws2_32
    winmm = txhyy_code.winmm
    gdi32 = txhyy_code.gdi32
    advapi32 = txhyy_code.advapi32
    odbc32 = txhyy_code.odbc32
    msimg32 = txhyy_code.msimg32
    winspool = txhyy_code.winspool
    setupapi = txhyy_code.setupapi
    crypt32 = txhyy_code.crypt32
    netapi32 = txhyy_code.netapi32


class Windowsdll:
    def __init__(self, dll_name):
        self._dll = ctypes.WinDLL(dll_name)

    def __getattr__(self, name):
        try:
            return getattr(self._dll, name)
        except AttributeError:
            raise AttributeError(f"Function {name} not found in {self._dll._name}")

class DllLoader:
    def __init__(self):
        self._loaded_dlls = {}

    def __getattr__(self, dll_name):
        if dll_name not in self._loaded_dlls:
            try:
                self._loaded_dlls[dll_name] = Windowsdll(dll_name)
            except OSError as e:
                print(f"ERROR: {dll_name} : {e}")
        return self._loaded_dlls.get(dll_name)


def print_class_tree(cls, level=0, is_last=False, prefix="", branch_extend=False):
    # 构建当前行的前缀
    if level > 0:
        if is_last:
            new_prefix = prefix + "    "
            line = prefix + "└── "
        else:
            new_prefix = prefix + "│   "
            line = prefix + "├── "
    else:
        new_prefix = ""
        line = ""
    # 打印当前类名
    print(line + cls.__name__)

    # 获取当前类的所有子类
    subclasses = cls.__subclasses__()
    num_subclasses = len(subclasses)

    for i, subclass in enumerate(subclasses):
        # 判断是否为最后一个子类
        is_last_subclass = (i == num_subclasses - 1)

        # 当根类有子类时打印分隔符 |
        if level == 0 and i == 0 and subclasses:
            print("|")

        # 如果当前分支需要加长，打印额外的分隔符
        if branch_extend:
            if level > 0:
                print(prefix.rstrip() + "│")

        next_branch_extend = branch_extend or cls.__name__ == "TestError"
        print_class_tree(subclass, level + 1, is_last_subclass, new_prefix, next_branch_extend)


def print_directory_tree(path, prefix='', is_root=True, is_last=True, output_file=None, error_list=None):
    if error_list is None:
        error_list = []

    if is_root:
        line = os.path.basename(path)
    else:
        marker = '└── ' if is_last else '├── '
        line = prefix + marker + os.path.basename(path)

    if output_file:
        output_file.write(line + '\n')
    else:
        print(line)

    if os.path.exists(path):
        if os.path.isdir(path):
            try:
                items = os.listdir(path)
                num_items = len(items)
                for index, item in enumerate(items):
                    item_path = os.path.join(path, item)
                    new_prefix = prefix + ('    ' if (is_last and not is_root) else '│   ')
                    is_last_item = (index == num_items - 1)
                    print_directory_tree(item_path, new_prefix, is_root=False, is_last=is_last_item, output_file=output_file, error_list=error_list)
            except PermissionError:
                error_msg = f"{prefix + ('    ' if (is_last and not is_root) else '│   ') + f'└── {os.path.basename(path)} (Permission denied)'}"
                error_list.append(error_msg)
            except FileNotFoundError:
                error_msg = f"{prefix + ('    ' if (is_last and not is_root) else '│   ') + f'└── {os.path.basename(path)} (Path not found)'}"
                error_list.append(error_msg)
    else:
        error_msg = f"{prefix + ('    ' if (is_root or is_last) else '│   ') + f'└── {os.path.basename(path)} (Path not found)'}"
        error_list.append(error_msg)

    return error_list


def set_ip_windows(ip_address, subnet_mask, gateway, dns_servers):
    try:
        # 设置 IP 地址和子网掩码
        ip_command = f'netsh interface ip set address name="以太网" static {ip_address} {subnet_mask} {gateway}'
        subprocess.run(ip_command, shell=True, check=True)

        # 设置 DNS 服务器
        dns_str = " ".join(dns_servers)
        dns_command = f'netsh interface ip set dns name="以太网" static {dns_str}'
        subprocess.run(dns_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"设置 IP 地址时出错（Windows）: {e}")

def set_ip_macos(ip_address, subnet_mask, gateway, dns_servers):
    try:
        # 设置 IP 地址、子网掩码和网关
        ip_command = f'sudo ifconfig en0 {ip_address} netmask {subnet_mask} {gateway}'
        subprocess.run(ip_command, shell=True, check=True)

        # 设置 DNS 服务器
        dns_str = " ".join(dns_servers)
        dns_command = f'sudo networksetup -setdnsservers Ethernet {dns_str}'
        subprocess.run(dns_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"设置 IP 地址时出错（macOS）: {e}")

def set_ip_linux(ip_address, subnet_mask, gateway, dns_servers):
    try:
        # 确定网卡名称，这里假设为 eth0，可根据实际情况修改
        interface = "eth0"
        # 生成 netplan 配置文件内容
        config = f"""network:
  version: 2
  renderer: networkd
  ethernets:
    {interface}:
      dhcp4: no
      addresses: [{ip_address}/{subnet_mask}]
      gateway4: {gateway}
      nameservers:
        addresses: {dns_servers}
"""
        # 写入配置文件
        with open("/etc/netplan/01-netcfg.yaml", "w") as f:
            f.write(config)

        # 应用配置
        subprocess.run("sudo netplan apply", shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"设置 IP 地址时出错（Linux）: {e}")
    except Exception as e:
        print(f"发生其他错误（Linux）: {e}")

def set_ip(ip_address, subnet_mask, gateway, dns_servers):
    system = platform.system()
    if system == "Windows":
        set_ip_windows(ip_address, subnet_mask, gateway, dns_servers)
    elif system == "Darwin":
        set_ip_macos(ip_address, subnet_mask, gateway, dns_servers)
    elif system == "Linux":
        set_ip_linux(ip_address, subnet_mask, gateway, dns_servers)
    else:
        print("不支持的操作系统")

Winloader = DllLoader()
Windll = DllLoader()

txhyy_code.brightness(100)

txhyycode = txhyy_code

#import math
#x = math.pi / 4
#txhyycode.sin(x)
#txhyycode._install_modules("modules: Any","mirror_url: str = 'https://pypi.tuna.tsinghua.edu.cn/simple'")