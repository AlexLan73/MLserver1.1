from Core.CountInitialData import *
import threading
import logging
from Core.StatDan import *
from Core.ReadWrite import *


class ConvertCLF(threading.Thread):
    import os, sys, copy, glob, json
    from subprocess import Popen, PIPE, STDOUT

    def __init__(self):
        threading.Thread.__init__(self)
        self.logger = logging.getLogger("exampleApp.LrfDec.__init__")
#        self.logger.info(" Разбор ini файла ")
        self.path_work = StatDan.__getItem__("path_work")
        StatDan.__setItem__("ConvertCLF_error", 0)
        self.path_common = StatDan.__getItem__("path_commonт")

        self.path_clf = self.path_work+"\\CLF"
        self._rw = ReadWrite()
        self._rw.make_dir(self.path_clf)

        self._clf_json = StatDan.__getItem__("iclf_json")


        k=1

    def run(self):
        pass


#*******************************


    def run_clf_text(self):
        __dan_clf = dict()
        logger = logging.getLogger("exampleApp.RunProgram.run_clf_text")
        logger.info(" start function run_clf_text")
        logger.info("   программа создает clf.json c информацией из *.clf ")

        def __data_time_convert(self, s: str):
            s1 = s.strip().replace(".", "-").split(" ")
            s01 = s1[0].split("-")
            return s01[2] + "-" + s01[1] + "-" + s01[0] + "_" + s1[1].split("-")[0].replace(":", "-")

        def __convert(self, _param, __name_file):
            import subprocess
            filtr01 = lambda x: x.split(":")[1].strip()
            filtr02 = lambda x: x.split(":")[1:]
            filtr03 = lambda x: str(':'.join(filtr02(x))).strip()
            filtr04 = lambda x, s: str(x[x.index(s) + 6:]).strip()
            filtr05 = lambda x, s: str(x[x.index(s) + 10:]).strip()

            output1 = subprocess.check_output(_param)

            p = self.Popen(_param, stdout=self.PIPE, stderr=self.STDOUT, bufsize=1)

            with p.stdout, open(self._rws.log_file, 'ab') as file:
                for line in iter(p.stdout.readline, b''):
                    print(line),
                    file.write(line)
            p.wait()

            return_code = p.returncode
            print("  код завершения  - ", return_code)

            output = str(output1).split("\\r\\n")
            __is = True
            __memory = dict()
            i = 0

            __mem_fxx = dict()
            while i < len(output):
                it = output[i]
                print(it)
                if __is:
                    if " Memory F" in it:
                        __mem = dict()

                        __i0 = it.index("F")
                        __s = it[__i0:]
                        __i1 = __s.index(":")
                        __fxx = __s[:__i1].strip()
                        __mem["Start"] = filtr04(__s, "Start")

                        while True:
                            i += 1
                            it = output[i]
                            if 'Trigger' in it:
                                xxx = filtr05(it, "Trigger")
                                __mem["Trigger"] = xxx
                            elif 'End' in it:
                                __mem["End"] = filtr04(it, "End")
                                break
                        i += 1
                        __mem_fxx[__fxx] = self.copy.deepcopy(__mem)
                        continue
                    if "--- File Comment -" in it:
                        __is = False
                    i += 1

                else:
                    if "Compilation time" in it:
                        __dan_clf["Compilation time"] = filtr01(it)
                    elif "Car name" in it:
                        __dan_clf["Car name"] = filtr01(it)
                    elif "Device serial number" in it:
                        __dan_clf["Device serial number"] = filtr01(it)
                    elif "VIN" in it:
                        __dan_clf["VIN"] = filtr01(it)
                    elif "Data date/time" in it:
                        __dan_clf["Data date time"] = filtr03(it)
                    elif "Readout date/time" in it:
                        __dan_clf["Readout date time"] = filtr03(it)
                    elif "Translation date/time" in it:
                        __dan_clf["Translation date time"] = filtr03(it)
                    elif "Odometer" in it:
                        __dan_clf["Odometer"] = filtr01(it)
                    i += 1

            __dan_clf["Memory"] = self.copy.deepcopy(__mem_fxx)

            __dan_clf["rename clf"] = []
            __dan_clf["rename clf"] += [__name_file]

            __ls_key = list(__mem_fxx.keys())
            if len(__ls_key) <= 0:
                __dan_clf["rename clf"] += [__dan_clf["Car name"] + "_" + "TIME ERROR"]
            elif len(__ls_key) == 1:
                __start = __data_time_convert(self, __mem_fxx[__ls_key[0]]["Start"])
                __end = __data_time_convert(self, __mem_fxx[__ls_key[0]]["End"])
                __new_files = __dan_clf["Car name"] + "_" + __start + "_" + __end + ".clf"
                __dan_clf["rename clf"] += [__new_files]
            else:
                __key_start = __ls_key[0]
                __key_end = __ls_key[-1]
                __start = __data_time_convert(self, __mem_fxx[__key_start]["Start"])
                __end = __data_time_convert(self, __mem_fxx[__key_end]["End"])
                __new_files = __dan_clf["Car name"] + "_" + __start + "_" + __end + ".clf"
                __dan_clf["rename clf"] += [__new_files]
                k = 1
                # if len(__mem_fxx) == 1:
                #     __start = __mem_fxx["Start"]
                #     __end =  __mem_fxx["End"]
                #     __new_files = __dan_clf["Car name"] + "_" +__start + "_" +__end+".clf"
                # else:

            return __dan_clf

        self._rws.cd(self._rws.path_sourse)
        _exe = self._rws.path_common + "\\DLL\\FileType.exe"
        __path_clf = self._rws.path_sourse + "\\CLF\\"
        logger.info("   запускаем программу " + _exe)
        logger.info("   данные из " + __path_clf)

        self._name_file_datax_clf = self.copy.deepcopy([x for x in self.os.listdir(__path_clf) if ".clf" in x])
        _all_file = {}
        if len(self._name_file_datax_clf) > 0:
            for it in self._name_file_datax_clf:
                _param = _exe + " -v " + __path_clf + it
                __dan_clf = {}
                __i = it.index(".clf")
                __name_file = it[:__i]
                __dan_clf = __convert(self, _param, __name_file + ".clf")
                _all_file[__name_file] = self.copy.deepcopy(__dan_clf)
                __info = " convert FileType name file -> {}".format(it)
                print(__info)
                logger.info(__info)

            self._rws.save_json(self._rws.path_sourse + "\\clf.json", _all_file)
        logger.info("   информация была сконвертирована и записана в clf.json ")

    # ==========  RENAMES_CLF ====================================+
    def rename_files(self):
        logger = logging.getLogger("exampleApp.RunProgram.rename_files")
        logger.info("  Start function rename_files ")
        logger.info("    rename files clf  данные из  clf.json")

        __clf_json = self._rws.read_dict_json(self._rws.path_sourse + "\\clf.json")
        __path_clf = self._rws.path_sourse + "\\CLF"
        self._rws.cd(__path_clf)
        __ls_clf = [x for x in self.os.listdir() if ".clf" in x]
        for it in __ls_clf:
            __name = it.split(".clf")[0]
            new_name = __clf_json[__name]["rename clf"]
            self.os.rename(new_name[0], new_name[1])
            logger.info("  --  " + new_name[1])