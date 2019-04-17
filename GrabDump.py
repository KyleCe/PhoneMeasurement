# just for grabbing heap dump file
# and convert it into format that can be recognized by EclipseMAT

import sys
import os
from os.path import dirname

import ConstResource as Res
import FunctionCommon as Fun

absolute_tmp_dump_path = '/data/local/tmp/heap.hprof'  # make sure the path is writeable on phone


def grab_dump_and_convert(dev, target_name, dest_path, pkg):
    Fun.p_open(Res.adb_grab_heap_dump_file_with_pkg(dev, absolute_tmp_dump_path, pkg))
    Fun.sleep(4)
    dump_file_path = os.path.join(dest_path, target_name)
    dump_file = dump_file_path + Res.hprof_suffix if not dump_file_path.endswith(
        Res.hprof_suffix) else dump_file_path
    if os.path.exists(dump_file):
        dump_file = dump_file.replace(Res.hprof_suffix, Fun.current_time() + Res.hprof_suffix)
    Fun.p_open(Res.adb_pull_heap_file_to_dest(dev, absolute_tmp_dump_path, dump_file))
    convert_file_into_directory(dump_file)


def convert_and_store(file_or_path):
    """

    :param file_or_path: use a single file with full path or a full path
    all the files end with under the path will be converted and store into directory named with the file name
    """
    if not os.path.isdir(file_or_path):
        convert_file_into_directory(file_or_path)
    else:
        for filename in os.listdir(file_or_path):
            if filename.endswith(Res.hprof_suffix):
                convert_file_into_directory(os.path.join(file_or_path, filename))


def convert_file_into_directory(file_with_full_path):
    path = dirname(file_with_full_path)
    tags = os.path.split(file_with_full_path)
    file_name = tags[1]
    convert_and_store_in_directory(path, file_name)


def convert_and_store_in_directory(dest_path, target_name):
    target_name = target_name.replace(Res.hprof_suffix, '')
    dump_file_path = os.path.join(dest_path, target_name)
    dump_file = dump_file_path + Res.hprof_suffix if not dump_file_path.endswith(
        Res.hprof_suffix) else dump_file_path
    Fun.make_dir_if_not_exist(dump_file_path)
    convert_file = os.path.join(dump_file_path, target_name + Res.convert_suffix)
    Fun.p_open(Res.adb_convert_heap_profile(dump_file, convert_file))


def execute(heap_dump_name):
    destination_path = '/Users/elex/Documents/dump'  # change directory path to your favorites
    grab_dump_and_convert(destination_path, heap_dump_name)


def main_process():
    print '''\n
    -----------------------------------------------
    you can pass params to define dump :(every param can be ignored)
    example----$ python GradDump.py  
    example----$ python GradDump.py  1_file_name  
    example----$ python GradDump.py  1_file_name  2_destination_directory  
    example----$ python GradDump.py  1_file_name  2_destination_directory  3_process_name
    1. 1_file_name
    2. 2_destination_directory
    3. 3_process_name
    
    NOTE: once you've input a param already, the next time function running will use the latest param you input
    -----------------------------------------------
    '''
    argv = sys.argv
    dump_name = 1
    path = 2
    process = 3
    params = ['', '', '', '']
    config_file_path = Res.config_path
    configs = Fun.get_usable_lines_from_file(config_file_path)
    for config in configs:
        data = config.split(Res.config_split)
        if data[0].startswith(Res.ck_dump_name) and len(data) > 1:
            params[dump_name] = data[1].strip()
        elif data[0].startswith(Res.ck_path) and len(data) > 1:
            params[path] = data[1].strip()
        elif data[0].startswith(Res.ck_process) and len(data) > 1:
            params[process] = data[1].strip()
    if Fun.list_contain_content_on_index(argv,
                                         dump_name):  # the python file name will take the 0 index in array
        params[dump_name] = argv[dump_name]
        Fun.replace_line_in_file(config_file_path, Res.ck_dump_name,
                                 Res.assemble_config(Res.ck_dump_name, params[dump_name]))
        if Fun.list_contain_content_on_index(argv, path):
            params[path] = argv[path]
            Fun.replace_line_in_file(config_file_path, Res.ck_path,
                                     Res.assemble_config(Res.ck_path, params[path]))
            if Fun.list_contain_content_on_index(argv, process):
                params[process] = argv[process]
                Fun.replace_line_in_file(config_file_path, Res.ck_process,
                                         Res.assemble_config(Res.ck_process, params[process]))
    grab_dump_and_convert(params[dump_name], params[path], params[process])

# main_process()
