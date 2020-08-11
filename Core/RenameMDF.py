from multiprocessing import Queue
from concurrent.futures.thread import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path  # https://python-scripts.com/pathlib # https://docs.python.org/3/library/pathlib.html

import logging
import logging.config
import threading
import os, time, copy, re

from .TimeWait import *
from .StatDan import *


class RenameMDF(threading.Thread):

    def __init__(self, clf, dir_filesXX, is_work, timewait=40):  # def __init__(self):
        threading.Thread.__init__(self)
        self.logger = logging.getLogger("exampleApp.RenameMDF.__init__")
        self.logger.info("RenameMDF.__init__")

        self.clf = clf

        self.dir_filesXX = dir_filesXX
        self.ext = ""
        self.__data_trigger = dict()
        self.maska1_datatime = r'%Y-%m-%d %H:%M:%S.%f'
        self.maska2_datatime = r'%d.%m.%Y %H:%M:%S.%f'
        self.is_rename_read_dir_files = True
        self.is_work = True
        self.queve_dir = Queue()
        self._lockRenameMDF = threading.Lock()

        self._is_uprav = True
        self.time = TimeWait(timewait, self._is_uprav)

        x = threading.Thread(
            target=RenameMDF.read_dir_mdf, args=(self, self.dir_filesXX, self.queve_dir,), daemon=True)
        x.start()

    def run(self):
        self.logger.info("RenameMDF.RUN  запуск потока")

        def __convert_data_time(self, s: str):
            __s0 = s.split(" ")
            __s01 = __s0[0].split(".")
            __s1 = str(__s0[1].split(".")[0]).replace(":", "-")
            return __s01[2] + "-" + __s01[1] + "-" + __s01[0] + "_" + __s1

        _old_count_files = 0
        while self.is_work or self.queve_dir.qsize() > 0 or self._count_not_convert_read_files() > 0:
            __i = len(os.listdir(self.dir_filesXX))
            if __i > _old_count_files:
                _old_count_files = __i
                self.time.set()

            if self.queve_dir.empty():
                time.sleep(0.5)
                # if not self.time.is_uprav:
                #     return
                # continue

            while not (self.queve_dir.empty()):
                __path_file = self.queve_dir.get()
                __name = Path(__path_file).stem
                __ext = Path(__path_file).suffix
                __path_files = Path(__path_file).parent
                __if00x = __name.rindex("F")
                _name = __name[:__if00x]
                _f00x = __name[__if00x:]

                with self._lockRenameMDF:
                    __d = copy.deepcopy(self.clf.dclf[_name])
                    __mem = copy.deepcopy(self.clf.dclf[_name]["Memory"][_f00x])

                __start = __convert_data_time(self, __mem["Start"])
                __end = __convert_data_time(self, __mem["End"])
                __trigget = ""
                if len(__mem) > 2:
                    __trigget = "_Trigger"

                    __triggerX = __mem.get("TriggerX", dict())

                    for key, val in __triggerX.items():
                        __trigget += "_({})".format(val[0])

                    print("  __trigget => ", __trigget)

                _name_file = __d["Car name"] + "_(" + __start + ")_(" + __end + ")_" + _f00x + __trigget + __ext

                if not (self.__test_read_file(__path_file)):
                    self.is_rename_read_dir_files = False
                    return -1

                Path(__path_file).rename(str(__path_files) + "\\" + _name_file)

        self.is_rename_read_dir_files = False

    def _count_not_convert_read_files(self):
        if "" == self.ext:
            return -1
        else:
            _all_files = list(Path(self.dir_filesXX).glob('*' + self.ext))  # '*.mdf'
            _files_count = len([x for x in _all_files if len(re.findall(r'\dF', str(x))) > 0])
            return _files_count

    def read_dir_mdf(self, dir_filesXX, queve_dir):
        self.logger.info("RenameMDF.read_dir_mdf  потока  чтение каталога MDF files")

        from pathlib import Path
        import re
        ls_dir = []
        _old_count_files = -1
        while True:
            _all_files = list(Path(dir_filesXX).glob("*.*"))  # '*.mdf'
            if len(_all_files) >= 2:
                __files = [x for x in _all_files if not (".ini" in str(x).lower())]
                self.ext = Path(__files[0]).suffix
                break
            else:
                time.sleep(1)

        while self.is_rename_read_dir_files or self._count_not_convert_read_files() > 0:
            _all_files = list(Path(self.dir_filesXX).glob('*' + self.ext))  # '*.mdf'
            _files = [x for x in _all_files if
                      len(re.findall(r'\dF', str(x))) > 0 and len(re.findall(r'_F', str(x))) == 0]

            __new_files = list(set(_files) - set(ls_dir))  # файлы которые нужно добавить к запуску

            if len(_all_files) == 0:  # если каталог очистить от ext то процесс начнется с начала
                ls_dir = []

            if len(__new_files) > 0:
                for it_file in __new_files:
                    if self.__test_read_file(it_file):
                        print(it_file)
                        ls_dir += [it_file]
                        queve_dir.put(it_file)
            else:
                time.sleep(1)

            _count_files = len(_files)
            if _old_count_files != _count_files and not (_count_files == 0):
                print(f"  RENAME не обработанно файлов - {_count_files} ")
                _old_count_files = _count_files

            if not self.is_work and _count_files == 0:
                break

        print("   -------  END  RenameMDF RUN ")

    def __test_read_file(self, path):
        try:
            with open(path, 'r') as file:
                return True
        except:
            return False
