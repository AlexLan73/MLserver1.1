
from Core.ViewProces import *

if __name__ == "__main__":
    print("Start Convert")
    _process = ViewProces()
    _process.proces1()
#    _ls = _process.find_process("chrome.exe")
    _ls = _process.find_process('SortDirStream.exe')
    print("  кол-во запущенных программ {} ".format(len(_ls)))
    for i, it in enumerate(_ls):
        print(" {}   {}".format(i, it))
    k=1
    _sls = set(_ls)
    _ls = list(_sls)
    print("----  кол-во запущенных программ {} ".format(len(_ls)))
    for i, it in enumerate(_ls):
        print(" {}   {}".format(i, it))
