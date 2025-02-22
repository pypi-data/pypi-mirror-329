import json


class UCCompileUTC(object):
    def compile(self, from_uc_json_file_path, to_utc_file_path) -> bool:
        pass
    def read(self, from_uc_json_file_path):
        with open(from_uc_json_file_path) as json_file:
            json_data = json.loads(json_file.read())
        return json_data

    def write(self, to_utc_file_path, data):
        with open(to_utc_file_path, 'w') as file:
            file.write(data)
        return True