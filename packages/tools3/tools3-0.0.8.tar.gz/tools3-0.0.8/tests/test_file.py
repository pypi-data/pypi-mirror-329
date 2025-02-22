import os.path
import unittest
from tools3 import get_file_absolute_path,check_path_is_file,check_path_is_dir, get_file_ext,get_file_dir,get_file_without_ext,get_file_name
class TestFile(unittest.TestCase):
    def test_file(self):
        # path=/webroot/idea/py/tools3/tests/test_file_path.txt
        path = get_file_absolute_path("tests/test_file_path.txt")
        self.assertNotEqual(path, "")
    def test_file_absolute_path(self):
        # path=/webroot/idea/py/tools3/tests/test_file_absolute_path.txt
        path = get_file_absolute_path("/webroot/idea/py/tools3/tests/test_file_absolute_path.txt")
        self.assertEqual(path, "/webroot/idea/py/tools3/tests/test_file_absolute_path.txt")

    def test_check_path_is_file(self):
        # path=/webroot/idea/py/tools3/tests/test_file_path.txt
        path = get_file_absolute_path("tests/test_file_path.txt")
        is_file = check_path_is_file(path)
        self.assertTrue(is_file)

        path = get_file_absolute_path("tests/test_file_path.txt not exist")
        is_file = check_path_is_file(path)
        self.assertFalse(is_file)
    def test_check_path_is_dir(self):
        # path=/webroot/idea/py/tools3/tests/test_file_path.txt
        path = get_file_absolute_path("tests/test_file_path.txt")
        is_dir = check_path_is_dir(path)
        self.assertFalse(is_dir)

        path = get_file_absolute_path("tests")
        is_dir = check_path_is_dir(path)
        self.assertTrue(is_dir)

        path = get_file_absolute_path("tests not exist")
        is_dir = check_path_is_dir(path)
        self.assertFalse(is_dir)

    def test_get_file_dir_path(self):
        # /webroot/idea/py/tools3/tests/test_file_path.txt
        path = get_file_absolute_path("tests/test_file_path.txt")
        # /webroot/idea/py/tools3/tests
        dir_path = os.path.dirname(path)
        self.assertNotEqual(dir_path, "")
    def test_get_file_name(self):
        # /webroot/idea/py/tools3/tests/test_file_path.txt
        path = get_file_absolute_path("tests/test_file_path.txt")
        # test_file_path.txt
        file_name = get_file_name(path)
        self.assertEqual(file_name, "test_file_path.txt")
    # 给一个路径,获取扩展名
    def test_get_file_ext(self):
        # /webroot/idea/py/tools3/tests/test_file_path.json.txt
        path = get_file_absolute_path("tests/test_file_path.json.txt")
        file_ext = get_file_ext(path)
        self.assertEqual(file_ext, ".txt")
    def test_get_file_without_ext(self):
        # /webroot/idea/py/tools3/tests/test_file_path.txt
        path = get_file_absolute_path("tests/test_file_path.txt")
        # /webroot/idea/py/tools3/tests/test_file_path
        file_without_ext = get_file_without_ext(path)
        self.assertEqual(file_without_ext, os.getcwd() + "/tests/test_file_path")

    def test_get_file_dir(self):
        # /webroot/idea/py/tools3/tests/test_file_path.txt
        path = get_file_absolute_path("tests/test_file_path.txt")
        # /webroot/idea/py/tools3/tests
        file_dir = get_file_dir(path)
        self.assertEqual(file_dir, os.getcwd() + "/tests")
