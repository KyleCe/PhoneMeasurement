import os

import sys
from xlwt import Workbook

import ConstResource as Res
import FunctionPackage as FunPkg
import FunctionCommon as FunCom
import time
import Modules as Modules


def access_to_electricity(tag, uid_info):
    info = Modules.BatteryInfo()
    info.end_time.append(FunCom.current_time())
    battery_info = FunCom.p_open(Res.adb_dump_battery(tag)).readlines()
    for ii in range(len(battery_info) - 1):
        if 'level:' in battery_info[ii]:
            battery_info_arr = battery_info[ii].split('  level: ')
            info.battery_percentage.append(battery_info_arr[1].strip())

    battery_detailed_info = FunCom.p_open(Res.adb_dump_battery_status(tag)).readlines()
    for i in range(len(battery_detailed_info) - 1):
        if 'Capacity:' in battery_detailed_info[i]:
            bat_info = battery_detailed_info[i].split(',')

            battery_capacity = bat_info[0].split('    Capacity: ')
            battery_computed_drain = bat_info[1].split(' Computed drain: ')
            info.battery_actual_drain = bat_info[2].split(' actual drain: ')
            info.capacity.append(int(battery_capacity[1].strip()))
            info.computed.append(float(battery_computed_drain[1].strip()))

        if 'Uid ' + str(uid_info) in battery_detailed_info[i]:
            num = battery_detailed_info[i].split(':')
            num = num[1].split('(')
            info.uid_item_info.append(float(num[0].strip()))
    return info


def arr_into_table(table, column, arr):
    for i in range(len(arr)):
        table.write(i + 1, column + 1, arr[i])


def write_data_into_excel(x, total_number_dalvik_size, dalvik_size, dalvik_alloc, app_map_name,
                          total_dalvik_size1,
                          dalvik_size1, dalvik_alloc1, first_time, end_time, levels, capacity,
                          computed, uid_item_info):
    book = Workbook(encoding='utf-8')
    table = book.add_sheet(Res.sheet_name)
    for r in range(6):
        table.write(0, r + 1, Res.sheet_row_arr[r])

    column_content_arr = [total_number_dalvik_size, dalvik_size, dalvik_alloc, total_dalvik_size1, dalvik_size1,
                          dalvik_alloc1, first_time, end_time, levels, capacity, computed,
                          uid_item_info]
    for c in range(len(column_content_arr)):
        arr_into_table(table, c, column_content_arr[c])
    book.save(str(app_map_name) + str(x) + Res.output_file_name)


def count_info(tag, total_number_dalvik_size, dalvik_size, dalvik_alloc):
    FunCom.sleep(15)
    mem_info = FunCom.p_open('adb -s ' + tag + '  shell dumpsys mem_info  com.kcg.com.fun').readlines()
    for info_item in mem_info:
        if 'Dalvik Heap' in info_item:
            info_item_info_arr = info_item.split('   ')
            if len(info_item_info_arr) > 4:
                total_number_dalvik_size.append(info_item_info_arr[1])
                dalvik_size.append(info_item_info_arr[-3])
                dalvik_alloc.append(info_item_info_arr[-2])
                FunCom.log(str(info_item_info_arr[1]) + '===============')


def count_info_first(tag, total_dalvik_size1, dalvik_size1, dalvik_alloc1):
    for i in range(10):
        FunCom.p_open('adb -s ' + tag + '  shell am dumpheap com.kcg.com.fun /sdcard/click_test.hprof ')
        FunCom.sleep(2)
        FunCom.p_open('adb -s ' + tag + '  shell dumpsys mem_info  com.kcg.com.fun')
        FunCom.sleep(2)
    FunCom.sleep(20)
    FunCom.p_open('adb -s ' + tag + '  shell dumpsys mem_info  com.kcg.com.fun')
    mem_info = FunCom.p_open('adb -s ' + tag + '  shell dumpsys mem_info  com.kcg.com.fun').readlines()
    for info_item in mem_info:
        if 'Dalvik Heap' in info_item:
            info_item_info_arr = info_item.split('   ')
            if len(info_item_info_arr) > 4:
                total_dalvik_size1.append(info_item_info_arr[1])
                dalvik_size1.append(info_item_info_arr[-3])
                dalvik_alloc1.append(info_item_info_arr[-2])

                FunCom.log(str(info_item_info_arr[1]) + '-------------------')


def memory_instrument_main():
    number = sys.argv[1]
    # number=10
    x = 0
    app_map = FunPkg.get_apk_file_in_project()
    while True:
        apk_path = os.getcwd()
        devices_info = FunCom.connected_devices_arr()
        devices_num = len(devices_info)
        if devices_num > 0:
            tag = devices_info[0]
        for app_map_item in range(len(app_map)):
            try:
                total_number_dalvik_size = []
                dalvik_size = []
                dalvik_alloc = []
                first_time = []
                end_time = []
                levels = []
                capacity = []
                computed = []
                uid_item_info = []
                app_map_name = app_map[app_map_item]
                total_dalvik_size1 = []
                dalvik_size1 = []
                dalvik_alloc1 = []
                app_map_name_path = apk_path + "/apk/" + app_map_name.strip()
                FunCom.log(app_map_name_path)
                FunPkg.uninstall(tag, Res.pkg_name)
                FunPkg.install(tag, app_map_name_path)
                FunCom.sleep(10)
                for i in range(500):
                    FunCom.serial_clicks_by_control_file(tag)
                    FunCom.p_open('adb -s ' + tag + ' shell dumpsys battery unplug')
                    count_info_first(tag, total_dalvik_size1, dalvik_size1, dalvik_alloc1)
                    datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    first_time.append(datetime)

                    uid_info = FunCom.get_device_uid(tag)

                    FunCom.p_open('adb -s ' + tag + ' shell ' + 'dumpsys batterystats  --reset')

                    FunCom.serial_operation_by_control_file(tag)
                    FunCom.log('------')
                    access_to_electricity(tag, end_time, levels, capacity, computed, uid_item_info, uid_info)

                    count_info(tag, total_number_dalvik_size, dalvik_size, dalvik_alloc)

                    if total_number_dalvik_size[i] < total_dalvik_size1[i]:
                        total_dalvik_size1.pop(i)
                        total_number_dalvik_size.pop(i)
                        dalvik_size.pop(i)
                        dalvik_size1.pop(i)
                        dalvik_alloc1.pop(i)
                        dalvik_alloc.pop(i)
                        first_time.pop(i)
                        end_time.pop(i)
                        levels.pop(i)
                        capacity.pop(i)
                        computed.pop(i)
                        uid_item_info.pop(i)

                    write_data_into_excel(x, total_number_dalvik_size, dalvik_size, dalvik_alloc, app_map_name,
                                          tag,
                                          total_dalvik_size1, dalvik_size1, dalvik_alloc1, first_time, end_time, levels,
                                          capacity,
                                          computed, uid_item_info)

                    FunPkg.clear(tag)
                    if len(total_number_dalvik_size) == int(number):
                        break
                x += 1
            except Exception as e:
                FunCom.log(e)
        if app_map_item == len(app_map) - 1:
            app_map_item == 0


def perform_operations(tag, uid_info, x, app_file):
    FunCom.p_open(Res.adb_dump_battery_status_reset(tag))
    FunCom.serial_operation_by_control_file(tag)

    battery_info = access_to_electricity(tag, uid_info)
    FunCom.sleep(5)
    write_data_into_excel(battery_info, x, app_file)


def write_the_data(data_time_map, data_time_map_begin, battery_percentage, capacity_map, computed_drain_map,
                   battery_actual_drain_map, carried_out_what, uid_detailed_info_map, uid_detailed_num_map, x,
                   app_map_name):
    times_num = 0
    f = Workbook(encoding='utf-8')
    table = f.add_sheet('Sheet')
    table.write(0, 0, u'time')
    table.write(0, 1, u'end_time')
    table.write(0, 2, u'levels')
    table.write(0, 3, u'Capacity')
    table.write(0, 4, u'Computed drain')
    # table.write(0, 5, u'actual drain')
    table.write(0, 5, u'steps')
    table.write(0, 6, u'UID')

    for times_num in range(len(data_time_map)):
        table.write(times_num + 1, 0, data_time_map[times_num])
    for times_nums in range(len(data_time_map_begin)):
        table.write(times_nums + 1, 1, data_time_map_begin[times_nums])
    for per_num in range(len(battery_percentage)):
        table.write(per_num + 1, 2, battery_percentage[per_num])
    for cap_num in range(len(capacity_map)):
        table.write(cap_num + 1, 3, capacity_map[cap_num])
    for cop_num in range(len(computed_drain_map)):
        table.write(cop_num + 1, 4, computed_drain_map[cop_num])
    # for bad_num in range(len(battery_actual_drain_map)):
    #     table.write(bad_num+1,5,battery_actual_drain_map[bad_num])
    for cow_num in range(len(carried_out_what)):
        table.write(cow_num + 1, 5, carried_out_what[cow_num])
    for udi_num in range(len(uid_detailed_info_map)):
        table.write(udi_num + 1, 6, uid_detailed_info_map[udi_num])

    f.save(str(app_map_name) + str(x) + 'dage.xlsx')


def battery_instrument_main():
    FunCom.log('launch battery instrument ')
    x = 0
    while True:
        for app_file in FunPkg.get_apk_file_in_project():
            try:
                tag = FunCom.devices_list_with_connection_check()[0]
                FunCom.p_open(Res.adb_dump_battery_unplug(tag))
                FunCom.send_key_home(tag)
                FunPkg.uninstall_and_install(tag, app_file, Res.pkg_name)
                FunCom.serial_clicks_by_control_file(tag)
                FunCom.sleep(20)
                perform_operations(tag, FunCom.get_device_uid(tag), x, app_file)
                x += 1
            except Exception as e:
                FunCom.log(e)
