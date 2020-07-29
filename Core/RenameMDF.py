import threading
from multiprocessing import Process, Queue
from concurrent.futures.thread import ThreadPoolExecutor

import time


class RenameMDF(threading.Thread):
    import os, time
    import logging

    def read_dir_mdf(self, path_files_mdf, ext, queve_dir):
            from pathlib import Path
            import re
            ls_dir = []
            while True:
                _all_files = list(Path(path_files_mdf).glob(ext))    #  '*.mdf'
                _files = [x for x in _all_files if len(re.findall(r'\dF', str(x))) >0 and len(re.findall(r'_F', str(x)))==0 ]
                __new_files = list(set(_files) - set(ls_dir))  # файлы которые нужно добавить к запуску

                if len(__new_files) > 0:
                    print("*-*-" * 30)
                    for it_file in __new_files:
                        if self.__test_read_file(it_file):
                            print(it_file)
                            ls_dir+=[it_file]
                            queve_dir.put(it_file)
                else:
                    time.sleep(1)
                print("  --  всего files - {} \n  нужных - {} \n    новых = {}"
                                .format(len(_all_files), len(_files), len(__new_files)))


#    def __init__(self, clf, is_work):
    def __init__(self):
        threading.Thread.__init__(self)
#        self.path_work = StatDan.__getItem__("path_work")

        path_files_mdf = r"E:\MLserver\data\PS33SED\log\2020-06-30_15-21-49\MDF"
        ext: str = '*.mdf'
        queve_dir = Queue()

#        executor = ThreadPoolExecutor(max_workers=1)
        x = threading.Thread(target=RenameMDF.read_dir_mdf, args=(self, path_files_mdf, ext, queve_dir,), daemon=True)
        x.start()
#        b = executor.submit(self.read_dir_mdf, path_files_mdf, ext, queve_dir, daemon=True)
#        k1=1
#        executor = Process(target=RenameMDF.read_dir_mdf, args=(self, path_files_mdf, ext, queve_dir), daemon=True)  # , daemon=True
#        _read_dir.start()


    def __test_read_file(self, path, n=50):
        while n>0:
            try:
                with open(path, 'r') as file:
                    return True
            except:
                self.time.sleep(0.1)
        return False
