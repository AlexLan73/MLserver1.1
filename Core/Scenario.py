from pathlib import Path  # https://python-scripts.com/pathlib

import threading
import time
import logging

from .StatDan import *
from .ConfigDan import *
from .StatDan import *
from .DopConfig import *
from .ReadXml import *
from .CountInitialData import *
from .CLFJson import *

from .LrfDec import *
from .ConvertCLF import *
from Core.ALLClexport import *
from Core.Clexport import *
from Core.TimeWait import *


class Scenario:

    def __init__(self):
        print("-- start Scenario")
        self.logger = logging.getLogger("Scenario.__init__")
        #  запуск потока инициализации
        self.logger.info(" Запуск потока инициализации переменных")

        self.dan_scenario = dict()
        self.dan_scenario["ind"] = 0

        self._lock_read_info = threading.Lock()  # self.lock.release()
        self.is_convert_clf_work_dir = False

        self.thread_inicial = threading.Thread(target=self._thread_inicial)
        self.thread_inicial.start()

        self.thread_read_info = threading.Thread(target=self._thread_read_info)
        self.thread_read_info.start()

    def _thread_inicial(self):

        self.dan_scenario["original"] = self.get_count_original_dan(),
        self.dan_scenario["work_dir_clf"] = len(list(Path(StatDan.__getItem__("path_work")).glob("*.clf"))),

        _path_clf = StatDan.__getItem__("path_work") + "\\CLF"
        self.dan_scenario["CLF_dir_clf"] = len(
            list(Path(StatDan.__getItem__("path_work") + "\\CLF").glob("*.clf"))) if Path(_path_clf).exists() else 0

        self.dan_scenario["ind"] = 0

        self.logger.info(" Init  self._rw = ReadWrite(PathWork=StatDan.__getItem__(path_work))")
        self._rw = ReadWrite(PathWork=StatDan.__getItem__("path_work"))

        self.logger.info(" Init  self._clf_json = CLFJson(StatDan.__getItem__(path_work) + \\clf.json")
        self._clf_json = CLFJson(StatDan.__getItem__("path_work") + "\\clf.json")
        StatDan.__setItem__("iclf_json", self._clf_json)

        self.logger.info(" Init  self._clf_json = CLFJson(StatDan.__getItem__(path_work) + \\clf.json")
        self._config = ConfigDan(PathConfig=StatDan.__getItem__("dir_start") + "\\mlserver.json")

        self.logger.info(" Init  self._dop_config = DopConfig(_rw)")
        self._dop_config = DopConfig(self._rw)

        self.logger.info(" Изменение конфигурации под конкретную машину {}".format(self._dop_config.CarName))
        self._config.set(self._dop_config.CarName)
        self._clf_json.set("Car name", self._dop_config.CarName)

        self.logger.info(" Пишем LoggerConfig  {}".format(self._dop_config.NameLogger))
        self._clf_json.set("LoggerConfig", self._dop_config.NameLogger)
        self._clf_json.write_json()

        self.logger.info(" Разбор XML файла  ")
        self._readxml = ReadXml(self._dop_config.path_common, self._dop_config.dir_analysis)
        StatDan.__setItem__("path_commonт", self._dop_config.path_common)

    def get_count_original_dan(self):
        _countInitialData = CountInitialData(StatDan.__getItem__("path_work"))
        return _countInitialData.count

    def _thread_read_info(self):
        """
            необходимо проверить наличие файлов
            1. Есть ли сырые файлы в каталогах !D2FX -> !D??????
            2. Наличие в корневом каталоге *.clf
            3. Наличие каталога CLF c файлами
        """
        while True:
            with self._lock_read_info:
                self.dan_scenario["original"] = self.get_count_original_dan(),
                self.dan_scenario["work_dir_clf"] = len(list(Path(StatDan.__getItem__("path_work")).glob("*.clf"))),

                _path_clf = StatDan.__getItem__("path_work") + "\\CLF"
                self.dan_scenario["CLF_dir_clf"] = len(
                    list(Path(StatDan.__getItem__("path_work") + "\\CLF").glob("*.clf"))) if Path(
                    _path_clf).exists() else 0

                self.dan_scenario["ind"] += 1
                k = 1
            time.sleep(1)

    def _convert_LrfDec(self):
        f1_type_int = lambda x: x[0] if "tuple" in str(type(x)) else x
        _infdec = LrfDec(self._config.lrf_dec)
        _infdec.start()  # _infdec.run()

        _time0 = self.dan_scenario["ind"]
        while True:

            with self._lock_read_info:
                k = f1_type_int(self.dan_scenario["work_dir_clf"])

            if k >= 1:
                self.is_convert_clf_work_dir = True
                break
            xtime = self.dan_scenario["ind"] - _time0
            if xtime >= 20:
                self.is_convert_clf_work_dir = False
                StatDan.__setItem__("is_lrf", False)
                break
            else:
                time.sleep(1)

        if self.is_convert_clf_work_dir:
            _convertCLF = ConvertCLF()
            _convertCLF.start()
            _convertCLF.join()

        _infdec.join()

        _countInitialData = CountInitialData(StatDan.__getItem__("path_work"))
        _countInitialData.call()
        if _countInitialData.count <= 0:
            _countInitialData.del_initial_data()

    def convert_LrfDec(self):

        self.convert_LrfDec__ = threading.Thread(target=self._convert_LrfDec, args=(), daemon=True)
        self.convert_LrfDec__.start()
#        self.convert_LrfDec__.join()
