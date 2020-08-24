import logging
import logging.config
import sys

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

    _scenario.run_scenario()

#    print("+"*40,"\n","+"*15," END  ","+"*15)


