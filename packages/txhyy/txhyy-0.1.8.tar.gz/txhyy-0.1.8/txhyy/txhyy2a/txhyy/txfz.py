import argparse
import importlib.util
import sys
import builtins


def print_class_tree(cls, level=0, is_last=False, prefix="", branch_extend=False):
    # 构建当前行的前缀
    if level > 0:
        if is_last:
            new_prefix = prefix + "    "
            line = prefix + "└── "
        else:
            new_prefix = prefix + "│   "
            line = prefix + "├── "
    else:
        new_prefix = ""
        line = ""
    # 打印当前类名
    output = line + cls.__name__
    if branch_extend:
        if level > 0:
            output = prefix.rstrip() + "│\n" + output
    print(output)

    # 获取当前类的所有子类
    subclasses = cls.__subclasses__()
    num_subclasses = len(subclasses)

    for i, subclass in enumerate(subclasses):
        # 判断是否为最后一个子类
        is_last_subclass = (i == num_subclasses - 1)

        # 当根类有子类时打印分隔符 |
        if level == 0 and i == 0 and subclasses:
            print("|")

        next_branch_extend = branch_extend or cls.__name__ == "TestError"
        print_class_tree(subclass, level + 1, is_last_subclass, new_prefix, next_branch_extend)


def main():
    parser = argparse.ArgumentParser(description='Generate class inheritance tree from a Python file.')
    parser.add_argument('-f', '--file', type=str, required=True, help='Path to the Python file. Use "." to search in the current interpreter.')
    parser.add_argument('-u', '--class-name', type=str, required=True, help='Name of the exception class in the file.')
    parser.add_argument('-p', '--output', type=str, default=None, help='Output file path. If not provided, print to console.')

    args = parser.parse_args()

    if args.file == ".":
        # 先尝试在当前全局命名空间中查找类
        target_class = globals().get(args.class_name)
        if target_class is None:
            # 若未找到，尝试从 builtins 模块中查找
            target_class = getattr(builtins, args.class_name, None)
        if target_class is None:
            print(f"Class {args.class_name} not found in the current interpreter or builtins.", file=sys.stderr)
            sys.exit(1)
    else:
        # 加载指定文件中的模块
        spec = importlib.util.spec_from_file_location("module.name", args.file)
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
        except FileNotFoundError:
            print(f"File {args.file} not found.", file=sys.stderr)
            sys.exit(1)

        # 获取指定的异常类
        try:
            target_class = getattr(module, args.class_name)
        except AttributeError:
            print(f"Class {args.class_name} not found in {args.file}.", file=sys.stderr)
            sys.exit(1)

    if args.output:
        # 如果指定了输出文件，将标准输出重定向到文件
        original_stdout = sys.stdout
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                sys.stdout = f
                print_class_tree(target_class)
        except Exception as e:
            print(f"Error writing to file: {e}", file=sys.stderr)
        finally:
            sys.stdout = original_stdout
    else:
        # 未指定输出文件，直接打印到控制台
        print_class_tree(target_class)


if __name__ == "__main__":
    main()