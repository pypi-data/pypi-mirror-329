from tools3.compile.config import ParamsJsonConfig
from tools3.compile import Compile
from tools3.compile.uc import CompileUC
import json

"""
编译成json用例
"""
class JsonConfigCompileUC(Compile):
    step_name = "json_config_compile_uc"
    params = {}
    fields_formatters = {}
    expected = None
    include_field_names = False
    separator = "_"

    json_file_path = ""

    def __init__(self, json_file_path):
        super().__init__()
        self.json_file_path = json_file_path

    def get_json_file_path(self):
        return self.json_file_path

    def compile(self, compile_json_file_path) -> bool:
        self.get_logger().info(self.step_name + " compile start")
        try:
            json_config_file_path = self.get_json_file_path()
            params_config = ParamsJsonConfig.new_instance(json_config_file_path)
            fields = params_config.convert_to_fields_params()
            formatter = params_config.convert_to_fields_formatters()
            expected = params_config.get_expected()

            uc = CompileUC(
                params=fields,
                fields_formatters=formatter,
                expected=expected,
                include_field_names=params_config.get_include_field_names(),
                separator=params_config.get_separator(),
            )
            uc.set_base_logger(self.get_base_logger())
            result = uc.compile(compile_json_file_path)
        except Exception as e:
            self.get_logger().error(self.step_name + " compile error: {}".format(e))
            raise e
        self.get_logger().info(self.step_name + " compile end")
        return result