from tools3.compile import Compile
from tools3.compile.config import ParamsJsonConfig

"""
json 配置编译成 python 模板
"""
class JsonConfigCompilePy(Compile):
    json_file_path = ""
    def __init__(self, json_file_path):
        self.json_file_path = json_file_path

    def get_json_file_path(self):
        return self.json_file_path

    def compile(self, compile_py_file_path) -> bool:
        """
        编译json文件为python文件
        :param compile_py_file_path:
        :return bool:
        """
        json_file_path = self.get_json_file_path()
        params_json_config = ParamsJsonConfig.new_instance(json_file_path)
        fields = params_json_config.convert_to_fields_params()
        formatter = params_json_config.convert_to_fields_formatters()
        expected = params_json_config.get_expected()
        # params_json_config 转python 文件
        py_template = f"""
from tools3 import generate_test_params_json,generate_test_params_to_php_data_provider

# 定义参数
params = {fields}

# 用户自定义参数值格式化规则
value_formatters = {formatter}


# 定义预期结果（可以是固定值或动态生成函数）
def dynamic_expected(case_data):
    return {expected}

# 生成测试用例
generate_test_params_to_php_data_provider(
    params=params,
    value_formatters=value_formatters,
    expected=dynamic_expected,  # 传入动态生成函数
    include_field_names=False,
    separator="_",
)
"""
        with open(compile_py_file_path, "w") as py_file:
            py_file.write(py_template)
        return True