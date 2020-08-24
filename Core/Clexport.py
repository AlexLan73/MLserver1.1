from pathlib import Path
from subprocess import Popen, PIPE, STDOUT
from multiprocessing import Queue
from concurrent.futures.thread import ThreadPoolExecutor

import logging
import logging.config
import threading
import time, uuid, glob, copy, os, pprint

from .StatDan import *
from .CLFJson import *
from .TimeWait import *
from .ConfigDan import *
from .ReadWrite import *
from .RenameMDF import *
from .CountInitialData import *
from .Error_Program import *

class ClexportXX(threading.Thread):
    # запись логов из потоков
    def fprint_log(self, queve_log):
        self.logger.info("- поток ClexportXX.fprint_log() \n -- запись потоков логов")
        while self.is_convert or not (queve_log.empty()):
            if queve_log.empty():
                time.sleep(0.2)
            else:
                while not (queve_log.empty()):
                    __log = queve_log.get()
                    print("->> {}".format(__log))
                    self.logger.info(__log)

    def read_dir_clf(self, config_dir, queve_dir):
        self.logger.info("- поток ClexportXX.read_dir_clf() \n -- чтение наименование файлов в корневой dir files *.clf ")
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
                    _info["repeat"] = 6
                    _info["maska_exsport"] = config_dir["maska_exsport"]
                    queve_dir.put([_id, copy.deepcopy(_info)])

                config_dir["bfiles"].extend(__new_files)
            else:
                time.sleep(0.2)

    def __countCLF(self):
        return len(list(Path(self.path_work + "\\CLF\\.").glob('*.clf')))

    def __init__(self, _key, _export, maxpool=5, timewait=20):
        threading.Thread.__init__(self)
        # инициализация
        self.logger = logging.getLogger("exampleApp.ClexportXX.__init__")
        self.logger.info("ClexportXX.__init__")

        self.perror = Error_Program()
        self.is_convert = True
        self._mlserver = str(os.environ.get("MLSERVER", ""))

        self._lock = threading.Lock()

        self._is_work_clf = StatDan.__getItem__("is_lrf")
        StatDan.__setItem__("is_clexport", True)
        self._key = _key

        if "dict" in str(type(_export)):
            _export = list(_export.values())[0]

        self.config_export = _export
        self.logger.info(f"ClexportXX.__init__   -> {self.config_export}")

        self.path_work = StatDan.__getItem__("path_work")
        self.path_common = StatDan.__getItem__("path_commonт")
        self._config: ConfigDan = StatDan.__getItem__("config")
        self.path_mlserver = StatDan.__getItem__("path_mlserver")

        self.count = self.__countCLF()
        self.maxpool = maxpool

        self.is_export = True
        _clf_json = StatDan.__getItem__("iclf_json")

        path_MDF = self.path_work + "\\" + _key

        self._is_uprav = True
        self._time = TimeWait(timewait, self._is_uprav)

        self.queve_log = Queue(maxsize=500)
        self.queve_dir = Queue(maxsize=1000)
        self.logger.info("Start ПОТОКА --  RenameMDF(_clf_json, path_MDF, self.is_export)  -- ")
        self.renamemdf = RenameMDF(_clf_json, path_MDF, self.is_export)
        self.renamemdf.start()

    # -------------------------------------------------
    def __test_read_file(self, path, n=50):
        while n > 0:
            try:
                with open(path, 'r') as file:
                    return False
            except:
                time.sleep(0.5)
        return True

    def __convert_dan(self, _id, info, _queve_log):
        self.logger.info("- поток ClexportXX.__convert_dan() \n -- конвертировать в clf файл ")
        with self._lock:
            _info = copy.deepcopy(info[_id])

        __maska = _info["maska_exsport"]

        __path_dit_clf = _info["file_clf"]  # self._rws.path_sourse + "\\" + key
        __path_out = _info["path_out"]
        _info["repeat"] -= 1

        _drive = Path(self.path_mlserver).drive
        os.chdir(_drive)
        os.chdir(self.path_mlserver)

        p0 = __maska.replace("file_clf", __path_dit_clf)
        p1 = str(p0).replace("my_dir", __path_out)
        _commanda = "CLexport.exe " + p1
        _name = os.path.splitext(os.path.basename(__path_dit_clf))[0]
        _log_start = " id-->> {} \n ".format(_name)
        _queve_log.put(_log_start + " start convert")
        _queve_log.put(_log_start + _commanda)
        print("_" * 80)
        print(_commanda)

        if self.__test_read_file(__path_dit_clf):
            return_code = 30
            print(" error  ", return_code)
            _queve_log.put(_log_start + "   код завершения {}".format(return_code))
            _queve_log.put(_log_start + " проблема с записью на диск  ")
            _info["error"] = 30
            _info["process"] = 1
            return

        try:
            p = Popen(_commanda, stdout=PIPE, stderr=STDOUT, bufsize=1)
        except:
            _queve_log.put(_log_start + " -200 The program stopped working with a fatal error ")
            _info["error"] = -200
            _info["process"] = 1
            _queve_log.put(_log_start + " выход по ошибки проблемма в CLexport.exe")

            with self._lock:
                info[_id] = copy.deepcopy(_info)
                return
        return_code = 0
        try:
            for line in iter(p.stdout.readline, b''):
                print(line),
                _queve_log.put(str(_log_start + str(line)))
            p.wait()
            return_code = p.returncode

            print(" код завершения  - ", return_code)
            _queve_log.put(_log_start + "   код завершения {}".format(return_code))

            __ss0 = str(self.perror.error_prog(return_code))
            print(__ss0)
            _queve_log.put(_log_start +  __ss0)
            _info["error"] = return_code
            _info["process"] = 1

        except:
            if return_code != 0:
                print(" error  ", return_code)
                _queve_log.put(_log_start + "   код завершения {}".format(return_code))
                _queve_log.put(_log_start + " проблема с записью на диск  ")

            _info["error"] = return_code
            _info["process"] = 1

        with self._lock:
            info[_id] = copy.deepcopy(_info)

    def run(self):
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

        self.queve_log.put("ClexportXX.run() - запуск потока  elf.read_dir_clf - для подсчета кол-ва clf файлов ")
        _read_dir = ThreadPoolExecutor(max_workers=1)
        _x0 = _read_dir.submit(self.read_dir_clf, config_dir, self.queve_dir)  # ,  daemon=True

        self.queve_log.put("ClexportXX.run() - запуск потока  _print_logf - для записи в LOGGER ")
        _print_log = ThreadPoolExecutor(max_workers=1)
        _x0 = _print_log.submit(self.fprint_log, self.queve_log)  # ,  daemon=True

        info = dict()

        self.queve_log.put("ClexportXX.run() - запуск пул потоков для конвертации в форматы ")
        executor = ThreadPoolExecutor(max_workers=self._config.all_config["pool"])

        self._time.set()
        while config_dir["is_read_files"]:
            _count_work_files = len(config_dir["bfiles"])
            _count_clf_files = len(list(glob.glob(config_dir["path_clr_files"])))
            _count_filesWork = _count_work_files - _count_clf_files
            if _count_filesWork < 0:
                self._time.set()

            self._is_work_clf = StatDan.__getItem__("is_lrf") and self._time.is_uprav

            if self.queve_dir.empty():
                time.sleep(0.1)
            else:
                while not (self.queve_dir.empty()):
                    print("-" * 80)
                    __dan = self.queve_dir.get()
                    __id = __dan[0]
                    with self._lock:
                        info[__id] = copy.deepcopy(__dan[1])
                    _ = executor.submit(self.__convert_dan, __id, info, self.queve_log)

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

        self.queve_log.put("ClexportXX.run() - завершение конвертации ")

        self.is_export = False
        self.is_convert = False
        self.renamemdf.is_work = False
        config_dir["is_read_files"] = False
