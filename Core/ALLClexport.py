from Core.CountInitialData import *
import threading

from Core.StatDan import *
from Core.ReadWrite import *

from multiprocessing import Queue
from subprocess import Popen, PIPE, STDOUT

class ALLClexport(threading.Thread):
    import os, sys, copy, glob, json, time
 #   from subprocess import Popen, PIPE, STDOUT
    import logging
#    from multiprocessing import Process, Queue

    def __init__(self, config_export: dict, siglog_config_basa):
        threading.Thread.__init__(self)
        self.config_export = config_export
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

    def copy_to_dir(self, s):
        self.llogger = logging.getLogger("exampleApp.copy_to_dir")
        for key, val in self.config_export.items():
            if len(str(val).lower()) > 0:
                __path = self._key_dir[key]
                __path_file = __path + "\\" + "siglog_config.ini"  # self.shutil.copy2
                self.logger.info(" Записать в кталог {}  ".format(__path_file))
                self.logger.info(" Пишем в файл  " + __path_file)

                with open(__path_file, "w") as file:
                    try:
                        for it in s[0]:
                            file.write(it)
                    except:
                        self.logger.critical(" Проблема записи в ", file0)

            else:
                self.logger.warning("  у key {} нет данных".format(key))

    def __fprint_logg(self, q, is_logg):
        while is_logg:
            if q.empty():
                time.sleep(0.05)
            else:
                while not (q.empty()):
                    print("  fprint  ===>>> ", q.get())

    def run(self):
        # запуск потока записи логов во время конвертации
        is_logg = True
        _fprint = threading.Thread(target=self.__fprint_logg, args=(self, self.queve, is_logg), daemon=True)  # , daemon=True
        _fprint.start()

        # загружаем функции для потока
        for key, val in self._key_prog.items():
            self._key_prog[key] = ClexportXX(key, self.config_export[key], self.queve)

        # запускаем поток
        for key, val in self._key_prog.items():
            if not (None in val):
                # val.start();
                val.run()

        # ожидаем завершения потоков
        for key, val in self._key_prog.items():
            if not (None in val):
                val.join()

    def get_key_export(self, key):
        return self.config_export[key]
