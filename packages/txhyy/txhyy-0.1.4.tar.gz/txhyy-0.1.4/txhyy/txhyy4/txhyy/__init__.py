__version__ = "0.0.4"
name = "txhyy"
title = name

from . import reg, dialog, pyc
from . import Video, Image
from . import encoding
from ._txhyy import *
from . import zhushi
from . import pi
import ctypes

class _TXHYY:
    user32 = ctypes.windll.user32
    shell32 = ctypes.windll.shell32