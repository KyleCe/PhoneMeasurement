import threading

from util import WifiKeeper
from util import StatusBarCover
from monkey import MonkeyThread
from core import MultiProcess


def keep_status_bar_cover_alive(dev):
    """
    keep sending 'turn on status bar cover' broadcast, for the cover effect is not very perfect
    :param dev: device id to process
    :return: None
    """
    StatusBarCover.switch_cover(dev, True)
    threading.Timer(5, keep_status_bar_cover_alive, [dev]).start()


def main_process(*args):
    # todo
    dev = args[0]
    WifiKeeper.start_wifi_keeper(dev, True)
    StatusBarCover.start_status_bar_cover(dev, True)
    keep_status_bar_cover_alive(dev)
    MonkeyThread.monkey_work(dev)


if __name__ == '__main__':
    MultiProcess.run(main_process, False)
