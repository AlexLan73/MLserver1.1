import threading


class CLFJson:
    import copy, os, json

    def __init__(self, path_file):
        self.path_file = path_file
        self._is_new = False
        self.dclf = dict()
<<<<<<< HEAD
<<<<<<< HEAD
        self.lock = threading.Lock()    # self.lock.release()
=======
        self.lock = threading.Lock()  # self.lock.release()
>>>>>>> adccf38... #23 Остановился на сравнении дат, для поиска и формирование номера триггера
=======
        self.lock = threading.Lock()  # self.lock.release()
>>>>>>> origin/RenameMDFfile
        self.read_json()

    def read_json(self):
        if self.os.path.isfile(self.path_file):
            return self.read(self.path_file)
        self._is_new = True

    def write_json(self):
        self.save(self.path_file, self.dclf)
        self._is_new = False

    def get(self, name):
<<<<<<< HEAD
<<<<<<< HEAD
        if name in self.dclf:
            with self.lock:
                x = self.dclf[name]
=======
        if name in self.dclf:  # self.lock.acquire() ....  # self.lock.release()
            x = self.dclf[name]
>>>>>>> adccf38... #23 Остановился на сравнении дат, для поиска и формирование номера триггера
            return x
        else:
            return None

    def set(self, name, dan):
        with self.lock:
            self.dclf[name] = dan

    def set_all(self, d: dict):
        with self.lock:
            self.dclf = self.copy.deepcopy(d)

    def get_all(self):
        with self.lock:
            x = self.copy.deepcopy(self.dclf)
        return x

    def save(self, path, dan_json):
        with self.lock:
            with open(path, 'w') as f:
                f.write(self.json.dumps(dan_json))

    def read(self, file):
<<<<<<< HEAD
        with self.lock:
            with open(file, 'r') as json_file:
                try:
                    self.dclf = self.json.load(json_file)
                    return self.dclf
                except:
                    pass
=======
        with open(file, 'r') as json_file:
            try:
                with self.lock:
                    self.dclf = self.json.load(json_file)
                return self.dclf
            except:
                pass
>>>>>>> adccf38... #23 Остановился на сравнении дат, для поиска и формирование номера триггера
