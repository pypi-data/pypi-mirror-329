import json

from tools3 import  BaseObj


class UCCompileUTC(BaseObj):
    step_name = ""
    def compile(self, from_uc_json_file_path, to_utc_file_path) -> bool:
        pass
    def read(self, from_uc_json_file_path):
        self.get_logger().info(self.step_name + " read start")
        try:
            with open(from_uc_json_file_path) as json_file:
                json_data = json.loads(json_file.read())
        except Exception as e:
            self.get_logger().error(self.step_name + " read error: {}".format(e))
            raise e
        self.get_logger().info(self.step_name + " read end")
        return json_data

    def write(self, to_utc_file_path, data):
        self.get_logger().info(self.step_name + " write start")
        try:
            with open(to_utc_file_path, 'w') as file:
                file.write(data)
        except Exception as e:
            self.get_logger().error(self.step_name + " write error: {}".format(e))
            raise e
        self.get_logger().info(self.step_name + " write end")
        return True