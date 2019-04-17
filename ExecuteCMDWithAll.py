# -*- coding:utf-8 -*-
import os
import sys
import getopt

import ConstResource as Res
import FunctionCommon as Fun
import FunctionCommon as FunCom
import FunctionLauncher as FunLch
import GrabDump as Grab
from threading import Thread

debug = True
collect_period = 5 * 60 if debug else 5 * 60 * 60  # 5 hour
collect_info_internal = 60 if debug else 30 * 60  # 30 min
collect_times = 2 if debug else 10 - 1  # collect_period / collect_info_internal


def main_process(cmd):
    devices = Fun.devices_list_with_connection_check()
    if len(devices) == 0:
        Fun.log('no device connected')
        sys.exit(2)
    for dev in devices:
        Thread(target=collect_dump_info, args=(dev, cmd)).start()


def collect_dump_info(dev, cmd):
    Fun.log('start thread for device:' + dev)
    FunCom.serial_operation_by_control_file(dev, '/case/%s.txt' % 'all_apps')


def main(argv):
    cmd = ''
    try:
        opts, args = getopt.getopt(argv, "hc:", ["cmd="])
    except getopt.GetoptError:
        print '*.py -c <cmd>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print '*.py -c <cmd>'
            sys.exit()
        elif opt in ("-c", "--cmd"):
            cmd = arg
    main_process(cmd)


if __name__ == '__main__':
    main(sys.argv[1:])
