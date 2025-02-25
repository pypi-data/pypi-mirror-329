from .base_logger import BaseLogger
class BaseObj(object):
    _base_logger: BaseLogger
    def __init__(self):
        self._base_logger = None

    def set_base_logger(self, logger: BaseLogger):
        self._base_logger = logger
        return self
    def get_base_logger(self):
        if self._base_logger is None:
            self._base_logger = BaseLogger()
        return self._base_logger

    def get_logger(self):
        return self.get_base_logger().get_logger()