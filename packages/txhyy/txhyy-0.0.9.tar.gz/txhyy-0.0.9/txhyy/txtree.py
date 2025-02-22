import os
import argparse


def print_directory_tree(path, prefix='', is_root=True, is_last=True, output_file=None, error_list=None):
    if error_list is None:
        error_list = []

    if is_root:
        line = os.path.basename(path)
    else:
        marker = '└── ' if is_last else '├── '
        line = prefix + marker + os.path.basename(path)

    if output_file:
        output_file.write(line + '\n')
    else:
        print(line)

    if os.path.exists(path):
        if os.path.isdir(path):
            try:
                items = os.listdir(path)
                num_items = len(items)
                for index, item in enumerate(items):
                    item_path = os.path.join(path, item)
                    new_prefix = prefix + ('    ' if (is_last and not is_root) else '│   ')
                    is_last_item = (index == num_items - 1)
                    print_directory_tree(item_path, new_prefix, is_root=False, is_last=is_last_item, output_file=output_file, error_list=error_list)
            except PermissionError:
                error_msg = f"{prefix + ('    ' if (is_last and not is_root) else '│   ') + f'└── {os.path.basename(path)} (Permission denied)'}"
                error_list.append(error_msg)
            except FileNotFoundError:
                error_msg = f"{prefix + ('    ' if (is_last and not is_root) else '│   ') + f'└── {os.path.basename(path)} (Path not found)'}"
                error_list.append(error_msg)
    else:
        error_msg = f"{prefix + ('    ' if (is_root or is_last) else '│   ') + f'└── {os.path.basename(path)} (Path not found)'}"
        error_list.append(error_msg)

    return error_list


def main():
    parser = argparse.ArgumentParser(description='Generate directory tree.')
    parser.add_argument('-d', '--directory', type=str, required=True, help='Path to the directory.')
    parser.add_argument('-o', '--output', type=str, default=None, help='Output file path. If not provided, print to console.')
    args = parser.parse_args()

    directory = args.directory
    if not os.path.exists(directory):
        print(f"Directory {directory} does not exist.")
        return

    error_list = []
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as output_file:
                error_list = print_directory_tree(directory, output_file=output_file, error_list=error_list)
        except Exception as e:
            print(f"Error writing to file: {e}")
    else:
        error_list = print_directory_tree(directory, error_list=error_list)

    if error_list:
        print("\nErrors encountered during traversal:")
        for error in error_list:
            print(error)


if __name__ == "__main__":
    main()