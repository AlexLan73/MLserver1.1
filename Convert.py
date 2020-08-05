import logging.config
import sys

from Core.Clexport import *
from Core.InArguments import *
from Core.LogFileSet import *
from Core.Scenario import *
from Core.StatDan import *


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


def error_run(t: tuple):
    print(" код -> {}  сообщение -> {}".format(t[0], t[1]))
    sys.exit(t[0])


# ------------------------------------------
if __name__ == "__main__":
    print("Start Convert")

    _inArguments = InArguments()
    args = _inArguments(error_run)

    StatDan.__setItem__("path_work", args["dir_work"])
    StatDan.__setItem__("dir_start", args["dir_start"])
    StatDan.__setItem__("is_lrf", False)
    StatDan.__setItem__("is_convert_clf", False)

    # переименовываем вайлы  -  для теста
    _is_rename = False  # True переименовать файлы False
    if _is_rename:
        _countInitialData = CountInitialData(StatDan.__getItem__("path_work"))

        _countInitialData.rename()
        sys.exit(0)

    inicial_logging()

    _scenario = Scenario()

    _scenario.thread_inicial.join()
    # _scenario.thread_read_info.join()

    f1_type_int = lambda x: x[0] if "tuple" in str(type(x)) else x

    if f1_type_int(_scenario.dan_scenario["original"]) > 0:
        # запускаем конвертацию  LrfDec
        _scenario.convert_LrfDec()

    _scenario.convert_LrfDec__.join()

    sys.exit(-111110)

    kk = 1

    # StatDan.__setItem__("path_work", args["dir_work"])
    # StatDan.__setItem__("dir_start", args["dir_start"])
    # StatDan.__setItem__("is_lrf", False)
    # StatDan.__setItem__("is_convert_clf", False)

    # _clf_json = CLFJson(StatDan.__getItem__("path_work") + "\\clf.json")
    # StatDan.__setItem__("iclf_json", _clf_json)

    # _countInitialData = CountInitialData(StatDan.__getItem__("path_work"))
    # _is_rename = False  # True переименовать файлы False
    # if _is_rename:
    #     _countInitialData.rename()
    #     sys.exit(0)
    #
    # inicial_logging()
    # logger = StatDan.__getItem__("loggerConfig")

    # _rw = ReadWrite(PathWork=StatDan.__getItem__("path_work"))
    #
    # _config = ConfigDan(PathConfig=StatDan.__getItem__("dir_start") + "\\mlserver.json")

    # _dop_config = DopConfig(_rw)
    # _config.set(_dop_config.CarName)
    #
    # _clf_json.set("LoggerConfig", _dop_config.NameLogger)
    # _clf_json.write_json()
    #
    # _readxml = ReadXml(_dop_config.path_common, _dop_config.dir_analysis)
    #
    # StatDan.__setItem__("path_commonт", _dop_config.path_common)

    #     _infdec = LrfDec(_config.lrf_dec)
    #     _infdec.start()  # _infdec.run()
    #
    # #    StatDan.__setItem__("is_lrf", True)
    #
    #     _convertCLF = ConvertCLF()
    #
    #     _is_uprav = True
    #     _time = TimeWait(20, _is_uprav)
    #     _time.set()
    #
    #     while True:
    #         if len(list(Path(StatDan.__getItem__("path_work")).glob("*.clf")))>0:
    #             break
    #
    #         time.sleep(0.5)
    #         if not _time.is_uprav:
    #             print("Нет данных CLF")
    #             sys.exit(-10)
    #
    #     _convertCLF.start()  # _convertCLF.run1()

    # i = -1
    # while StatDan.__getItem__("is_lrf"):
    #     i += 1
    #     print(" {} -- * - * - * -".format(i))
    #     time.sleep(1)

    #    _convertCLF.join()
    #
    #     _countInitialData.call()
    #     if _countInitialData.count <= 0:
    #         _countInitialData.del_initial_data()

    _clexport = ALLClexport(_config, _readxml.siglog_config_basa)
    _clexport.start()

    _infdec.join()  # _infdec.run()

    _convertCLF.join()  # _convertCLF.run1()

    _clexport.join()

    k = 1

    logger.info("END нормальное завершение программы")
