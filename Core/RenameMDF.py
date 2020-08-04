import threading
from multiprocessing import Process, Queue
from concurrent.futures.thread import ThreadPoolExecutor
from pathlib import Path    # https://python-scripts.com/pathlib
import copy                  # https://docs.python.org/3/library/pathlib.html
from Core.TimeWait import *

import time
from datetime import datetime

class RenameMDF(threading.Thread):
    import os, time
    import logging

    def __init__(self, clf, dir_filesXX, is_work, timewait=10):  # def __init__(self):
        threading.Thread.__init__(self)

#        dir_filesXX = r"E:\MLserver\data\PS33SED\log\2020-06-30_15-21-49\MDF"
        self.clf = clf

        self.dir_filesXX = dir_filesXX
        self.__data_trigger = dict()
        self.maska1_datatime = r'%Y-%m-%d %H:%M:%S.%f'
        self.maska2_datatime = r'%d.%m.%Y %H:%M:%S.%f'

        self.is_work = is_work
        self.queve_dir = Queue()
        self._lockRenameMDF = threading.Lock()

        self._is_uprav = True
        self._time = TimeWait(timewait, self._is_uprav)

        x = threading.Thread(
            target=RenameMDF.read_dir_mdf, args=(self, dir_filesXX, self.queve_dir,), daemon=True)
        x.start()

    def run(self):
        def __convert_data_time(self, s: str):
            __s0 = s.split(" ")
            __s01 = __s0[0].split(".")
            __s1 = str(__s0[1].split(".")[0]).replace(":", "-")
            return __s01[2] + "-" + __s01[1] + "-" + __s01[0] + "_" + __s1

        _old_count_files = 0
        while True:
            __i = len(self.os.listdir(self.dir_filesXX))
            if __i > _old_count_files:
                _old_count_files = __i
                self._time.set()

            if self.queve_dir.empty():
                time.sleep(0.5)
                if not self._time.is_uprav:
                    return
                continue

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

                    print("  __trigget => ",__trigget)
                    k=1
                _name_file = __d["Car name"] + "_(" + __start + ")_(" + __end + ")_" + _f00x + __trigget + __ext

                if not (self.__test_read_file(__path_file)):
                    return -1

                Path(__path_file).rename(str(__path_files) + "\\" + _name_file)

    def read_dir_mdf(self, dir_filesXX, queve_dir):
        from pathlib import Path
        import re
        ls_dir = []

        while True:
            _all_files = list(Path(dir_filesXX).glob("*.*"))  # '*.mdf'
            if len(_all_files) >= 2:
                __files = [x for x in _all_files if not(".ini" in str(x).lower())]
                ext = Path(__files[0]).suffix
                break
            else:
                time.sleep(1)

        while True:
            _all_files = list(Path(dir_filesXX).glob('*'+ext))  # '*.mdf'
            _files = [x for x in _all_files if
                      len(re.findall(r'\dF', str(x))) > 0 and len(re.findall(r'_F', str(x))) == 0]
            __new_files = list(set(_files) - set(ls_dir))  # файлы которые нужно добавить к запуску

            if len(_all_files) == 0:  # есликаталог очистить от ext то процесс начнется с начала
                ls_dir = []

            if len(__new_files) > 0:
                print("*-*-" * 30)
                for it_file in __new_files:
                    if self.__test_read_file(it_file):
                        print(it_file)
                        ls_dir += [it_file]
                        queve_dir.put(it_file)
            else:
                time.sleep(1)

            print("  --  всего files - {} \n не обработанно файлов - {} \n    новых = {}"
                  .format(len(_all_files), len(_files), len(__new_files)))

    def __test_read_file(self, path):
        try:
            with open(path, 'r') as file:
                return True
        except:
            return False
