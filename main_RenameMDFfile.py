from Core.CLFJson import *
import os, copy

import threading
import time
from concurrent.futures.thread import ThreadPoolExecutor
from multiprocessing import Process, Queue
from subprocess import Popen, PIPE, STDOUT

_lockRenameMDF = threading.Lock()

def __test_read_file(path, n=50):
    while n>0:
        try:
            with open(path, 'r') as file:
                return False
        except:
            time.sleep(0.1)
    return True

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def __convert_data_time(self, s: str):
    __s0 = s.split(" ")
    __s01 = __s0[0].split(".")
    __s1 = str(__s0[1].split(".")[0]).replace(":", "-")
    return __s01[2] + "-" + __s01[1] + "-" + __s01[0] + "_" + __s1

def __rename_file(_clf, __path_file):
    from pathlib import Path      # https://python-scripts.com/pathlib

#    logger = logging.getLogger("exampleApp.RunProgram.run_clexport.__rename_file")
#    logger.info(" rename MDF files  ")
    _path = Path(__path_file)
    __name = _path.stem
    __ext = _path.suffix
    __path_files = _path.parent

#    __name_ext = os.path.splitext(os.path.basename(__path_file))
#    __name = __name_ext[0]
#    __ext = __name_ext[1]    #".MDF"             #it_file[__imdf:]

                    #__imdf = str(it_file).index(".MDF")
                    #__name = it_file[:__imdf]
#        __ext = ".MDF"             #it_file[__imdf:]
    __if00x = __name.index("F")
    _name = __name[:__if00x]
    _f00x = __name[__if00x:]

    with _lockRenameMDF:
        __d =  copy.deepcopy(_clf[_name])
        __mem = copy.deepcopy(_clf[_name]["Memory"][_f00x])

    __start = __convert_data_time(__mem["Start"])
    __end = __convert_data_time(__mem["End"])
    __trigget = "_Trigger" if len(__mem) > 2 else ""

    _name_file = __d["Car name"] + "_" + __start + "_" + __end + "_" + _f00x + __trigget + __ext

    if __test_read_file(__path_file):
        return -1

    _path.rename(_name_file)
#    __path0 = __path_dit + "\\" + _name_file
#    self.os.rename(__path_dit + "\\" + it_file, __path0)
#    logger.info(__path0)


if __name__ == "__main__":

    RenameMDF

    print("  test main_RenameMDFfile")
    _clf_json = CLFJson(r"E:\MLserver\data\PS33SED\log\2020-06-30_15-21-49\clf.json")


    executor = ThreadPoolExecutor(max_workers=5)

    _is_repeat = True
    while _is_repeat:
        if queve_dir.empty():
            time.sleep(0.1)
        else:
            while not (queve_dir.empty()):
                print("-" * 80)
                __dan = queve_dir.get()
                __id = __dan[0]
                with _lock:
                    info[__id] = copy.deepcopy(__dan[1])
                    print(" start MDF ")
                    b = executor.submit(__convert_dan, __id, info, queve_log)


            pprint.pprint(info, width=1)
        __count = 0







    __rename_file(_clf_json, __path_file)
    k=1

"""

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


"""
