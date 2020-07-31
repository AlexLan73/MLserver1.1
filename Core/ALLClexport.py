from Core.CountInitialData import *
import threading

from Core.StatDan import *
from Core.ReadWrite import *


class ALLClexport(threading.Thread):
    import os, sys, copy, glob, json, time
    from subprocess import Popen, PIPE, STDOUT
    import logging
    from multiprocessing import Queue

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
        self.queve = self.Queue()

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

    def __fprint_logg(q, is_logg):
        while is_logg:
            if q.empty():
                time.sleep(0.05)
            else:
                while not (q.empty()):
                    print("  fprint  ===>>> ", q.get())

    def run(self):
        # запуск потока записи логов во время конвертации
        is_logg = True
        _fprint = Process(target=__fprint_logg, args=(self.queve, is_logg), daemon=True)  # , daemon=True
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


    # ==========  CLEXPORT ====================================
    def run_clexport(self, bconvert=True):
        logger = logging.getLogger("exampleApp.RunProgram.run_clexport")
        logger.info(" start  function CLEXPORT конвертируем в MDF и в прочее ")

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        def __convert_data_time(self, s: str):
            __s0 = s.split(" ")
            __s01 = __s0[0].split(".")
            __s1 = str(__s0[1].split(".")[0]).replace(":", "-")
            return __s01[2] + "-" + __s01[1] + "-" + __s01[0] + "_" + __s1

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
        def __rename_file(self, _key_dir_json):
            logger = logging.getLogger("exampleApp.RunProgram.run_clexport.__rename_file")
            logger.info(" rename MDF files  ")

            __data_cfl_ = _key_dir_json

            for key, val in _key_dir.items():
                __path_dit = self._rws.path_sourse + "\\" + key
                if not self.os.path.isdir(__path_dit):
                    break

                ls_file = [x for x in self.os.listdir(__path_dit) if ".MDF" in x]
                if len(ls_file) <= 0:
                    break

                for it_file in ls_file:
                    __imdf = str(it_file).index(".MDF")
                    __name = it_file[:__imdf]
                    __ext = it_file[__imdf:]
                    __if00x = __name.index("F")
                    _name = __name[:__if00x]
                    _f00x = __name[__if00x:]
                    __d = __data_cfl_[_name]

                    __mem = __data_cfl_[_name]["Memory"][_f00x]
                    __start = __convert_data_time(self, __mem["Start"])
                    __end = __convert_data_time(self, __mem["End"])
                    __trigget = "_Trigger" if len(__mem) > 2 else ""
                    _name_file = __d["Car name"] + "_" + __start + "_" + __end + "_" + _f00x + __trigget + __ext
                    __path0 = __path_dit + "\\" + _name_file
                    self.os.rename(__path_dit + "\\" + it_file, __path0)
                    logger.info(__path0)

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

        self._rws.cd(self._rws.path_sourse)

        _key_dir_json = self._rws.read_dict_json(self._rws.path_sourse + "\\clf.json")

        __rename_file(self, _key_dir_json)
