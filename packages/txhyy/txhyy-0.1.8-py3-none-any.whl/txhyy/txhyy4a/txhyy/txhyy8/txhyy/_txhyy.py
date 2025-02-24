import wmi
import ctypes
import winreg
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
            attributes = ctypes.windll.kernel32.GetFileAttributesW(file_path)
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
            ctypes.windll.kernel32.SetFileAttributesW(file_path, attributes)
        else:
            print('文件未找着')
            exit(1)
    else:
        print('attributes: 此功能只支持Windows系统! ')
        exit(1)


installlist = ['https://pypi.tuna.tsinghua.edu.cn/simple - 清华',"https://mirrors.aliyun.com/pypi/simple/ - 阿里云","https://pypi.mirrors.ustc.edu.cn/simple/ - 中国科学技术大学","https://pypi.doubanio.com/simple/ - 豆瓣镜像"]


def _install_modules(modules, mirror_url="https://pypi.tuna.tsinghua.edu.cn/simple"):
    """
    依次安装指定的多个模块，可以指定镜像源，并返回安装输出
    :param modules: 要安装的模块列表
    :param mirror_url: 可选的镜像源 URL
    :return: 安装过程的输出信息
    """
    all_output = []
    for module in modules:
        command = ['pip', 'install']
        if mirror_url:
            command.extend(['-i', mirror_url])
        command.append(module)
        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output = result.stdout + result.stderr
            all_output.append(f"{output}")
        except subprocess.CalledProcessError as e:
            all_output.append(f"安装 {module} 时出现错误: {e.stderr}")
    combined_output = "\n".join(all_output)
    return combined_output


def quit(code):
    exit(code)


def ctrlc(text):
    """复制指定的内容"""
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_UNICODETEXT, text)
    win32clipboard.CloseClipboard()


def curani(cursor_path):
    """设置鼠标指针(.cur,.ani)"""
    hCursor = win32gui.LoadImage(0, cursor_path, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_LOADFROMFILE)
    if hCursor:
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
        shortcut.WorkingDirectory = os.path.dirname(target_path)
        shortcut.RunAsAdmin = True
    shortcut.save()

shell = Dispatch('WScript.Shell')

def brightness(brightness):
    """
    设置笔记本屏幕亮度
    brightness:设置亮度的百分比
    """
    if system() == 'Windows':
        try:
            c = wmi.WMI(namespace='wmi')
            methods = c.WmiMonitorBrightnessMethods()[0]
            methods.WmiSetBrightness(brightness, 0)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit()
    elif system() == 'Linux':
        try:
            backlight_dir = '/sys/class/backlight'
            controllers = os.listdir(backlight_dir)
            if not controllers:
                print("未找到背光控制器")
                return
            controller = controllers[0]
            max_brightness_path = os.path.join(backlight_dir, controller, 'max_brightness')
            with open(max_brightness_path, 'r') as f:
                max_brightness = int(f.read().strip())
            brightness_value = int(max_brightness * (brightness / 100))
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


def getcwd():
    """get? 获取当前工作目录"""
    if system() == 'Windows':
        kernel32 = ctypes.WinDLL('kernel32')
        buffer = ctypes.create_unicode_buffer(260)
        kernel32.GetCurrentDirectoryW(260, buffer)
        return buffer.value
    else:
        libc = ctypes.CDLL(ctypes.util.find_library('c'))
        buffer = ctypes.create_string_buffer(4096)
        libc.getcwd(buffer, 4096)
        return buffer.value.decode('utf-8')
    

def username():
    """获取用户名"""
    if system() == "Windows":
        return os.getenv("USERNAME")
    else:
        return os.getenv("USER")
    

def increase(file_extension=None, file_type=None, icon_path=None, associated_program=None):
    """
    :param file_extension 自定义后缀名
    :param file_type 自定义文件类型名称
    :param icon_path 图标文件路径，确保图标文件存在
    :param associated_program 关联的程序路径
    """
    if all(arg is None for arg in [file_extension, file_type, icon_path, associated_program]):
        print("Error: 至少需要提供一个参数")
        return
    try:
        if system() == 'Windows':
            try:
                if file_type:
                    key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, file_type)
                    winreg.SetValue(key, "", winreg.REG_SZ, "Custom File")
                if icon_path and file_type:
                    icon_key = winreg.CreateKey(key, "DefaultIcon")
                    winreg.SetValue(icon_key, "", winreg.REG_SZ, icon_path)
                if associated_program and file_type:
                    shell_key = winreg.CreateKey(key, r"shell\open\command")
                    winreg.SetValue(shell_key, "", winreg.REG_SZ, f'"{associated_program}" "%1"')
                if file_extension and file_type:
                    ext_key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, file_extension)
                    winreg.SetValue(ext_key, "", winreg.REG_SZ, file_type)
            except Exception as e:
                print(f"Error: {e}")
            finally:
                if 'key' in locals():
                    winreg.CloseKey(key)
                if 'icon_key' in locals():
                    winreg.CloseKey(icon_key)
                if 'shell_key' in locals():
                    winreg.CloseKey(shell_key)
                if 'ext_key' in locals():
                    winreg.CloseKey(ext_key)
        elif system() == 'macOS':
            if file_extension and associated_program:
                try:
                    subprocess.run(["duti", "-s", associated_program, file_extension], check=True)
                except subprocess.CalledProcessError as e:
                    print(f"Error: {e}")
        elif system() == 'Linux':
            if file_extension and associated_program:
                mime_type = subprocess.run(['xdg-mime', 'query', 'filetype', f'test{file_extension}'], capture_output=True, text=True).stdout.strip()
                try:
                    with open(os.path.expanduser('~/.local/share/applications/mimeapps.list'), 'a') as f:
                        f.write(f'[Default Applications]\n{mime_type}={associated_program}\n')
                except Exception as e:
                    print(f"Error: {e}")
    except Exception as e:
        raise Exception('increase Error:',e)
    

def delete(file_extension, file_type):
    """
    删除文件扩展名关联的函数
    :param file_extension: 要删除关联的文件扩展名
    :param file_type: 要删除关联的文件类型
    """
    if system() == 'Windows':
        try:
            try:
                ext_key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, file_extension, 0, winreg.KEY_ALL_ACCESS)
                winreg.DeleteKey(ext_key, "")
                winreg.CloseKey(ext_key)
            except FileNotFoundError:
                pass
            try:
                key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, file_type, 0, winreg.KEY_ALL_ACCESS)
                winreg.DeleteKey(key, "")
                winreg.CloseKey(key)
            except FileNotFoundError:
                raise Exception('delete Error: 文件不存在')
        except Exception as e:
            print(f"Error: {e}")
    elif system() == 'macOS':
        if file_extension:
            try:
                subprocess.run(["duti", "-d", file_extension], check=True)
            except subprocess.CalledProcessError as e:
                raise Exception('delete Error:',e)
    elif system() == 'Linux':
        if file_extension:
            mime_type = subprocess.run(['xdg-mime', 'query', 'filetype', f'test{file_extension}'], capture_output=True, text=True).stdout.strip()
            try:
                with open(os.path.expanduser('~/.local/share/applications/mimeapps.list'), 'r') as f:
                    lines = f.readlines()
                with open(os.path.expanduser('~/.local/share/applications/mimeapps.list'), 'w') as f:
                    for line in lines:
                        if not line.startswith(f'{mime_type}='):
                            f.write(line)
            except Exception as e:
                raise Exception('delete Error:',e)
            

def modify(old_file_extension=None, old_file_type=None, new_file_extension=None, new_file_type=None,
           new_icon_path=None, new_associated_program=None):
    """修改 文件后缀名的关联 """
    new_params = [new_file_extension, new_file_type, new_icon_path, new_associated_program]
    if all(arg is None for arg in new_params):
        print("Error: 至少需要提供一个新参数进行修改")
        return
    if system() == 'Windows':
        try:
            if old_file_extension and old_file_type:
                try:
                    ext_key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, old_file_extension, 0, winreg.KEY_ALL_ACCESS)
                    winreg.DeleteKey(ext_key, "")
                    winreg.CloseKey(ext_key)
                except FileNotFoundError:
                    pass
                try:
                    key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, old_file_type, 0, winreg.KEY_ALL_ACCESS)
                    winreg.DeleteKey(key, "")
                    winreg.CloseKey(key)
                except FileNotFoundError:
                    pass
            increase(new_file_extension, new_file_type, new_icon_path, new_associated_program)
        except Exception as e:
            raise Exception('modify Error:',e)
    elif system() == 'macOS':
        if old_file_extension:
            try:
                subprocess.run(["duti", "-d", old_file_extension], check=True)
            except subprocess.CalledProcessError as e:
                raise Exception('modify Error:',e)
        increase(new_file_extension, new_file_type, new_icon_path, new_associated_program)
    elif system() == 'Linux':
        if old_file_extension:
            mime_type = subprocess.run(['xdg-mime', 'query', 'filetype', f'test{old_file_extension}'], capture_output=True, text=True).stdout.strip()
            try:
                with open(os.path.expanduser('~/.local/share/applications/mimeapps.list'), 'r') as f:
                    lines = f.readlines()
                with open(os.path.expanduser('~/.local/share/applications/mimeapps.list'), 'w') as f:
                    for line in lines:
                        if not line.startswith(f'{mime_type}='):
                            f.write(line)
            except Exception as e:
                raise Exception('modify Error:',e)
        increase(new_file_extension, new_file_type, new_icon_path, new_associated_program)


def activate_windows(product_key):
    try:
        set_key_command = f'slmgr.vbs /ipk {product_key}'
        set_key_result = subprocess.run(set_key_command, shell=True, capture_output=True, text=True)
        if set_key_result.returncode == 0:
            pass
        else:
            return False + ' key'

        activate_command = 'slmgr.vbs /ato'
        activate_result = subprocess.run(activate_command, shell=True, capture_output=True, text=True)
        if activate_result.returncode == 0:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error：{e}")


Roaming = os.getenv('APPDATA')

def home() -> str:
    """获取用户文件夹路径"""
    if system() == "Windows":
        return os.environ.get('USERPROFILE')

    else:
        return os.path.expanduser('~')
    
from wmi import *

def _TEST() -> None:
    user = home()
    print(user)
    output = install(['txhyy','PyInstaller','pandas','pyqt6'])
    print("",output)

install = _install_modules
attr = attributes

if __name__ == "__main__":
    _TEST()