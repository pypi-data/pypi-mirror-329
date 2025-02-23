# _txhyy

import wmi
import ctypes
import winreg
import hashlib
import os
import sys
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

def exit(code: int) -> None: ...

def attributes(file_path: str, hidden: bool = False, readonly: bool = False, archive: bool = False,
               system: bool = False, compressed: bool = False) -> None: ...

installlist: list[str]

def _install_modules(modules: list[str], mirror_url: str = "https://pypi.tuna.tsinghua.edu.cn/simple") -> str: ...

def quit(code: int) -> None: ...

def ctrlc(text: str) -> None: ...

def curani(cursor_path: str) -> None: ...

def size() -> None: ...

def copy(source_file: str, destination_file: str, TrueorFalse: bool = False) -> None: ...

def system(none = None) -> None: ...

def shortcut(target_path: str, shortcut_path: str, run_as_admin: bool = False) -> None: ...

shell: Dispatch

def brightness(brightness: int) -> None: ...

Error: Exception

def desktop() -> None: ...

def backend(file: str) -> None: ...

def getcwd() -> None: ...

def username() -> None: ...

def increase(file_extension: str = None, file_type: str = None, icon_path: str = None,
             associated_program: str = None) -> None: ...

def delete(file_extension: str, file_type: str) -> None: ...

def modify(old_file_extension: str = None, old_file_type: str = None, new_file_extension: str = None,
           new_file_type: str = None, new_icon_path: str = None, new_associated_program: str = None) -> None: ...

def activate_windows(product_key: str) -> None: ...

Roaming: str

def home() -> str: ...

def _TEST() -> None: ...

install: callable
attr: callable