import os
import subprocess, shlex
import basis.logger

LOG = basis.logger.get_logger()

ICONVERT_PATH = '/a-vfx/stuff/programs/linux/houdini-16.0.705/bin/iconvert'
MAKETX_PATH = '/a-vfx/stuff/tools/Maya2017/modules/mtoa/bin/maketx'
OCIO_CONFIG_PATH = '/a-vfx/stuff/tools/OCIO/OpenColorIO-Configs-aces1.0.1/' \
                   'aces_1.0.1/config.ocio'
DESTINATION_FOLDER_NAME = 'converted_by_af'
WORK_DIR = '/a-vfx/studio/db/temp'

def split_file(file_path):
    path_to = os.path.split(file_path)[0]
    file_base = os.path.basename(file_path)
    file_name = os.path.splitext(file_base)[0]
    file_format = os.path.splitext(file_base)[1][1:].lower()
    return path_to, file_base, file_name, file_format

def convert_script(source_file, target_path, option):
    maketx_path = MAKETX_PATH
    ocio_config_path = OCIO_CONFIG_PATH

    path_from = source_file.abs_path
    target_file = target_path + "/" +source_file.file_name + ".tx"

    cmd = (
        "{maketx_path} -v -u -o {target_file} --unpremult --oiio "
        "--colorengine syncolor --colorconfig {ocio_config_path} "
        "--colorconvert {option} {path_from}".format(**locals())
    )

    process = subprocess.Popen(
        shlex.split(cmd),
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
    )
    out, error = process.communicate()

    LOG.info(out)
    if error or process.returncode != 0:
        LOG.error(
            "error during convert: exit code {}\n{}".format(
                process.returncode, error
            )
        )
    
