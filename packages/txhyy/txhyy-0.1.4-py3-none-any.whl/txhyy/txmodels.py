import argparse
import requests
import tarfile
import os
import shutil
from tqdm.rich import tqdm
from colorama import init, Fore
from packaging import version

# 初始化 colorama
init(autoreset=True)


def download_file(url, filename):
    """
    Download the file and display a colored progress bar using tqdm.rich
    """
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024

    with open(filename, 'wb') as file, tqdm(
            desc=f"Downloading {filename}",
            total=total_size,
            unit='iB',
            unit_scale=True,
    ) as progress_bar:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)


def remove_extra_files(directory):
    """
    Remove extra files and directories, such as PKG-INFO and directories ending with .egg-info
    """
    for root, dirs, files in os.walk(directory):
        # Remove PKG-INFO files
        for file in files:
            if file == 'PKG-INFO':
                file_path = os.path.join(root, file)
                os.remove(file_path)
        # Remove directories ending with .egg-info
        for dir in dirs[:]:
            if dir.endswith('.egg-info'):
                dir_path = os.path.join(root, dir)
                shutil.rmtree(dir_path)
                dirs.remove(dir)


def main():
    parser = argparse.ArgumentParser(description='Download and extract Python module source files from PyPI')
    parser.add_argument('-o', '--output', help='Specify the output directory for extraction', default='.')
    parser.add_argument('-m', '--module', help='Specify the module to download', required=True)
    parser.add_argument('-v', '--version', help='Specify the module version', default=None)
    parser.add_argument('-whl', action='store_true', help='Download the .whl file instead of the source distribution')
    parser.add_argument('-gzwhl', action='store_true', help='Download both .whl and .tar.gz files')

    args = parser.parse_args()

    module_name = args.module
    version_str = args.version
    output_dir = args.output
    download_whl = args.whl
    download_gzwhl = args.gzwhl

    if download_whl and download_gzwhl:
        print(Fore.YELLOW + "You have specified both -whl and -gzwhl. The script will follow the -gzwhl logic "
                            "and download both .whl and .tar.gz files.")

    print(f"Checking module: {module_name}...")

    # Build the PyPI API URL
    if version_str:
        print(f"Checking version number: {version_str}...")
        pypi_url = f'https://pypi.org/pypi/{module_name}/{version_str}/json'
    else:
        print("Checking the latest version number...")
        pypi_url = f'https://pypi.org/pypi/{module_name}/json'

    # Get PyPI metadata
    response = requests.get(pypi_url)
    print(f"Request URL: {pypi_url}")
    print(f"Response status code: {response.status_code}")
    if response.status_code != 200:
        print(Fore.RED + f"Failed to get metadata for {module_name}. Status code: {response.status_code}")
        print(Fore.RED + f"Response text: {response.text}")
        return

    try:
        data = response.json()
        print(f"Full data received from PyPI: {data}")
    except ValueError:
        print(Fore.RED + f"Failed to parse JSON data from response. Response text: {response.text}")
        return

    if version_str:
        release_files = data.get('urls', [])
    else:
        # Use the packaging library to get the latest version
        releases = data.get('releases', {})
        sorted_versions = sorted(releases.keys(), key=lambda v: version.Version(v))
        latest_version = sorted_versions[-1]
        print(f"The latest version of {module_name} is {latest_version}.")
        release_files = releases.get(latest_version, [])

    if download_gzwhl:
        # 查找 .whl 文件
        whl_file = next((f for f in release_files if f['packagetype'] == 'bdist_wheel'), None)
        if not whl_file:
            print(Fore.RED + f"No .whl distribution found for {module_name}")
        else:
            whl_download_url = whl_file['url']
            whl_filename = whl_file['filename']
            download_file(whl_download_url, whl_filename)
            print(Fore.GREEN + f"Successfully downloaded {whl_filename} to {output_dir}")

        # 查找 .tar.gz 文件
        gz_file = next((f for f in release_files if f['packagetype'] == 'sdist'), None)
        if not gz_file:
            print(Fore.RED + f"No source distribution found for {module_name}")
        else:
            gz_download_url = gz_file['url']
            gz_filename = gz_file['filename']
            download_file(gz_download_url, gz_filename)

            # 提取 .tar.gz 文件
            with tarfile.open(gz_filename, 'r:gz') as tar:
                tar.extractall(path=output_dir)

            # 移除多余文件和目录
            extracted_dir = os.path.join(output_dir, os.path.splitext(os.path.splitext(gz_filename)[0])[0])
            remove_extra_files(extracted_dir)

            # 清理临时文件
            os.remove(gz_filename)

            # 获取解压后的文件夹名
            extracted_folder_name = os.path.basename(extracted_dir)
            print(Fore.GREEN + f"Successfully downloaded and extracted {module_name} to {output_dir}. "
                               f"The extracted folder name is: {extracted_folder_name}")
    elif download_whl:
        target_file = next((f for f in release_files if f['packagetype'] == 'bdist_wheel'), None)
        if not target_file:
            print(Fore.RED + f"No .whl distribution found for {module_name}")
            return
        download_url = target_file['url']
        filename = target_file['filename']
        download_file(download_url, filename)
        print(Fore.GREEN + f"Successfully downloaded {filename} to {output_dir}")
    else:
        target_file = next((f for f in release_files if f['packagetype'] == 'sdist'), None)
        if not target_file:
            print(Fore.RED + f"No source distribution found for {module_name}")
            return
        download_url = target_file['url']
        filename = target_file['filename']
        download_file(download_url, filename)

        # 提取文件
        with tarfile.open(filename, 'r:gz') as tar:
            tar.extractall(path=output_dir)

        # 移除多余文件和目录
        extracted_dir = os.path.join(output_dir, os.path.splitext(os.path.splitext(filename)[0])[0])
        remove_extra_files(extracted_dir)

        # 清理临时文件
        os.remove(filename)

        # 获取解压后的文件夹名
        extracted_folder_name = os.path.basename(extracted_dir)
        print(Fore.GREEN + f"Successfully downloaded and extracted {module_name} to {output_dir}. "
                           f"The extracted folder name is: {extracted_folder_name}")


if __name__ == "__main__":
    main()