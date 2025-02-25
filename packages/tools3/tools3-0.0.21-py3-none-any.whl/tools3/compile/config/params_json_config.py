import json
class ParamsJsonConfig(object):
    name = ""
    desc = ""
    params = {}
    expected = {}
    config = {}

    def __init__(self, name, desc, params, expected, config = {}):
        self.name = name
        self.desc = desc
        self.params = params
        self.expected = expected
        self.config = config

    def get_name(self):
        return self.name
    def get_desc(self):
        return self.desc

    def get_params(self):
        if self.params:
            return self.params
        else:
            return {}

    def get_expected(self):
        if self.expected:
            return self.expected
        else:
            return None

    def get_config(self):
        if self.config is None:
            return {}
        return self.config

    def get_field_values(self, field):
       values = self.get_params().get(field, {})
       return values

    def get_field_config(self, field):
        field_config = self.get_config().get("fields", {}).get(field, {})
        field_config["format"] = field_config.get("format", "default")
        values = self.get_field_values(field)
        values_new = {}
        for nickname, value in values.items():
            values_new[value] = nickname
        field_config["values"] = values_new
        return field_config

    def get_include_field_names(self):
        return self.get_config().get("include_field_names", False)

    def get_separator(self):
        return self.get_config().get("separator", "_")

    def convert_to_fields_params(self):
        params = self.get_params()
        if params is None:
            return {}

        fields_params = {}
        for field, values in params.items():
            fields_params[field] = list(values.values())
        return fields_params

    def convert_to_fields_formatters(self):
        formatters = {}
        fields = self.convert_to_fields_params()
        for field, values in fields.items():
            formatters[field] = self.get_field_config(field)

        return formatters

    @staticmethod
    def new_instance(json_config_file_path):
        with open(json_config_file_path) as json_file:
            json_data = json.loads(json_file.read())
        params_json_config = ParamsJsonConfig(
            name=json_data.get("name", ""),
            desc=json_data.get("desc", ""),
            params=json_data.get("params", {}),
            expected=json_data.get("expected", {}),
            config=json_data.get("config", {}),
        )
        return params_json_config