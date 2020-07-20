

import threading
import time
import  os, sys
import logging
import logging.config

from Core.ViewProces import *
from Core.LogFileSet  import *
from Core.InArguments  import *

# pyinstaller -F Convert.py

class AllDan:
    def __init__(self):
        pass

def inicial_logging(_dan:AllDan):
    pass
    # _path_log = _dan.path_file_logger
    #
    # if not (os.path.isdir(_path_log)):
    #     os.mkdir(_path_log)
    #
    # dictLogConfig = logging_dict(_path_log)
    # path_file_logger = dictLogConfig['handlers']["fileHandler"]["filename"]
    #
    # logging.config.dictConfig(dictLogConfig)
    # logger = logging.getLogger("exampleApp")
    # logger.info("START")

def process_test():
    _process = ViewProces()
    _process.proces1()
    count, all_process, _ls = _process.find_process('chrome.exe')
    print("  кол-во запущенных программ {} ".format(count))
    for i, it in enumerate(all_process):
        print(" {}   {}".format(i, it))


def error_run(t:tuple):
    print(" код -> {}  сообщение -> {}".format(t[0], t[1]))
    sys.exit(t[0])

if __name__ == "__main__":
    print("Start Convert")
    _all_dan = AllDan()
    _inArguments = InArguments()
    args = _inArguments(error_run)
    path_work = args["ls"]
    k=1


    # print(_inArguments["s_error"] )
    #
    #
    #
    #         elif _args["kod_error"] ==-3:
    #             print(_args["s_error"] )
    #             fprint(_args["ls_arg"])
    #             path_file_logger = _args["dir_start"]
    #             _dan=AllDan()
    #             inicial_logging(_dan)
    #             # for it in _args["ls_arg"]:
    #             #     logger.info(it)
    #             # logger.critical(_args["s_error"])
    #             sys.exit(_args["kod_error"])
    #



# def parse_input_arguments(_dan:AllDan, ferror):
#     name_file_run = __file__  # путь старта программы
#     _dargs = dict(
#         s_error="Ok!",
#         kod_error=0,
#         dir_start="",
#         dir_work="",
#         ls_arg=[]
#     )
#
#     ls_arg = sys.argv
#     k = 0
#
#     for it in ls_arg:
#         _s = " Номер аргумента -{} значение ->  {} ".format(k, it)
#         print(_s)
#         _dargs["ls_arg"] += [_s]
#         k += 1
#
#     if len(ls_arg) < 2:
#         _dargs["kod_error"] = -1
#         _dargs["s_error"] = " нет  аргументов  код -1"
#         print(_dargs["s_error"])
#         return _dargs
#
#     _dargs["dir_start"] = os.path.dirname(ls_arg[0])
#     if not (os.path.isdir(_dargs["dir_start"])):
#         _dargs["kod_error"] = -2
#         _dargs["s_error"] = "Не правильно определился каталог старта програмы  код -2"
#         return _dargs
#
#     _dargs["dir_work"] = ls_arg[1]
#     if not (os.path.isdir(_dargs["dir_work"])):
#         _dargs["kod_error"] = -3
#         _dargs["s_error"] = "Нет директории с данными код -3"
#         return _dargs
#
#     return _dargs
#
