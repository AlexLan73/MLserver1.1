from multiprocessing import Queue
import threading
import logging
import logging.config

from .StatDan import *
from .Clexport import *
from .ReadWrite import *
from .ConfigDan import *
from .CountInitialData import *


class ALLClexport(threading.Thread):

    def __init__(self, _config: ConfigDan, siglog_config_basa):
        # инициализация переменных ALLClexport
        threading.Thread.__init__(self)

        self.logger = logging.getLogger("exampleApp.ALLClexport.__init__")
        self.logger.info("инициализация переменных ALLClexport")

        self.is_logg = True                                     # нужно обратить внимание
        self._config = _config                                  # конфигурация
        self.config_export = _config.clexport                   # маска экспорта MDF ......

        self.path_work = StatDan.__getItem__("path_work")
        self.path_common = StatDan.__getItem__("path_commonт")

        self._rw = ReadWrite()
        __ls_key_config_export = list(self.config_export.keys())
        self._key_prog = {x: None for x in __ls_key_config_export}
        self._key_dir = {x: self.path_work + "\\" + x for x in __ls_key_config_export}
        self._rw.make_ddir(self._key_dir, True)

        self.copy_to_dir(siglog_config_basa)
        self.queve = Queue()

        self.log_file_basa = self.path_work + "\\LOG\\Log_Clexport_"
        self._pool = _config.all_config["pool"]
        self._timewail = _config.all_config["timewait"]

    def copy_to_dir(self, s):
        self.logger.info("exampleApp.copy_to_dir")
        self.logger.info(" copy_to_dir -  копируем файл конфигурации siglog_config.ini в каталог по маске")

        for key, val in self.config_export.items():
            if len(str(val).lower()) > 0:
                __path = self._key_dir[key]
                __path_file = __path + "\\" + "siglog_config.ini"  # self.shutil.copy2
                self.logger.info(f" Записать в кталог {__path}  ")
                self.logger.info(" Пишем в файл  " + __path_file)

                with open(__path_file, "w") as file:
                    try:
                        for it in s:
                            file.write(it)
                    except:
                        self.logger.critical(" Проблема записи в ", __path_file)

            else:
                self.logger.warning("  у key {} нет данных".format(key))

    def run(self):
        self.logger.info("ALLClexport.run инициализация потоков по KEY (типа MDF)")
        for key, val in self._key_prog.items():
            self._key_prog[key] = ClexportXX(key, self.config_export, self._pool, self._timewail)

        # запускаем поток
        self.logger.info("ALLClexport.run запуск потоков")
        for key, val in self._key_prog.items():
            try:
                val.start()
            except ValueError:
                pass

        # ожидаем завершения потоков
        self.logger.info("ALLClexport.run ожидание завершения потоков")
        for key, val in self._key_prog.items():
            try:
                val.join()
            except ValueError:
                pass
# ------------------------------------------------
        # ожидаем завершения потоков
        self.logger.info("ALLClexport.run ожидание завершения потоков")
        for key, val in self._key_prog.items():
            try:
                val.renamemdf.join()
            except ValueError:
                pass

        for key, val in self._key_prog.items():
            try:
                val.renamemdf.time.clear()
                val.renamemdf.is_work = False
            except ValueError:
                pass

        self.logger.info("ALLClexport.run все потоки завершены")
        StatDan.__setItem__("is_clexport", False)

        print("ALLClexport --  exit")

    def get_key_export(self, key):
        return self.config_export[key]
