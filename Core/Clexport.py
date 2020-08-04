from Core.CountInitialData import *
import threading

from Core.StatDan import *
from Core.ReadWrite import *
from Core.RenameMDF import *
from Core.CLFJson import *
from Core.TimeWait import *

import uuid, glob, time, copy, os
import pprint
from pathlib import Path

import threading
import time
from concurrent.futures.thread import ThreadPoolExecutor
from multiprocessing import Queue
from subprocess import Popen, PIPE, STDOUT


class ClexportXX(threading.Thread):
    import os, sys, copy, glob, json, time
    from subprocess import Popen, PIPE, STDOUT
    import logging

    def __countCLF(self):
        return len(list(Path(self.path_work + "\\CLF\\.").glob('*.clf')))

    def __init__(self, _key, _export, maxpool=5, timewait=20):
        threading.Thread.__init__(self)
        self._lock = threading.Lock()

        self._is_work_clf = StatDan.__getItem__("is_lrf")

        self._key = _key
        self.config_export = _export

        self.logger = self.logging.getLogger("exampleApp.Clexport.__init__")

        self.path_work = StatDan.__getItem__("path_work")
        self.path_common = StatDan.__getItem__("path_commonт")

        self.count = self.__countCLF()
        self.maxpool = maxpool

        self.is_export = True
        #        StatDan.__setItem__("path_work", r"E:\MLserver\data\PS33SED\log\2020-06-30_15-21-49")

        #        _clf_json = CLFJson(StatDan.__getItem__("path_work") + "\\clf.json")
        _clf_json = StatDan.__getItem__("iclf_json")

        path_MDF = self.path_work + "\\" + _key

        self._is_uprav = True
        self._time = TimeWait(timewait, self._is_uprav)

        self._renamemdf = RenameMDF(_clf_json, path_MDF, self.is_export)
        self._renamemdf.start()

    def read_dir_clf(self, config_dir, queve_dir):
        while config_dir["is_read_files"]:
            __new_files = list(set(glob.glob(config_dir["path_clr_files"])) - set(
                config_dir["bfiles"]))  # файлы которые нужно добавить к запуску
            if len(__new_files) > 0:
                print("*" * 60)
                for it_file in __new_files:
                    _id = uuid.uuid1()
                    _info = dict()
                    _info["file_clf"] = it_file
                    _info["path_out"] = config_dir["path_out"]
                    _info["process"] = -2
                    _info["error"] = -1000
                    _info["repeat"] = 0
                    _info["maska_exsport"] = config_dir["maska_exsport"]
                    queve_dir.put([_id, copy.deepcopy(_info)])

                config_dir["bfiles"].extend(__new_files)
            else:
                time.sleep(0.2)

    def fprint_log(self, queve_log):
        while self.is_convert:
            if queve_log.empty():
                time.sleep(0.2)
            else:
                while not (queve_log.empty()):
                    __log = queve_log.get()
                    print("->> {}".format(__log))

    # -------------------------------------------------

    def __test_read_file(self, path, n=50):
        while n > 0:
            try:
                with open(path, 'r') as file:
                    return False
            except:
                time.sleep(0.1)
        return True

    def __convert_dan(self, _id, info, _queve_log):
        with self._lock:
            _info = copy.deepcopy(info[_id])

        __maska = _info["maska_exsport"]
        __path_dit_clf = _info["file_clf"]  # self._rws.path_sourse + "\\" + key
        __path_out = _info["path_out"]
        _info["repeat"] += 1

        os.chdir(r"C:\Program Files (x86)\GIN\MLserver")
        p0 = __maska.replace("file_clf", __path_dit_clf)
        p1 = str(p0).replace("my_dir", __path_out)
        _commanda = "CLexport.exe " + p1
        _name = os.path.splitext(os.path.basename(__path_dit_clf))[0]
        _log_start = " id-->> {} \n ".format(_name)
        _queve_log.put(_log_start + " start convert")
        _queve_log.put(_log_start + _commanda)
        print(_commanda)

        if self.__test_read_file(__path_dit_clf):
            return_code = 30
            print(" error  ", return_code)
            _queve_log.put(_log_start + "   код завершения {}".format(return_code))
            _queve_log.put(_log_start + "  проблема с записью на диск  ")
            _info["error"] = 30
            _info["process"] = 0
            return

        try:
            p = Popen(_commanda, stdout=PIPE, stderr=STDOUT, bufsize=1)
        except:
            _queve_log.put(_log_start + " -200 The program stopped working with a fatal error ")
            _info["error"] = -200
            _info["process"] = -1
            _queve_log.put(_log_start + " выход по ошибки проблемма в CLexport.exe")

            with self._lock:
                info[_id] = copy.deepcopy(_info)
                return

        try:
            for line in iter(p.stdout.readline, b''):
                print(line),
                _queve_log.put(str(_log_start + str(line)))
            p.wait()
            return_code = p.returncode
            print(" код завершения  - ", return_code)
            _queve_log.put(_log_start + "   код завершения {}".format(return_code))
            _queve_log.put(_log_start + "   " + _error_prog(return_code))

            _info["error"] = return_code
            _info["process"] = 1

        except:
            print(" error  ", return_code)
            _queve_log.put(_log_start + "   код завершения {}".format(return_code))
            _queve_log.put(_log_start + "  проблема с записью на диск  ")

            _info["error"] = return_code
            _info["process"] = 1

        with self._lock:
            info[_id] = copy.deepcopy(_info)

    def run(self):
        queve_dir = Queue()
        queve_log = Queue()
        self.is_convert = True
        path_in = self.path_work + "\\CLF"
        path_out = self.path_work + "\\" + self._key
        config_dir = dict(
            patn_clr=path_in,
            path_out=path_out,
            path_clr_files=path_in + "\\*.clf",
            maska_exsport=self.config_export,
            path_clr_log_file_mask=path_in + "\\maskalog.log",
            bfiles=[],
            is_read_files=True
        )

        _read_dir = threading.Thread(target=self.read_dir_clf, args=(config_dir, queve_dir),
                                     daemon=True)  # , daemon=True
        _read_dir.start()
        _print_log = threading.Thread(target=self.fprint_log, args=(queve_log),
                                      daemon=True)  # , daemon=True
        _print_log.start()

        info = dict()

        executor = ThreadPoolExecutor(max_workers=5)

        self._time.set()
        while config_dir["is_read_files"]:
            _count_work_files = len(config_dir["bfiles"])
            _count_clf_files = len(list(glob.glob(config_dir["path_clr_files"])))
            _count_filesWork = _count_work_files - _count_clf_files
            if _count_filesWork < 0:
                self._time.set()

            self._is_work_clf =  StatDan.__getItem__("is_lrf") and self._time.is_uprav

            if queve_dir.empty():
                time.sleep(0.1)
            else:
                while not (queve_dir.empty()):
                    print("-" * 80)
                    __dan = queve_dir.get()
                    __id = __dan[0]
                    with self._lock:
                        info[__id] = copy.deepcopy(__dan[1])
                    b = executor.submit(self.__convert_dan, __id, info, queve_log)

                pprint.pprint(info, width=1)

            if not self._is_work_clf:  # Если процесс закончен
                '''
                 1 Вариант
                    Программа закончила формировать CLF файлы, 
                    и мы должны закончить формирование MDF (другие) из оставшихся файлов
                 2. вариант сохли по времени       
                '''
                if _count_clf_files == sum([val["process"] for val in info.values()]):
                    break

                for key, val in info.items():
                    _info = val
                    if _info["error"] != -1000:
                        _info["process"] = 1
                    info[key] = _info

        self.is_export = False
        self.is_convert = False
        self._renamemdf.join()

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
