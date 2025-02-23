"""
Author: Huang Yiyi
=========================================================
Txhyy version: 0.0.6
Txhyy title: txhyy
"""
__version__ = "0.0.6"
name = "txhyy"
title = name

from . import reg, dialog, pyc
from . import Video, Image
from .encoding import *
from .setting import *
from ._txhyy import *
from . import zhushi
from .pi import *
import ctypes

class _Setting:
    user32 = ctypes.windll.user32
    shell32 = ctypes.windll.shell32