import uuid, glob, time, copy, os
import pprint

import threading
import time
from concurrent.futures.thread import ThreadPoolExecutor
from multiprocessing import Process, Queue
from subprocess import Popen, PIPE, STDOUT

_lock = threading.Lock()

def read_dir_clf(config_dir, queve_dir):
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
                _info["file_log"] = copy.deepcopy(config_dir["path_clr_log_file_mask"].replace("maskalog", str(_id)))
                _info["process"] = -2
                _info["error"] = 0
                _info["repeat"] = 0
                _info["maska_exsport"] = config_dir["maska_exsport"]
                #                pprint.pprint(_info, width=1)
                queve_dir.put([_id, copy.deepcopy(_info)])

            config_dir["bfiles"].extend(__new_files)
        else:
            time.sleep(0.2)


def fprint_log(is_convert, queve_log):
    while is_convert:
        if queve_log.empty():
            time.sleep(0.2)
        else:
            while not (queve_log.empty()):
                __log = queve_log.get()
                print("->> {}".format(__log))
#-------------------------------------------------

def __convert_dan(_id, info, _queve_log):

    with _lock:
        _info =  copy.deepcopy(info[_id])

    __maska = _info["maska_exsport"]
    __path_dit_clf = _info["file_clf"]      # self._rws.path_sourse + "\\" + key
    __path_out = _info["path_out"]
    _info["repeat"] += 1

    os.chdir(r"C:\Program Files (x86)\GIN\MLserver")
    p0 = __maska.replace("file_clf", __path_dit_clf)
    p1 = str(p0).replace("my_dir", __path_out)
    _commanda ="CLexport.exe "+ p1
    _log_start = " id-{} \n ".format(str(_id))
    _queve_log.put(_log_start+ " start convert")
    _queve_log.put(_log_start+_commanda)

    try:
        p = Popen(_commanda, stdout=PIPE, stderr=STDOUT, bufsize=1)
    except:
        _queve_log.put(_log_start+" -200 The program stopped working with a fatal error ")
        _info["error"] = -200
        _info["process"] = -1
        _queve_log.put(_log_start+" выход по ошибки проблемма в CLexport.exe")

        with _lock:
            info[_id] = copy.deepcopy(_info)
            return

    try:
        with p.stdout, open(_info["file_log"], 'ab') as file:
            for line in iter(p.stdout.readline, b''):
                print(line),
#                file.write(line)
                _queve_log.put(str(_log_start + str(line)))
            p.wait()
            return_code = p.returncode
            print(" код завершения  - ", return_code)
            _queve_log.put(_log_start + "   код завершения {}".format(return_code))
            _info["error"] = return_code
            _info["process"] = 1

#                        __error_name = self._error_prog(return_code)
#                        logger.info(__error_name)
    except:
        print(" error  ",return_code)
        _queve_log.put(_log_start + "   код завершения {}".format(return_code))
        _queve_log.put(_log_start + "  проблема с записью на диск  ")

        _info["error"] = return_code
        _info["process"] = 1

    with _lock:
        info[_id] = copy.deepcopy(_info)


if __name__ == "__main__":
    queve_dir = Queue()
    queve_log = Queue()
    is_convert = True
    path_in = r"E:\MLserver\data\PS33SED\log\2020-06-30_15-21-49\CLF"
    path_out = r"E:\MLserver\data\PS33SED\log\2020-06-30_15-21-49\MDF"
    config_dir = dict(
        patn_clr=path_in,
        path_out= path_out,
        path_clr_files=path_in + "\\*.clf",
        maska_exsport =  r" -v -~ -o -t -l \"file_clf\" -MB -O  \"my_dir\" SystemChannel=Binlog_GL.ini",
        path_clr_log_file_mask=path_in + "\\maskalog.log",
        bfiles=[],
        is_read_files=True

    )

    _read_dir = Process(target=read_dir_clf, args=(config_dir, queve_dir), daemon=True)  # , daemon=True
    _read_dir.start()
    _print_log = Process(target=fprint_log, args=(is_convert, queve_log), daemon=True)  # , daemon=True
    _print_log.start()

    info = dict()

    executor = ThreadPoolExecutor(max_workers=2)

    while config_dir["is_read_files"]:
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



        for key, val in info.items():
            if val["process"] == 2:
                __count += 1
            if __count >= 5:
                config_dir["is_read_files"] = False

    is_convert = False
    l = 1
#    basa=[]

#    z = uuid.uuid1()
#    print(z, type(z))
#    print(str(z))

#    is_new_file_clf = True

# while is_new_file_clf:
#     __new_files =list(set(glob.glob(path_clr_files)) - set(basa))             # файлы которые нужно добавить к запуску
#     if len(__new_files) >0:
#         print("*"*60)
#         for it_file in __new_files:
#             _id = uuid.uuid1()
#             _info = dict()
#             _info["file_clf"] = it_file
#             _info["file_log"] = copy.deepcopy(path_clr_log_file_mask.replace("maskalog",str(_id)))
#             _info["process"] = -1
#             _info["error"] = 0
#             pprint.pprint(_info, width=1)
#             info[_id]=copy.deepcopy(_info)
#             pprint.pprint(info, width=1)
#
#         basa.extend(__new_files)
#         print(*basa, sep='\n')
#         k=1
#     time.sleep(0.2)


# id_info = dict( "file_clf" = "...", "file_log" = "...", "process" = -1, "error" = 0, )
#        self.info=dict(  "id":id_info)
#        self.info=dict(id=dict())
