import os
import socket
import subprocess

import errno
import time
import sys
import fileinput
# import configparser

import ConstResource as Res
import FunctionPackage as FunPkg
from time import gmtime, strftime
from config import ConfigHelper as CfgU
from config import Config as Cfg


def get_abspath(f):
    return os.path.abspath(f)


def get_dirname(f):
    return os.path.dirname(f)


def path_join(path, f):
    return os.path.join(path, f)


def linux_path_join(path, f):
    return path + Res.linux_sep + f


def exists(f):
    return os.path.exists(f)


def list_dir(path):
    return os.listdir(path)


# def get_conf_parser(conf_file_name, conf_dir=Res.config_dir):
#     return conf_parser(get_config_file(conf_file_name, conf_dir))
#
#
# def conf_parser(ini_file):
#     cp = ConfigParser.ConfigParser()
#     cp.read(ini_file)
#     return cp


def get_config_file(conf_file_name, conf_dir=Res.config_dir):
    return path_join(get_abspath(conf_dir), conf_file_name)


def assert_options_presents(parser, opts):
    for opt in opts:
        assert_option(parser, opt)


def assert_option(parser, opt):
    if not parser.options(opt):
        raise_error(opt + ' not exist in configuration file')


def get_android_version(tag):
    err, out = get_command_result(Res.asb_shell_android_version(tag))
    if err:
        raise_error(err)
    return out.rstrip().replace('.', '_')  # the windows OS could not parse '.' char, what an idiot


def get_command_result(cmd):
    p = subprocess.Popen(cmd.split(Res.white_space),
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return err, out


def get_my_ip():
    """
    Returns the actual ip of the local machine.
    This code figures out what source address would be used if some traffic
    were to be sent out to some well known address on the Internet. In this
    case, a Google DNS server is used, but the specific address does not
    matter much.  No traffic is actually sent.
    """
    try:
        csock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        csock.connect(('8.8.8.8', 80))
        (addr, port) = csock.getsockname()
        csock.close()
        return addr
    except socket.error:
        return "127.0.0.1"


def tell_app_installed(tag, pkg_name):
    result = p_open(Res.asb_shell_list_packages(tag, pkg_name)).readlines()
    return len(result) > 0


def kill_monkey(tag):
    """
    kill the running monkey
    """
    err, out = get_command_result(Res.asb_shell_grep_monkey(tag))
    if err != '':
        raise_error(err)
    elif out != '':
        pid = out.split()[1]
        p_open(Res.asb_shell_kill_process(tag, pid))


def current_time():
    return strftime(Res.time_format, gmtime())


def logs(*args):
    for arg in args:
        log(arg)


def log(info):
    print(current_time() + ' ' + str(info))


def log_cat_to_file(tag):
    device_info = parse_device_info(tag)
    log_path = get_abspath(
        os.path.join(Res.log_path, device_info + Res.underline + Res.logcat_tag
                     + current_time() + Res.logcat_suffix))
    log('log cat to file::: ' + log_path)
    p_open(Res.asb_shell_logcat_to_file(tag, log_path))


def list_contain_content_on_index(arr, index):
    return (len(arr) > index) and (arr[index] != '')


def p_open(command):
    log('COMMAND: ' + command)
    return os.popen(command)


def p_open_with_line_1_result(command):
    return p_open(command).readlines()[0].strip()


def execute_with_try_catch(cmd):
    try:
        p_open(cmd)
    except Exception as e:
        log(e)


def raise_error(info):
    raise Exception(info)


def replace_line(f, start_exp, to_replace):
    for line in fileinput.input(f, inplace=1):
        if line.startswith(start_exp):
            line = to_replace
        sys.stdout.write(line)


def replace_line_in_file(f, start_exp, to_replace):
    lines = read_lines_of_file(f)
    for i in range(len(lines)):
        if lines[i].startswith(start_exp):
            lines[i] = to_replace + os.linesep
    write_lines_into_file(Res.project_path + f, lines)


def write_lines_into_file(f, lines):
    fo = open(f, 'w')
    fo.writelines(lines)
    fo.close()


def erase_file_content(f):
    open(f, 'w').close()


def create_file(f):
    try:
        os.makedirs(os.path.dirname(f))
    except OSError as exc:  # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise
    p_open(Res.mk_file + f)


def sleep(seconds, log_info=''):
    if Res.sleep_open:
        log('sleep for seconds: ' + str(seconds) + log_info)
        time.sleep(seconds)
    else:
        log('cannot sleep, function turned off')


def make_dir_if_not_exist(path):
    path = get_abspath(path)
    log('make dir::' + path)
    if not os.path.isdir(path):
        os.makedirs(path)


def parse_device_model_and_bluetooth(d):
    model = parse_model(d)
    bluetooth = parse_bluetooth(d)
    return model, bluetooth


def parse_model(d):
    return p_open_with_line_1_result(Res.asb_shell_get_model(d)).replace(Res.white_space, '') \
        .replace('(', '').replace(')', '')


def parse_bluetooth(d):
    return Res.bluetooth + p_open_with_line_1_result(
        Res.asb_shell_get_bluetooth_address(d)).replace(':', '')


def parse_device_info(device_id):
    model, bluetooth = parse_device_model_and_bluetooth(device_id)
    device_info = model + Res.underline + get_android_version(device_id) + Res.underline + bluetooth
    return device_info


def get_device_uid(tag):
    uid_info = p_open(Res.adb_ps_grep(tag)).readlines()
    uid_info = uid_info[0].split('   ')[0]
    uid_info = uid_info.split('_')
    uid_info = uid_info[0] + uid_info[1]
    return uid_info


def connected_devices_arr():
    result = []
    conn_result = p_open('adb devices').readlines()
    conn_devices_info = conn_result[1:len(conn_result) - 1]
    conn_devices_num = len(conn_devices_info)
    if conn_devices_num > 0:
        for i in range(conn_devices_num):
            address = conn_devices_info[i].split('\t')[0]
            result.append(address)
    return result


def devices_list_with_connection_check():
    devices = connected_devices_arr()
    if len(devices) == 0:
        raise Exception('no device found, confirm connection')
    else:
        log('found device(s): ' + str(devices))
        return devices


def read_lines_of_file(f, absolute_path=False):
    if f.startswith('./'):
        f = f.replace('./', '/')
    with open((Res.project_path if not absolute_path else '') + f, 'r') as splash:
        return splash.read().splitlines()


def get_usable_lines(lines):
    usable_lines = []
    for line in lines:
        if (not line) | line.startswith(Res.comment_mark) | line.startswith(Res.new_line) \
                | line.startswith(Res.new_line_r) | line.startswith(Res.new_line_nr):
            continue
        usable_lines.append(line)
    return usable_lines


def get_usable_lines_from_file(f, absolute_path=False):
    return get_usable_lines(read_lines_of_file(f, absolute_path))


def send_key_home(tag):
    p_open(Res.adb_key_event_home(tag))


def send_key_back(tag):
    p_open(Res.adb_key_event_back(tag))


def serial_clicks_by_control_file(tag):
    log('launch click process of ' + tag)
    p_open(Res.adb_start_launcher(tag))
    sleep(Res.pkg_init_delay)  # init taking time

    lines = get_usable_lines_from_file(Res.splash_file)
    for i in range(len(lines)):
        items = lines[i].split(Res.split_mark)
        if i == Res.action_kcg_launcher_index:
            send_key_home(tag)
            sleep(1)  # invoke default home takes time
        p_open(Res.adb_tap_with_tag(tag, items[1], items[2]))
        if len(items) > Res.delay_index_one_point:
            sleep(items[Res.delay_index_one_point])
        sleep(3 if i < Res.action_kcg_launcher_index else Res.default_delay_in_click)
        if i >= Res.action_always_index:
            send_key_home(tag)


def serial_operation_by_control_file(tag, case_file=Res.case_file, c=Cfg.SMCommon(), commands=[]):
    log('launch swipe process of ' + tag)
    lines = get_usable_lines_from_file(case_file)

    # parse if have special configuration
    case_w, case_h, case_nav = 0, 0, 0
    for line in lines:
        items = line.split(Res.split_mark)
        if Res.case_display_config in line:
            case_w = int(items[1])
            case_h = int(items[2])
            case_nav = int(items[3])
            break
    case_has_nav = case_nav > 0
    alta_height = (0 if c.has_nav and not case_has_nav
                   else -(c.nav_height if not case_has_nav else case_nav))
    real_w, real_h, nav_h = CfgU.device_real_config_info(tag)
    f_x = float(real_w) / (c.size_x if case_w == 0 else case_w)
    f_y = float(real_h) / ((c.size_y if case_h == 0 else case_h) + alta_height)
    for line in lines:
        items = line.split(Res.split_mark)
        if real_item(Res.action_click, items[0]):
            p_open(Res.adb_tap_with_tag(tag, cor(items[1], f_x), cor(items[2], f_y)))
            delay_index = Res.delay_index_one_point
        elif real_item(Res.action_hold, items[0]):
            p_open(Res.adb_touch_screen_with_tag(tag, cor(items[1], f_x), cor(items[2], f_y)))
            delay_index = Res.delay_index_one_point
        elif real_item(Res.action_home, items[0]):
            send_key_home(tag)
            delay_index = Res.delay_index_zero_point
        elif real_item(Res.action_back, items[0]):
            p_open(Res.adb_key_event_back(tag))
            delay_index = Res.delay_index_zero_point
        elif real_item(Res.action_wait, items[0]):
            delay_index = Res.delay_index_zero_point
        elif real_item(Res.action_swipe, items[0]):
            p_open(Res.adb_swipe_with_tag(tag, cor(items[1], f_x), cor(items[2], f_y)
                                          , cor(items[3], f_x), cor(items[4], f_y)))
            delay_index = Res.delay_index_two_point
        elif real_item(Res.special_start, items[0]):
            p_open(Res.asb_shell_start_activity(tag, c.act))
            delay_index = Res.delay_index_zero_point
        elif real_item(Res.special_stop, items[0]):
            p_open(Res.asb_shell_force_stop(tag, c.pkg))
            delay_index = Res.delay_index_zero_point
        elif real_item(Res.special_clear_data, items[0]):
            p_open(Res.asb_shell_clear_data(tag, c.pkg))
            delay_index = Res.delay_index_zero_point
        elif real_item(Res.special_clear_logcat, items[0]):
            p_open(Res.asb_shell_clear_logcat(tag))
            delay_index = Res.delay_index_zero_point
        elif real_item(Res.special_invoke_watcher, items[0]):
            p_open(commands[2])  # start collector activity
            delay_index = Res.delay_index_zero_point
        elif real_item(Res.special_start_command, items[0]):
            p_open(commands[0])
            delay_index = Res.delay_index_zero_point
        elif real_item(Res.special_stop_command, items[0]):
            p_open(commands[1])
            delay_index = Res.delay_index_zero_point
        elif real_item(Res.action_uninstall, items[0]):
            FunPkg.uninstall(tag, c.pkg)
            delay_index = Res.delay_index_zero_point
        elif real_item(Res.action_install, items[0]):
            delay_index = install_and_parse_index(tag, c, items[1])
        elif real_item(Res.action_install_r, items[0]):
            delay_index = install_and_parse_index(tag, c, items[1], True)
        elif real_item(Res.action_reboot, items[0]):
            p_open(Res.adb_reboot(tag))
            delay_index = Res.delay_index_zero_point
        else:
            continue
        seconds = items[delay_index] if len(items) > delay_index else Res.default_delay_in_action
        sleep(float(seconds))


def install_and_parse_index(tag, c, item, r=False):
    item_not_apk = item is None or len(item) == 1
    FunPkg.install_r(tag, parse_apk_full_path(c.apk if item_not_apk else item), r)
    return Res.delay_index_zero_point if item is int else Res.delay_index_1_param


def real_item(standard, sample):
    return standard == sample.strip()


def cor(c, factor):
    return float(c) * factor


def case_file_special(f):
    lines = get_usable_lines_from_file(f)
    for line in lines:
        if Res.special_mode in line:
            return True
    return False


def parse_apk_full_path(keyword):
    apk_path = get_abspath(Res.apk_path)
    pkg_list = list_dir(apk_path)
    available_pkg = ''
    logs(keyword + 'matching in ::', pkg_list)
    keyword = keyword.strip()
    for pkg in pkg_list:
        if keyword in pkg or keyword == pkg:
            available_pkg = pkg
    if available_pkg == '':
        raise_error(Res.monkey_target_not_found + ' key: \'' + keyword + '\'')
    return path_join(apk_path, available_pkg)
