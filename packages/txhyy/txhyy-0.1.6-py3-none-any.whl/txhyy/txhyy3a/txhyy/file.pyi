from typing import Tuple

def getcwd() -> str: 
    """获取当前工作目录"""
    ...

def remove(path: str) -> None:
    """删除文件"""
    ...

def removedir(path: str) -> None: 
    """删除目录"""
    ...

def cmd(command: str) -> int:
    """执行cmd命令"""
    ...

def powershell(command: str): 
    """执行PowerShell命令"""
    ...

def chdir(path: str) -> None: 
    """调整工作目录"""
    ...

def mkdir(path: str) -> None: 
    """创建一个文件夹"""
    ...

def get_encoding(file_path: str) -> Tuple[str, float]: 
    """获取一个文件的编码"""
    ...

def moencoding(input_file_path: str, output_file_path: str, new_encoding: str = 'utf-8') -> None:
    """修改一个文件的编码"""
    ...