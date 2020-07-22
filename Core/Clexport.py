
from Core.CountInitialData import *
import threading

from Core.StatDan import *
from Core.ReadWrite import *


class Clexport(threading.Thread):
    import os, sys, copy, glob, json, time
    from subprocess import Popen, PIPE, STDOUT
    import logging

    def __init__(self, config_export : dict ):
        threading.Thread.__init__(self)
        self.config_export = config_export
        self.logger = self.logging.getLogger("exampleApp.Clexport.__init__")

        self.path_work = StatDan.__getItem__("path_work")
        self.path_common = StatDan.__getItem__("path_commonт")

    # ==========  CLEXPORT ====================================
    def run_clexport(self, bconvert=True):
        logger = logging.getLogger("exampleApp.RunProgram.run_clexport")
        logger.info(" start  function CLEXPORT конвертируем в MDF и в прочее ")

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        def __convert_dan(self, __path_clexport, _key_dir):
            logger = logging.getLogger("exampleApp.RunProgram.run_clexport.__path_clexport")
            logger.info(" Вызываем CLexsport ")

            for key, val in _key_dir.items():
                __path_dit = self._rws.path_sourse + "\\" + key
                if self.os.path.isdir(__path_dit):
                    for it_file in __file_clf:
                        __val01 = str(val).replace("file_clf", it_file)
                        __val = __val01.replace("my_dir", __path_dit)
                        __common = __path_clexport + __val
                        logger.info(" Командная строка к CLexsport  " + __common)

                        try:
                            p = self.Popen(__common, stdout=self.PIPE, stderr=self.STDOUT, bufsize=1)
                        except:
                            logger.critical(" The program stopped working with a fatal error ")
                            self.sys.exit(-200)

                        try:
                            with p.stdout, open(self._rws.log_file_mdf, 'ab') as file:
                                for line in iter(p.stdout.readline, b''):
                                    print(line),
                                    file.write(line)
                                    logger.info(line)
                            p.wait()
                            return_code = p.returncode
                            print(" код завершения  - ", return_code)
                            logger.info("   код завершения {}".format(return_code))
                            __error_name = self._error_prog(return_code)
                            logger.info(__error_name)
                        except:
                            logger.warning("  Проблема с записью в файл log_file_mdf.txt")

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        logger.info(" запуск функции find_file_ext_clf() - поиск всех clf файлов")
        __file_clf = self.find_file_ext_clf()
        if len(__file_clf) == 0:
            logger.error(" - Нет файлов с расширением clf в каталоге \\CLF ")
            return
        self._rws.cd(self._rws._mlserver)
        __path_clexport = "clexport.exe"

        _key_dir = {key: val for key, val in self._rws.dir_key.items() if len(val) > 0}
        # формируем DataXF00X  <-----
        if bconvert:
            __convert_dan(self, __path_clexport, _key_dir)

