import errno

from tools3 import get_file_absolute_path, check_path_is_file, get_file_without_ext, get_file_name, \
    get_file_ext, BaseObj
from tools3.compile.py import JsonConfigCompilePy
from tools3.compile.uc import JsonConfigCompileUC
from tools3.compile.utc import UCCompilePhpUnit
from tools3.compile.uc import CompileUC
from tools3.compile.uc import PyCompileUC
from .func import get_output_file_path, file_exists_error, raise_output_file_exists_error,raise_from_file_not_exists_error, check_path_is_dir
import os
import logging

class Compiler(BaseObj):
    def __init__(self):
        super().__init__()

    def jc_py(self, from_file, output_file):
        from_file_new = get_file_absolute_path(from_file)
        self.get_logger().info("start", data={
            "from_file": from_file,
            'from_file_new': from_file_new,
            "output_file": output_file,
        })
        from_file = from_file_new
        raise_from_file_not_exists_error(from_file)
        output_file = get_output_file_path(from_file, output_file, ".py")
        self.get_logger().info("start2", data={
            "from_file": from_file,
            "output_file": output_file,
        })
        raise_output_file_exists_error(output_file)
        c = JsonConfigCompilePy(from_file)
        c.set_base_logger(self.get_base_logger())
        c.compile(output_file)
        self.get_logger().info("end")

    def jc_uc(self, from_file, output_file):
        try:
            from_file_new = get_file_absolute_path(from_file)
            self.get_logger().info("start", data={
                "from_file": from_file,
                'from_file_new': from_file_new,
                "output_file": output_file,
            })
            from_file = from_file_new
            raise_from_file_not_exists_error(from_file)
            output_file = get_output_file_path(from_file, output_file, ".uc.json")
            self.get_logger().info("start2", data={
                "from_file": from_file,
                "output_file": output_file,
            })
            raise_output_file_exists_error(output_file)
            c = JsonConfigCompileUC(from_file)
            c.set_base_logger(self.get_base_logger())
            c.compile(output_file)
            self.get_logger().info("end")
        except Exception as e:
            self.get_logger().exception(e)
            raise e

    def py_uc(self, from_file, output_file):
        try:
            from_file_new = get_file_absolute_path(from_file)
            self.get_logger().info("start", data={
                "from_file": from_file,
                'from_file_new': from_file_new,
                "output_file": output_file,
            })
            from_file = from_file_new
            raise_from_file_not_exists_error(from_file)
            output_file = get_output_file_path(from_file, output_file, ".uc.json")
            self.get_logger().info("start2", data={
                "from_file": from_file,
                "output_file": output_file,
            })
            raise_output_file_exists_error(output_file)
            uc = PyCompileUC()
            uc.compile(from_file)
            self.get_logger().info("end")
        except Exception as e:
            self.get_logger().exception(e)
            raise e

    def uc_phpunit(self, from_file, output_file):
        try:
            from_file_new = get_file_absolute_path(from_file)
            self.get_logger().info("start", data={
                "from_file": from_file,
                'from_file_new': from_file_new,
                "output_file": output_file,
                "exist": os.path.exists(from_file_new)
            })
            from_file = from_file_new
            raise_from_file_not_exists_error(from_file)
            utc = UCCompilePhpUnit()
            output_file = get_output_file_path(from_file, output_file, ".phpunit")
            self.get_logger().info("start2", data={
                "from_file": from_file,
                "output_file": output_file,
            })
            raise_output_file_exists_error(output_file)
            utc.compile(from_file, output_file)
            self.get_logger().info("end")
        except Exception as e:
            self.get_logger().exception(e)
            raise e