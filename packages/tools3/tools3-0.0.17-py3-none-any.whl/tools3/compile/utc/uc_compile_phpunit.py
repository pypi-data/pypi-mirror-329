from tools3.compile.utc import UCCompileUTC

def json_to_php_array(obj, indent=0):
    """
    将Python/JSON对象转换为PHP数组语法字符串,使用方括号语法

    参数:
        obj: Python对象(dict, list, str, int, float, bool, None)
        indent: 缩进级别(默认为0)

    返回:
        str: PHP数组语法的字符串
    """
    # 缩进字符串
    indent_str = "    " * indent

    # 处理None
    if obj is None:
        return "null"

    # 处理布尔值
    if isinstance(obj, bool):
        return "true" if obj else "false"

    # 处理数字
    if isinstance(obj, (int, float)):
        return str(obj)

    # 处理字符串
    if isinstance(obj, str):
        return f"'{obj}'"  # 使用单引号包裹字符串

    # 处理列表/数组
    if isinstance(obj, list):
        if not obj:  # 空列表
            return "[]"
        items = [f"{indent_str}    {json_to_php_array(item, indent + 1)}" for item in obj]
        return "[\n" + ",\n".join(items) + "\n" + indent_str + "]"

    # 处理字典/对象
    if isinstance(obj, dict):
        if not obj:  # 空字典
            return "[]"
        items = [f"{indent_str}    '{key}' => {json_to_php_array(value, indent + 1)}"
                for key, value in obj.items()]
        return "[\n" + ",\n".join(items) + "\n" + indent_str + "]"

    raise TypeError(f"Unsupported type: {type(obj)}")

class UCCompilePhpUnit(UCCompileUTC):
    def compile(self, from_uc_file_path, to_utc_file_path) -> bool:
        json_data = self.read(from_uc_file_path)
        # 将 JSON 数据转换为 PHP 数组格式的字符串
        php_array = json_to_php_array(json_data)
        # PHP 模板
        php_template = '''
        function getDataProvider() {{
            $data = {php_array};
            // 直接使用 PHP 数组
            $dataNew = [];
            foreach ($data as $item) {{
                $testcase = $item['case'];
                $data = $item['data'];
                $expected = $item['expected'];
                $dataNew[] = [
                    $testcase,
                    $data,
                    $expected,
                ];
            }}
            return $dataNew;
        }}
        
        /**
         * @param string $testcase
         * @param $data
         * @param $expected
         * @return void
         * @dataProvider getDataProvider
         */
        public function testOk($testcase, $data, $expected)
        {{
            if ($testcase != "__testcase__") {{
                $this->assertTrue(true);
                return;
            }}
            $this->assertEquals(true, true, $testcase);
        }}
        '''
        code = php_template.format(php_array=php_array)
        self.write(to_utc_file_path, code)
        return True


