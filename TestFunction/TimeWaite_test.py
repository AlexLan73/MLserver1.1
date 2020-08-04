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

if __name__ == "__main__":
    _maska=""
    __maska ={"MDF":"1q2w3e4r5"}
    if "dict" in str(type(__maska)):
        print("dict   ",type(__maska))
        _maska = list(__maska.values())[0]
    else:
        print("----")
    z =list(__maska.values())[0]

    ls =[1,1,1,1,1,1]
    print(len(ls), "    ",sum(ls))
    count = 5



    _is_work = True
    _time = TimeWait(count, _is_work)

    _time.set()
    k = 5
    while _time.is_uprav:
        print("-----", k)
        time.sleep(0.5)
        k -= 1
        if k <= 0:
            _time.clear()
            k = 6
    print("====   END  ===")
