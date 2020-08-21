from pathlib import Path  # https://python-scripts.com/pathlib
from collections import OrderedDict

import threading
import time
import logging
import logging.config

from .LrfDec import *
from .StatDan import *
from .StatDan import *
from .ReadXml import *
from .CLFJson import *
from .Clexport import *
from .TimeWait import *
from .ConfigDan import *
from .DopConfig import *
from .ConvertCLF import *
from .ALLClexport import *
from .CountInitialData import *


class Scenario:
    def __init__(self):
        print("-- start Scenario")
        self.logger = logging.getLogger("exampleApp.Scenario.__init__")
        self.logger.info("Scenario.__init__")

        self.logger.info(" Запуск потока инициализации переменных")  # запуск потока инициализации

        self.dan_scenario = dict()  # инициализация переменных
        self.dan_scenario["ind"] = 0
        self._is_read_info = True
        self._lock_read_info = threading.Lock()  # self.lock.release()
        self.is_convert_clf_work_dir = False

        self.thread_inicial = threading.Thread(target=self._thread_inicial)
        self.thread_inicial.start()  # поток- инициализация сонфогурации

        self.thread_read_info = threading.Thread(target=self._thread_read_info, daemon=True)
        self.thread_read_info.start()  # поток - чтение переменных

        self.dthreading = OrderedDict()

    def _thread_inicial(self):
        # если есть clf.jsomn удалить
        __path = Path(StatDan.__getItem__("path_work")+"\\clf.json")
        __path.unlink( missing_ok = True )

        self.dan_scenario["original"] = self.get_count_original_dan()  # кол-во (исходных) файлов

        # кол-во сформированных или существующих  clf файлов
        self.dan_scenario["work_dir_clf"] = len(list(Path(StatDan.__getItem__("path_work")).glob("*.clf")))

        # кол-во сформированных, переименнованых и записанных файлов в в каталог CLF
        _path_clf = StatDan.__getItem__("path_work") + "\\CLF"
        self.dan_scenario["CLF_dir_clf"] = len(
            list(Path(StatDan.__getItem__("path_work") + "\\CLF").glob("*.clf"))) if Path(_path_clf).exists() else 0

        self.dan_scenario["ind"] = 0  # индекс счетчик с интервалом 1 сек

        # грузим класс ReadWrite для записи/чтения данных
        self.logger.info(" Init  self._rw = ReadWrite(PathWork=StatDan.__getItem__(path_work))")
        self._rw = ReadWrite(PathWork=StatDan.__getItem__("path_work"))

        # грузим класс CLFJson для работы с файлом clf.json
        self.logger.info(" Init  self._clf_json = CLFJson(StatDan.__getItem__(path_work) + \\clf.json")
        self._clf_json = CLFJson(StatDan.__getItem__("path_work") + "\\clf.json")
        StatDan.__setItem__("iclf_json", self._clf_json)

        # грузим класс ConfigDan для настройки программы
        self.logger.info(" Init  ConfigDan(PathConfig=StatDan.__getItem__(dir_start) + \\mlserver.json ")
        self._config = ConfigDan(PathConfig=StatDan.__getItem__("dir_start") + "\\mlserver.json")
        StatDan.__setItem__("config", self._config)

        # грузим класс DopConfig для дополнительной настройки программы
        self.logger.info(" Init  self._dop_config = DopConfig(_rw)")
        self._dop_config = DopConfig(self._rw)

        # конфогурируем под конкретную машину
        self.logger.info(" Изменение конфигурации под конкретную машину {}".format(self._dop_config.CarName))
        self._config.set(self._dop_config.CarName)
        self._clf_json.set("Car name", self._dop_config.CarName)

        self.logger.info(" Пишем LoggerConfig  {}".format(self._dop_config.NameLogger))
        self._clf_json.set("LoggerConfig", self._dop_config.NameLogger)
        self._clf_json.write_json()

        # грузим класс ReadXml для 1. разбора XML; 2. настройки конвертации
        self.logger.info(" Разбор XML файла  ")
        self._readxml = ReadXml(self._dop_config.path_common, self._dop_config.dir_analysis)
        StatDan.__setItem__("path_commonт", self._dop_config.path_common)

        self.dthreading["LrfDec"] = threading.Thread(target=self._convert_LrfDec, args=(), daemon=True)
        self.dthreading["convertCLF"] = ConvertCLF()

        # подключаем общий клас конвертации ALLClexport
        self.logger.info(" грузим -> ALLClexport(self._config, self._readxml.siglog_config_basa)")

        self.dthreading["clexport"] = ALLClexport(self._config, self._readxml.siglog_config_basa)

    # расчет сколько "исходных" файлов нужно обработать
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
        self.logger.info(" за работал поток -> _thread_read_info")
        while True:
            with self._lock_read_info:
                self.dan_scenario["original"] = self.get_count_original_dan()
                self.dan_scenario["work_dir_clf"] = len(list(Path(StatDan.__getItem__("path_work")).glob("*.clf")))

                _path_clf = StatDan.__getItem__("path_work") + "\\CLF"
                self.dan_scenario["CLF_dir_clf"] = len(
                    list(Path(StatDan.__getItem__("path_work") + "\\CLF").glob("*.clf"))) if Path(
                    _path_clf).exists() else 0

                self.dan_scenario["ind"] += 1

                if not self._is_read_info:
                    return

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
            if xtime >= 30:
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
        self.logger.info(" Запуск основного сценария CLF ")
        self.logger.info("   -запуск потоко  elf._convert_LrfDec - конвертируес в CLF ")
        self.dthreading["LrfDec"].start()

    def convert_CLF(self):
        self.logger.info(" Запуск вспомогательного сценария без 'сырых данных' сценария CLF ")
        self.logger.info("   -запуск потока  elf._convert_LrfDec - конвертируес в CLF ")
        StatDan.__setItem__("is_lrf", False)
        self.logger.info("   -запуск потока  ConvertCLF() переименование данных и запись в каталог CLF ")
        self.dthreading["convertCLF"].start()

    # запуск сценария в зависимости от ситуации
    def run_scenario(self):
        f1typeint = lambda x: x[0] if "tuple" in str(type(x)) else x

        if f1typeint(self.dan_scenario["original"]) > 0:
            # запускаем конвертацию  LrfDec
            if f1typeint(self.dan_scenario["work_dir_clf"]) > 0:
                self.logger.info("   - стирание данных clf из основногокаталога ")
                for f in list(Path(StatDan.__getItem__("path_work")).glob("*.clf")):
                    f.unlink()

            self.convert_LrfDec()

        elif f1typeint(self.dan_scenario["work_dir_clf"]) > 0:
            # запускаем конвертацию  LrfDec
            self.convert_CLF()

        xtime_wait_files_dir_clf = self.dan_scenario["ind"]
        __iswhile = True
        while ((self.dan_scenario["ind"] - xtime_wait_files_dir_clf) <= 30) and __iswhile:
            if f1typeint(self.dan_scenario["CLF_dir_clf"]) > 0:
                self.logger.info("   -запуск потока  self.clexport__.start()- формирование данных типа MDF ")
                __iswhile = False
                self.dthreading["clexport"].start()
#                break

        print("Ждем завершения программы")
        self.logger.info("Ждем завершения программы")

        self.dthreading["clexport"].join()
        self._is_read_info = False
        self.logger.info("END  нормальное завершение программы")

