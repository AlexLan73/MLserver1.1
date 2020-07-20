class InArguments:
    import sys, os

    def __call__(self,  *args):
        if args.__len__() >0:
            self.fun_error = args[0]

        args = self.parse()

        if args["kod_error"] < 0:
            # проблема с аргументами
            self._error_args(args)
        return args

    def _fun_error(self, t:tuple):
        print(" код -> {} ".format(t[0]))
        print(" сообщение -> {} ".format(t[1]))
        sys.exit(t[0])

    def parse(self):
        name_file_run = __file__  # путь старта программы
        _dargs = dict(
            s_error="Ok!",
            kod_error=0,
            dir_start="",
            dir_work="",
            ls_arg=[],
            ls=[]
        )

        ls_arg = self.sys.argv
        k = 0
        print("Входные аргументы")
        for it in ls_arg:
            _s = "  - Номер аргумента -{} значение ->  {} ".format(k, it)
            print(_s)
            if len(it) >5:
                _dargs["ls"] += [it]
            _dargs["ls_arg"] += [_s]
            k += 1


        if len(ls_arg) < 2:
            _dargs["kod_error"] = -1
            _dargs["s_error"] = " нет  аргументов  код -1"
            return _dargs

        _dargs["dir_start"] = self.os.path.dirname(ls_arg[0])
        if not (self.os.path.isdir(_dargs["dir_start"])):
            _dargs["kod_error"] = -2
            _dargs["s_error"] = "Не правильно определился каталог старта програмы  код -2"
            return _dargs

        _dargs["dir_work"] = _dargs["ls"][1]
        if not (self.os.path.isdir(_dargs["dir_work"])):
            _dargs["kod_error"] = -3
            _dargs["s_error"] = "Нет директории с данными код -3"
            return _dargs

        return _dargs

    def _error_args(self, _args):
        if _args["kod_error"] < 0:
            # проблема с конфигурацией
            self.fun_error((_args["kod_error"], _args["s_error"]))
