import logging
import copy, os

from pprint import pprint
from .ReadWrite import *
from .StatDan import *
from pathlib import Path, PurePath


class ReadXml:

    def __init__(self, path_common, path_analiz_dan):
        self.logger = logging.getLogger("exampleApp.ReadXml.__init__")
        self.logger.info(" ReadXml.__init__ инициаллизация")

        self.dir_analysis = path_analiz_dan
        self.path_common = path_common
#        self._mlserver = self.test_environment_windows()
        self._mlserver = StatDan.__getItem__("path_mlserver")

        self.maska_zip = "Analysis.gla"
        d0, d_err = self.read_xml_dan(path_analiz_dan + "\\" + self.maska_zip)
        self.Catalog_copy_information = self.convert_to_ini(dan=d0, dan_err=d_err, path=path_analiz_dan)

        print("*" * 80 + "\n" + self.Catalog_copy_information + "*" * 80 + "\n")

        _rw = ReadWrite()
        self.siglog_config_basa = []
        self.siglog_config_basa += _rw.ReadTextBasa0(self.path_common + "\\DLL\\" + "siglog_config.ini")
        self.siglog_config_basa += [self.Catalog_copy_information]

        self.copy_siglog_vsysvar(d_err)

    def read_xml_dan(self, path):
        self.logger.info(" ReadXml.read_xml_dan Разбираем файл  Analysis.gla")

        def __convert(self, _d):
            __bus = str(_d["bustype"]).split("_")[1]
            _d["bustype"] = __bus
            if ("CAN" in __bus.upper()) or ("LIN" in __bus.upper()):
                _d["type"] = ""
            return _d

        import xml.etree.ElementTree as ET

        tree = ET.parse(path)
        root = tree.getroot()
        print(tree, "\n", root.tag)

        DatabaseList = root.find('DatabaseList')
        dan = dict()
        i = 0
        for x in DatabaseList.findall("Database"):
            z = dict()
            try:
                z["path"] = x.find('Path').text
            except:
                z["path"] = "path"
            try:
                z["bustype"] = x.find('BusType').text
            except:
                z["bustype"] = "bt_bustype"
            try:
                z["channel"] = x.find('Channel').text
            except:
                z["channel"] = "-1"
            try:
                z["type"] = x.find('Type').text
            except:
                z["type"] = "type"

            z = __convert(self, z)
            dan[i] = copy.deepcopy(z)
            i += 1

        pprint(dan, width=1)
        dan_err = dict()
        for key0, val0 in dan.items():
            for kye1, val1 in val0.items():
                #                if (kye1 in val1) | (('channel'in kye1) & ( "-1" in val1) ):
                #                if (kye1 in val1) or ( "-1" in val1) or ( "vsysvar" in str(val1).lower()):
                if "vsysvar" in str(val1).lower():
                    dan_err[key0] = copy.deepcopy(val0)
                    break

        return dan, dan_err

    def copy_siglog_vsysvar(self, d_err: dict):
        from shutil import copyfile
        self.logger.info(" function copy_siglog_vsysvar ")

        for key, val in d_err.items():
            __name_file = val["path"]
            __type = val["type"]
            if str(__type).lower() in str(__name_file).lower():
                __src = self.dir_analysis + "\\" + __name_file
                if os.path.isfile(__src):
                    # 'CANoeCANalyzer.vsysvar' - существует копируем на сервер
                    try:
                        _name = PurePath(__src).name
                        copyfile(__src, self._mlserver+"\\"+_name)
                        __src_CANoeCANalyzer_vsysvar = self._mlserver + "\\" + __name_file
                        if os.path.isfile(__src_CANoeCANalyzer_vsysvar):
                            os.replace(__src_CANoeCANalyzer_vsysvar, self._mlserver + "\\" + "siglog.vsysvar")
                            self.logger.info(
                                " Копирование и переименование " + self._mlserver + "\\" + "siglog.vsysvar")

                    except:
                        print(" Не удалось скопировать, нужны права администратора")
                        self.logger.warning(" Не удалось скопировать " + self._mlserver + "\\" + "siglog.vsysvar")
                        self.logger.warning("    нужны права администратора")


                elif os.path.isfile(self.dir_analysis + "\\" + "siglog.vsysvar"):
                    try:
                        self.shutil.copy2(self.dir_analysis + "\\" + "siglog.vsysvar",
                                          self._mlserver + "\\" + "siglog.vsysvar")
                    except:
                        print(" Не удалось скопировать, нужны права администратора")

    def convert_to_ini(self, **kwargs):
        self.logger.info("ReadXml.cconvert_to_ini")

        dan = kwargs.get("dan", {})
        dan_err = kwargs.get("dan_err", {})
        path = kwargs.get("path", "")
        s = ""
        if len(dan) <= 0:
            self.logger.critical(" нет словоря с данными  для конвертации ")
            return s

        if len(dan_err) > 0:
            for key, val in dan_err.items():
                del dan[key]
        i = 1
        for key, val in dan.items():
            s += "[DB{}] \n".format(i)
            s += "Path=" + path + "\\" + val["path"] + "\n"
            s += "Network=" + val["type"] + "\n"
            s += "Bus=" + val["bustype"] + "\n"
            s += "Channels=" + val["channel"] + "\n"
            i += 1
        #        print(s)
        self.logger.info(" convert_to_ini отработал ")
        return s
#  Чтение из окружения Windows
    # def test_environment_windows(self):
    #     self.logger.info(" ReadXml.test_environment_windows")
    #
    #     self._mlserver = str(os.environ.get("MLSERVER", ""))
    #
    #     if len(self._mlserver) <= 0:
    #         print("Не прописана системная переменная MLSERVER -> путь к каталогу \n "
    #               " к примеру C:\Program Files (x86)\GIN\MLserver")
    #         self.logger.critical("Не прописана системная переменная MLSERVER -> путь к каталогу")
    #         self.sys.exit(-2)
    #     else:
    #         self.logger.info(" Системная переменная MLSERVER -> путь к каталогу - прописана ")
    #     return self._mlserver
