# main.pyi

from typing import List
from moviepy.editor import VideoFileClip
import pysrt
import os
import re
import subprocess

def clip(input_file: str, output_file: str, start_time: float, end_time: float) -> None:
    """视频剪辑"""

def convert(input_file: str, output_file: str) -> None:
    """视频格式转换"""

def extract_audio(input_file: str, output_file: str) -> None:
    """音频提取"""

def subtitles(input_file: str, output_file: str, subtitle_file: str) -> None:
    """添加字幕"""

def merge_videos(input_files: List[str], output_file: str) -> None:
    """合并视频"""

def adjust_video_speed(input_file: str, output_file: str, speed_factor: float) -> None:
    """调整视频速度,1是正常速度"""

def split_video(input_file: str, output_prefix: str, segment_duration: float) -> None:
    """分割视频,segment_duration是每个片段的时长"""

def merge_videos_moviepy(input_files: List[str], output_file: str) -> None:
    """合并视频"""

def clip(input_file: str, output_file: str, start_time: float, end_time: float) -> None:
    """视频剪辑"""

def convert(input_file: str, output_file: str) -> None:
    """视频格式转换"""

def extract_audio(input_file: str, output_file: str) -> None:
    """音频提取"""

def subtitles(input_file: str, output_file: str, subtitle_file: str) -> None:
    """添加字幕"""

def merge_videos(input_files: List[str], output_file: str) -> None:
    """合并视频"""

def adjust_video_speed(input_file: str, output_file: str, speed_factor: float) -> None:
    """调整视频速度,1是正常速度"""

def split_video(input_file: str, output_prefix: str, segment_duration: float) -> None:
    """分割视频,segment_duration是每个片段的时长"""

def merge_videos_moviepy(input_files: List[str], output_file: str) -> None:
    """合并视频"""

class Pytopyc:
    def __call__(self, py_file_path: str) -> str:
        """将 .py 文件编译为 .pyc 文件"""

class Pyctopy:
    def __call__(self, pyc_file_path: str) -> None:
        """将 .pyc 文件反编译为 .py 文件"""

def encoding(infile: str, outfile: str, target_encoding: str) -> int:
    """
    转换文件编码。

    :param infile: 输入文件的路径
    :param outfile: 输出文件的路径
    :param target_encoding: 目标编码，支持 "UTF-8" 和 "GBK"
    :return: 编码转换结果，0 表示成功，非 0 表示失败
    """
    ...

def pi(terms: int) -> str:
    """
    Calculate pi using Leibniz series.

    Args:
        terms (int): The number of terms to use in the Leibniz series.

    Returns:
        str: An approximation of pi as a string.
    """
    ...

def remove_jing(input_file_path: str, output_file_path: str) -> None:
    """去除#号"""

def remove_ying(file_path: str) -> None:
    """去除三引号(''''''和"""""")"""

import winreg
import ctypes
import sys

user32 = ctypes.windll.user32
shell32 = ctypes.windll.shell32
HKEY_CURRENT_USER = winreg.HKEY_CURRENT_USER
HKEY_CLASSES_ROOT = winreg.HKEY_CLASSES_ROOT
HKEY_CURRENT_CONFIG = winreg.HKEY_CURRENT_CONFIG
HKEY_DYN_DATA = winreg.HKEY_DYN_DATA
HKEY_LOCAL_MACHINE = winreg.HKEY_LOCAL_MACHINE
HKEY_PERFORMANCE_DATA = winreg.HKEY_PERFORMANCE_DATA
HKEY_USERS = winreg.HKEY_USERS

class Namespace:
    def __init__(self) -> None: ...
    def getguid(self) -> list[str]: ...
    def addicon(self, guid: str, icon_path: str) -> None: ...
    def deleteicon(self, guid: str) -> None: ...

def is_admin() -> bool: ...
def system(none = None) -> str: ...
def username() -> str: ...

def ctrlc(text: str) -> None:
    """复制指定的内容"""

def desktop() -> str:
    """获取桌面位置(Desktop)"""

from PIL.Image import Resampling
from PIL import Image

def convert_image(input_file: str, output_file: str) -> None:
    """图像格式转换"""

def resize_image(input_file: str, output_file: str, width: int, height: int) -> None:
    """图像缩放"""

def exit(code: int) -> None: ...
def quit(code: int) -> None: ...

FILE_ATTRIBUTE_HIDDEN = 0x2
FILE_ATTRIBUTE_READONLY = 0x1
FILE_ATTRIBUTE_ARCHIVE = 0x20
FILE_ATTRIBUTE_SYSTEM = 0x4
FILE_ATTRIBUTE_COMPRESSED = 0x800

def attributes(file_path: str, hidden: bool = False, readonly: bool = False, archive: bool = False,
               system: bool = False, compressed: bool = False) -> None:
    """
    设置指定文件的属性为隐藏、只读、存档、系统或压缩
    :param file_path: 文件路径
    :param hidden: 是否设置为隐藏，默认为False
    :param readonly: 是否设置为只读，默认为False
    :param archive: 是否设置为存档，默认为False
    :param system: 是否设置为系统，默认为False
    :param compressed: 是否设置为压缩，默认为False
    """

...