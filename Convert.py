from Core.ViewProces import *


def process_test():
    _process = ViewProces()
    _process.proces1()
    count, all_process, _ls = _process.find_process('chrome.exe')
    print("  кол-во запущенных программ {} ".format(count))
    for i, it in enumerate(all_process):
        print(" {}   {}".format(i, it))


if __name__ == "__main__":
    print("Start Convert")
    process_test()
