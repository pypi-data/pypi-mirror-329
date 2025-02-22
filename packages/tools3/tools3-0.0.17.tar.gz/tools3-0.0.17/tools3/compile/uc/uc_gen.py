import json
from itertools import product
from collections import OrderedDict

class UCGen:
    def __init__(self, params, fields_formatters, expected, include_field_names=False, separator="_"):
        """
        初始化 ParamsGenerator
        :param params: 参数字典，定义参数及其取值范围
        :param fields_formatters: 参数值格式化规则
        :param expected: 预期结果，可以是固定值或动态生成函数
        :param include_field_names: 是否在测试用例名称中包含字段名
        """
        self.params = OrderedDict(params)
        self.fields_formatters = fields_formatters
        self.expected = expected
        self.include_field_names = include_field_names
        self.separator = separator
        self.use_cases = []

    @staticmethod
    def default_formatter(value):
        """
        默认的格式化规则
        :param value: 需要格式化的值
        :return: 格式化后的字符串
        """
        return str(value)

    def generate_case_name(self, case_data, include_field_names=True, case_number=""):
        """
        根据 case 数据和格式化规则生成可读的 case 名称
        :param case_data: 测试用例数据字典（key-value 对）
        :param include_field_names: 是否在名称中包含字段名
        :return: 可读的 case 名称
        """
        case_name_parts = []
        if case_number != "":
            case_name_parts.append(case_number)
        for param, value in case_data.items():
            # 获取当前参数的格式化规则
            formatter_config = self.fields_formatters.get(param, {})

            # 根据配置应用格式化规则
            if isinstance(formatter_config, dict):
                # 如果配置中有 values 映射，优先使用映射
                if "values" in formatter_config and value in formatter_config["values"]:
                    value_str = formatter_config["values"][value]
                else:
                    # 如果没有 values 映射，使用默认格式化规则
                    value_str = self.default_formatter(value)

                # 如果配置中有 format 规则，应用 format 规则
                if "format" in formatter_config:
                    if formatter_config["format"] == "replace_dot":
                        value_str = value_str.replace(".", "_")
                    elif formatter_config["format"] == "default":
                        # 默认情况下，直接使用 value_str
                        pass
            else:
                # 如果 formatter_config 不是字典，直接使用默认规则
                value_str = self.default_formatter(value)

            # 根据 include_field_names 决定是否包含字段名
            if include_field_names:
                case_name_parts.append(f"{param}{self.separator}{value_str}")
            else:
                case_name_parts.append(value_str)
        return self.separator.join(case_name_parts)

    def generate_cases(self):
        """
        生成所有参数组合并构造测试用例
        """
        # 测试用例编号
        case_number = 0
        for pairs in product(*self.params.values()):
            case_number += 1
            # 构建 case 字典
            case = {param: value for param, value in zip(self.params.keys(), pairs)}

            # 生成可读的 case_name（包含字段名）
            case_name_with_fields = self.generate_case_name(case, self.include_field_names, str(case_number))

            # 动态生成预期结果
            if callable(self.expected):
                expected = self.expected(case)  # 如果 expected 是函数，动态生成
            else:
                expected = self.expected  # 否则使用固定值

            # 构建测试用例字典（包含字段名）
            case_with_fields = {
                "case": case_name_with_fields,
                "data": case,
                "expected": expected
            }

            # 将生成的测试用例添加到列表中
            self.use_cases.append(case_with_fields)

    def get_use_cases(self):
        """
        获取生成的测试用例列表
        :return: 测试用例列表
        """
        return self.use_cases

    def save_to_json(self, output_file):
        """
        将测试用例保存到 JSON 文件
        :param output_file: 输出文件名
        """
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(self.use_cases, f, ensure_ascii=False, indent=4)
        print(f"测试用例已经生成并保存到 {output_file}")