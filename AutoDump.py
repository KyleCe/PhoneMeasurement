import os

import ConstResource as Res
import FunctionCommon as Fun
import FunctionPackage as FunPkg
import FunctionLauncher as FunLch
import GrabDump as Grab
from threading import Thread

debug = True
pkg_list = ['35711', '50003']
collect_period = 5 * 60 if debug else 5 * 60 * 60  # 5 hour
collect_info_internal = 60 if debug else 30 * 60  # 30 min
collect_times = 2 if debug else 10 - 1  # collect_period / collect_info_internal


def main_process():
    devices = Fun.devices_list_with_connection_check()
    for dev in devices:
        Thread(target=collect_dump_info, args=(dev,)).start()


def collect_dump_info(dev):
    Fun.log('start thread for device:' + dev)
    path = make_device_tag_dir(dev)
    for apk in pkg_list:
        inspect_apk_dump_with_internal(apk, dev, path)


def inspect_apk_dump_with_internal(apk, dev, path):
    refresh_with_apk(dev, apk)
    collect_info_repeat_with_fixed_rate(apk, dev, path)


def collect_info_repeat_with_fixed_rate(apk, dev, path):
    for i in range(collect_times):
        information_collection(apk, dev, path)
        Fun.sleep(collect_info_internal)


def refresh_with_apk(dev, apk_tag):
    FunPkg.uninstall_and_install(dev, os.path.join(Res.apk_path, apk_tag + Res.pgk_suffix),
                                 Res.pkg_name)
    FunLch.start_launcher_omit_splash(dev)


def information_collection(apk_tag, dev, path):
    Fun.log('trigger gc')
    absolute_tmp_dump_path = os.path.realpath(path)
    Fun.p_open(Res.adb_grab_heap_dump_file_with_pkg(dev, absolute_tmp_dump_path, Res.pkg_name))
    Fun.sleep(10)

    lines = Fun.p_open(Res.asb_shell_dump_mem_info(dev)).readlines()
    name = apk_tag + Res.dump + Fun.current_time()
    dump_mem_info_store_to_file(name, lines, path)
    Grab.grab_dump_and_convert(dev, name, absolute_tmp_dump_path, Res.pkg_name)


def dump_mem_info_store_to_file(name, lines, path):
    file_path = os.path.join(path, name + Res.txt_suffix)
    if not os.path.exists(file_path):
        Fun.p_open('touch ' + file_path)
    Fun.write_lines_into_file(file_path, lines)


def make_device_tag_dir(d):
    model, bluetooth = Fun.parse_device_model_and_bluetooth(d)
    path = os.path.join(Res.output_path, model + Res.underline + bluetooth)
    Fun.make_dir_if_not_exist(path)
    return path



main_process()
