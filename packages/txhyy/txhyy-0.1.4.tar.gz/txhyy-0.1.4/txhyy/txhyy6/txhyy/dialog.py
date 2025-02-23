import os

WXPYTHON = "wxpython"
PYQT6 = "pyqt6"
TKINTER = "tkinter"
PYQT5 = "pyqt5"

wxpython = "wxpython"
PyQt6 = "pyqt6"
Tkinter = "tkinter"
PyQt5 = "pyqt5"

class FileDialogIntegrator:
    def __init__(self, preferred_lib='auto', open_title="Open File", save_title="Save File",
                 filetypes=[("All Files", "*.*"), ("Text Files", "*.txt"), ("Python 源文件", "*.py")], initial_dir=None):
        self.preferred_lib = preferred_lib
        self.open_title = open_title
        self.save_title = save_title
        self.filetypes = filetypes
        self.initial_dir = initial_dir
        self.strategy = self._select_strategy()

    def _select_strategy(self):
        if self.preferred_lib == 'auto':
            # 按优先级尝试选择可用的库
            for lib in ['pyqt6', 'pyqt5', 'tkinter', 'wxpython']:
                try:
                    return self._get_strategy(lib)
                except ImportError:
                    continue
            raise ImportError("No supported GUI library found.")
        else:
            return self._get_strategy(self.preferred_lib)

    def _get_strategy(self, lib):
        if lib == 'tkinter':
            import tkinter as tk
            from tkinter import filedialog

            class TkinterFileDialogStrategy:
                def __init__(self, open_title, save_title, filetypes, initial_dir):
                    self.open_title = open_title
                    self.save_title = save_title
                    self.filetypes = filetypes
                    self.initial_dir = initial_dir

                def open_file_dialog(self):
                    root = tk.Tk()
                    root.withdraw()
                    # 居中显示主窗口（虽然 filedialog 依赖主窗口位置，但不一定能完全保证居中）
                    root.update_idletasks()
                    width = root.winfo_width()
                    height = root.winfo_height()
                    x = (root.winfo_screenwidth() // 2) - (width // 2)
                    y = (root.winfo_screenheight() // 2) - (height // 2)
                    root.geometry(f'{width}x{height}+{x}+{y}')

                    file_path = filedialog.askopenfilename(
                        title=self.open_title,
                        filetypes=self.filetypes,
                        initialdir=self.initial_dir
                    )
                    root.destroy()
                    return file_path

                def save_file_dialog(self):
                    root = tk.Tk()
                    root.withdraw()
                    # 居中显示主窗口
                    root.update_idletasks()
                    width = root.winfo_width()
                    height = root.winfo_height()
                    x = (root.winfo_screenwidth() // 2) - (width // 2)
                    y = (root.winfo_screenheight() // 2) - (height // 2)
                    root.geometry(f'{width}x{height}+{x}+{y}')

                    file_path = filedialog.asksaveasfilename(
                        title=self.save_title,
                        defaultextension=".txt",
                        filetypes=self.filetypes,
                        initialdir=self.initial_dir
                    )
                    root.destroy()
                    return file_path

            return TkinterFileDialogStrategy(self.open_title, self.save_title, self.filetypes, self.initial_dir)

        elif lib == 'pyqt6':
            from PyQt6.QtWidgets import QApplication, QFileDialog
            import sys

            class PyQt6FileDialogStrategy:
                def __init__(self, open_title, save_title, filetypes, initial_dir):
                    self.open_title = open_title
                    self.save_title = save_title
                    self.filetypes = self._convert_filetypes(filetypes)
                    self.initial_dir = initial_dir

                def _convert_filetypes(self, filetypes):
                    return ';;'.join([f'{name} ({pattern})' for name, pattern in filetypes])

                def open_file_dialog(self):
                    app = QApplication(sys.argv)
                    dialog = QFileDialog()
                    dialog.setWindowTitle(self.open_title)
                    dialog.setNameFilter(self.filetypes)
                    if self.initial_dir:
                        dialog.setDirectory(self.initial_dir)

                    # 居中显示对话框
                    screen_geometry = app.primaryScreen().geometry()
                    dialog_size = dialog.sizeHint()
                    x = (screen_geometry.width() - dialog_size.width()) // 2
                    y = (screen_geometry.height() - dialog_size.height()) // 2
                    dialog.move(x, y)

                    if dialog.exec():
                        file_path = dialog.selectedFiles()[0]
                    else:
                        file_path = None
                    app.quit()
                    return file_path

                def save_file_dialog(self):
                    app = QApplication(sys.argv)
                    dialog = QFileDialog()
                    dialog.setWindowTitle(self.save_title)
                    dialog.setNameFilter(self.filetypes)
                    if self.initial_dir:
                        dialog.setDirectory(self.initial_dir)

                    # 居中显示对话框
                    screen_geometry = app.primaryScreen().geometry()
                    dialog_size = dialog.sizeHint()
                    x = (screen_geometry.width() - dialog_size.width()) // 2
                    y = (screen_geometry.height() - dialog_size.height()) // 2
                    dialog.move(x, y)

                    if dialog.exec():
                        file_path = dialog.selectedFiles()[0]
                    else:
                        file_path = None
                    app.quit()
                    return file_path

            return PyQt6FileDialogStrategy(self.open_title, self.save_title, self.filetypes, self.initial_dir)

        elif lib == 'pyqt5':
            from PyQt5.QtWidgets import QApplication, QFileDialog
            import sys

            class PyQt5FileDialogStrategy:
                def __init__(self, open_title, save_title, filetypes, initial_dir):
                    self.open_title = open_title
                    self.save_title = save_title
                    self.filetypes = self._convert_filetypes(filetypes)
                    self.initial_dir = initial_dir

                def _convert_filetypes(self, filetypes):
                    return ';;'.join([f'{name} ({pattern})' for name, pattern in filetypes])

                def open_file_dialog(self):
                    app = QApplication(sys.argv)
                    dialog = QFileDialog()
                    dialog.setWindowTitle(self.open_title)
                    dialog.setNameFilter(self.filetypes)
                    if self.initial_dir:
                        dialog.setDirectory(self.initial_dir)

                    # 居中显示对话框
                    screen_geometry = app.desktop().screenGeometry()
                    dialog_size = dialog.sizeHint()
                    x = (screen_geometry.width() - dialog_size.width()) // 2
                    y = (screen_geometry.height() - dialog_size.height()) // 2
                    dialog.move(x, y)

                    if dialog.exec_():
                        file_path = dialog.selectedFiles()[0]
                    else:
                        file_path = None
                    app.quit()
                    return file_path

                def save_file_dialog(self):
                    app = QApplication(sys.argv)
                    dialog = QFileDialog()
                    dialog.setWindowTitle(self.save_title)
                    dialog.setNameFilter(self.filetypes)
                    if self.initial_dir:
                        dialog.setDirectory(self.initial_dir)

                    # 居中显示对话框
                    screen_geometry = app.desktop().screenGeometry()
                    dialog_size = dialog.sizeHint()
                    x = (screen_geometry.width() - dialog_size.width()) // 2
                    y = (screen_geometry.height() - dialog_size.height()) // 2
                    dialog.move(x, y)

                    if dialog.exec_():
                        file_path = dialog.selectedFiles()[0]
                    else:
                        file_path = None
                    app.quit()
                    return file_path

            return PyQt5FileDialogStrategy(self.open_title, self.save_title, self.filetypes, self.initial_dir)

        elif lib == 'wxpython':
            import wx

            class WxPythonFileDialogStrategy:
                def __init__(self, open_title, save_title, filetypes, initial_dir):
                    self.open_title = open_title
                    self.save_title = save_title
                    self.filetypes = self._convert_filetypes(filetypes)
                    self.initial_dir = initial_dir

                def _convert_filetypes(self, filetypes):
                    return '|'.join([f'{name}|{pattern}' for name, pattern in filetypes])

                def open_file_dialog(self):
                    app = wx.App()
                    frame = wx.Frame(None, -1, self.open_title)
                    frame.SetSize(0, 0, 200, 50)
                    dialog = wx.FileDialog(frame, self.open_title,
                                           defaultDir=self.initial_dir if self.initial_dir else "",
                                           wildcard=self.filetypes, style=wx.FD_OPEN)
                    if dialog.ShowModal() == wx.ID_OK:
                        file_path = dialog.GetPath()
                    else:
                        file_path = None
                    dialog.Destroy()
                    app.Destroy()
                    return file_path

                def save_file_dialog(self):
                    app = wx.App()
                    frame = wx.Frame(None, -1, self.save_title)
                    frame.SetSize(0, 0, 200, 50)
                    dialog = wx.FileDialog(frame, self.save_title,
                                           defaultDir=self.initial_dir if self.initial_dir else "",
                                           wildcard=self.filetypes, style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
                    if dialog.ShowModal() == wx.ID_OK:
                        file_path = dialog.GetPath()
                    else:
                        file_path = None
                    dialog.Destroy()
                    app.Destroy()
                    return file_path

            return WxPythonFileDialogStrategy(self.open_title, self.save_title, self.filetypes, self.initial_dir)
        else:
            raise ValueError(f"Unsupported library: {lib}")

    def open_file(self):
        return self.strategy.open_file_dialog()

    def save_file(self):
        return self.strategy.save_file_dialog()

if __name__ == "__main__":
    dialog = FileDialogIntegrator(
        preferred_lib=PyQt6,
        open_title="Select a Python file",
        save_title="Save your Python script",
        filetypes=[("Python Files", "*.py"), ("All Files", "*.*")],
        initial_dir=os.getcwd()
    )

    open_path = dialog.open_file()
    if open_path:
        print(f"Selected file to open: {open_path}")
    else:
        print("No file selected for opening.")

    save_path = dialog.save_file()
    if save_path:
        print(f"File will be saved at: {save_path}")
    else:
        print("No save path selected.")