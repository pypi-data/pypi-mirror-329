import requests
from tqdm.rich import tqdm
import subprocess
import argparse
import os
from rich.console import Console
from rich.style import Style

console = Console()
error_style = Style(color="red")

def download_get_pip(download_path):
    url = "https://bootstrap.pypa.io/get-pip.py"
    file_name = os.path.join(download_path, "get-pip.py")
    try:
        response = requests.get(url, stream=True)
        total_size_in_bytes = int(response.headers.get('content-length', 0))
        block_size = 1024
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
        with open(file_name, 'wb') as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
        progress_bar.close()
        if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
            console.print("Download error occurred.", style=error_style)
        return file_name
    except Exception as e:
        console.print(f"Error downloading get-pip.py: {e}", style=error_style)
        return None

def modify_get_pip(file_name, pip_version):
    if pip_version:
        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            for i, line in enumerate(lines):
                if 'args.append("pip")' in line:
                    lines[i] = f'args.append("pip=={pip_version}")\n'
            with open(file_name, 'w', encoding='utf-8') as f:
                f.writelines(lines)
        except Exception as e:
            console.print(f"Error modifying get-pip.py: {e}", style=error_style)

def run_get_pip(file_name):
    try:
        subprocess.run(['python', file_name], check=True)
        console.print("pip installation succeeded.")
    except subprocess.CalledProcessError as e:
        console.print(f"pip installation failed: {e}", style=error_style)

def check_pip_installed():
    try:
        subprocess.run(['pip', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False

def install_module(module_name, module_version):
    if module_name:
        if module_version:
            package = f"{module_name}=={module_version}"
        else:
            package = module_name
        try:
            result = subprocess.run(['pip', 'install', package], check=True, text=True, capture_output=True)
            console.print(result.stdout)
            console.print("Module installation succeeded.")
        except subprocess.CalledProcessError as e:
            console.print(f"Module installation failed: {e.stderr}", style=error_style)

def main():
    parser = argparse.ArgumentParser(description='Automatically download and run get-pip.py to install pip and modules')
    parser.add_argument('-v', '--version', help='Specify the version of pip to install or upgrade')
    parser.add_argument('-o', '--output', default='.', help='Specify the download path for get-pip.py')
    parser.add_argument('-u', '--unexecute', action='store_true', help='Only download get-pip.py without running it')
    parser.add_argument('-m', '--module', help='Specify the module to install')
    parser.add_argument('-mv', '--module-version', help='Specify the version of the module to install')
    args = parser.parse_args()

    if not os.path.exists(args.output):
        try:
            os.makedirs(args.output)
        except Exception as e:
            console.print(f"Error creating directory: {e}", style=error_style)
            return

    if not check_pip_installed():
        file_name = download_get_pip(args.output)
        if file_name:
            modify_get_pip(file_name, args.version)
            if not args.unexecute:
                run_get_pip(file_name)
    else:
        console.print("pip is already installed.")

    install_module(args.module, args.module_version)

    # Clean up the downloaded file if needed
    # You can uncomment the following lines if you want to keep the file only when -u is used
    # if not args.unexecute and os.path.exists(file_name):
    #     os.remove(file_name)

if __name__ == "__main__":
    main()