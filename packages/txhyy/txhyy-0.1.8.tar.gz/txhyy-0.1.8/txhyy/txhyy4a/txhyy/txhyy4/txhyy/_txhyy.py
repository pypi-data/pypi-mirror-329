import wmi
import ctypes
import os, sys
import win32con
import win32gui
import win32api
import subprocess
from hashlib import *
import win32clipboard
from win32com.client import Dispatch


FILE_ATTRIBUTE_HIDDEN = 0x2
FILE_ATTRIBUTE_READONLY = 0x1
FILE_ATTRIBUTE_ARCHIVE = 0x20
FILE_ATTRIBUTE_SYSTEM = 0x4
FILE_ATTRIBUTE_COMPRESSED = 0x800


def exit(code):
    raise SystemExit(code)


def attributes(file_path, hidden=False, readonly=False, archive=False, system=False, compressed=False):
    """
    设置指定文件的属性为隐藏、只读、存档、系统或压缩
    :param file_path: 文件路径
    :param hidden: 是否设置为隐藏，默认为False
    :param readonly: 是否设置为只读，默认为False
    :param archive: 是否设置为存档，默认为False
    :param system: 是否设置为系统，默认为False
    :param compressed: 是否设置为压缩，默认为False
    """
    if os.name == 'nt':
        if os.path.exists(file_path):
            # 获取当前文件属性
            attributes = ctypes.windll.kernel32.GetFileAttributesW(file_path)
            
            # 根据参数设置属性
            if hidden:
                attributes |= FILE_ATTRIBUTE_HIDDEN
            else:
                attributes &= ~FILE_ATTRIBUTE_HIDDEN
            
            if readonly:
                attributes |= FILE_ATTRIBUTE_READONLY
            else:
                attributes &= ~FILE_ATTRIBUTE_READONLY
            
            if archive:
                attributes |= FILE_ATTRIBUTE_ARCHIVE
            else:
                attributes &= ~FILE_ATTRIBUTE_ARCHIVE
            
            if system:
                attributes |= FILE_ATTRIBUTE_SYSTEM
            else:
                attributes &= ~FILE_ATTRIBUTE_SYSTEM
            
            if compressed:
                attributes |= FILE_ATTRIBUTE_COMPRESSED
            else:
                attributes &= ~FILE_ATTRIBUTE_COMPRESSED
            
            # 更新文件属性
            ctypes.windll.kernel32.SetFileAttributesW(file_path, attributes)
        else:
            print('文件未找着')
            exit(1)

    else:
        print('attributes: 此功能只支持Windows系统! ')
        exit(1)


def quit(code):
    exit(code)


def ctrlc(text):
    """复制指定的内容"""
    # 打开剪贴板
    win32clipboard.OpenClipboard()
    # 清空剪贴板
    win32clipboard.EmptyClipboard()
    # 将文本以Unicode格式放入剪贴板
    win32clipboard.SetClipboardData(win32clipboard.CF_UNICODETEXT, text)
    # 关闭剪贴板
    win32clipboard.CloseClipboard()


def curani(cursor_path):
    """设置鼠标指针(.cur,.ani)"""
    # 加载自定义光标
    hCursor = win32gui.LoadImage(0, cursor_path, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_LOADFROMFILE)
    if hCursor:
        # 设置全局光标
        win32api.SetSystemCursor(hCursor, win32con.OCR_NORMAL)


def size():
    """获取屏幕分辨率"""
    screen_width = win32api.GetSystemMetrics(0)
    screen_height = win32api.GetSystemMetrics(1)

    return screen_width, screen_height


def copy(source_file, destination_file, TrueorFalse=False):
    """
    复制文件,且不用管理员权限(如果文件是管理员权限或更高权限复制需要管理员权限)
    :param source_file:源文件路径,例如 "C:/path/to/source.txt"
    :param destination_file:目标文件路径,例如 "C:/path/to/destination.txt"
    :param TrueorFalse:是否覆盖文件,默认不覆盖.False:不覆盖,True:覆盖
    """
    if os.path.exists(destination_file):
        if not TrueorFalse:
            print(f"目标文件 {destination_file} 已存在，且不允许覆盖，跳过复制操作。")
            return

    try:
        source_hash = sha256(source_file)
        temp_file = destination_file + '.tmp'

        chunk_size = 4096
        with open(source_file, 'rb') as src_file:
            with open(temp_file, 'wb') as dest_file:
                while True:
                    chunk = src_file.read(chunk_size)
                    if not chunk:
                        break
                    dest_file.write(chunk)

        temp_hash = sha256(temp_file)

        if source_hash == temp_hash:
            os.replace(temp_file, destination_file)
        else:
            print("文件复制完成，但验证失败：内容不匹配。")
            os.remove(temp_file)

    except FileNotFoundError:
        raise Exception('copy2 Error: 复制失败')
    except PermissionError:
        if os.path.exists(temp_file):
            os.remove(temp_file)

        raise Exception('copy2 Error: 没有权限')
    except Exception as e:
        if os.path.exists(temp_file):
            os.remove(temp_file)

        raise Exception('copy2 Error:',e)
    
    except Exception as e:
        if os.path.exists(temp_file):
            os.remove(temp_file)

        raise Exception('copy2 Error:',e)
    

def system(none = None):
    """通过调用系统命令识别操作系统"""
    if none == None:
        try:
            result = subprocess.run("ver", capture_output=True, text=True, shell=True)
            if "Microsoft" in result.stdout:
                return "Windows"
            
            result = subprocess.run("uname", capture_output=True, text=True, shell=True)
            if "Darwin" in result.stdout:
                return "macOS"
            
            result = subprocess.run("uname", capture_output=True, text=True, shell=True)
            if "Linux" in result.stdout:
                return "Linux"
            
        except Exception as e:
            return f"发生错误: {e}"

        return "未知操作系统"

    else:
        return none
    

def shortcut(target_path, shortcut_path, run_as_admin=False):
    """
    创建指定文件的快捷方式
    :param target_path: 目标文件路径
    :param shortcut_path: 快捷方式保存路径
    :param run_as_admin: 是否以管理员权限运行，默认为False
    """
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = target_path
    if run_as_admin:
        # 设置快捷方式以管理员权限运行
        shortcut.WorkingDirectory = os.path.dirname(target_path)
        shortcut.RunAsAdmin = True
    shortcut.save()


def brightness(brightness):
    """
    设置笔记本屏幕亮度
    brightness:设置亮度的百分比
    """
    if system() == 'Windows':
        try:
            # 创建 WMI 实例
            c = wmi.WMI(namespace='wmi')
            methods = c.WmiMonitorBrightnessMethods()[0]
            # 设置屏幕亮度
            methods.WmiSetBrightness(brightness, 0)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit()

    elif system() == 'Linux':
        try:
            # 查找背光控制器目录
            backlight_dir = '/sys/class/backlight'
            controllers = os.listdir(backlight_dir)
            if not controllers:
                print("未找到背光控制器")
                return
            controller = controllers[0]
            # 获取最大亮度值
            max_brightness_path = os.path.join(backlight_dir, controller, 'max_brightness')
            with open(max_brightness_path, 'r') as f:
                max_brightness = int(f.read().strip())
            # 计算要设置的亮度值
            brightness_value = int(max_brightness * (brightness / 100))
            # 设置亮度
            brightness_path = os.path.join(backlight_dir, controller, 'brightness')
            with open(brightness_path, 'w') as f:
                f.write(str(brightness_value))
        except Exception as e:
            print(f"Error: {e}")
            sys.exit()

    elif system() == 'macOS':
        try:
            subprocess.run(['brightness', str(brightness / 100)], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            sys.exit()

    else:
        print("不支持的操作系统")

Error = Exception

def desktop():
    """获取桌面位置(Desktop)"""
    return os.path.join(os.path.expanduser("~"), "Desktop")


def backend(file):
    """将指定的文件在后台运行"""
    subprocess.Popen(file, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)