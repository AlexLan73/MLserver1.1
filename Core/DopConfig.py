import logging
import os, sys, glob

from .ReadWrite import *
from .StatDan import *


class DopConfig:

    def __init__(self, rw: ReadWrite):
        self.logger = logging.getLogger("exampleApp.DopConfig.__init__")
        self.logger.info("DopConfig.__init__")

        self._rw = rw
        self.path_work = self._rw.path_work
        self.path_common = self.find_common(self.path_work, "#COMMON")
        self.path_lrf_dec = self.path_common + "\\DLL\\lrf_dec.exe"
        self.path_mlserver = self.path_common + "\\DLL\\MLserver"
        StatDan.__setItem__("path_commonт", self.path_common)
        StatDan.__setItem__("path_mlserver", self.path_mlserver)


        self.CarName = ""

        self.name_config = self.file_config_from_ml_rt()
        self.NameLogger = self.name_config[0]
        self.path_name_Configuration(self.name_config[0])

    def find_common(self, path, _find):
        self.logger.info(" ReadWriteMLserver.find_common - Осуществляем поиск каталога #COMMON")

        _path = path.lower()
        _find = _find.lower()
        i = _path.find(_find)
        if i > 0:
            _path0 = _path[:i] + _find

            path_ls = os.path.dirname(_path0).split("\\")
            os.chdir(path_ls[0])
            os.chdir(_path0)
            self.path_common = _path0
            set.logger.info(" Нашли #COMMON")
            return self.path_common
        else:
            _find = _find.upper()
            os.chdir(_path)

            while len(_path) > 2:
                os.chdir(_path)
                ls = os.listdir()
                if _find in ls:
                    self.path_common = _path + "\\" + _find
                    return self.path_common
                else:
                    k = _path.rfind("\\")
                    _path = _path[:k]
            self.logger.critical("  Не смогла найти каталог #COMMON")
            print("Отсутствует директория {} ".format(_find))
            sys.exit(-4)

    def file_config_from_ml_rt(self):
        self.logger.info("DopConfig.file_config_from_ml_rt")
        __path = self.path_work + "\\" + "ml_rt.ini"
        print(__path)

        if os.path.isfile(__path):
            self.logger.info(" чтение файла " + __path)
        ls = self._rw.ReadText(__path)
        ls1 = [x for x in ls if "filename" in x.lower()]
        if len(ls1) <= 0:
            return None
        _ls = (ls1[0].split("=")[1]).split(".")
        try:
            _s = _ls[0]
            _i = _s.index("_#")
            if _i > 0:
                _ls[0] = _s[:_i]
                _ls[1] = _s[_i + 2:]
        except:
            pass
        _CarName = [x for x in ls if "CarName" in x]
        self.CarName = _CarName[0].split("=")[1]
        return _ls

        _s = f"В каталоге {self.path_sourse} нет файла ml_rt.ini"
        self.logger.critical(_s)
        print(_s)
        sys.exit(-3)

    def path_name_Configuration(self, name_congig):
        self.logger.info("DopConfig.path_name_Configuration")

        def __test_datetime(self, _dan):
            import operator
            from datetime import datetime

            __path_analysis = ""

            __count = len(_dan)
            if __count == 0:
                return ""

            elif __count == 1:
                __key = list(_dan.keys())
                __path_analysis = __key[0]
                return __path_analysis
            else:
                _d = dict()
                if "dict" in str(type(_dan)):
                    for key, val in _dan.items():
                        if ".analysis" in val:
                            __s = (val.split(".analysis")[0]).replace(name_congig + "_", "")
                            __s = __s[-19:]
                            __dt = __s.split("_")
                            __date = __dt[0]
                            __time = __dt[1].replace("-", ":")
                            __dt_ = __date + " " + __time
                            _deadline = datetime.strptime(__dt_,
                                                          "%Y-%m-%d %H:%M:%S")  # print(_deadline)     # 2017-05-22 00:00:00
                            _d[val] = _deadline

            __path_analysis = max(_d.items(), key=operator.itemgetter(1))[0]

            return __path_analysis

        __path = self.path_common + "\\Configuration\\" + name_congig

        __ls = glob.glob(__path + "\\*analysis.zip")
        print(" Поиск analysis.zip  !!!!")
        print("   путь -> ", __path)
        for it in __ls:
            print("            {} ".format(it))

        self.logger.info(" Читаем  конфигурации " + __path)

        name_file_analysis_zip = __test_datetime(self, {x: x for x in __ls if "analysis.zip" in x})
        print("   найдено -> ", name_file_analysis_zip)

        if name_file_analysis_zip == "":
            print("Нет файла с расширением  analysis ")
            self.logger.critical("Нет файла с расширением  analysis ")

            sys.exit(-5)

        ___s = {x: x for x in os.walk(__path).__next__()[1]}
        name_dir_analysis = __test_datetime(self, ___s)

        __z = name_file_analysis_zip.split(".zip")[0]
        if __z in name_dir_analysis:
            self.dir_analysis = __path + "\\" + name_dir_analysis
            self.logger.info(" Файл analysis найден ")
            return self.dir_analysis

        __path = __z
        self.zip_extractall(name_file_analysis_zip, __path)
        self.dir_analysis = __path
        self.logger.info(" Файл analysis найден ")
        return self.dir_analysis

    def zip_extractall(self, path_file, path_dir):
        import zipfile
        fantasy_zip = zipfile.ZipFile(path_file)
        fantasy_zip.extractall(path_dir)
        fantasy_zip.close()
