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
        ls = []
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
                   ls += [_s]

        if type_duplicate:
            _sls = set(ls)
            ls = list(_sls)

        return ls
