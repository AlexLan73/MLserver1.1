import threading
from multiprocessing import Queue
from subprocess import Popen, PIPE, STDOUT

from .Clexport import *
from .CountInitialData import *
from .ReadWrite import *
from .StatDan import *


class ALLClexport(threading.Thread):
    import copy
    import time
    import logging
    #    from multiprocessing import Process, Queue

    def __init__(self, _config: dict, siglog_config_basa):
        threading.Thread.__init__(self)
        self._config = _config
        self.config_export = _config.clexport
        self.logger = self.logging.getLogger("exampleApp.Clexport.__init__")

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
        self.llogger = logging.getLogger("exampleApp.copy_to_dir")
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
                        self.logger.critical(" Проблема записи в ", file0)

            else:
                self.logger.warning("  у key {} нет данных".format(key))

    def run(self):
        for key, val in self._key_prog.items():
            self._key_prog[key] = ClexportXX(key, self.config_export, self._pool, self._timewail)

        # запускаем поток
        for key, val in self._key_prog.items():
            try:
                val.start()
            except:
                pass

        # ожидаем завершения потоков
        for key, val in self._key_prog.items():
            try:
                val.join()
            except:
                pass

        self.is_logg = False

    def get_key_export(self, key):
        return self.config_export[key]
