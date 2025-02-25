from tools3.compile import Compile
import subprocess
import sys

class PyCompileUC(Compile):

    def compile(self, compile_file_path) -> bool:
        # 使用 subprocess 调用 Python 解释器执行脚本
        subprocess.run([sys.executable, compile_file_path], check=True)
        return True
