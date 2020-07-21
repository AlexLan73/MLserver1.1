class ReadWrite:
    import os

    def __init__(self, *args, **kwargs):
        print(" ==-- START class ReadWrite --==")
        self.path_work = kwargs.get("PathWork", self.os.getcwd())

    def _cd(self, path: str):
        self.os.chdir(path)

    def cd(self, path: str):
        if self.os.path.isdir(path):
            try:
                __i = path.index(":")
                if __i > 0:
                    __path_c = path[:__i + 1]
                    self.os.chdir(__path_c)
                    self.os.chdir(path)
            except:
                self.os.chdir(path)
        else:
            print("Нет каталога -> {}".format(path))

    def __read_type_files(self, path_to_file=""):
        from chardet.universaldetector import UniversalDetector

        detector = UniversalDetector()
        with open(path_to_file, 'rb') as fh:
            for line in fh:
                detector.feed(line)
                if detector.done:
                    break
            detector.close()
        # print(detector.result)
        return detector.result['encoding']

    def ReadText(self, path_to_file=""):
        b1 = self.os.path.isfile(path_to_file)
        if not (self.os.path.isfile(path_to_file)):
            return -1
        _encoding = self.__read_type_files(path_to_file)
        with open(path_to_file, encoding=_encoding) as f:  # utf-8-sig   #utf-8  , encoding='utf-8-sig'
            myList = [line.replace("\n", "") for line in f]
        return myList

    def write_list(self, file, s):
        with open(file, "w") as file:
            for it in s:
                file.write(it)

    def make_dir(self, dir, new=False):
        import shutil
        import time

        if new:
            try:
                shutil.rmtree(dir)  # self.os.rmdir(dir)
                time.sleep(0.01)
                self.os.mkdir(dir)

            except OSError as e:
                if self.os.path.isdir(dir):
                    return
                self.os.mkdir(dir)

        else:
            if self.os.path.isdir(dir):
                return
            else:
                self.os.mkdir(dir)

    def make_ddir(self, ddir, new=False):
        for key, val in ddir.items():
            self.make_dir(val, new)

    def __test_name_picle(self, path):
        if path.index('.pickle') <= 0:
            return path + '.pickle'

    def SaveFilePckle(self, name, data):
        import pickle
        with open(self.__test_name_picle(name), 'wb') as f:
            pickle.dump(data, f)

    def LoadFilePckle(self, name):
        import pickle
        with open(self.__test_name_picle(name), 'rb') as f:
            return pickle.load(f)
