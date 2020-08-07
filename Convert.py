import logging.config
import sys

from Core.Clexport import *
from Core.InArguments import *
from Core.LogFileSet import *
from Core.Scenario import *
from Core.StatDan import *

# pyinstaller -F Convert.py

logger = dict()


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

    f1typeint = lambda x: x[0] if "tuple" in str(type(x)) else x

    if f1typeint(_scenario.dan_scenario["original"]) > 0:
        # запускаем конвертацию  LrfDec
        _scenario.convert_LrfDec()
    elif f1typeint(_scenario.dan_scenario["work_dir_clf"]) > 0:
        # запускаем конвертацию  LrfDec
        _scenario.convert_CLF()

    xtime_wait_files_dir_clf = _scenario.dan_scenario["ind"]
    while (_scenario.dan_scenario["ind"] - xtime_wait_files_dir_clf) <= 30:
        if f1typeint(_scenario.dan_scenario["CLF_dir_clf"]) > 0:
            _scenario.allclexport()
            break

    try:
        _scenario.convert_LrfDec__.join()
    except AttributeError:
        pass

    try:
        _scenario.convertCLF__.join()
    except AttributeError:
        pass

    _scenario.set_off_stop_read_info()

    try:
        _scenario.clexport__.join()
    except AttributeError:
        pass

    _scenario.logger.info("END нормальное завершение программы")
    k=1
    sys.exit(0)
