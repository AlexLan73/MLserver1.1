import threading
import time
import os, sys
import logging
import logging.config
import time

from Core.ReadWrite import *
#from Core.ViewProces import *
from Core.LogFileSet import *
from Core.InArguments import *
from Core.ConfigDan import *
from Core.StatDan import *
from Core.DopConfig import *
from Core.ReadXml import *
from Core.LrfDec import *
from Core.CountInitialData import *
from Core.ConvertCLF import *
from Core.CLFJson import *
from Core.ALLClexport import *
#from Core.ConvertAll import *
from Core.Clexport import *


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


# def process_test():
#     _process = ViewProces()
#     _process.proces1()
#     count, all_process, _ls = _process.find_process('chrome.exe')
#     print("  кол-во запущенных программ {} ".format(count))
#     for i, it in enumerate(all_process):
#         print(" {}   {}".format(i, it))


def error_run(t: tuple):
    print(" код -> {}  сообщение -> {}".format(t[0], t[1]))
    sys.exit(t[0])


# ------------------------------------------
if __name__ == "__main__":
    print("Start Convert")

    _inArguments = InArguments()
    args = _inArguments(error_run)
#    _convert = ConvertAll(args["dir_start"], args["dir_work"])


    StatDan.__setItem__("path_work", args["dir_work"])
    StatDan.__setItem__("dir_start", args["dir_start"])
    StatDan.__setItem__("is_lrf", False)
    StatDan.__setItem__("is_convert_clf", False)

    _clf_json = CLFJson(StatDan.__getItem__("path_work") + "\\clf.json")
    StatDan.__setItem__("iclf_json", _clf_json)

    _countInitialData = CountInitialData(StatDan.__getItem__("path_work"))
    _is_rename = False  # True переименовать файлы False
    if _is_rename:
        _countInitialData.rename()
        sys.exit(0)

    inicial_logging()
    logger = StatDan.__getItem__("loggerConfig")

    _rw = ReadWrite(PathWork=StatDan.__getItem__("path_work"))

    _config = ConfigDan(PathConfig=StatDan.__getItem__("dir_start") + "\\mlserver.json")

    _dop_config = DopConfig(_rw)
    _config.set(_dop_config.CarName)

    _clf_json.set("LoggerConfig", _dop_config.NameLogger)
    _clf_json.write_json()

    _readxml = ReadXml(_dop_config.path_common, _dop_config.dir_analysis)

    StatDan.__setItem__("path_commonт", _dop_config.path_common)

    _infdec = LrfDec(_config.lrf_dec)
    _convertCLF = ConvertCLF()

    _infdec.start()  # _infdec.run()

    _convertCLF.start()  # _convertCLF.run1()

    i = -1
    while StatDan.__getItem__("is_lrf"):
        i += 1
        print(" {} -- * - * - * -".format(i))
        time.sleep(1)

    _convertCLF.join()

    _countInitialData.call()
    if _countInitialData.count <= 0:
        _countInitialData.del_initial_data()

    _clexport =  ALLClexport(_config.clexport, _readxml.siglog_config_basa)
#    _clexport.start()
#    _clexport.join()

    _key = "MDF"
    _key_prog = {_key: None}
    _export = _clexport.get_key_export(_key)
    _maxpool = 5
    _timewait =20

    for key, val in _key_prog.items():
            _key_prog[key] =  ClexportXX(_key, _export, _maxpool, _timewait)

    # запускаем поток
    for key, val in _key_prog.items():
        try:
            val.start()
        except:
            pass

    # ожидаем завершения потоков
    for key, val in _key_prog.items():
        try:
            val.join()
        except:
            pass


#    _clexportxx =  ClexportXX(_key, _export, _maxpool, _timewait)
#    _clexportxx.start()
#    _clexportxx.join()

    k = 1

    logger.info("END нормальное завершение программы")

    k = 1

