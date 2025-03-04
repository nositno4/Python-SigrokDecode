import os
import shutil

# 这个脚本干了什么?
# 遍历decoders目录下的所有子文件夹，将其中的pd.py文件复制到doc目录并重命名为[子文件夹名].txt
# 对doc目录下的所有.txt文件进行处理，删除文件开头的注释和空行，仅保留有效代码内容

# 获取当前脚本的绝对路径
script_path = os.path.abspath(__file__)

# 设置基础路径（脚本所在目录）
base_dir = os.path.dirname(script_path)

# 定义源目录和目标目录（相对路径）
source_dir = os.path.join(base_dir, 'bak')       # 需要处理的文件夹所在目录
target_dir = os.path.join(base_dir, 'doc')       # 目标目录

def process_files(source_dir=source_dir, target_dir=target_dir):
    # 创建目标目录（如果不存在）
    os.makedirs(target_dir, exist_ok=True)
    
    # 遍历源目录下的所有子文件夹
    for folder_name in os.listdir(source_dir):
        folder_path = os.path.join(source_dir, folder_name)
        
        # 确保处理的是文件夹
        if os.path.isdir(folder_path):
            pd_file = os.path.join(folder_path, 'pd.py')
            
            if os.path.exists(pd_file):
                # 生成新文件名
                new_filename = f"py_{folder_name}.txt"
                target_path = os.path.join(target_dir, new_filename)
                
                # 移动并重命名文件
                shutil.copy(pd_file, target_path)
                print(f"已处理：{folder_name} -> {new_filename}")
            else:
                print(f"警告：{folder_path} 中没有找到 pd.py 文件")

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 寻找第一个非注释/非空行的索引
    start_index = 0
    for i, line in enumerate(lines):
        stripped_line = line.lstrip()  # 忽略前导空格
        # 判断是否为注释行或空行
        if stripped_line.startswith('#') or stripped_line.strip() == '':
            continue
        else:
            start_index = i
            break
    else:  # 整个文件都是注释或空行
        start_index = len(lines)

    # 保留从第一个代码行开始的内容
    new_content = lines[start_index:]
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_content)

def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                process_file(file_path)
                print(f"已处理：{file_path}")

if __name__ == '__main__':
    process_files(source_dir, target_dir)
    process_directory(target_dir)
