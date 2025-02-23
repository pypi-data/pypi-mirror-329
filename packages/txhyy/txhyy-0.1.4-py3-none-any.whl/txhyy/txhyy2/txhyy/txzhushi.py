import re
import os
import sys
import argparse

def remove_jing(input_file_path, output_file_path):
    """去除#号"""
    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        new_lines = []
        for line in lines:
            stripped_line = line.lstrip()
            if not stripped_line.startswith('#'):
                line = re.sub(r'\s*#.*$', '', line)
                if line.strip():
                    new_lines.append(line)

        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.writelines(new_lines)

    except FileNotFoundError:
        print(f"文件 {input_file_path} 未找到。")


def remove_ying(file_path):
    # 去除三引号(''''''和"""""")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # 去除三引号注释块
        triple_quote_pattern = r'("""[\s\S]*?""")|(\'\'\'[\s\S]*?\'\'\')'
        content = re.sub(triple_quote_pattern, '', content)

        # 去除纯注释行和行内注释
        lines = content.splitlines()
        new_lines = []
        for line in lines:
            stripped_line = line.lstrip()
            if not stripped_line.startswith('#'):
                line = re.sub(r'\s*#.*$', '', line)
                if line.strip():
                    new_lines.append(line)

        new_content = '\n'.join(new_lines)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)

        print(f"已成功处理文件 {file_path}，去除注释和三引号注释块。")
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到。")


def main():
    parser = argparse.ArgumentParser(description="处理文件，去除注释和三引号注释块")
    parser.add_argument('-i', '--input', help="输入文件路径")
    parser.add_argument('-o', '--output', help="输出文件路径")

    args = parser.parse_args()

    input_file_path = args.input
    output_file_path = args.output

    if not input_file_path:
        print("请提供输入文件路径")
        sys.exit(1)

    if not output_file_path:
        # 如果没有 -o 参数，在当前文件夹创建一个 'txhyy-output' 文件夹
        output_dir = os.path.join(os.getcwd(), 'txhyy-output')
        os.makedirs(output_dir, exist_ok=True)
        file_name = os.path.basename(input_file_path)
        output_file_path = os.path.join(output_dir, file_name)
    elif input_file_path == output_file_path and not args.i:
        # 如果没有 -i 参数且输入输出路径相同，不覆盖源文件
        print("没有指定 -i 参数，不覆盖源文件。")
        sys.exit(1)

    remove_jing(input_file_path, output_file_path)
    remove_ying(output_file_path)


if __name__ == "__main__":
    main()