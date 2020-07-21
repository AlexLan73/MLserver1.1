import threading
import time
import os, sys
import logging
import logging.config

from Core.ReadWrite import *
from Core.ViewProces import *
from Core.LogFileSet import *
from Core.InArguments import *
from Core.ConfigDan import *
from Core.StatDan import *
from Core.DopConfig import *
from Core.ReadXml import *
from Core.LrfDec import *
from Core.CountInitialData import *


# pyinstaller -F Convert.py

def inicial_logging():
    _path_log = StatDan.__getItem__("path_work") + "\\LOG"

    if not (os.path.isdir(_path_log)):
        os.mkdir(_path_log)

    dictLogConfig = logging_dict(_path_log)
    path_file_logger = dictLogConfig['handlers']["fileHandler"]["filename"]
    StatDan.__setItem__("path_file_logger", path_file_logger)

    logging.config.dictConfig(dictLogConfig)
    logger = logging.getLogger("exampleApp")
    logger.info("START")
    StatDan.__setItem__("logger", logger)


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

    # StatDan.add("path_work", args["dir_work"])
    # StatDan.add("dir_start", args["dir_start"])
    StatDan.__setItem__("path_work", args["dir_work"])
    StatDan.__setItem__("dir_start", args["dir_start"])
    StatDan.__setItem__("is_lrf", args[False])


    _countInitialData = CountInitialData(StatDan.__getItem__("path_work"))
    _is_rename = False  #  True переименовать файлы False
    if _is_rename:
        _countInitialData.rename()
        sys.exit(0)


#    _countInitialData.test_null()
#    _countInitialData.call()
#    _countInitialData.del_initial_data()


    inicial_logging()
    logger = StatDan.__getItem__("logger")

    _rw = ReadWrite(PathWork= StatDan.__getItem__("path_work"))

    _config = ConfigDan(PathConfig= StatDan.__getItem__("path_work") + "\\mlserver.json")

    _dop_config = DopConfig(_rw)
    _config.set(_dop_config.CarName)


    _readxml = ReadXml(_dop_config.path_common, _dop_config.dir_analysis)

    StatDan.__setItem__("path_commonт", _dop_config.path_common)

    _infdec  = LrfDec(_config.lrf_dec)
    _infdec.run()


    logger.info("END нормальное завершение программы")


    k = 1

#
# def set_dir(rwserver, config):
#     name_config = rwserver.file_config_from_ml_rt()
#     rwserver.path_name_Configuration(name_config[0])
#
#     maska_zip = "Analysis.gla"
#     d0, d_err = rwserver.read_xml_dan(rwserver.dir_analysis+"\\"+maska_zip)
#     s = rwserver.convert_to_ini(dan=d0, dan_err=d_err, path=rwserver.dir_analysis)
#
#     siglog_config_basa = rwserver.ReadTextBasa0(rwserver.path_common+"\\DLL\\"+"siglog_config.ini")
#     siglog_config_basa+=[s]
#     rwserver.copy_to_dir(siglog_config_basa)
#
#     rwserver.copy_siglog_vsysvar(d_err)
