# -*- coding:utf-8 -*-
import os
import sys
import getopt


def getcpuritio(times, package):
    print 'reading mitop lines...'
    cpuinfo = os.popen("adb shell mitop -n %d" % times).readlines()

    bro_cpu = []
    cpu_taking = []
    for line in cpuinfo:
        val_list = line.split()
        if val_list.__len__() > 4 and val_list[4] != 'CPU':
            cpu_taking.append(int(val_list[4]))
        if package in line:
            if package == val_list[val_list.__len__() - 1]:
                bro_cpu.append(int(val_list[4]))

    print
    print "====below is result of parsing CMD: 'adb shell mitop -n %d'====" % times
    print
    print 'Among %d times, the %s found count: %d' % (times, package, len(bro_cpu))
    print 'mitop-cpu coefficient of %s : %.2f' % (package, float(len(bro_cpu) / float(times)))
    ratio = float(sum(bro_cpu)) / float(sum(cpu_taking))
    print 'average cpu usage of %s in top processes is: %.3f' % (package, ratio)


def main(argv):
    times = ''
    package = ''
    try:
        opts, args = getopt.getopt(argv[1:], "ht:p:", ["times=", "package="])
        # print  "opts:"+str(opts),"args:"+str(args[1])
    except getopt.GetoptError:
        print 'usage: cputatio.py -t times -p packagename \neg. cputatio.py -t 50 -p com.android.browser '
        sys.exit(2)
    if len(opts) != 2:
        print 'usage: cputatio.py -t times -p packagename \neg. cputatio.py -t 50 -p com.android.browser '
        sys.exit(2)
    for opt, arg in opts:
        # print opt,arg
        if opt == '-h':
            print 'usage: cputatio.py -t times -p packagename \neg. cputatio.py -t 50 -p com.android.browser '
            sys.exit()
        elif opt in ("-t", "--times"):
            times = arg
        elif opt in ("-p", "--package"):
            package = arg
    getcpuritio(int(times), package)


if __name__ == "__main__":
    main(sys.argv)
    # getcpuritio(int(2), 'com.xiaomi.mipicks')
