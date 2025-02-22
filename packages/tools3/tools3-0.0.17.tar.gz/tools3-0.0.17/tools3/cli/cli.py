import argparse
import os
import sys

from tools3 import get_file_absolute_path, check_path_is_file, check_path_is_dir, get_file_without_ext, get_file_name, \
    get_file_ext
from tools3.compile.uc import JsonConfigCompileUC
from tools3.compile.utc import UCCompilePhpUnit
from tools3.compile.uc import CompileUC
from tools3.compile.uc import PyCompileUC

TYPE_IS_JSON_PHPUNIT = "json_phpunit"
TYPE_IS_PY_PHPUNIT = "py_phpunit"
TYPE_IS_JSON_PY = "json_py"
TYPE_IS_CASES_PHPUNIT = "cases_phpunit"

TYPES_MAP = {
    TYPE_IS_JSON_PHPUNIT: TYPE_IS_JSON_PHPUNIT,
    TYPE_IS_PY_PHPUNIT: TYPE_IS_PY_PHPUNIT,
    TYPE_IS_JSON_PY: TYPE_IS_JSON_PY,
    TYPE_IS_CASES_PHPUNIT: TYPE_IS_CASES_PHPUNIT,
}


def run() -> None:
    parse = argparse.ArgumentParser(
        prog="tools3-cli",
        description="compile unit tool",
        epilog="Copyright (c) 2023, tools3",
    )

    parse.add_argument("from_file", type=check_from_file, help="from file")
    parse.add_argument(
        "-t",
        "--type",
        type=check_type,
        default="json_phpunit",
        help="""compile type，default=json_phpunit [json_phpunit, py_phpunit, cases_phpunit, json_py]""")
    parse.add_argument("-o", "--output-file", type=check_output_file, help="output file")
    args = parse.parse_args()
    ctype = args.type
    print(args)
    from_file = args.from_file
    output_file = args.output_file
    if ctype == TYPE_IS_JSON_PHPUNIT:
        jsonc_phpunit(from_file, output_file)
        return
    if ctype == TYPE_IS_PY_PHPUNIT:
        py_phpunit(from_file, output_file)
        return
    if ctype == TYPE_IS_CASES_PHPUNIT:
        cases_phpunit(from_file, output_file)
        return
    if ctype == TYPE_IS_JSON_PY:
        json_py(from_file, output_file)
        return


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
    raise argparse.ArgumentTypeError(f"{output_file} not found")


def get_output_file_path(from_file, output_file, utc_file_ext) -> str:
    if output_file is None or output_file == "":
        output_file = get_file_without_ext(from_file) + utc_file_ext
        return output_file

    is_file = check_path_is_file(output_file)
    if is_file:
        return output_file
    is_dir = check_path_is_dir(output_file)
    if is_dir:
        file_name = get_file_name(from_file)
        output_file = os.path.join(output_file, file_name + utc_file_ext) + ""
        return output_file

    raise argparse.ArgumentTypeError(f"output file not found: {output_file}")


def check_type(ctype):
    if ctype in TYPES_MAP:
        return ctype
    raise argparse.ArgumentTypeError(f"type {ctype} not found")


def jsonc_phpunit(from_file, output_file):
    uc = JsonConfigCompileUC(from_file)
    uc_output_file = get_output_file_path(from_file, output_file, ".json")
    utc_output_file = get_output_file_path(from_file, output_file, ".phpunit")
    uc.compile(uc_output_file)
    utc = UCCompilePhpUnit()
    utc.compile(uc_output_file, utc_output_file)
    os.remove(uc_output_file)


def py_phpunit(from_file, output_file):
    uc = PyCompileUC()
    uc_output_file = get_output_file_path(from_file, output_file, ".json")
    utc_output_file = get_output_file_path(from_file, output_file, ".phpunit")
    print(from_file)
    print(uc_output_file)
    uc.compile(from_file)
    utc = UCCompilePhpUnit()
    utc.compile(uc_output_file, utc_output_file)
    os.remove(uc_output_file)
    pass

def cases_phpunit(from_file, output_file):
    utc = UCCompilePhpUnit()
    utc_output_file = get_output_file_path(from_file, output_file, ".phpunit")
    utc.compile(from_file, utc_output_file)
    pass

def json_py(from_file, output_file):
    uc = JsonConfigCompileUC(from_file)
    uc_output_file = get_output_file_path(from_file, output_file, ".json")
    os.remove(uc_output_file)
    utc_output_file = get_output_file_path(from_file, output_file, ".phpunit")
    uc.compile(uc_output_file)
    utc = UCCompilePhpUnit()
    utc.compile(uc_output_file, utc_output_file)
    pass


def main():
    run()
