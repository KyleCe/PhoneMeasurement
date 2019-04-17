import ConstResource as Res
import FunctionCommon as FunCom
import FunctionPackage as FunPkg
from config import ConfigHelper as CfgU


def click_test():
    tags = FunCom.devices_list_with_connection_check()
    tag = tags[0]
    apk_files = FunPkg.get_apk_file_in_project()
    if len(apk_files) > 0:
        for f in apk_files:
            if str(f).endswith(Res.pgk_suffix):
                FunPkg.uninstall(tag, Res.pkg_name)
                FunPkg.install_r(tag, FunCom.get_abspath(f), True)
                break
    else:
        raise Exception("no apk found in project '/apk' directory, put one at least")
    FunCom.serial_clicks_by_control_file(tag)


def swipe_test():
    tags = FunCom.devices_list_with_connection_check()
    for tag in tags:
        FunCom.serial_operation_by_control_file(tag, '/case/%s.txt' % 'all_apps')


# click_test()
swipe_test()
