"""
Author: Huang Yiyi
=========================================================
Txhyy version: 0.0.8
Txhyy title: txhyy
"""

__version__ = "0.0.8"
name = "txhyy"
title = name

from . import reg, dialog, pyc
from . import Video, Image
from .setting import *
from ._txhyy import *
from . import zhushi
import ctypes

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


c = WMI
WindowsDLL = DllLoader()
Windll = DllLoader()

_txhyy.brightness(100)
pyc.pytopyc("Txhyy")

txhyycode = _txhyy