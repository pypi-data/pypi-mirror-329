import os
import subprocess
import compileall


class Pytopyc:
    def __call__(self, py_file_path):
        if not py_file_path.endswith('.py'):
            print("输入的文件不是 .py 文件。")
            return

        try:
            compileall.compile_file(py_file_path)
            pyc_file_path = py_file_path + 'c'
            return pyc_file_path
        except Exception as e:
            print(f"编译过程中出现错误: {e}")


class Pyctopy:
    def __call__(self, pyc_file_path):
        if not pyc_file_path.endswith('.pyc'):
            print("输入的文件不是 .pyc 文件。")
            return

        py_file_path = os.path.splitext(pyc_file_path)[0] + '.py'

        try:
            subprocess.run(['uncompyle6', '-o', py_file_path, pyc_file_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"反编译过程中出现错误: {e}")
        except Exception as e:
            print(f"发生未知错误: {e}")

pytopyc = Pyctopy()
pyctopy = Pyctopy()