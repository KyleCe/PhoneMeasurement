# coding=utf-8
import os

# base
current_path = os.getcwd()
project_path = os.path.dirname(os.path.abspath(__file__))
project_root_path = os.path.abspath(os.path.dirname(__file__))
new_line = '\n'
new_line_r = '\r'
new_line_nr = '\n\r'
split_mark = ','
linux_sep = '/'
comment_mark = '#'
underline = '_'
white_space = ' '
comment_marks = ['~', '!', '@', comment_mark, '$', '%', '^', new_line]
time_format = "%Y-%m-%d-%H-%M-%S"
splash_file = '/splash/splash.txt'
case_file_pattern = '/case/%s.txt'
case_file = '/case/case.txt'
config_path = '/config/config.txt'
parsed_device_info_file_path = '/sdcard'
parsed_device_info_file = 'phone_info.ini'
key_navigation_bar_height = 'navigation_bar_height'
key_display_size_x = 'display_size_x'
key_display_size_y = 'display_size_y'
standard_size_a = 1080
standard_size_b = 1920
config_dir = './config'
monkey_conf_file = 'monkey.ini'
monkey_target_key_word_opt = 'target_key_word'
monkey_target_key_word_key = 'pkg_key'
monkey_target_not_found = 'no available apk found for installation'
output_path = './output'
phone_info_dir = '/phone_info'
phone_info_dir_name = 'phone_info'
output_clean_path = '/output'
output_path_name = 'output'
apk_path = './apk'
util_path = './util'
dump = 'dump'
txt_suffix = '.txt'
config_split = '='
ck_dump_name = 'dump_name'
ck_path = 'path'
ck_process = 'process'
root_dir = '/apk/'
pgk_suffix = '.apk'
hprof_suffix = '.hprof'
convert_suffix = '_conv' + hprof_suffix
log_path = 'log'
lib_path = 'lib'
monkey_lib_file_name = 'AutoTest.jar'
log_suffix = '.log'
logcat_tag = 'logcat_'
logcat_suffix = '.logcat'
path_suffix = '.path'
bluetooth = 'bluetooth_'
sleep_open = True
output_file_name = 'result.xlsx'
sheet_name = 'Sheet'
sheet_row_arr = [u'Dalvik Heap total', u'Dalvik Heap Size', u'Dalvik Alloc Size',
                 u'Dalvik Heap total', u'Dalvik Heap Size', u'Dalvik Alloc Size']

# package
pkg_name = 'com.kcg.com.fun'
activity_name = pkg_name + '/.fun'
app_name = 'Launcher'

# time control
pkg_init_delay = 20
default_delay_in_click = .2
default_delay_in_action = .5

# action in 'splash.txt' file
action_start = 'start'
action_next = 'next'
action_enable_now = 'enable_now'
action_kcg_launcher = 'kcg_launcher'
action_always = 'always'
action_start_index = 0
action_next_index = 1
action_enable_now_index = 2
action_kcg_launcher_index = 3
action_always_index = 4

# action in case file
case_display_config = 'display_config'
action_swipe = 'swipe'
action_hold = 'hold'
action_click = 'click'
action_home = 'home'
action_back = 'back'
action_wait = 'wait'
special_mode = 'special_mode'
special_start = 'start'
special_stop = 'stop'
special_clear_data = 'clear_data'
special_clear_logcat = 'clear_logcat'
special_invoke_watcher = 'invoke_watcher'
special_start_command = 'start_command'
special_stop_command = 'stop_command'
action_uninstall = 'uninstall'
action_install = 'install'
action_install_r = 'install_r'
action_reboot = 'reboot'

# delay index
delay_index_zero_point = 1
delay_index_1_param = 2
delay_index_one_point = 3
delay_index_two_point = 5

# command
rm = 'rm '
mk_file = 'echo nul > '
chmod = 'chmod 777 '
adb = 'adb'
adb_s = 'adb -s '
install = ' install '
install_r = ' install -r '
uninstall = ' uninstall '
shell_reboot = ' reboot '
shell_start = ' shell am start -n ' + activity_name
shell_clear = ' shell pm clear ' + pkg_name
shell_input_tap = ' shell input tap  %d  %d '
shell_swipe = ' shell  input swipe  %s  %s  %s  %s '
shell_touch_swipe = ' shell input touchscreen swipe  %s  %s  %s  %s %s'
shell_touch_delay = 1200
key_event_home = '3'
key_event_back = '4'
shell_key_event = ' shell input keyevent '
shell_dump_battery = ' shell dumpsys battery'
shell_dump_battery_unplug = ' shell dumpsys battery unplug'
shell_dump_battery_status = ' shell  dumpsys batterystats ' + pkg_name
shell_dump_battery_status_reset = ' shell dumpsys batterystats  --reset'
shell_ps_grep = ' shell ps |grep ' + pkg_name
shell_grab_dump = ' shell am dumpheap '
shell_pull_dump_file = ' pull '
shell_convert_heap_profile = 'hprof-conv '
shell_get_product_model = ' shell getprop ro.product.model'
shell_get_bluetooth_address = ' shell settings get secure bluetooth_address'
shell_start_activity_command = ' shell am start -n '
shell_start_activity = shell_start_activity_command + activity_name
shell_force_stop = ' shell am force-stop %s'
shell_clear_data = ' shell pm clear %s'
shell_clear_logcat = ' logcat -c'
shell_dump_mem_info = ' shell dumpsys meminfo ' + pkg_name
shell_android_version = ' shell getprop ro.build.version.release'
# shell_android_version = '''echo version=$(adb shell getprop |awk -F":"
# '/build.version.release/ { print $2 }')|tr -d '[]' '''

# monkey
shell_find_kcg_launcher = ' shell  uiautomator  runtest  AutoTest.jar  -c  util.find_kcg_launcher '
shell_click_menu = ' shell  uiautomator  runtest  AutoTest.jar  -c  util.click_menu '
shell_setting_complete = ' shell  uiautomator  runtest  AutoTest.jar  -c  util.settingcomplete '
shell_monkey_with_s = ' shell monkey -p %s  -v  %s  --pct-trackball 0 --pct-nav 0 ' \
                      ' --pct-majornav 0 --pct-syskeys 0 --pct-anyevent 0 --throttle %s ' \
                      ' --ignore-security-exceptions –monitor-native-crashes > %s '
shell_grep_monkey = ' shell ps|grep monkey'
shell_kill_process = ' shell kill '
shell_list_packages = ' shell pm list packages | grep '
shell_logcat_to_file = ' logcat -d > '
shell_push_file = ' push %s /data/local/tmp'
app_log_path = '/sdcard/Android/data/com.kcg.com.fun/files/logs'
shell_pull_log_file = ' pull %s %s'
shell_broadcast_with_action = ' shell am broadcast -a %s'

# windows not support the grep/ awk command
shell_orientation = ' shell dumpsys input | grep \'SurfaceOrientation\' | awk \'{ print $2 }\''
shell_screen_size = ' shell dumpsys window | grep cur= |tr -s " " | cut -d " " -f 4|cut -d "=" -f 2'


def adb_s_tag_prefix(tag):
    return adb_s + str(tag)


def adb_start_launcher(tag):
    return adb_s_tag_prefix(tag) + shell_start


def command_tap_suffix(x, y):
    return shell_input_tap % (int(x), int(y))


def command_swipe_suffix(from_x, from_y, to_x, to_y):
    return shell_swipe % (int(from_x), int(from_y), int(to_x), int(to_y))


def command_touchscreen_swipe_suffix(from_x, from_y, to_x, to_y, delay):
    return shell_touch_swipe % (int(from_x), int(from_y), int(to_x), int(to_y), delay)


def adb_tap_with_tag(tag, x, y):
    return adb_s_tag_prefix(tag) + command_tap_suffix(x, y)


def adb_swipe_with_tag(tag, from_x, from_y, to_x, to_y):
    return adb_s_tag_prefix(tag) + command_swipe_suffix(from_x, from_y, to_x, to_y)


# swipe on location to simulate long press
def adb_touch_screen_with_tag(tag, x, y):
    return adb_s_tag_prefix(tag) + command_touchscreen_swipe_suffix(x, y, x, y, shell_touch_delay)


def adb_key_event_home(tag):
    return adb_s_tag_prefix(tag) + shell_key_event + key_event_home


def adb_key_event_back(tag):
    return adb_s_tag_prefix(tag) + shell_key_event + key_event_back


def adb_dump_battery(tag):
    return adb_s_tag_prefix(tag) + shell_dump_battery


def adb_dump_battery_unplug(tag):
    return adb_s_tag_prefix(tag) + shell_dump_battery_unplug


def adb_dump_battery_status(tag):
    return adb_s_tag_prefix(tag) + shell_dump_battery_status


def adb_dump_battery_status_reset(tag):
    return adb_s_tag_prefix(tag) + shell_dump_battery_status_reset


def adb_ps_grep(tag):
    return adb_s_tag_prefix(tag) + shell_ps_grep


def adb_grab_heap_dump_file(tmp_path):
    return adb_shell_grab_dump_with_pkg(pkg_name) + white_space + tmp_path


def adb_grab_heap_dump_file_with_pkg(tag, tmp_path, pkg):
    return adb_shell_grab_dump_with_pkg(tag, pkg) + white_space + tmp_path


def adb_pull_heap_file_to_dest(tag, tmp_path, dest_path):
    return adb_s_tag_prefix(
        tag) + shell_pull_dump_file + white_space + tmp_path + white_space + dest_path


def adb_convert_heap_profile(tmp_path, dest_path):
    return shell_convert_heap_profile + white_space + tmp_path + white_space + dest_path


def adb_shell_grab_dump_with_pkg(tag, pkg):
    return adb_s_tag_prefix(tag) + shell_grab_dump + pkg


def adb_shell_send_click_broadcast():
    return adb_shell_send_click_broadcast_with_pkg(pkg_name)


def adb_shell_send_click_broadcast_with_pkg(pkg):
    return 'adb shell am broadcast -a ' + pkg + '".action.clickapp" -f 0x10000000'


def assemble_config(key, value):
    return key + config_split + value


def asb_shell_get_model(tag):
    return adb_s_tag_prefix(tag) + shell_get_product_model


def asb_shell_get_bluetooth_address(tag):
    return adb_s_tag_prefix(tag) + shell_get_bluetooth_address


def start_activity_str(activity):
    return shell_start_activity_command + activity


def asb_shell_start_activity(tag, act_name=activity_name):
    return adb_s_tag_prefix(tag) + start_activity_str(act_name)


def asb_shell_force_stop(tag, pkg=pkg_name):
    return adb_s_tag_prefix(tag) + shell_force_stop % pkg


def asb_shell_clear_data(tag, pkg=pkg_name):
    return adb_s_tag_prefix(tag) + shell_clear_data % pkg


def asb_shell_clear_logcat(tag):
    return adb_s_tag_prefix(tag) + shell_clear_logcat


def asb_shell_dump_mem_info(tag):
    return adb_s_tag_prefix(tag) + shell_dump_mem_info


def asb_shell_find_kcg_launcher(tag):
    return adb_s_tag_prefix(tag) + shell_find_kcg_launcher


def asb_shell_click_menu(tag):
    return adb_s_tag_prefix(tag) + shell_click_menu


def asb_shell_setting_complete(tag):
    return adb_s_tag_prefix(tag) + shell_setting_complete


def asb_shell_start_monkey_with_s(tag):
    return adb_s_tag_prefix(tag) + shell_monkey_with_s


def asb_shell_android_version(tag):
    return adb_s_tag_prefix(tag) + shell_android_version


def asb_shell_grep_monkey(tag):
    return adb_s_tag_prefix(tag) + shell_grep_monkey


def asb_shell_kill_process(tag, pid):
    return adb_s_tag_prefix(tag) + shell_kill_process + pid


def asb_shell_list_packages(tag, pkg):
    return adb_s_tag_prefix(tag) + shell_list_packages + pkg


def asb_shell_logcat_to_file(tag, file_full_path):
    return adb_s_tag_prefix(tag) + shell_logcat_to_file + file_full_path


def asb_shell_push_file(tag, file_to_push):
    return adb_s_tag_prefix(tag) + (shell_push_file % file_to_push)


def asb_shell_pull_log_file(tag, path_to_store, sour_path=app_log_path):
    return adb_s_tag_prefix(tag) + (shell_pull_log_file % (sour_path, path_to_store))


def asb_shell_broadcast(tag, action):
    return adb_s_tag_prefix(tag) + (shell_broadcast_with_action % action)


def adb_orientation(tag):
    return adb_s_tag_prefix(tag) + shell_orientation


def adb_screen_size(tag):
    return adb_s_tag_prefix(tag) + shell_screen_size


def adb_reboot(tag):
    return adb_s_tag_prefix(tag) + shell_reboot
