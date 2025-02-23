"""
Author: Huang Yiyi
=========================================================
Txhyy version: 0.0.7
Txhyy title: txhyy
"""
__version__ = "0.0.7"
name = "txhyy"
title = name

from . import reg, dialog, pyc
from . import Video, Image
from .setting import *
from ._txhyy import *
from . import zhushi
import ctypes

class _Setting:
    user32 = ctypes.windll.user32
    shell32 = ctypes.windll.shell32

c = WMI