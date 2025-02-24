import os

def create_structure_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    base_path = os.getcwd()  # 当前工作目录
    stack = []  # 用于记录目录层级

    for line in lines:
        line = line.rstrip()  # 去掉行尾的换行符和空格
        if not line:
            continue  # 忽略空行

        # 计算缩进层级
        indent_level = 0
        while line.startswith('│   ') or line.startswith('    '):
            indent_level += 1
            line = line[4:]

        # 根据缩进层级调整当前路径
        while len(stack) > indent_level:
            stack.pop()

        # 获取当前路径
        current_path = os.path.join(base_path, *stack)

        if line.startswith('├── ') or line.startswith('└── '):
            # 处理文件或目录
            name = line[4:].split('#')[0].strip()  # 去掉注释部分
            if name.endswith('/'):
                # 创建目录
                dir_name = name[:-1]
                dir_path = os.path.join(current_path, dir_name)
                os.makedirs(dir_path, exist_ok=True)
                stack.append(dir_name)  # 将目录加入栈
            else:
                # 创建文件
                file_path = os.path.join(current_path, name)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)  # 确保父目录存在
                with open(file_path, 'w', encoding='utf-8') as f:
                    pass  # 创建空文件

        elif line.startswith('├──') or line.startswith('└──'):
            # 处理没有空格的文件或目录
            name = line[3:].split('#')[0].strip()
            if name.endswith('/'):
                # 创建目录
                dir_name = name[:-1]
                dir_path = os.path.join(current_path, dir_name)
                os.makedirs(dir_path, exist_ok=True)
                stack.append(dir_name)
            else:
                # 创建文件
                file_path = os.path.join(current_path, name)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)  # 确保父目录存在
                with open(file_path, 'w', encoding='utf-8') as f:
                    pass  # 创建空文件

def main():
    import argparse
    parser = argparse.ArgumentParser(description="根据文件描述创建目录结构")
    parser.add_argument('file', type=str, help="包含目录结构的文件路径")
    args = parser.parse_args()

    create_structure_from_file(args.file)
    print("目录结构已成功创建！")

if __name__ == "__main__":
    main()