"""
Author: Huang Yiyi
=========================================================
Txhyy version: 0.1.3
Txhyy title: txhyy
"""

__version__ = "0.1.3"
name = "txhyy"
title = name

import os, ctypes
from . import reg, dialog, pyc
from . import Video, Image
from .setting import *
from ._txhyy import *
from . import zhushi
from .file import *
from ._hash import *
from .count import *
from typing import Callable


class _Setting:
    user32 = setting.user32
    shell32 = setting.shell32
    kernel32 = setting.kernel32
    ole32 = setting.ole32
    ws2_32 = setting.ws2_32
    winmm = setting.winmm
    gdi32 = setting.gdi32
    advapi32 = setting.advapi32
    odbc32 = setting.odbc32
    msimg32 = setting.msimg32
    winspool = setting.winspool
    setupapi = setting.setupapi
    crypt32 = setting.crypt32
    netapi32 = setting.netapi32


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


Winloader = DllLoader()
Windll = DllLoader()

_txhyy.brightness(100)

txhyycode = _txhyy
#txhyycode._install_modules("modules: Any","mirror_url: str = 'https://pypi.tuna.tsinghua.edu.cn/simple'")