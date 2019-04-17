import sys

sys.path.append('..')
import ConstResource as Res
import FunctionCommon as FunCom
import FunctionPackage as FunPkg
import FunctionLauncher as FunLch
import MailSender as Sender

debug = True
skip_internal = 30 if not debug else 3


def skip(tag):
    FunCom.execute_with_try_catch(Res.asb_shell_find_kcg_launcher(tag))
    FunCom.sleep(skip_internal)
    FunCom.execute_with_try_catch(Res.asb_shell_click_menu(tag))
    FunCom.sleep(skip_internal)
    FunCom.execute_with_try_catch(Res.asb_shell_setting_complete(tag))


def push_lib_to_phone(tag):
    lib_file = FunCom.get_abspath(FunCom.path_join(Res.lib_path, Res.monkey_lib_file_name))
    FunCom.p_open(Res.asb_shell_push_file(tag, lib_file))


def start(tag, pkg, events, throttle, logfile):
    FunCom.p_open(Res.asb_shell_start_monkey_with_s(tag) % (
        pkg, events, throttle, FunCom.get_abspath(logfile))).read()


def prepare_log_file_path_file(log_f):
    create_or_erase(log_f)
    path_f = log_f.replace(Res.log_suffix, Res.path_suffix)
    create_or_erase(path_f)


def create_or_erase(f):
    f = FunCom.get_abspath(FunCom.path_join(Res.project_path, f))
    FunCom.log('to parse file: ' + f)
    if not FunCom.exists(f):
        FunCom.log('not exist, creating')
        FunCom.create_file(f)
    else:
        FunCom.log('exist, erasing')
        FunCom.erase_file_content(f)


def prepare_path_record_file(log_path, str_path):
    f = log_path.replace(Res.log_suffix, Res.path_suffix)
    create_or_erase(f)
    FunCom.write_lines_into_file(f, str_path)


def install_pkg_and_prepare_record_file(d, apk_path, package_name, logfile, installed_once=True):
    parser = FunCom.get_conf_parser(Res.monkey_conf_file)
    if not parser.has_option(Res.monkey_target_key_word_opt, Res.monkey_target_key_word_key):
        FunCom.raise_error(Res.monkey_target_not_found)
    key_word = parser.get(Res.monkey_target_key_word_opt, Res.monkey_target_key_word_key)
    apk_full_path = FunCom.parse_apk_full_path(key_word)

    if not installed_once:
        FunPkg.uninstall_and_install(d, apk_full_path, package_name)
        FunLch.start_launcher_omit_splash(d)
    else:
        FunPkg.install_r(d, apk_full_path, True)
        FunLch.start_launcher_omit_splash(d, False, False)
    prepare_path_record_file(logfile, apk_full_path)


def refresh_with_apk(d, apk_path, package_name, logfile, installed_once):
    install_pkg_and_prepare_record_file(d, apk_path, package_name, logfile, installed_once)


def log_trick(device_id, monkey_log, sender, pwd, receivers, anr_receivers, subject,
              logfile, browser, device, version, keyword):
    FunCom.log('start log analyze')

    # todo
    # exception_handle(device_id)
    if FunCom.exists(monkey_log):
        f = open(monkey_log)
        lines = f.read()
        exception = "Exception"
        crash = "CRASH"
        anr = "ANR"
        native_crash = 'Short Msg: Native crash'
        not_running = 'is your activity running'

        focus_on = "Bitmap"
        logcat_to_file = focus_on in lines
        if exception in lines or crash in lines:
            crash_result = lines[lines.index(crash) - 200:]
            crash_result = crash_result.replace('\n', '<br>')
            exception_handle(device_id, logcat_to_file)
            if check_key_word(crash_result, keyword):
                Sender.sendException(crash_result, sender, pwd, receivers, subject, logfile,
                                     browser, device, version)
                FunCom.log("monkey finished with exception")
            else:
                FunCom.log('monkey finished with system exception\n')
                FunCom.log('<<<<<<<<<<<<<<<<<<<<<\n' + crash_result)
        elif anr in lines:
            FunCom.log("monkey finished with anr")
            FunCom.log(lines[lines.index(anr):lines.index(anr) + 10000])
            crash_result = lines[lines.index(anr):lines.index(anr) + 200]
            crash_result = crash_result.replace('\n', '<br>')
            exception_handle(device_id, logcat_to_file)
            Sender.sendException(crash_result, sender, pwd, anr_receivers,
                                 subject.replace('Crash', 'ANR'),
                                 logfile, browser, device, version)
        elif native_crash in lines:
            exception_handle(device_id, logcat_to_file)
            FunCom.log('monkey finished with native crash')
        elif not_running in lines:
            FunCom.log('monkey finished with activity not running')

        f.close()
        FunCom.log('>>> monkey finished...\n\n')


def exception_handle(device_id, logcat_to_file=False):
    # if logcat_to_file:
    FunCom.log_cat_to_file(device_id)
    device_info = FunCom.parse_device_info(device_id)
    dir_to_store_logfile = FunCom.get_abspath(
        FunCom.path_join(Res.log_path,
                         device_info + Res.underline + Res.logcat_tag + FunCom.current_time()))
    FunCom.make_dir_if_not_exist(dir_to_store_logfile)
    FunCom.log('Exception handle id:' + device_id + " dir to store log::" + dir_to_store_logfile)
    FunCom.p_open(Res.asb_shell_pull_log_file(device_id, dir_to_store_logfile))


def check_key_word(crash_result, keyword):
    if len(keyword) == 1 and crash_result.count(keyword[0]) > 1:
        return True
    if len(keyword) > 1:
        for tmp in keyword:
            if crash_result.count(tmp) < 1:
                return False
        return True
    return False
