from tools3.compile.uc import UCGen
from tools3.compile import Compile
import json

"""
编译成json用例
"""
class CompileUC(Compile):
    step_name = "compile_uc"
    params = {}
    fields_formatters = {}
    expected = None
    include_field_names = False
    separator = "_"

    def __init__(self, params, fields_formatters, expected, include_field_names, separator):
        super().__init__()
        self.params = params
        self.fields_formatters = fields_formatters
        self.expected = expected
        self.include_field_names = include_field_names
        self.separator = separator

    def compile(self, compile_json_file_path) -> bool:
        self.get_logger().info(self.step_name + " compile start")
        try:
            uc_gen = UCGen(
                params=self.params,
                fields_formatters=self.fields_formatters,
                expected=self.expected,  # 传入动态生成函数
                include_field_names=self.include_field_names,
                separator=self.separator,
            )

            # 生成测试用例
            uc_gen.generate_cases()
            # 保存测试用例到 JSON 文件
            use_cases = uc_gen.get_use_cases()
            with open(compile_json_file_path, "w", encoding="utf-8") as fp:
                json.dump(use_cases, fp, ensure_ascii=False, indent=4)
        except Exception as e:
            self.get_logger().error(self.step_name + " compile error: {}".format(e))
            raise e
        self.get_logger().error(self.step_name + " compile end")
        return True