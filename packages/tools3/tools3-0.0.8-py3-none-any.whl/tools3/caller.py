import os
import inspect

class Caller(object):

    @staticmethod
    def get_caller_filepath(new_extension=None, include_filename=True, absolute=True, level=1):
        """
        获取调用者的文件路径，并支持替换扩展名。

        :param new_extension: 新的扩展名（如 ".custom"），默认为 None。
        :param include_filename: 是否包含文件名，默认为 True。
        :param absolute: 是否返回绝对路径，默认为 True。
        :param level: 需要获取的调用层级（1 表示直接调用者，2 表示上上层，依此类推）。
        :return: 调用者的文件路径。
        """
        try:
            stack = inspect.stack()
            # 获取当前帧的上一级帧（即调用此函数的代码的上下文）
            if len(stack) <= level:
                return None  # 调用层级超出范围

            caller_frame = stack[level]  # 获取指定层级的调用帧
            # 获取文件路径
            caller_file_path = caller_frame.filename  # 获取文件路径

            # 如果需要绝对路径
            if absolute:
                caller_file_path = os.path.abspath(caller_file_path)

            # 如果不需要文件名，仅返回目录路径
            if not include_filename:
                return os.path.dirname(caller_file_path)

            # 如果需要替换扩展名
            if new_extension:
                # 分离文件目录和文件名
                directory, filename = os.path.split(caller_file_path)
                # 获取文件名，不带扩展名
                name_without_extension, _ = os.path.splitext(filename)
                # 组合新文件名
                new_filename = f"{name_without_extension}{new_extension}"
                # 重新构建文件路径
                caller_file_path = os.path.join(directory, new_filename)

            return caller_file_path
        except Exception as e:
            print(f"Error occurred while getting caller file path: {e}")
            return None


