import os
import shutil
import requests
import argparse
from tqdm.rich import tqdm
import multiprocessing
import time
import subprocess
import zipfile


PROXY_LIST = [
    {'ip': '36.89.158.93', 'port': 4480, 'type': 'HTTPS'},
    {'ip': '217.64.149.146', 'port': 8118, 'type': 'HTTP'},
]

# 用于存储下载结果的全局变量
download_success = False
downloaded_file_path = None

# 检查代理可用性并测量速度
def check_proxy(proxy):
    proxy_type = proxy['type'].lower()
    proxy_address = f"{proxy_type}://{proxy['ip']}:{proxy['port']}"
    proxies = {
        'http': proxy_address,
        'https': proxy_address
    }
    try:
        start_time = time.time()
        response = requests.get('http://www.baidu.com', proxies=proxies, timeout=5)
        end_time = time.time()
        speed = end_time - start_time
        return response.status_code == 200, speed
    except Exception:
        return False, None

# 使用代理下载文件
def download_with_proxy(url, filename, download_dir, proxy=None):
    global download_success, downloaded_file_path
    if download_success:
        return
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    if proxy:
        proxy_type = proxy['type'].lower()
        proxy_address = f"{proxy_type}://{proxy['ip']}:{proxy['port']}"
        proxies = {
            'http': proxy_address,
            'https': proxy_address
        }
        print(f"Using proxy: {proxy_address}")
    else:
        proxies = None
        print("Downloading without proxy.")

    max_retries = 3
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(url, stream=True, proxies=proxies, headers=headers, timeout=10)
            response.raise_for_status()  # 检查响应状态码
            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024
            file_path = os.path.join(download_dir, filename)

            # 确保下载目录存在
            if not os.path.exists(download_dir):
                os.makedirs(download_dir)

            with tqdm(total=total_size, unit='iB', unit_scale=True, colour='green') as progress_bar:
                with open(file_path, 'wb') as file:
                    for data in response.iter_content(block_size):
                        progress_bar.update(len(data))
                        file.write(data)

            if total_size != 0 and progress_bar.n != total_size:
                print("Download error")
                # 删除已下载的不完整文件
                if os.path.exists(file_path):
                    os.remove(file_path)
                retries += 1
                print(f"Download attempt {retries} failed. Retrying in 5 seconds...")
                time.sleep(5)
            else:
                print(f"{filename} download completed, saved at: {file_path}")
                download_success = True
                downloaded_file_path = file_path
                return
        except requests.RequestException as e:
            retries += 1
            # 删除已下载的不完整文件
            file_path = os.path.join(download_dir, filename)
            if os.path.exists(file_path):
                os.remove(file_path)
            if proxy:
                print(f"Download attempt {retries} failed using proxy {proxy_address}: {e}. Retrying in 5 seconds...")
            else:
                print(f"Download attempt {retries} failed without proxy: {e}. Retrying in 5 seconds...")
            time.sleep(5)
        except Exception as e:
            retries += 1
            print(f"Unexpected error in download attempt {retries}: {e}. Retrying in 5 seconds...")
            time.sleep(5)

# 下载文件
def download_file(url, filename, download_dir, use_proxy=False):
    global download_success, downloaded_file_path
    download_success = False
    downloaded_file_path = None

    if use_proxy:
        available_proxies = []
        for proxy in PROXY_LIST:
            is_available, speed = check_proxy(proxy)
            if is_available:
                proxy['speed'] = speed
                available_proxies.append(proxy)
                print(f"Proxy {proxy['ip']}:{proxy['port']} is available, speed: {speed:.2f} seconds")
            else:
                print(f"Proxy {proxy['ip']}:{proxy['port']} is not available")

        if not available_proxies:
            print("No available proxies found. Trying without proxy...")
            download_with_proxy(url, filename, download_dir)
        else:
            # 根据速度排序
            available_proxies.sort(key=lambda x: x['speed'])

            processes = []
            for proxy in available_proxies:
                process = multiprocessing.Process(target=download_with_proxy, args=(url, filename, download_dir, proxy))
                processes.append(process)
                process.start()

            for process in processes:
                process.join()
    else:
        print("Downloading without proxy as requested.")
        download_with_proxy(url, filename, download_dir)

    if not download_success:
        print("All attempts have been tried. Download failed.")
    return downloaded_file_path

# Download apktool.jar file
def download_apktool_jar(download_dir, jar_url, use_proxy=False):
    return download_file(jar_url, 'apktool.jar', download_dir, use_proxy)

# 生成 apktool.bat 文件
def generate_apktool_bat(download_dir, java_home):
    bat_content = f"""
@echo off
rem 设置 JAVA_HOME 环境变量
set JAVA_HOME={java_home}
rem 获取脚本所在目录
set SCRIPT_DIR=%~dp0
rem 拼接 apktool.jar 文件的完整路径
set APKTOOL_JAR=%SCRIPT_DIR%apktool.jar

rem 检查 apktool.jar 文件是否存在
if not exist "%APKTOOL_JAR%" (
    echo apktool.jar not found!
    pause
    exit /b 1
)

rem 调用 Java 命令执行 apktool.jar
java -jar "%APKTOOL_JAR%" %*
    """
    bat_content = bat_content.strip()
    bat_file_path = os.path.join(download_dir, 'apktool.bat')
    with open(bat_file_path, 'w', encoding='utf-8') as f:
        f.write(bat_content)
    print(f"apktool.bat 文件已生成，保存路径为: {bat_file_path}")

# Move files to the specified folder
def move_files_to_destination(source_dir, destination_dir):
    # Check if the destination folder exists, create it if not
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # List of files to move
    files_to_move = ["apktool.jar", "apktool.bat"]

    for file in files_to_move:
        source_file = os.path.join(source_dir, file)
        destination_file = os.path.join(destination_dir, file)
        if os.path.exists(source_file):
            try:
                # Move the file
                shutil.move(source_file, destination_file)
                print(f"File {file} has been successfully moved to {destination_file}")
            except Exception as e:
                print(f"Error moving file {file}: {e}")
        else:
            print(f"Source file {source_file} not found.")

# Check if apktool exists
def check_apktool_exists(destination_dir):
    apktool_jar = os.path.join(destination_dir, "apktool.jar")
    apktool_bat = os.path.join(destination_dir, "apktool.bat")
    return os.path.exists(apktool_jar) and os.path.exists(apktool_bat)

# Execute apktool to extract APK resources
def extract_apk(apk_file, output_dir, destination_dir):
    apktool_bat = os.path.join(destination_dir, "apktool.bat")
    apk_filename = os.path.splitext(os.path.basename(apk_file))[0]
    final_output_dir = os.path.join(output_dir, apk_filename)

    import subprocess
    try:
        # 使用 -f 参数强制覆盖目标目录
        command = [apktool_bat, "d", "-f", apk_file, "-o", final_output_dir]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(f"Resources of APK file {apk_file} have been successfully extracted to {final_output_dir}.")
        print("Extraction log information:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred during extraction: {e.stderr}")
    except Exception as e:
        print(f"An unknown error occurred: {e}")

# 检查 Android SDK 是否安装
def check_android_sdk_installed():
    android_home = os.getenv('ANDROID_HOME')
    if android_home and os.path.exists(android_home):
        sdkmanager_path = os.path.join(android_home, 'cmdline-tools', 'latest', 'bin', 'sdkmanager')
        if os.name == 'nt':
            sdkmanager_path += '.bat'
        return os.path.exists(sdkmanager_path)
    return False

# 安装 Android SDK
def install_android_sdk():
    # 定义 Android SDK 下载链接和安装目录
    sdkmanager_url = 'https://dl.google.com/android/repository/commandlinetools-win-9477386_latest.zip'
    sdk_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'Android', 'Sdk')
    temp_zip = os.path.join(os.getcwd(), 'cmdline-tools.zip')

    # 下载 sdkmanager
    print("Downloading Android SDK Command-line Tools...")
    download_file(sdkmanager_url, 'cmdline-tools.zip', os.getcwd())

    # 解压下载的文件
    print("Extracting Android SDK Command-line Tools...")
    if os.path.exists(temp_zip):
        with zipfile.ZipFile(temp_zip, 'r') as zip_ref:
            zip_ref.extractall(sdk_dir)
        print("Extraction completed.")
    else:
        print("Downloaded zip file not found.")
        return

    # 移动文件到正确的目录结构
    cmdline_tools_dir = os.path.join(sdk_dir, 'cmdline-tools')
    latest_dir = os.path.join(cmdline_tools_dir, 'latest')
    if not os.path.exists(latest_dir):
        os.makedirs(latest_dir)
    for item in os.listdir(cmdline_tools_dir):
        if item != 'latest':
            item_path = os.path.join(cmdline_tools_dir, item)
            new_path = os.path.join(latest_dir, item)
            if os.path.exists(item_path):
                if os.path.isfile(item_path):
                    if os.path.exists(new_path):
                        os.remove(new_path)
                    shutil.move(item_path, new_path)
                else:
                    for sub_item in os.listdir(item_path):
                        sub_item_path = os.path.join(item_path, sub_item)
                        new_sub_path = os.path.join(latest_dir, sub_item)
                        if os.path.exists(new_sub_path):
                            if os.path.isfile(new_sub_path):
                                os.remove(new_sub_path)
                            else:
                                shutil.rmtree(new_sub_path)
                        shutil.move(sub_item_path, new_sub_path)
                    if os.path.exists(item_path):
                        shutil.rmtree(item_path)

    # 检查 sdkmanager 路径是否存在
    sdkmanager_path = os.path.join(sdk_dir, 'cmdline-tools', 'latest', 'bin', 'sdkmanager')
    if os.name == 'nt':
        sdkmanager_path += '.bat'
    if not os.path.exists(sdkmanager_path):
        print(f"Error: sdkmanager not found at {sdkmanager_path}")
        print("Current cmdline-tools directory content:")
        for root, dirs, files in os.walk(cmdline_tools_dir):
            for name in files:
                print(os.path.join(root, name))
            for name in dirs:
                print(os.path.join(root, name))
        return

    # 检查并设置 JAVA_HOME
    java_home = os.getenv('JAVA_HOME')
    if not java_home:
        # 从命令行参数获取 JAVA_HOME
        import sys
        for i, arg in enumerate(sys.argv):
            if arg == '-j' or arg == '--java_home':
                if i + 1 < len(sys.argv):
                    java_home = sys.argv[i + 1]
                    os.environ['JAVA_HOME'] = java_home
                    break
        if not java_home:
            print("Error: JAVA_HOME is not set. Please set it using -j or --java_home option.")
            return

    # 安装必要的 SDK 组件
    components = [
        "platform-tools",
        "build-tools;33.0.2",
        "platforms;android-33"
    ]
    for component in components:
        print(f"Installing {component}...")
        try:
            subprocess.run([sdkmanager_path, component], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error installing {component}: {e}")

    # 设置 ANDROID_HOME 环境变量
    os.environ['ANDROID_HOME'] = sdk_dir
    print(f"ANDROID_HOME set to {sdk_dir}")

    # 清理临时文件
    if os.path.exists(temp_zip):
        os.remove(temp_zip)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract resources from an APK file using apktool')
    parser.add_argument('-f', '--file', required=True, help='Specify the path of the APK file')
    parser.add_argument('-o', '--output', required=True, help='Specify the output path for the extracted resources')
    parser.add_argument('-p', '--path', default=os.path.join(os.getenv('APPDATA'), 'apktool'),
                        help='Specify the location to download and store apktool')
    parser.add_argument('-u', '--urls', nargs=2, metavar=('JAR_URL', 'BAT_URL'),
                        help='Specify the download URLs for apktool.jar and apktool.bat')
    parser.add_argument('-j', '--java_home', default='C:\\Program Files\\Java\\jdk1.8.0_271',
                        help='Specify the JAVA_HOME path')
    parser.add_argument('--use-proxy', action='store_true', help='Use proxy for downloading')
    args = parser.parse_args()

    apk_file = args.file
    output_dir = args.output
    download_and_destination_dir = args.path
    java_home = args.java_home
    use_proxy = args.use_proxy

    default_jar_url = 'https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.6.1.jar'
    # 这里由于我们会生成 apktool.bat，不需要下载，所以可忽略该参数
    # default_bat_url = 'https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/windows/apktool.bat'

    jar_url = args.urls[0] if args.urls else default_jar_url
    # bat_url = args.urls[1] if args.urls else default_bat_url

    # 检查并安装 Android SDK
    if not check_android_sdk_installed():
        print("Android SDK not found. Installing...")
        try:
            install_android_sdk()
        except Exception as e:
            print(f"Failed to install Android SDK: {e}. Continuing with apktool extraction.")

    # 检查并处理 apktool
    if not check_apktool_exists(download_and_destination_dir):
        print("apktool not detected, starting download and generation...")
        download_dir = download_and_destination_dir
        jar_file = download_apktool_jar(download_dir, jar_url, use_proxy)
        if jar_file:
            generate_apktool_bat(download_dir, java_home)
            # 由于下载和目标目录相同，无需移动文件
            print("Files are already in the destination directory.")
    else:
        print("apktool detected, continuing with the extraction operation.")
        time.sleep(0.5)
        print("Processing, please wait...")

    extract_apk(apk_file, output_dir, download_and_destination_dir)