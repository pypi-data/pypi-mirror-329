# my_package/runner.py
import subprocess
import sys
import os


def run_script(script_path):
    """
    执行指定路径的 Python 脚本。
    :param script_path: 要执行的 Python 文件路径（支持绝对路径和相对路径）
    """
    # 将路径转换为绝对路径
    script_path = os.path.abspath(script_path)

    if not os.path.isfile(script_path):
        print(f"错误: 文件不存在: {script_path}")
        return

    try:
        # 使用 subprocess 调用 Python 解释器执行脚本
        subprocess.run([sys.executable, script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"执行脚本时出错: {e}")
    except Exception as e:
        print(f"发生未知错误: {e}")


def main():
    if len(sys.argv) != 2:
        print("用法: run-python <python_file>")
        sys.exit(1)

    script_path = sys.argv[1]
    run_script(script_path)


if __name__ == "__main__":
    main()