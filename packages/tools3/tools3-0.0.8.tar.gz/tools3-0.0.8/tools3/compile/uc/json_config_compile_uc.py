from tools3.compile.config import ParamsJsonConfig
from tools3.compile import Compile
from tools3.compile.uc import CompileUC
import json

"""
编译成json用例
"""
class JsonConfigCompileUC(Compile):
    params = {}
    fields_formatters = {}
    expected = None
    include_field_names = False
    separator = "_"

    json_file_path = ""

    def __init__(self, json_file_path):
        self.json_file_path = json_file_path

    def get_json_file_path(self):
        return self.json_file_path

    def compile(self, compile_json_file_path) -> bool:
        json_config_file_path = self.get_json_file_path()
        params_config = ParamsJsonConfig.new_instance(json_config_file_path)
        fields = params_config.convert_to_fields_params()
        formatter = params_config.convert_to_fields_formatters()
        expected = params_config.get_expected()

        compile_use_cases = CompileUC(
            params=fields,
            fields_formatters=formatter,
            expected=expected,
            include_field_names=params_config.get_include_field_names(),
            separator=params_config.get_separator(),
        )
        return compile_use_cases.compile(compile_json_file_path)