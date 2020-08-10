import threading
import time, copy


class TimeWait(threading.Thread):
    def __init__(self, count_sec, is_uprav):
        threading.Thread.__init__(self)
        self.lock = threading.Lock()  # self.lock.release()

        self.is_uprav = is_uprav
        self.count_sec = count_sec
        self.repeat = copy.deepcopy(self.count_sec)
        self.is_wait = False
        self._wait = threading.Thread(target=self.time_wait, args=(), daemon=True)  # , daemon=True
        self._wait.start()

    def time_wait(self):
        while True:
            if self.is_wait:
                with self.lock:
                    self.repeat -= 1

                if self.repeat <= 0:
                    self.is_uprav = not self.is_uprav
                    return

            time.sleep(1)

    def set(self, count_sec=0):
        with self.lock:
            self.repeat = copy.deepcopy(self.count_sec) if count_sec == 0 else count_sec
            self.is_wait = True

    def clear(self):
        with self.lock:
            self.repeat = -1
            self.is_wait = True


