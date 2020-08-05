# psutil - интересная утилита https://github.com/giampaolo/psutil
# https://ru.stackoverflow.com/questions/863925/%D0%9A%D0%B0%D0%BA-%D0%BF%D0%BE%D0%BB%D1%83%D1%87%D0%B8%D1%82%D1%8C-%D0%BF%D1%83%D1%82%D1%8C-%D0%B4%D0%BE-%D0%B7%D0%B0%D0%BF%D1%83%D1%89%D0%B5%D0%BD%D0%BD%D0%BE%D0%B3%D0%BE-%D0%BF%D1%80%D0%BE%D1%86%D0%B5%D1%81%D1%81%D0%B0
class ViewProces:
    from subprocess import Popen, PIPE
    import subprocess

    def __init__(self):
        print("ViewProces")

    def proces1(self):
        print(*[line.decode('cp866', 'ignore') for line in self.Popen('tasklist', stdout=self.PIPE).stdout.readlines()])

    def find_process(self, maska, type_duplicate = True):
        import psutil # pip install psutil
        proc_name = maska
        all_process = []
        for proc in psutil.process_iter():
            # Пока скрипт работает, процесс уже может перестать существовать
            # (поскольку между psutil.process_iter() и proc.name() проходит время)
            # и будет выброшено исключение psutil.NoSuchProcess
            try:
                proc_name_in_loop = proc.name()
            except psutil.NoSuchProcess:
                pass
            else:
                if proc_name_in_loop == proc_name:
                   _s = proc.exe()  # print(proc.cwd()) #<-- значение коммандной строки
                   all_process += [_s]

        count = len(all_process)

        if type_duplicate:
            _sls = set(all_process)
            path_start_process = list(_sls)

        return count, all_process, path_start_process


# def process_test():
#     _process = ViewProces()
#     _process.proces1()
#     count, all_process, _ls = _process.find_process('chrome.exe')
#     print("  кол-во запущенных программ {} ".format(count))
#     for i, it in enumerate(all_process):
#         print(" {}   {}".format(i, it))
