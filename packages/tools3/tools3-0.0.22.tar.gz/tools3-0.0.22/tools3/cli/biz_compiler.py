from .compiler import Compiler
from .func import get_output_file_path
import tempfile

from .. import get_file_without_ext


class BizCompiler(Compiler):

    def jc_phpunit(self, from_file, output_file):
        super().get_logger().info("jc_phpunit start")
        with tempfile.NamedTemporaryFile(suffix="") as temp_uc_file:
            temp_uc_file_name = temp_uc_file.name + ".uc.json"
            super().get_logger().info("temp_uc_file", data={"temp_uc_file_name": temp_uc_file_name})
            super().jc_uc(from_file, temp_uc_file_name)
            phpunit_output_file = get_output_file_path(from_file, output_file, ".phpunit")
            super().uc_phpunit(temp_uc_file_name, phpunit_output_file)

    # 以下方法没有测试
    def py_phpunit(self, from_file, output_file):
        super().get_logger().info("py_phpunit start")
        with tempfile.NamedTemporaryFile(suffix="", mode='w+', delete=False) as temp_uc_file:
            temp_uc_file_name = temp_uc_file.name + ".uc.json"
            super().get_logger().info("temp_uc_file", data={"temp_uc_file_name": temp_uc_file_name})
            super().py_uc(from_file, temp_uc_file_name)
            phpunit_output_file = get_output_file_path(from_file, output_file, ".phpunit")
            super().uc_phpunit(temp_uc_file_name, phpunit_output_file)
