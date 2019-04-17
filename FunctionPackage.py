import os
import ConstResource as Res
import FunctionCommon as FunCom
from module.AppAndActivityInfo import AppInfo


def install(device, apk_path):
    install_r(device, apk_path, False)


def install_r(device, apk_path, r):
    install_cmd = Res.install_r if r else Res.install
    try:
        command = Res.adb_s + device + install_cmd + '%s' % apk_path
        return FunCom.p_open(command)
    except Exception as e:
        FunCom.log(e)


def get_apk_file_in_path(path):
    apk_map = []
    for parent, dir_names, filenames in os.walk(path):
        for f in filenames:
            if f.endswith(Res.pgk_suffix):
                apk_map.append(os.path.join(parent, f))
    return apk_map


def get_apk_file_in_project():
    return get_apk_file_in_path(Res.project_root_path)


def uninstall(device_id, package_name):
    command = Res.adb_s + device_id + Res.uninstall + package_name
    FunCom.p_open(command)


def uninstall_launcher(device_id):
    command = Res.adb_s + device_id + Res.uninstall + Res.pkg_name
    FunCom.p_open(command)


def uninstall_directly():
    command = Res.adb + Res.uninstall + Res.pkg_name
    FunCom.p_open(command)


def uninstall_and_install(device_id, name_path, package_name):
    uninstall(device_id, package_name)
    install(device_id, name_path)


def clear(devices_id):
    FunCom.p_open('adb -s ' + devices_id + Res.shell_clear)


def install_app_start_activity(tag, pkg, act, app_file, replace_apk=False, delay=6):
    if replace_apk or not FunCom.tell_app_installed(tag, pkg):
        apk_path = ''
        for f in FunCom.list_dir(FunCom.Res.util_path):
            if app_file in f:
                apk_path = FunCom.get_abspath(FunCom.path_join(FunCom.Res.util_path, f))
        if apk_path == '':
            FunCom.raise_error(
                app_file + ' Apk file not found under ./util directory')
        # windows do not support grep command, cannot tell existence
        install_r(tag, apk_path, False)
        FunCom.sleep(delay)
    FunCom.p_open(FunCom.Res.asb_shell_start_activity(tag, act))
