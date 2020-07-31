import threading
from multiprocessing import Process, Queue
from concurrent.futures.thread import ThreadPoolExecutor
from pathlib import Path  # https://python-scripts.com/pathlib
import copy  # https://docs.python.org/3/library/pathlib.html

import time
from datetime import datetime

class RenameMDF(threading.Thread):
    import os, time
    import logging

    def __init__(self, dir_work, clf, ext, is_work):  # def __init__(self):
        threading.Thread.__init__(self)

        path_files_mdf = r"E:\MLserver\data\PS33SED\log\2020-06-30_15-21-49\MDF"
        self.clf = clf

#        __data_trigger:dict = copy.deepcopy(self.clf.dclf["data_trigger"])

        self.__data_trigger = dict()
        self.maska1_datatime = r'%Y-%m-%d %H:%M:%S.%f'
        self.maska2_datatime = r'%d.%m.%Y %H:%M:%S.%f'
#        for key, val in __data_trigger.items():
#            __datatime = datetime.strptime(key, self.maska1_datatime)
#            self.__data_trigger[__datatime] = copy.deepcopy(val)

        self.is_work = is_work
        self.queve_dir = Queue()
        self._lockRenameMDF = threading.Lock()

        x = threading.Thread(target=RenameMDF.read_dir_mdf, args=(self, path_files_mdf, ext, self.queve_dir,),
                             daemon=True)
        x.start()

    def run1(self):
        def __convert_data_time(self, s: str):
            __s0 = s.split(" ")
            __s01 = __s0[0].split(".")
            __s1 = str(__s0[1].split(".")[0]).replace(":", "-")
            return __s01[2] + "-" + __s01[1] + "-" + __s01[0] + "_" + __s1

        while True:
            if self.queve_dir.empty():
                time.sleep(0.5)
                if not self.is_work:
                    return
                continue

            while not (self.queve_dir.empty()):
                __path_file = self.queve_dir.get()
                #                _path = Path(__path_file)
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
                __trigget=""
                if len(__mem) > 2:
                    __trigget = "_Trigger"

                    __triggerX = __mem.get("TriggerX",dict())

                    for key, val in __triggerX.items():
                        __trigget += "_({})".format(val[0])

                    print("  __trigget => ",__trigget)
                    k=1
                _name_file = __d["Car name"] + "_(" + __start + ")_(" + __end + ")_" + _f00x + __trigget + __ext

                if not(self.__test_read_file(__path_file)):
                    return -1

                Path(__path_file).rename(str(__path_files)+"\\"+_name_file)
                k = 1


    def read_dir_mdf(self, path_files_mdf, ext, queve_dir):
        from pathlib import Path
        import re
        ls_dir = []
        while True:
            _all_files = list(Path(path_files_mdf).glob(ext))  # '*.mdf'
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

    #        executor = ThreadPoolExecutor(max_workers=1)
    #        b = executor.submit(self.read_dir_mdf, path_files_mdf, ext, queve_dir, daemon=True)
    #        k1=1
    #        executor = Process(target=RenameMDF.read_dir_mdf, args=(self, path_files_mdf, ext, queve_dir), daemon=True)  # , daemon=True
    #        _read_dir.start()
