import logging


class CountInitialData:
    import os, shutil

    def __init__(self, path_sourse):
        self.logger = logging.getLogger("exampleApp.ReadXml.convert_to_ini")
        self.logger.info(" Разбор ini файла ")

        self.path_sourse = path_sourse
        self.count = 0
        self.count_repit = 0
        self.call()

    def call(self):
        __ls = self.__all_files()
        __x = [x for x in __ls if ("\\!D" in x) and ("X\\D" in x) and (not (".GLX" in x))]
        _count = len(__x)
        if self.count != _count:
            self.count_repit = 0
        self.count = _count
        self.count_repit += 1
        return  self.count


    def __all_files(self, maska=""):  # для переименованиея  maska=~D
        matches = []
        for root, dirnames, filenames in self.os.walk(self.path_sourse):
            if maska == "":
                for it1 in filenames:
                    matches.append(self.os.path.join(root, it1))
            else:
                _files = [filename for filename in filenames if maska in filename]
                for it in _files:
                    matches.append(self.os.path.join(root, it))
        return matches

    def rename(self):
        try:
            self.shutil.rmtree( self.path_sourse + "\\CLF")     # удалить каталог CLF
        except:
            pass

        __files = self.__all_files("~D")
        for it in __files:
            print(it)
            it1 = it.replace("~D", "D")
            self.os.rename(it, it1)

    def test_null(self):
        __x = self.__all_files()
        __x0 = [x for x in __x if "X\\D" in x and (not (".GLX" in x))]

        __file_error = []
        for it in __x0:
            __size = self.os.path.getsize(it)
            if __size == 0:
                print(it, "   -->>", __size)
                __i = it.index("!D")
                __file_error += [it[__i:]]
        self.__convert_files(__file_error)

    def __convert_files(self, dir_files):
        for __it_file in dir_files:
            __path_src = self.path_sourse + "\\" + __it_file
            if self.os.path.isfile(__path_src):
                _dir_file = __it_file.split("\\")
                __path_d = self.path_sourse + "\\" + _dir_file[0] + "\\~" + _dir_file[1]
                if self.os.path.isfile(__path_d):
                    self.os.remove(__path_d)

                self.rename_file(__path_src, __path_d)

    def rename_file(self, path0, path1):
        if self.os.path.isfile(path0):
            try:
                with open(path0) as f:
                        pass

                self.os.rename(path0, path1)

            except:
                    self.logger.warning(" - файл {}  занят другой программой или не сущест ".format(path0))
        else:
            self.logger.warning(" - файл {} не существует ".format(path0))

    def del_initial_data(self):
        import shutil

        if not(self.os.path.isdir(self.path_sourse + "\\clf")):
            return

        count_files_clf = len(self.os.listdir(self.path_sourse + "\\clf"))
        if count_files_clf == 0:
            return

        __ls = [self.path_sourse + "\\" + x for x in self.os.listdir(self.path_sourse) if "!D" in x]
        for it in __ls:
            try:
                print(it)
                shutil.rmtree(it)
            except OSError as e:
                print("Ошибка: в удаление каталога %s  : %s" % (it, e.strerror))
