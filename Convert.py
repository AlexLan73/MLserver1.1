import threading
import time
import os, sys
import logging
import logging.config

from Core.ViewProces import *
from Core.LogFileSet import *
from Core.InArguments import *


# pyinstaller -F Convert.py

class StatDan:
    dan = dict()

    @staticmethod
    def add(name, d):
        StatDan.dan[name] = d

    @staticmethod
    def read( name):
        return StatDan.dan.get(name, "")


def inicial_logging():
    _path_log = StatDan.read("path_work")+"\\LOG"

    if not (os.path.isdir(_path_log)):
        os.mkdir(_path_log)

    dictLogConfig = logging_dict(_path_log)
    path_file_logger = dictLogConfig['handlers']["fileHandler"]["filename"]
    StatDan.add("path_file_logger", path_file_logger)

    logging.config.dictConfig(dictLogConfig)
    logger = logging.getLogger("exampleApp")
    logger.info("START")
    StatDan.add("logger", logger)

def error_run_log(t: tuple):
    print(" код -> {}  сообщение -> {}".format(t[0], t[1]))
    sys.exit(t[0])


def process_test():
    _process = ViewProces()
    _process.proces1()
    count, all_process, _ls = _process.find_process('chrome.exe')
    print("  кол-во запущенных программ {} ".format(count))
    for i, it in enumerate(all_process):
        print(" {}   {}".format(i, it))


def error_run(t: tuple):
    print(" код -> {}  сообщение -> {}".format(t[0], t[1]))
    sys.exit(t[0])


# ------------------------------------------
if __name__ == "__main__":
    print("Start Convert")

    _inArguments = InArguments()
    args = _inArguments(error_run)

    StatDan.add("path_work", args["dir_work"])
    StatDan.add("dir_start", args["dir_start"])

    inicial_logging()
    logger = StatDan.read("logger")

    logger.info("END нормальное завершение программы")
