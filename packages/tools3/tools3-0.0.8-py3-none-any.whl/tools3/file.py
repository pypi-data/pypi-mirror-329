import os

PATH_TYPE_IS_FILE = 1
PATH_TYPE_IS_DIR = 2

def get_file_absolute_path(path):
    # 如果是绝对路径，直接返回
    if os.path.isabs(path):
        return path
    else:
        # 如果是相对路径，转换为绝对路径
        return os.path.abspath(path)


def check_path_type(path):
    # 判断路径是否存在
    if not os.path.exists(path):
        return 0
    # 判断路径是文件还是目录
    if os.path.isfile(path):
        return PATH_TYPE_IS_FILE
    elif os.path.isdir(path):
        return PATH_TYPE_IS_DIR
    else:
        return 0

def check_path_is_file(path):
    return check_path_type(path) == PATH_TYPE_IS_FILE

def check_path_is_dir(path):
    return check_path_type(path) == PATH_TYPE_IS_DIR

# 给定一个文件获取文件名
def get_file_name(file_path):
    return os.path.basename(file_path)

# 给定一个文件名获取目录路径
def get_file_dir(file_path):
    return os.path.dirname(file_path)

def get_file_ext(file_path):
    return os.path.splitext(file_path)[1]

def get_file_without_ext(file_path):
    return os.path.splitext(file_path)[0]