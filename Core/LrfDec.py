from Core.CountInitialData import *
import threading
import logging
from Core.StatDan import *
from Core.ReadWrite import *


class LrfDec(threading.Thread):
    import os, sys, copy, glob
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

    # - - - - - - -
    def __run__lrf_dec(self):

        self.logger = logging.getLogger("exampleApp.RunProgram.LrfDec")
        self.logger.info("  Start function lrf_dec ")

        s = self.path_lrf_dec + self.config_lrfdec + self.path_work
        self.logger.info("  строка запуска " + s)

        f = open(self.log_file_clf, 'wb')
        f.close()

        try:
            p = self.Popen(s, stdout=self.PIPE, stderr=self.STDOUT, bufsize=1)
        except:
            self.logger.critical(" The program stopped working with a fatal error ")
            self.sys.exit(-100)

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
            __error_name = self._error_prog(return_code)
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

        _files = [self.path_work + "\\" + x for x in self.os.listdir(self.path_work) if ".clf" in x]

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
            if self.os.path.isfile(__path_src):
                _dir_file = __it_file.split("\\")
                __path_d = self.path_work + "\\" + _dir_file[0] + "\\~" + _dir_file[1]
                if self.os.path.isfile(__path_d):
                    self.os.remove(__path_d)

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

    # ==========  ERROR PROG  ====================================+
    def _error_prog(self, kode):
        if kode == 0:
            return " EC_Okay 0 Execution without any error."
        elif kode == 1:
            return " EC_NoRequest 1	Nothing was requested (no parameters), and nothing was done"
        elif kode == 20:
            return "EC_Memory 20 Not enough main memory available."
        elif kode == 21:
            return "EC_System 21 System problem e.g. needed DLL file missing."
        elif kode == 22:
            return "EC_Phys 22 Problem with physical interface – e.g. COM2 not installed."
        elif kode == 30:
            return "EC_Arg 30 The call specified illegal program arguments."
        elif kode == 31:
            return "EC_FilFind 31 A specified input file is not available."
        elif kode == 32:
            return "EC_FilForm 32 An input file does not have the required format."
        elif kode == 33:
            return "EC_FilVer 33 An input file has an incompatible file version."
        elif kode == 34:
            return "EC_FilWrite	34 An output file could not be opened or wrote on to."
        elif kode == 40:
            return "EC_NoConn 40 Connection to the device failed."
        elif kode == 41:
            return "EC_Comm 41 Error during communication or communication abort."
        elif kode == 42:
            return "EC_Timeout 42 Communication timeout (caused by a communications problem or device failure)."
        elif kode == 50:
            return "EC_Intern 50 Internal error – should not occur."
        elif kode == 51:
            return "EC_IllDev 51 Illegal device behavior – maybe caused by communications failure."
        elif kode == 52:
            return "EC_DevSW 52	The necessary software is not available on the device."
        elif kode == 53:
            return "EC_DevVer 53 The device uses an incompatible software version."
        elif kode == 54:
            return "EC_NoData 54 The device does not contain any data of the requested kind."
        elif kode == 55:
            return "EC_Conf 55 The device does not contain a valid configuration."
        elif kode == 56:
            return "EC_Compile 56 During compilation of the configuration an error occurred."
        else:
            return "NOT kod ERROR."

#####################################

# EC_Okay 	    0 	Execution without any error.
# EC_NoRequest 	1 	Nothing was requested (no parameters), and nothing was done.
# EC_Memory 	20 	Not enough main memory available.
# EC_System 	21 	System problem e.g. needed DLL file missing.
# EC_Phys 	    22 	Problem with physical interface – e.g. COM2 not installed.
# EC_Arg 	    30 	The call specified illegal program arguments.
# EC_FilFind 	31 	A specified input file is not available.
# EC_FilForm 	32 	An input file does not have the required format.
# EC_FilVer 	33 	An input file has an incompatible file version.
# EC_FilWrite 	34 	An output file could not be opened or wrote on to.
# EC_NoConn 	40 	Connection to the device failed.
# EC_Comm 	    41 	Error during communication or communication abort.
# EC_Timeout 	42 	Communication timeout (caused by a communications problem or device failure).
# EC_Intern 	50 	Internal error – should not occur.
# EC_IllDev 	51 	Illegal device behavior – maybe caused by communications failure.
# EC_DevSW 	    52 	The necessary software is not available on the device.
# EC_DevVer 	53 	The device uses an incompatible software version.
# EC_NoData 	54 	The device does not contain any data of the requested kind.
# EC_Conf 	    55 	The device does not contain a valid configuration.
# EC_Compile 	56 	During compilation of the configuration an error occurred.
