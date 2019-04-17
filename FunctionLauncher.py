import ConstResource as Res
import FunctionCommon as Fun


def start_launcher_omit_splash(d, omit_splash=True, back_press=True):
    if omit_splash:
        Fun.p_open(Res.asb_shell_start_activity(d))
        Fun.sleep(Res.pkg_init_delay)
        Fun.p_open(Res.asb_shell_force_stop(d))
    Fun.p_open(Res.asb_shell_start_activity(d))
    if back_press:
        for i in range(5):
            Fun.sleep(3)
            Fun.p_open(Res.adb_key_event_back(d))
