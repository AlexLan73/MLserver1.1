import threading

class CLFJson:
    import copy, os
    def __init__(self, path_file):
        self.path_file = path_file
        self._is_new = False
        self.dclf = dict()
        self.lock = threading.Lock()
        self.read_json()

    def read_json(self):
        if self.os.path.isfile(self.path_file):
            self.read(self.path_file)
        self._is_new = True

    def write_json(self):
        self.save(path, self.dclf)
        self._is_new = False

    def get(self, name):
        if name in self.dclf:
            self.lock.acquire()
            x = self.dclf[name]
            self.lock.release()
            return x
        else:
            return None

    def set(self, name, dan):
        if name in self.dclf:
            with self.lock:
                self.dclf[name] = dan
        else:
            return None

    def set_all(self, d: dict):
        with self.lock:
            self.dclf = self.copy.deepcopy(d)

    def get_all(self):
        self.lock.acquire()
        x = self.copy.deepcopy(self.dclf)
        self.lock.release()
        return x



    def save(self, path, dan_json):
        self.lock.acquire()
        with open(path, 'w') as f:
            f.write(self.json.dumps(dan_json))
        self.lock.release()


    def read(self, file):
        with open(file, 'r') as json_file:
            try:
                self.lock.acquire()
                self.dclf = self.json.load(json_file)
                self.lock.release()
            except:
                pass
