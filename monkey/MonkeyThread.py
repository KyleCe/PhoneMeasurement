import sys

sys.path.append('..')
import MonkeyFun as Mon
import FunctionCommon as Fun
import ConstResource as Res
import FunctionLauncher as FunLch


def monkey_work(device_id, app_name=Res.app_name):
    browser = app_name
    device = device_id

    conf = Fun.get_conf_parser(Res.monkey_conf_file)
    Fun.assert_options_presents(conf, ['mail', 'ftp', 'apk', 'monkey_params'])
    sender = conf.get('mail', 'sender')
    mail_pwd = conf.get('mail', 'pwd')
    subject = conf.get('mail', 'subject')
    receivers = conf.get('mail', 'receivers').split(',')
    anr_receivers = conf.get('mail', 'anr_receivers').split(',')
    pkg_name = conf.get('apk', 'package_name')
    subject = conf.get('apk', 'name') + subject
    keyword = conf.get('apk', 'keyword')
    events = conf.get('monkey_params', 'events')
    throttle = conf.get('monkey_params', 'throttle')

    apk_path = Fun.get_abspath(Res.apk_path)
    android_version = Fun.get_android_version(device_id)
    device_info = Fun.parse_device_info(device_id)
    logfile = Fun.get_abspath(Fun.path_join(Res.log_path, device_info + Res.log_suffix))

    package_installed_once = False
    Mon.push_lib_to_phone(device)

    while True:
        if not package_installed_once:
            try:
                # todo
                Mon.prepare_log_file_path_file(logfile)
                Mon.refresh_with_apk(device, apk_path, pkg_name, logfile, package_installed_once)
                package_installed_once = True

                # todo
                Mon.skip(device)
                start_monkey_and_analyze(android_version, anr_receivers, browser, device,
                                         device_info, events, keyword, logfile, mail_pwd, pkg_name,
                                         receivers, sender, subject, throttle)
            except Exception as e:
                Fun.log(e)
        else:

            # todo
            Fun.kill_monkey(device)

            # todo
            FunLch.start_launcher_omit_splash(device, False, False)
            Fun.sleep(2)
            start_monkey_and_analyze(android_version, anr_receivers, browser, device,
                                     device_info, events, keyword, logfile, mail_pwd, pkg_name,
                                     receivers, sender, subject, throttle)


def start_monkey_and_analyze(android_version, anr_receivers, browser, device, device_info, events,
                             keyword, logfile, mail_pwd, pkg_name, receivers, sender, subject,
                             throttle):
    Fun.kill_monkey(device)
    Mon.prepare_log_file_path_file(logfile)
    # todo
    Mon.start(device, pkg_name, events, throttle, logfile)
    try:
        Mon.log_trick(device, logfile, sender, mail_pwd, receivers
                      , anr_receivers, subject, logfile,
                      browser, device_info, android_version, keyword)
    except Exception as e:
        Fun.log(e)
