import re

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
    #去除三引号(''''''和"""""")
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

remove_jing(r"D:\编程\txhyy\txhyy\txhyy\Image\jpeg.py",r"D:\编程\txhyy\txhyy\txhyy\Image\jpegs.py")