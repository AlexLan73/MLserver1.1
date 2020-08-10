from Core.CountInitialData import *
import threading
import logging
import os, sys

from .StatDan import *
from .ReadWrite import *
from .Error_Program import *

class LrfDec(threading.Thread):

    from subprocess import Popen, PIPE, STDOUT

    def __init__(self, config_lrfdec: dict):
        threading.Thread.__init__(self)
        self.logger = logging.getLogger("exampleApp.LrfDec.__init__")
        self.path_work = StatDan.__getItem__("path_work")
        StatDan.__setItem__("lrf_error", 0)
        StatDan.__setItem__("is_lrf", True)

        self._countInitialData = CountInitialData(self.path_work)
        self.path_common = StatDan.__getItem__("path_commonт")
        self.config_lrfdec = config_lrfdec
        self.log_file_clf = self.path_work + "\\LOG\\log_clf.txt"
        self.path_lrf_dec = self.path_common + "\\DLL\\lrf_dec.exe"
        self._rw = ReadWrite()
        self.perror = Error_Program()

    # - - - - - - -
    def __run__lrf_dec(self):

        self.logger.info(" LrfDec.__run__lrf_dec   Start function lrf_dec ")

        s = self.path_lrf_dec + self.config_lrfdec + self.path_work
        self.logger.info("  строка запуска " + s)

        f = open(self.log_file_clf, 'wb')
        f.close()

        try:
            p = self.Popen(s, stdout=self.PIPE, stderr=self.STDOUT, bufsize=1)
        except:
            self.logger.critical(" The program stopped working with a fatal error ")
            sys.exit(-100)

        try:
            with p.stdout, open(self.log_file_clf, 'ab') as file:
                for line in iter(p.stdout.readline, b''):
                    print(line),
                    file.write(line)
            p.wait()

            return_code = p.returncode

            __ls = self._rw.ReadText(self.log_file_clf)
            for item in __ls:
                it = item.replace("\n", "")
                if len(it) > 0:
                    self.logger.info(it)

            print(" код завершения  - ", return_code)
            self.logger.info("   код завершения {}".format(return_code))
            __error_name = self.perror.error_prog(return_code)
            self.logger.info(__error_name)

        except:
            self.logger.warning("  Проблема с записью в файл log_file_clf.txt")

    # - - - - - - -
    def __filtr_log(self, __ls):
        import re
        __ls0 = []
        for it in __ls:
            __s = re.sub(r'\r', "", re.sub(r'\n', "", it))  # it.replace('\r', "")).replace("\n","")
            if len(__s) > 0:
                __ls0 += [__s]

        __ls_handling = [re.sub(r'\n', "", x) for x in __ls if "Handling" in x]
        __dir_file_handling = []
        for x in __ls_handling:
            _i0 = x.index("!")
            _x = x[_i0:]
            __dir_file_handling += [_x[:-1]]

        __ls_not_handling = [re.sub(r'\n', "", x).strip() for x in __ls
                             if not ("Handling" in x)
                             # and ("entries" in x)
                             and (len(x.strip()) > 0)]

        _files = [self.path_work + "\\" + x for x in os.listdir(self.path_work) if ".clf" in x]

        __dir_file_handling01 = []

        __dir_file_handling0 = [x.split("'") for x in __dir_file_handling]
        for it in __dir_file_handling0:
            __dir_file_handling01 += [it[0]]

        if len(__ls0) > 10:
            __ls0 = __ls0[-10:]

        return __dir_file_handling01, __ls0

    # - - - - - - -
    def __test_messange(self, __ls0):
        error = 0
        _text = "Ignored part of corrupted file"
        _files_error = []
        for it in __ls0:
            if _text in it:
                __s = it.split(_text)
                __s0 = str(__s[1]).strip().replace(".", "")
                print("  --  FILE ERROR   ", __s0)
                _files_error += [__s0]

        if len(_files_error) > 0:
            error = -1
            self.logger.info(" if len(_files_error) >0 -> __convert_files(self, _files_error)")
            __convert_files(self, _files_error)
        return error

    # - - - - - - -
    def __convert_files(self, dir_files):
        for __it_file in dir_files:
            __path_src = self.path_work + "\\" + __it_file
            if os.path.isfile(__path_src):
                _dir_file = __it_file.split("\\")
                __path_d = self.path_work + "\\" + _dir_file[0] + "\\~" + _dir_file[1]
                if os.path.isfile(__path_d):
                    os.remove(__path_d)

                self._countInitialData.rename_file(__path_src, __path_d)

    # - - - - - - -
    def run(self):
        StatDan.__setItem__("is_lrf", True)

        while self._countInitialData.call() > 0:
            if self._countInitialData.count_repit > 4:
                self.logger.warning("  кол-во циклов обработки исходных данных привысило 3")
                self.logger.warning("  кол-во данных не уменьшается")
                return
            print("  -- нужно обработать {}  файлов ".format(self._countInitialData.count))
            self.__run__lrf_dec()  # запускаем программу конвертации

            __ls = self._rw.ReadText(self.log_file_clf)
            self.logger.info(
                " Обработка файла {} на предмет с конвертированных \"Сырых данных\" ".format(self.log_file_clf))

            __dir_file_handling01, __file_error = self.__filtr_log(__ls)

            self.logger.info(" Обработанные данные переименновываем, добавляем ~ к имени файла  ")
            self.__convert_files(__dir_file_handling01)

            _error = self.__test_messange(__file_error)
            if _error < 0:
                StatDan.__setItem__("lrf_error", _error)
                StatDan.__setItem__("is_lrf", False)
                self.logger.warning("  LrfDec завершено с ошибкой ")

                return _error

        self.logger.info("  LrfDec завершено Ok! ")
        StatDan.__setItem__("is_lrf", False)
        StatDan.__setItem__("lrf_error", 0)
        return 0
