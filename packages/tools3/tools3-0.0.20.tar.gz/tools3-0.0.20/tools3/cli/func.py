from build.lib.tools3 import get_file_dir
from tools3 import get_file_absolute_path, check_path_is_file, check_path_is_dir, get_file_without_ext, get_file_name, \
    get_file_ext
import os
import argparse
import errno

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

    is_dir = get_file_dir(output_file)
    if is_dir:
        return output_file

    raise argparse.ArgumentTypeError(f"output file not found: {output_file}")


def parse_error(parse, msg):
    msg =f"\033[91m{msg}\033[0m".format(msg=msg)
    parse.error(msg)


def file_exists_error(msg, file):
    exists = os.path.exists(file)
    if exists:
        raise FileExistsError(
            errno.EEXIST,
            msg,
            file
        )

def file_not_found_error(msg, file):
    return FileNotFoundError(
        errno.ENOENT,
        msg,
        file
    )
def raise_from_file_not_exists_error(output_file):
    exists = os.path.exists(output_file)
    if exists is False:
        raise file_not_found_error("from file not exists", output_file)

def raise_output_file_exists_error(output_file):
    exists = os.path.exists(output_file)
    if exists:
        raise file_exists_error("output file already exists", output_file)