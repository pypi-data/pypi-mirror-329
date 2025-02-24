import ast
import argparse
import os


def generate_pyi(file_path, output_dir):
    # 读取 Python 文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        source_code = file.read()

    # 解析代码为抽象语法树
    tree = ast.parse(source_code)

    # 为 AST 节点添加 parent 属性
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            child.parent = node

    # 存储生成的 pyi 内容
    pyi_content = []

    # 存储导入语句
    import_statements = []

    # 处理导入语句
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            module = node.module
            for name in node.names:
                alias = name.asname if name.asname else name.name
                import_statements.append(f"from {module} import {name.name} as {alias}")
        elif isinstance(node, ast.Import):
            for name in node.names:
                alias = name.asname if name.asname else name.name
                import_statements.append(f"import {name.name} as {alias}")

    # 添加导入语句到 pyi 内容
    pyi_content.extend(import_statements)
    pyi_content.extend([
        "from typing import *",
        "from types import *",
        ""
    ])

    # 用于记录已经处理过的类
    processed_classes = set()

    # 遍历抽象语法树节点
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # 处理函数定义
            print("Processing function definitions...")
            function_name = node.name
            args = []
            for arg in node.args.args:
                arg_name = arg.arg
                if arg.annotation:
                    if isinstance(arg.annotation, ast.Name):
                        if arg.annotation.id in ('int', 'str'):
                            arg_str = f"{arg_name}: {arg.annotation.id}"
                        else:
                            arg_str = arg_name
                    else:
                        arg_str = arg_name
                else:
                    arg_str = arg_name
                args.append(arg_str)
            args_str = ', '.join(args)

            # 检查函数体中是否有 return 语句以及 return 后面是否有值
            print("Processing return statement...")
            return_type = get_return_type(node)

            if hasattr(node, 'parent') and isinstance(node.parent, ast.ClassDef):
                # 类中的方法
                class_name = node.parent.name
                if class_name not in processed_classes:
                    pyi_content.append(f"class {class_name}:")
                    processed_classes.add(class_name)
                pyi_content.append(f"    def {function_name}({args_str}) -> {return_type} : ...")
            else:
                # 全局函数
                pyi_content.append(f"def {function_name}({args_str}) -> {return_type} : ...")
        elif isinstance(node, ast.ClassDef):
            print("Processing class...")
            class_name = node.name
            methods = [sub_node for sub_node in node.body if isinstance(sub_node, ast.FunctionDef)]
            if len(methods) == 1 and methods[0].name == '__init__':
                pyi_content.append(f"class {class_name}: ...")
            elif methods:
                if class_name not in processed_classes:
                    pyi_content.append(f"class {class_name}:")
                    processed_classes.add(class_name)
                for method in methods:
                    method_name = method.name
                    args = []
                    for arg in method.args.args:
                        arg_name = arg.arg
                        if arg.annotation:
                            if isinstance(arg.annotation, ast.Name):
                                if arg.annotation.id in ('int', 'str'):
                                    arg_str = f"{arg_name}: {arg.annotation.id}"
                                else:
                                    arg_str = arg_name
                            else:
                                arg_str = arg_name
                        else:
                            arg_str = arg_name
                        args.append(arg_str)
                    args_str = ', '.join(args)
                    return_type = get_return_type(method)
                    pyi_content.append(f"    def {method_name}({args_str}) -> {return_type} : ...")

    # 生成 pyi 文件路径
    file_name = os.path.basename(file_path)
    pyi_file_name = file_name.replace('.py', '.pyi')
    print("正在完成代码的生成...")
    pyi_file_path = os.path.join(output_dir, pyi_file_name)

    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 保存 pyi 文件
    with open(pyi_file_path, 'w', encoding='utf-8') as pyi_file:
        pyi_file.write('\n'.join(pyi_content))

    print(f"Generated PYI path: {pyi_file_path}")


def get_return_type(node):
    for stmt in node.body:
        if isinstance(stmt, ast.Return):
            if stmt.value is None:
                return 'None'
            else:
                return_type_annotation = getattr(node, 'returns', None)
                if return_type_annotation and isinstance(return_type_annotation, ast.Name):
                    if return_type_annotation.id in ('int', 'str'):
                        return return_type_annotation.id
                return '...'
    return 'None'


def process_directory(dir_path, output_dir):
    for root, _, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, dir_path)
                output_sub_dir = os.path.join(output_dir, relative_path)
                generate_pyi(file_path, output_sub_dir)


def main():
    parser = argparse.ArgumentParser(description='Generate .pyi files for Python code.')
    parser.add_argument('-o', '--output', default='txhyy-output', help='Specify the output directory for .pyi files (default: txhyy-output in the current directory)')
    parser.add_argument('-f', '--file', help='Specify the path of the Python file to generate .pyi for')
    parser.add_argument('-p', '--path', help='Specify the path of the directory containing Python files to generate .pyi for')

    args = parser.parse_args()

    if args.file:
        generate_pyi(args.file, args.output)
    elif args.path:
        process_directory(args.path, args.output)
    else:
        print("Please specify either a file (-f) or a directory (-p) to generate .pyi for.")


if __name__ == "__main__":
    main()