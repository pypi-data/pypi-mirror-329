import argparse
import os
import sys

from build.lib.tools3 import get_file_dir
from tools3 import get_file_absolute_path, check_path_is_file, check_path_is_dir, get_file_without_ext, get_file_name, \
    get_file_ext
from tools3.compile.uc import JsonConfigCompileUC
from tools3.compile.utc import UCCompilePhpUnit
from tools3.compile.uc import CompileUC
from tools3.compile.uc import PyCompileUC
from .biz_compiler import BizCompiler
from .func import get_output_file_path, parse_error
from .compiler import Compiler

TYPE_IS_JC_PY = "jc_py"
TYPE_IS_JC_UC = "jc_uc"
TYPE_IS_PY_UC = "py_uc"
TYPE_IS_UC_PHPUNIT = "uc_phpunit"

TYPE_IS_PY_PHPUNIT = "py_phpunit"
TYPE_IS_JC_PHPUNIT = "jc_phpunit"

TYPES_MAP = {
    TYPE_IS_JC_PY: TYPE_IS_JC_PY,
    TYPE_IS_JC_UC: TYPE_IS_JC_UC,
    TYPE_IS_PY_UC: TYPE_IS_PY_UC,
    TYPE_IS_UC_PHPUNIT: TYPE_IS_UC_PHPUNIT,

    # TYPE_IS_PY_PHPUNIT: TYPE_IS_PY_PHPUNIT,
    TYPE_IS_JC_PHPUNIT: TYPE_IS_JC_PHPUNIT,
}


def run() -> None:
    parse = argparse.ArgumentParser(
        prog="tools3-cli",
        description="compile unit tool",
        epilog="Copyright (c) 2025, tools3",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parse.add_argument("from_file", type=check_from_file, help="from file")
    parse.add_argument(
        "-t",
        "--type",
        type=check_type,
        default="jc_phpunit",
        help="""compile type (default: jc_phpunit)
Available options:  
- jc_py: Compile Python file from JSON config  
- jc_uc: Compile use case (UC) file from JSON config  
- py_uc: Compile use case (UC) file from Python config  
- uc_phpunit: Compile PHPUnit file for use case (UC)

Business scenarios: 
- jc_phpunit: Compile Json config file for PHPUnit
        """)
    parse.add_argument("-o", "--output-file", type=check_output_file, help="output file")
    args = parse.parse_args()
    ctype = args.type
    from_file = args.from_file
    output_file = args.output_file
    compiler = BizCompiler()
    try:
        if ctype == TYPE_IS_JC_PY:
            compiler.jc_py(from_file, output_file)
            return
        if ctype == TYPE_IS_JC_UC:
            compiler.jc_uc(from_file, output_file)
            return
        if ctype == TYPE_IS_PY_UC:
            compiler.py_uc(from_file, output_file)
            return
        if ctype == TYPE_IS_UC_PHPUNIT:
            compiler.uc_phpunit(from_file, output_file)
            return

        # 业务场景
        if ctype == TYPE_IS_PY_PHPUNIT:
            compiler.py_phpunit(from_file, output_file)
            return
        if ctype == TYPE_IS_JC_PHPUNIT:
            compiler.jc_phpunit(from_file, output_file)
            return
    except Exception as e:
        parse_error(parse, e)


def check_from_file(from_file):
    from_file = get_file_absolute_path(from_file)
    is_file = check_path_is_file(from_file)
    if is_file:
        return from_file
    raise argparse.ArgumentTypeError(f"from file not found: {from_file}")


def check_output_file(output_file):
    if output_file is None or output_file == "":
        return ""
    output_file = get_file_absolute_path(output_file)
    is_file = check_path_is_file(output_file)
    if is_file:
        return output_file

    is_dir = check_path_is_dir(output_file)
    if is_dir:
        return output_file

    is_dir = get_file_dir(output_file)
    if is_dir:
        return output_file

    raise argparse.ArgumentTypeError(f"{output_file} not found")

def check_type(ctype):
    if ctype in TYPES_MAP:
        return ctype
    raise argparse.ArgumentTypeError(f"type {ctype} not found")

def main():
    run()
