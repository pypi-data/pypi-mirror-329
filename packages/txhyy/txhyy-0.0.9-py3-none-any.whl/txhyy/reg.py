import subprocess
import winreg
import ctypes
import sys
import os

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
    def __init__(self):
        self.namespace_path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\MyComputer\NameSpace"

    def getguid(self):
        try:
            # 打开 NameSpace 注册表项
            namespace_key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                self.namespace_path,
                0,
                winreg.KEY_READ
            )
            guids = []
            index = 0
            while True:
                try:
                    # 枚举子项名称（即 GUID）
                    subkey_name = winreg.EnumKey(namespace_key, index)
                    guids.append(subkey_name)
                    index += 1
                except OSError:
                    # 枚举结束，跳出循环
                    break
            winreg.CloseKey(namespace_key)
            return guids
        except Exception as e:
            print(f"获取 GUID 时出现错误: {e}")
            return []

    def addicon(self, guid, icon_path):
        try:
            # 打开 NameSpace 注册表项
            namespace_key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                self.namespace_path,
                0,
                winreg.KEY_ALL_ACCESS
            )

            try:
                # 尝试打开指定 GUID 的子项
                item_key = winreg.OpenKey(namespace_key, guid, 0, winreg.KEY_ALL_ACCESS)
            except FileNotFoundError:
                print(f"未找到 GUID 为 {guid} 的项。")
                winreg.CloseKey(namespace_key)
                return

            try:
                # 尝试打开或创建 DefaultIcon 子项
                default_icon_key = winreg.CreateKeyEx(item_key, "DefaultIcon", 0, winreg.KEY_SET_VALUE)
                # 设置默认图标路径
                winreg.SetValue(default_icon_key, "", winreg.REG_SZ, icon_path)
                print(f"GUID 为 {guid} 的项的图标已成功设置为 {icon_path}。")
            except Exception as e:
                print(f"设置图标时出现错误: {e}")
            finally:
                if 'default_icon_key' in locals():
                    winreg.CloseKey(default_icon_key)

            winreg.CloseKey(item_key)
            winreg.CloseKey(namespace_key)

        except Exception as e:
            print(f"操作注册表时出现错误: {e}")

    def deleteicon(self, guid):
        try:
            # 打开 NameSpace 注册表项
            namespace_key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                self.namespace_path,
                0,
                winreg.KEY_ALL_ACCESS
            )

            try:
                # 尝试打开指定 GUID 的子项
                item_key = winreg.OpenKey(namespace_key, guid, 0, winreg.KEY_ALL_ACCESS)
            except FileNotFoundError:
                print(f"未找到 GUID 为 {guid} 的项。")
                winreg.CloseKey(namespace_key)
                return

            try:
                # 删除 DefaultIcon 子项
                winreg.DeleteKey(item_key, "DefaultIcon")
                print(f"GUID 为 {guid} 的项的图标已成功删除。")
            except FileNotFoundError:
                print(f"GUID 为 {guid} 的项没有设置图标。")
            except Exception as e:
                print(f"删除图标时出现错误: {e}")
            finally:
                winreg.CloseKey(item_key)

            winreg.CloseKey(namespace_key)

        except Exception as e:
            print(f"操作注册表时出现错误: {e}")

def is_admin():
    try:
        # 尝试打开需要管理员权限的注册表项来检查是否已有权限
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE", 0, winreg.KEY_ALL_ACCESS)
        winreg.CloseKey(key)
        return True
    except PermissionError:
        return False

script = sys.argv[0]


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


def username():
    """获取用户名"""

    if system() == "Windows":
        return os.getenv("USERNAME")

    else:
        return os.getenv("USER")

name = system()

if __name__ == "__main__":
    print(name)